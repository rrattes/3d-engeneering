# Parametric interfaces and orthographic drawings

Source overlay evaluation: unchanged `cad3d-engineering:1.7.0`, mounted source read only at `/candidate`; no host CAD dependencies or new packages. Negative controls initially failed because the requested modules were absent (`interfaces-drawings-red.log`). Final targeted evidence is in `interfaces-drawings-green.log`.

## Interfaces API

```python
from interface_library import generate_interface
shapes, report = generate_interface({
    'type': 'thread_pair', 'major_diameter_mm': 12, 'pitch_mm': 2,
    'length_mm': 6, 'thread_depth_mm': .8, 'radial_clearance_mm': .2,
    'wall_mm': 2, 'handedness': 'right',
})
```

All dimensions above are synthetic regression inputs, not product defaults. Every geometric input is mandatory and millimetres; unknown fields, booleans, nonfinite/negative dimensions and unsupported types are rejected. Every generated part must have one valid positive-volume CAD solid. Outputs are independent parts in their nominal installed poses.

- `thread_pair` returns `male`, `female`. Actual swept triangular helical profiles support right and left handed single-start threads; pitch equals lead. Required keys are those in the example. Profile root width is 0.70 pitch; the profile is deliberately custom, without ISO fit claims, chamfers, runout, head or drive. Bounds: 1–64 engaged turns, depth below radius, cutter expansion below both depth/2 and 0.15 pitch. Female cutter expands crest/root radially and flank axially; this is **not uniform normal clearance**. A CAD test caught lost core volume when fusing an overlength sweep; clipping the rib before core fusion preserves it. Tests verify actual handed geometry using opposite quarter-turn probe points and require volume above the cylindrical root.
- `pin_hinge` returns `leaf_a`, `leaf_b`, `pin`; three knuckles on Z, two outer knuckles attached to one continuous leaf, middle knuckle attached to the other. Required keys: `pin_diameter_mm`, `barrel_outer_diameter_mm`, `length_mm`, `leaf_width_mm`, `leaf_thickness_mm`, `radial_clearance_mm`, `axial_clearance_mm`. Plain pin has no axial retention. Rotation range, stopping, mounting holes and loaded fit remain unassessed.
- `sliding_rail` returns `rail`, `carriage`; T profile translates along Y. Required keys: `length_mm`, `width_mm`, `height_mm`, `wall_mm`, `clearance_mm`. Stem width and lower height are half supplied rail width/height. Carriage opens underneath and at both ends; no stops, fasteners or minimum engagement/load rating is inferred.

All installed part pairs run `brep_pairs.check_pair` with atomic-solid common-volume checks; any positive intersection produces `FAIL`, and kernel uncertainty produces `NOT_EVALUATED`. `report.status` aggregates that nominal interference result separately from `cad_validity`. Zero-clearance undeclared contact can fail despite valid CAD. Reports separate CAD validity from fit, manufacturing and physical validation (`NOT_EVALUATED`). Nominal nonintersection in regression examples proves neither motion clearance nor tolerance fit. Dimension budget is 10000 mm per numeric field; pathological or unsupported geometry fails closed rather than returning a nominal success.

## Drawings API

```python
from pathlib import Path
from technical_drawings import generate_drawings
report = generate_drawings(shapes, Path('build/drawings'), {
    'title': 'Interface nominal CAD', 'samples_per_edge': 64,
})
```

Produces one `<part>.svg` and `<part>.pdf` for each part, with actual OCP hidden-line orthographic front, top and right views, visible/hidden edge separation, extension lines and overall horizontal/vertical dimensions. Numeric dimensions come from the BREP bounding box. No synthetic silhouette or geometry placeholder is used. Part identifiers accept bounded ASCII letters/digits/underscores/hyphens; traversal and unknown settings fail before output creation. Config accepts `title` (printable, max 200 chars), `samples_per_edge` (integer 8–512), `sections` and `feature_dimensions` (see below). Maximum 64 parts. Requires installed Matplotlib, already present in the evaluated image.

Rendering samples CAD curves; dimensions use actual BREP bounds. Views are independently scaled and marked unsuitable for paper measurement. Sheets provide overall envelope dimensions and optional measurements selected from actual CAD faces, plus actual planar section contour sheets. They have no datum scheme, tolerances, GD&T or ISO/ASME certification. Physical and standards validation remain `NOT_EVALUATED`. Reusing an existing output directory replaces files with matching part names; callers should select a dedicated output folder.

## Targeted controls

`test-interface-library.py`: both actual thread handednesses, native right-hand 0.5 mm helical service path PASS and wrong-hand FAIL, valid independent solids and engaged nominal nonoverlap, hinge/rail pair nonoverlap, dimensional variant volume propagation, rejected malformed/unsafe specifications.

`test-technical-drawings.py`: asymmetric translated bored block produces three actual CAD views, expected 10 × 20 × 6 mm dimensions, populated SVG text, real PDF bytes, and rejects unsafe names/empty inputs/bad configuration without leaving output. Drawings are generated within a disposable test directory in the container.

Run command:

```sh
docker run --rm -v "$PWD:/candidate:ro" --entrypoint sh cad3d-engineering:1.7.0 \
  -c 'python /candidate/scripts/test-interface-library.py && python /candidate/scripts/test-technical-drawings.py'
```

## Sections and measured interface features

```python
config = {
    'sections': [
        {'name': 'cut_z', 'part': 'bracket', 'axis': 'z', 'at_mm': 0},
    ],
    'feature_dimensions': [
        {'name': 'bore', 'part': 'bracket', 'type': 'diameter',
         'selector': {'surface': 'cylinder', 'radius_mm': 2}},
        {'name': 'thickness', 'part': 'bracket', 'type': 'minimum_distance',
         'first': {'surface': 'plane', 'normal': [0, 0, 1]},
         'second': {'surface': 'plane', 'normal': [0, 0, -1]}},
    ],
}
```

`sections` declares up to 64 planes through named parts, in world coordinates. Axis must be `x`, `y` or `z`; plane location `at_mm` must be finite. `build123d.section` produces an actual CAD intersection, whose positive area and edges are checked before creating output. Empty cuts fail without producing files. Safe names and unique generated filenames are required. Separate `bracket-section-cut_z.svg` / `.pdf` sheets identify the plane and plot actual section boundary contours with axes and CAD section area. They do not apply standards-compliant material hatching.

`feature_dimensions` declares up to 64 measurements total and eight per part sheet. Diameter derives from the selected cylindrical surface radius; minimum distance is the actual OCP minimum between two selected trimmed faces. The supplied radius in a selector is a selection constraint, never a value used directly for the dimension. All selection uses `face_references.select_face`; selectors should carry point/normal constraints where needed. Missing/ambiguous faces or a noncylindrical diameter reference produce `NOT_EVALUATED`, no numeric `value_mm`, and an explicit unresolved legend on the part drawing. The drawing report also becomes `NOT_EVALUATED`. Unknown measurement fields, including a supplied `value_mm`, are rejected. Successful measurement legends show the CAD-derived millimetre value on SVG/PDF, with selection evidence and numeric results in the report. Minimum face distance is not automatically wall thickness, a datum dimension or a fit clearance.

Additional source-overlay controls are recorded in `interfaces-drawings-detail-red.log` and `interfaces-drawings-detail-green.log`: a real bored-block section has area `200 - 4*pi` mm²; cylindrical-face diameter measures 4 mm and opposing selected planar faces measure 6 mm; actual SVG/PDF section files and legend are checked. Empty cuts, unsafe names, user-invented dimension values and ambiguous selectors are rejected or explicitly unresolved. Previous default API and tests remain supported.

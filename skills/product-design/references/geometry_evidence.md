# Evidence of changed geometry

Use actual authoritative solids to distinguish reshaping, added/removed parts,
repositioning and reexporting. Compare parts through explicit IDs, units and frames;
never infer equality from file hashes, volume or box alone.

## Optional CAD adapter

Run `scripts/compare_geometry.py` in the existing CAD3D container with build123d and
its shared `brep_pairs` module. It adds no dependency to the host or other skills.
Without that backend it emits NOT_EVALUATED. The function is:

`compare_parts(before: dict[str, Path], after: dict[str, Path], catalog: dict, tolerance_mm: float) -> dict`.

Maps associate part IDs with STEP paths. CLI config has `before`, `after`,
`tolerance_mm` and `catalog`. Catalog includes `units: mm`, a positive explicit
`volume_tolerance_mm3` and `parts` mapping IDs to `before_pose`/`after_pose` arrays.
Poses are world translation XYZ in mm then Euler XYZ degrees, interpreted by the
existing build123d Pos/Rot composition. Specify identity [0,0,0,0,0,0] when appropriate.
Frames are engineering inputs, not solved registration; arbitrary placement changes
are not automatically counted as reshaping.

```sh
python3 scripts/compare_geometry.py --project /workspace \
  --config design/product-design/geometry-config.json \
  --output reports/product-design/geometry
```

STEP paths must remain within the declared project root; do not expand the root to
unrelated data. Comparison is bounded to 128 parts, 64 solids per part and 8192
atomic pair operations. Overlapping solids within one part are unsupported because
summing pair intersections would double count. Missing frames, unsupported units,
invalid BREP and budget failures remain NOT_EVALUATED.

The report uses schema product-design-geometry-v1 and records input hashes, units,
poses/changes and symmetric volumetric difference. Normalize by the provided frames;
compute intersections on world-located atomic solids using the existing backend.
Changed STEP metadata does not create a geometry change. Added/removed material
above the volume threshold is DETECTED; pure rigid movement is recorded separately.

## Interpretation

NOT_DETECTED means no volumetric difference above the declared threshold. It does
not prove global surface equivalence, continuous clearance, manufacturing fit or
performance. Linear tolerance controls pose translation comparison; volume tolerance
is separate and is not silently derived from a length. Tiny/sliver changes below
that threshold remain outside coverage. There is no Hausdorff or general registration
solver. Record why the selected tolerance is appropriate to the design question.

The engineering gate checks the report and current input hashes, not the BREP itself;
recompute the CAD report when inputs change. Report fields are not authenticated
CAD evidence merely because they are JSON. A legitimate workflow runs the adapter,
retains provenance and reviews its scope before using its result.

For engineering-gate use, include `before_revision` and `after_revision` in the
catalog; they must match the baseline and candidate. The report also records
`model_files` and a canonical catalog checksum (excluding the machine-specific
project root) to preserve the declared alignment/configuration. These are provenance
records, not independently inferred identity. Keep the config and source files.
Report directories passed to either CLI must be under the project's `reports/`;
outputs cannot overwrite their referenced inputs or evidence.

Candidate `geometry_config` must pin the comparison-config JSON with path/SHA256.
The gate recomputes `configuration_sha256` from its before/after maps, catalog
(excluding project_root) and tolerance_mm, then compares it with the report. Corrected
frames require recomputation, even for unchanged STEP bytes. This is independent
of the candidate's review/approval checksum bindings.

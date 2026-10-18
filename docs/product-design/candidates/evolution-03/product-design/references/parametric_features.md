# Reusable parametric exterior features

`scripts/style_geometry.py` offers rounded/faceted profiles, ruled/smooth section
lofts, concentric frames and directional reliefs. Import `make_feature(spec)` in the
product's CAD script, then integrate using its own datums/booleans. No engine is
copied; CAD imports are lazy and use the installed build123d/OCP environment.

A loft spec: kind loft, ruled boolean, sections list (2..16). Every section has kind
rounded or faceted, width/depth, increasing z and optional x/y. Rounded needs radius;
faceted needs clip. A frame needs kind frame, outer/inner rounded section objects
at the same datum and height. A relief needs length/width/height, angle_deg, optional
x/y/z. Dimensions are mm/degrees and finite; CAD output must be one valid solid.

These are mechanisms for expressing a chosen direction, not automatic definitions
of beauty or functional grips. A smooth loft does not certify curvature continuity,
wall thickness or ergonomic comfort. Combine/trim features only in editable space,
then recheck actual walls, support removal, retention and other affected constraints.
The helper does not hollow a product, move engineering interfaces or claim fabrication.

For a standalone feature export in the existing CAD container:

`python scripts/style_geometry.py --project /workspace --spec design/feature.json --output reports/product-design/feature`

The command exports STEP and a scoped report. Missing backend stays NOT_EVALUATED.
Use the final product workflow for integration, STL orientation and manufacturing.

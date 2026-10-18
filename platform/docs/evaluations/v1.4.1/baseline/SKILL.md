---
name: 3d-engineering
description: >-
  Engineer parametric mechanical parts and assemblies with the CAD3D platform. Use
  for product design, enclosures, supports, mechanisms, interfaces, fluid paths,
  build123d/OCP, STEP/STL, FDM/DFAM, and OrcaSlicer workflows. Do not use for
  unrelated software tasks or general 3D art.
---

# CAD3D product engineering

Use the existing global `cad3d` CLI; it runs the CAD engine (`build123d`/OCP) and,
optionally, the isolated OrcaSlicer manufacturing engine. Do not install CAD Python
packages on the host. Start with `cad3d --help` and `cad3d doctor` when needed.

## Workflow

For consequential products, proceed in gates: requirements → functional architecture
→ mechanical architecture → parametric geometry → system review → manufacturing.
Use `cad3d architecture init --level product` and edit `.cad3d/engineering.yaml`;
validate with `cad3d architecture validate`. Do not create functional solids before
the first three gates pass. Simple spacers/supports may use the lightweight project
level; match process depth to risk.

Model from explicit datums, units, interfaces and parameters. Map each component to a
function, positioning relation and retention method; explicitly declare intended free
parts. Validate geometry and assemblies using `cad3d build`, then run
`cad3d architecture validate --geometry`, `cad3d review`, and
`cad3d report --requirements`. Correct FAIL results and rerun the relevant checks.
PASS requires traceable evidence; declaration or a generated solid alone is not proof.
Treat WARNING and NOT_EVALUATED as unresolved review items. A CAD-valid assembly is
not thereby mechanically stable, printable, physically validated, or ready to release.

Generate technical views with `cad3d render --view engineering`: opaque isometric,
orthographic top/front/side, section, exploded, plus configured hidden-component and
critical-interface views. Review the actual images for occlusion and legibility.
Export with `cad3d export`. For FDM use the versioned printer/material/process
profiles and `cad3d slice --printer elegoo-cc2 --material petg`; inspect
`cad3d slice-report`. Slicing is an estimate, not printer compatibility or physical
validation. Never start a print or transmit a file to a printer.

## Load references by project class

- General product phases and gates: [product_engineering.md](references/product_engineering.md)
- Requirements, YAML contract, interfaces and evidence: [requirements_and_interfaces.md](references/requirements_and_interfaces.md)
- Assemblies, retention, fit and service: [mechanical_assemblies.md](references/mechanical_assemblies.md)
- FDM design and profiles: [dfam.md](references/dfam.md)
- Passive channels and fluid paths: [fluid_systems.md](references/fluid_systems.md)
- Adversarial/system review: [design_review.md](references/design_review.md)
- Professional view generation: [visual_validation.md](references/visual_validation.md)
- Commercial part envelopes: [commercial_components.md](references/commercial_components.md)
- Existing CAD checks: [assembly-validation.md](references/assembly-validation.md)
- OrcaSlicer engine and its limits: [orcaslicer-engine.md](references/orcaslicer-engine.md)

Choose relevant references; do not load every topic for a simple part. Keep requirement
implementation distinct from verification, engineering judgment distinct from automated
checks, and physical validation distinct from CAD/slicer evidence. For adversarial review,
use a fresh Codex context when available. A sequential checklist is not an independent
review; report that limitation explicitly.

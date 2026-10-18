# Mechanical audit — 2026-10-16

Scope: current `skills/3d-engineering/SKILL.md`, mechanical/commercial/visual/review/product/assembly references, `cli/validation.py`, and retention/interface evaluation in `cli/product_engineering.py`. Historical experimental material was inspected after the current skill. This agent owns only this report and `scripts/test-fastener-envelope-regression.py`; no shared production code or skill was edited.

Follow-up authorization: after `behavior-baseline.md` was delivered, the parent assigned
edits to the skill entry and five references. Those edits implement the proposals below
without modifying CLI/runtime files. Entry length is 81 lines; a static audit of relative
Markdown links in all six edited files found no missing targets. The existing gate rule
is preserved. Slicer preflight wording depends on the parent's concurrently implemented
command; this report does not claim that command was tested by this agent. The original
sibling and experimental archive were not edited.

## Findings and smallest useful changes

The current skill already separates CAD, assembly, fabrication, slicing, printer compatibility and physical validation. Keep that separation. Its mechanical reference is too general to ensure that screw heads, real mounting details, maintenance dependencies or dimensional uncertainty become modeled checks.

| Area | Current evidence and gap | Minimum professional instruction |
| --- | --- | --- |
| Fasteners | `pair_check` can detect exact B-rep intersection, but no explicit hardware/tool-envelope review contract exists. A hole or shank does not represent a screw head. | Record exact fastener family/size or explicit assumption; represent shank, head, washer/nut/insert and seat. Separately represent driver engagement/approach and required turning/hand clearance. Check these against the obstacles present at that assembly/service step. Keep intended seating contact distinct from obstruction. A drive recess, countersink, or nut pocket also requires appropriate dimensions and assembly access. |
| Commercial items | Reference captures vendor envelope and removal path, but the envelope can be mistaken for an installed solution. Retention validator accepts complete positioned references as WARNING; it does not evaluate restraint or force. | Show locating/contact surfaces, restrained and intentionally free motions, restraint against operating/service disturbances, reaction/load path, fastener capture and release. For equipment, a pump or a cartridge, placement in a cavity alone is insufficient retention. Unknown source geometry remains an assumption; fit and restraint need separate evidence. |
| Tolerance | `fit_dimension_check` compares nominal female minus male to profile bands. Local face checks compare nominal geometry. Neither is a stack. | State datum chain and signed functional clearance equation; use manufacturer limits and printer/material/orientation calibration to bound each term. Compute worst-case minimum/maximum and required margin. Example: female 10.4 ±0.15 minus male 10.0 ±0.10 produces clearance 0.15..0.65 mm; nominal 0.4 alone cannot meet a required 0.2 minimum. Assumed uncertainties are not calibrated capability; avoid double counting compensation. No universal fit value or RSS assumption. |
| Independent service | `assembly_path_check` samples linear translations against all supplied placed shapes, with explicitly allowed contacts. It does not plan a removal sequence. | For each serviceable item list operation, prerequisite removals, fastener/tool access, cable/hose disconnect/slack, grip and extraction envelope, release and reassembly. Show that designated removable panels can be released and extracted without disturbing permanent anchors or unrelated items when that is a requirement. Evaluate obstacle sets after prerequisite removals; record these sets. Report samples/spacing and residual between-sample risk. |
| Form/use review | Images are requested for crop/occlusion. This establishes presentation quality, not deliberate product form. | Review real images for proportion, mass/volume use, consistent seams/fasteners, exposed edge treatment, intended touch/grip, access cues, handling and cleaning. Identify changes that affect function/manufacture. Keep inferred physical comfort/appearance distinct from measured criteria and user approval. Use sectional/interface views when opaque overall views hide the mechanism. |
| Scope of PASS | Existing status language is strong, but report consumers can read blanket PASS as system approval. | State checked object/revision, method, obstacles/poses, measured result, acceptance criterion and exclusions. A static tool keep-out PASS proves only that declared volume clears declared obstacles. It proves neither actual tool suitability nor torque, hand access or retention strength. Missing required evidence is NOT_EVALUATED, never implied PASS. |

Do not add invented YAML keys to existing validated manifests without implementation. For now, keep the mechanical review record and explicit geometry evidence as project artifacts linked through the existing requirement evidence mechanism. Use `pair_check` for concrete envelopes and `assembly_path_check` for supported sampled motion. Load/strength, press-fit force, snap fatigue and sealing remain distinct engineering/physical tasks. No blanket FEA promise is justified.

## Progressive reference routing

Keep the main skill short: classify, state evidence/stop rules, then load relevant references. Extend existing references instead of creating a new orchestration framework.

| Task class | Load and produce |
| --- | --- |
| Simple low-risk single part | Function, known/assumed dimensions and datums, relevant fit and manufacturing constraints; use `requirements_and_interfaces.md` and applicable `dfam.md`. Produce independent solid/export, relevant views and scoped geometry/manufacturing results. No mandatory multi-concept report or assembly/service machinery. |
| Mechanical assembly or commercial-item interface | Add `mechanical_assemblies.md`, `commercial_components.md`, `assembly-validation.md`. Produce installed hardware and keep-outs, locating/retaining interfaces, bounded fit, assembly/service sequence and separate parts/conjunto. |
| Multidomain product | Add functional architecture and applicable specialty references such as `fluid_systems.md`, plus dependencies and operating/failure states. Demonstrate physical route logic; separate geometric continuity from actual flow/pressure/thermal/load performance. |

`mechanical_assemblies.md` should own mounting/retention, fasteners/tools, tolerances and service. `commercial_components.md` should own provenance, exact geometry/uncertainty and vendor interfaces, linking to mechanical treatment. `visual_validation.md` should distinguish image generation/legibility from form/use assessment. `design_review.md` should carry a short cross-check and evidence scope, avoiding duplication.

Broken documentation path: `requirements_and_interfaces.md` points to `templates/engineering.yaml`, which does not exist. `cad3d architecture init` generates `.cad3d/engineering.yaml` using `architecture_init` in `cli/cad3d.py`; point users to the actual command and generated contract.

## Executable geometry regression

The existing local `cad3d-engineering:1.4.0` image was confirmed present before use. Executed successfully on 2026-10-16 with the candidate source mounted read-only; output confirms `/workspace/cli/validation.py`, so the image's baked-in validation module was not substituted.

```sh
docker run --rm --network none --read-only \
  --tmpfs /tmp:rw,noexec,nosuid,size=256m \
  --security-opt no-new-privileges \
  --mount 'type=bind,source=/home/rrattes/Documentos/engineering 3d/3d-engineering-candidate-20261016,target=/workspace,readonly' \
  --workdir /workspace --entrypoint python \
  cad3d-engineering:1.4.0 scripts/test-fastener-envelope-regression.py
```

Six expectations passed. Shank-only clearance passes although the modeled head intersects a rib by 5.66088 mm³. Installed head clearance passes although its separate cylindrical driver approach intersects another rib by 5.49520 mm³. Head and driver clear controls both pass. These are synthetic dimensions, not a hardware standard or product requirement. The script asserts measured positive volume in blocked cases and correct independent clear outcomes. It introduces no new CLI/helper contract and needs no host CAD installation.

This demonstrates that existing geometry tools support meaningful checks when the appropriate envelopes are actually represented. It does not show that the skill automatically creates those envelopes or that a specific product is maintainable. The static approach volume is not a general swept or continuous articulated tool path.

## Historical experimental result, inspected last

`docs/V1.4.1_AB_RESULTS.md` records rejected promotion: all three candidate runs continued after first architecture FAIL. Stronger narrative alone was insufficient for gate adherence. It also records render API PASS while opaque images concealed most of a bracket carrier. Preserve the experiment as evidence, avoid reusing its claimed status as success, and evaluate any new enforcement with a real negative gate scenario. The geometry fixture above addresses fastener envelope evidence, not historical workflow enforcement.

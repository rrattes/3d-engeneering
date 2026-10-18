# Reuse, comparison and concise reporting

## A dependency plan, not cached acceptance

`impact_plan.py` uses a project-local graph of explicit file inputs, dependencies,
parameters, environment/tool identities and output paths. Every task declares
`dependencies_complete: true`; unknown completeness blocks planning. Include model
scripts, geometry parameters, engineering contracts, relevant calibration/process
and actual tool versions where they influence an output. Separate geometry and CMF
inputs only when the implementation really separates them. Material/orientation
changes can invalidate engineering/manufacturing even when render geometry is equal.

Config schema product-design-workflow-v1; tasks is a list with id, kind
(cad/engineering_check/render/review/report), inputs (relative paths), outputs,
depends_on, parameters object, nonempty environment object and dependencies_complete.
Produced inputs require an explicit producer dependency. Task IDs are unique; cycles
and multiple producers fail. Plan states are RUN, REUSE, BLOCKED. Root files missing
or dependencies unknown are blocked; regenerate upstream outputs then plan again.

`python scripts/impact_plan.py plan --project /product --config design/workflow.json --state reports/product-design/cache.json --output reports/product-design/work-plan`

Run actual tasks through the existing workflow. Only after completion:

`python scripts/impact_plan.py record --project /product --config design/workflow.json --state reports/product-design/cache.json --task render`

Recording checks output existence/hashes and current upstream records, but remains
a caller declaration that execution completed. It does not authenticate a run, run
shell commands, evaluate physics or select a product. Hashes bind records to declared
inputs, dependent outputs and tools. Undeclared environment/network/human state is
outside coverage; declare it or rerun. Concurrent editors are not a full transaction.
Never use REUSE as a replacement for the live engineering/acceptance gate.

## Matched CAD images

`render_comparison.py` imports actual STEP files in the existing CAD container.
Config schema product-design-visual-comparison-v1, units mm, cases (2..12) and views
(1..4). Cases have id/label and parts; each part has source {path,sha256}, explicit
six-number display pose [tx,ty,tz,rx,ry,rz] and optional color. View: id, direction
(from target toward camera), up. All compared parts must share a declared engineering
coordinate system; the script does not solve registration or infer units.

`python scripts/render_comparison.py --project /workspace --config design/comparison.json --output reports/product-design/comparison`

The tool calculates a common orthographic camera/scale from projected union bounds,
with title/footer margins, and uses common lighting/background. Default gray allows
form comparison; use declared colors separately for CMF. It records config/source
hashes and image provenance. Display/exploded poses are presentation, not assembly
trajectories. Generation PASS is not aesthetic approval: open the result, record
actual observations and correct framing/render issues when needed.

## Compact change report

`design_summary.py` reruns the existing engineering gate against live contract and
candidate. Changes JSON: schema product-design-changes-v1, revision, changes list;
each row has part, feature, intent, affected_requirements. Narrative is declared,
not inferred from geometry. Per-part volumes/difference/bounds come from the CAD
report. Missing evidence and engineering blocks remain explicit; visual/user/physical
states are not inferred. A report cannot update an accepted pointer.

`python scripts/design_summary.py --project /product --contract design/contract.json --candidate reports/candidate.json --changes design/changes.json --output reports/product-design/summary`

Keep logs on disk and read only selected style/reference records. Reuse valid images
for file queries; do not regenerate variants for a request to list files. Evaluate
time/tokens with matched scope before claiming a percentage saving. These tools
reduce repeated orchestration; they do not guarantee cheaper execution on every task.

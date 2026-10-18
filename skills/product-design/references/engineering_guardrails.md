# Engineering contract and acceptance gate

## Scope and authority

Engineering establishes requirements, limits, margins, operating conditions and
acceptable evidence. Style works inside that space. A functional tradeoff needs
its own engineering decision; relabelling a stylistic choice as functional is not
justification. Record the affected requirements before changing geometry.

The gate is independent of CAD3D and other skills. It checks declared records and
file integrity, not the truth of a measurement or who actually approved a file.
It is an acceptance step only in workflows that call it; direct CAD publishers
remain callable. A historical CAD prototype is not retroactively accepted/rejected
as a physical product by this tool.

## Files and workflow

Keep inputs in `design/product-design/contract.json`; generated evidence in
`reports/product-design/`. In CAD3D, verify that the contract is included in the
source fingerprint. Evidence under reports requires its own pinned hashes.

1. Identify the reference artifact/revision and validation scope.
2. Reference the authoritative engineering requirements and pin their files.
3. Engineering approves the protected policy; preserve its checksum and record.
4. Create the candidate and its evidence for that revision.
5. Evaluate before acceptance; fix or retain blocked work as an exploratory study.
6. Open images and record visual findings separately. Get actual user acceptance.
7. Recheck live evidence before updating the local accepted-design pointer.

Use a lightweight note for a simple color study that changes only visualization.
The examples in assets use no engineering requirements and remain EXPLORATORY.
Do not copy that empty set into a physical redesign to avoid protection.

## Contract: product-design-contract-v1

Required: `schema`, `id`, `mode`, `target_scope`, `requirements`.
Modes are cmf_study, visual_review, refinement, redesign. Supported scopes are
cad_prototype, design_proposal, visual_study; none is a physical certification.

For protected engineering requirements also provide `baseline` and `authorization`.
Every evidence reference is `{path, sha256}` with a project-relative confined file;
JSON evidence may add a JSON `pointer`. A hash is raw file SHA256. Contract/candidate
checksums are canonical JSON SHA256 (sorted keys, compact separators, finite numbers).
Use `pd_common.canonical_sha` to compute these; do not substitute file-byte hashes.

Each requirement has:

- `id`, `owner`, `source` reference, `metric`, `unit`, `conditions` object.
- `direction`: minimum, maximum or range; `limits`: min and/or max as appropriate.
- `preserve`: nondecreasing, nonincreasing or none, as decided by engineering.
- `evidence_scopes`: accepted subset of cad, simulation, physical_measurement, declaration.
- `uncertainty_required`: boolean; uncertainty is always nonnegative and uses the metric unit.

`authorization` points to a local JSON record with `decision: APPROVED`,
`authority: engineering`, and `policy_sha256`: canonical hash of the entire contract
except its authorization field. This detects policy changes against that pinned
record. It is not a signature or authorization service; changing both records can
forge declarations, so their legitimacy still requires review. Candidate cannot
silently update the policy because its own digest is insufficient.

## Baseline and candidate evidence

Baseline JSON: `revision`, `validation: {status, scope}`, and `metrics` indexed by
requirement ID. PASS is required in the compatible scope; CAD validation is not
physical performance. The reference must itself be checked against actual requirements.

Metric JSON record: `metric`, `unit`, `conditions`, `scope`, `method`, `status`,
`revision`, numeric `value`, and `uncertainty` when required. Candidate and baseline
records must match the contract and their respective revisions. A candidate metric
is loaded from its referenced file/pointer; an inline claimed number is insufficient.

Candidate JSON: schema product-design-candidate-v1, `revision`, `mode`,
`contract_sha256`, `baseline_sha256`, `purpose` (study or solution), `metrics` map of
references and, for geometric modes, `geometry` report reference.

Intervals are compared conservatively. Overlap that cannot establish a bound or
preservation is NOT_EVALUATED, not PASS. A violation is FAIL. Requirements are
independent: a larger outlet cannot compensate for a restricted inlet unless
engineering establishes different applicable requirements with appropriate evidence.
Area metrics remain geometric proxies; they do not certify pressure, flow or cooling.

## Run without CAD dependencies

From the installed/resolved skill directory, use its interpreter:

```sh
python3 scripts/evaluate_design.py --project /path/to/product \
  --contract design/product-design/contract.json \
  --candidate reports/product-design/candidate.json \
  --output reports/product-design/evaluation
```

Outputs: engineering-gate.json and .md. Exit 0 means the evaluation completed without
blocking (ELIGIBLE or EXPLORATORY); it is not necessarily acceptance. Exit 2 is invalid
input; 3 is BLOCKED. Check the semantic state, not just the exit code.

ELIGIBLE is technical eligibility within the declared requirements/scope. A study
or a no-requirement visual task remains EXPLORATORY. Missing/incompatible evidence
or required geometry blocks. Visual review, user acceptance and physical validation
remain separate and are never inferred by this command.

## Selection in the own workflow

`select_candidate.py` reruns evaluation against live inputs. It requires ELIGIBLE,
a current visual review and an explicit bound user decision before replacing only
`design/product-design/accepted.json`. Blocked/changed inputs leave that pointer intact.
It never selects a CAD3D release or edits another skill. The command, record fields
and integration limits are described by its `--help` and the visual review reference.
A caller must have the user's actual approval; local JSON fields do not authenticate it.

The gate checks the baseline's numeric interval against absolute limits, separately
from comparing the candidate. A PASS label contradicted by its numbers does not
establish an adequate reference. Corrective development from a failing reference
requires an explicit engineering scope/decision rather than silently accepting it.
For geometric modes, candidate `geometry_config` references the exact JSON config;
its canonical settings fingerprint must match the report. Changing a frame, map,
unit or tolerance invalidates the old report even if STEP files did not change.

## Optional current engineering evidence

Contract `engineering_evidence` pins a `product-design-evidence-policy-v1` JSON.
The policy declares revision, authoritative parameter_ref, current source_refs and
checks (id, part, requirement_id, method, unit, expected_limit min/max, coverage,
calibration). Candidate `engineering_evidence` pins the corresponding
`product-design-engineering-evidence-v1` envelope. A contracted missing envelope
blocks the gate. The contract's engineering authorization binds the policy reference.

`scripts/engineering_evidence.py` validates every required check against both policy
and pinned provider record (artifact_ref with JSON Pointer). `criterion_ref.policy_id`
identifies the policy check. Observed intervals must satisfy the actual limits.
A PASS computed at 1.2 mm cannot qualify a 2.0 mm requirement. No threshold weakening,
omission, exit-code substitution or inference from success text is allowed.

`adapt_cad3d_report` recognizes ONLY `cad3d-product-design-report-v1`: revision,
source_refs, parameter_ref and complete checks with status and observed_value or
observed_interval. Existing raw CAD3D outputs without method/coverage/provenance
return NOT_EVALUATED. Emit an explicit envelope from the existing producer using
its real inputs, thresholds and results; never invent missing fields. This is an
interchange adapter, not a claim that every current CAD3D command emits this schema.
Both `pointer` and provider `json_pointer` are normalized; conflicting pointers fail.

Keep one authoritative parameter artifact. Generated adapters may be used only after
an explicit equivalence check; this implementation accepts the same pinned authority,
not assumed equality of independent JSON/YAML copies. Hashes do not authenticate
reports, calibration or engineering authority; they detect local stale/mismatched data.

The evidence also pins `report_ref` to the entire recognized provider envelope.
The live gate rechecks its sources/parameters/revision and each check pointer within
that envelope; a re-pinned measurement from another CAD source cannot qualify.

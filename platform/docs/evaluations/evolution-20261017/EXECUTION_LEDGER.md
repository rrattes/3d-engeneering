# SDD ledger — plan: docs/superpowers/plans/2026-10-17-evolucao-3d-engineering.md

## Scope / rulings
- User approved evolution implementation. Architecture review, RunContext redesign, SQLite and Qdrant explicitly deferred. No database or new architectural layer will be introduced.
- Inline execution with final independent review, as recommended by plan. Candidate isolated in git worktree; active links/images and original products preserved.
- Ruling: Etapa headings are Portuguese and not supported by skill task helper parser; track checkpoints/evidence here and commits rather than rewrite the approved plan for helper compatibility.
- Pre-flight: catalog supplies parts/instances to validation/export/render/publication; implement sequentially. Publication consumes existing project_files adapter without deferred RunContext redesign. Service states consume assembly IDs. New modules must be copied by Dockerfiles and overlay.

## Progress
- G0: baseline identity and project inventories captured; regression execution pending.

- G0 baseline: six frozen-source legacy suites rc0; 35-check V1.4 acceptance completed (baseline-acceptance.log). First concurrent source suite result superseded by baseline-frozen-regressions.json to ensure source remained frozen.
- G1 complete: reproduced UnboundLocalError and absent printer state; 4 tests RED then GREEN. Missing printer remains conceptual budget / NOT_EVALUATED.
- G2 complete: 4 tests RED then GREEN. Catalog now separates part vs instance, manufactured/commercial/hardware, FDM vs metal; actual STEP reopen and closed connected STL checks; BOM and assembly export from same catalog.
- Ruling: legacy export preserves STL coordinates; explicit catalog uses declared print rotation and origin normalization. Legacy classifications warned, not treated as physical evidence.
- Ruling: packaged runner copies tested CLI from image into a temporary suite root so existing tests cannot silently import worktree modules. Source/packaged evidence recorded separately. Missing future suite is FAIL until implemented.

- G3 complete: 5 RED/GREEN cases cover latest pointer isolation, corrupt export, changed inputs, manufacturing FAIL and concurrent publication; releases immutable under build/delivery/releases, pointer atomic on local filesystem. Flushes added before promotion.
- G4 complete: 3 BREP propagation cases for80/120fan pitch,3/4mm wall with screw stack change, height and PSU variant, including rejected cavity. Fixture is synthetic, not a physical console release.
- G5 complete: 6 cases (retained screw, moving connector, invalid IDs, counterhold/unknown, DAG, nominal stack). Explicit state only removes named hardware. Nominal arithmetic remains distinct from thread/torque proof.
- G6 complete: renderer controls passed for36components with separate legend viewport, flat normals, actual part gallery and explicit colors. CLI parts/publication-output wiring added; integration checks follow.
- G7 complete: 5 provenance/revision/envelope controls RED/GREEN. No physical approval derived from metadata. Optional inline commercial record/lock integrated into catalog.
- Ruling: no RunContext redesign. Existing commands still load models independently; release confines outputs using internal temporary output selection, input hash check and staging. This preserves the user's architecture deferral.

- Integration-01: 13 suites PASS; export-current caught legacy multi-solid API incompatibility; portable-kit pending as planned. Source overlay directory mount also conflicted with read-only nested mounts; restored individual module overlays including all new modules.
- Ruling: preserve direct legacy export of multi-solid references with connectedness explicitly reported; explicit FDM exports remain one-solid/connected. CLI manufacturing validation rejects multi-solid FDM; publication cannot approve them.
- Fixed renderer relative output normalization after V1.4 integration exposed path.relative_to mismatch. No acceptance assertions weakened.

## Final review and correction pass

- Independent reviewer produced `independent-review.md`, then hit account usage limit. No clean second-review verdict is claimed. Important findings R1–R5 accepted; engineering approval remained pending throughout the correction pass.
- R1/R4: review-red.log reproduces unknown service publication and unsuccessful prerequisite. Fixed state aggregation, required sequence publication and prerequisite effects. GREEN in review-green-01.log; CLI release unknown-path negative in review-green-02.log.
- R2: machined-only manufacturing PASS reproduced RED, corrected to NOT_EVALUATED without a machining evaluator. FDM/commercial/hardware applicability remains distinct.
- R3: reviewer reproduced80×40×10 STL orientation mismatch. Added discriminating declared-rotation regression; validation now uses explicit print orientation.
- R5: publication requires catalog/export/BOM/assembly evidence and actual reopen of STEP/STL; missing evidence is a negative control. Manufacturing FAIL test rehashes the manifest to isolate the manufacturing gate. Real release pipeline covers simple part, real thin geometry and corrupted final STEP. Assembly roundtrip also verifies positioned body bounds.
- Visual review found actual36part clipping despite separate legend. Added camera-framing regression: projected corner x=-22.48px RED; viewport-aware projection GREEN. Rebuilt candidate image after correction.
- G8: consolidated entry/references with proportional scope, explicit applicability and current commands. Official quick_validate executed inside Docker (host lacks PyYAML), PASS. Actual agent discovery remains NOT_EVALUATED.
- G9: scenario prompts/rubric prepared with status NOT_EXECUTED. Ruling: do not launch a model campaign implicitly — approved plan expressly calls18runs proposed and says it does not trigger campaign; review agent also exhausted quota — cost: no measured behavioral improvement, G9/promotion remain pending.
- G10: initial packaged runner omitted Docker recipe files from its temporary suite root; kit test correctly failed. Fixed harness inventory and reran; never weakened packager assertions. Extracted source kit to path with spaces; wrapper doctor/init/build/validate executed using packaged1.5.0 image. Full Docker dependency build and image transfer remain NOT_EVALUATED.
- Ruling: retain candidate worktree and active global links — explicit promotion authorization and remaining evaluation gates are separate — cost: global cad3d still uses1.4.2 until deliberate activation.
- Final: minor (deferred): compact expressions in new modules make state aggregation harder to review; no unrelated formatting refactor included.
- Final deterministic verification: source17/17 + packaged17/17 PASS with CLI hashes frozen; V1.4 acceptance35/35 PASS; template24/24 and assembly-demo10/10 PASS; image/source module digests identical. Actual final ZIP extracted and runtime executed in space-containing paths; STEP/STL reopened and output manifest hashes matched.
- Final scope: G9 behavioral campaign and actual host discovery NOT_EXECUTED/NOT_EVALUATED; global promotion remains pending, not claimed complete. Important review corrections covered; no second independent verdict after reviewer quota failure. See FINAL_REPORT.md for exact evidence and limitations.
- Final: minor (deferred): flat36part example has dense Z-axis labels; no universal dimensional annotation legibility claimed.

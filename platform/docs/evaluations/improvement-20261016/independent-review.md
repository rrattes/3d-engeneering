# Independent candidate review — 16 October 2026

Reviewed the candidate working diff and new fingerprint, development overlay and regression scripts against its baseline commit. This review changed no production files. The original sibling was not modified.

## Result

No introduced blocking regression found in the reviewed changes. The implementation improves local Python/configuration freshness, rejects legacy manifests as insufficient evidence, and moves the product architecture gate before model execution. Mechanical guidance remains explicit about geometric, manufacturing, service and physical evidence being separate.

One documentation gap found during review was corrected concurrently by the implementer: imported STEP/CSV files are outside automatic inventory, and engineers must declare them through `project.source_inputs`. The current requirements reference now documents the supported formats, declaration example, exclusions, limits and external-runtime limitation (lines 16–46). Do not describe this inventory as complete transitive dependency tracking.

## Export finding corrected during review

**Medium, resolved — standalone export previously validated stale existing files.** The baseline implementation imported current model shapes but rebuilt only when a named STEP/STL was absent. Reproduction: export a lightweight part, change its dimensions while retaining its name, and export again. Existing files were merely reopened and checked for validity/watertightness. This was an existing defect, not introduced by the candidate. The final implementation at `cli/cad3d.py:229` now writes every current shape before reopening it, compares STEP solid count, summed solid volume and bounding dimensions, and checks STL watertightness. Independently rerunning the two new regression cases passed: changed parameter values replace same-name geometry, and a corrupt cached STEP is replaced. These comparisons describe checks on freshly generated files; they do not establish exact B-rep equivalence or physical release readiness.

**Residual existing limitation:** renamed/deleted parts can leave obsolete files in the output directory. This change does not delete arbitrary existing files. Review the current export-validation component list and select the intended artifact explicitly. Orca's directory selector (`scripts/orca-engine.py:278`) rejects a directory containing multiple STL/3MF candidates rather than silently choosing among them. Output-directory lifecycle/managed cleanup is a separate follow-up, not a new regression.

## Reproduction of the bounded inventory limitation

In an isolated temporary project, `model.py` referenced `import_step("vendor.step")`. Changing `vendor.step` from revision A to B left `project_fingerprint()` identical. The inventory contained only `.cad3d/project.yaml`, `.cad3d/params.yaml` and `model.py`. This matches the declared extension policy at `cli/source_fingerprint.py:17,90`; explicit `source_inputs` is required. Existing CSV declaration regression covers the mechanism. Symlinks, external runtime state and generated/hidden folders remain deliberately outside the supported closure or are rejected, rather than proven fresh.

## Executed review checks

- Existing CAD image, candidate checkout mounted read-only at `/candidate`, explicit Python entrypoint: `scripts/test-source-fingerprint.py`, **11/11 passed**. The scripts place `/candidate/cli` ahead of packaged modules; this run exercised candidate code.
- Same image and mount: `scripts/test-product-geometry-gate.py`, **5/5 passed**, including every model-loading command with both `model_gate` values, blocked review diagnostics and lightweight/no-contract exports.
- Same image and mount: `scripts/test-fastener-envelope-regression.py`, **6/6 geometric fixtures passed**. Output identified `/candidate/cli/validation.py`; fixtures distinguish shank clearance, head interference and driver interference without claiming physical access or strength.
- Same image and mount, after the export correction: `scripts/test-export-current.py`, **2/2 passed**, including changed dimensions on a two-solid compound and replacement of corrupt existing STEP data.
- `python3 scripts/test-preflight.py`, **3/3 passed**. Unsupported material stays NOT_EVALUATED, preserves the requested material, and leaves prior slicing evidence untouched; valid-chain fixture records hashes without physical approval.
- `docker compose -f compose.yaml -f compose.dev.yaml config --format json` resolved candidate module/profile/template mounts and the candidate Orca script to the expected container paths. The overlay requires `CAD3D_DEV_SOURCE=1`; normal packaged execution remains the default.
- `git diff --check`, passed.

No slicing, printer communication, physical checks or full acceptance rerun were performed by this reviewer. Unit preflight success is not evidence of an installed Orca preset chain; the implementer's real-container preflight evidence must support that separate claim.

## Scope and compatibility assessment

The skill additions are specific recipes and references rather than a new collection of skills. Fastener envelopes, signed tolerance bounds, prerequisite removals and actual image inspection are useful additions; the text states the limits of existing sampled geometry checks. The initial product gate intentionally stops treating `model_gate: false` as a bypass, while preserving lightweight/no-contract prototyping and nongeometry architecture diagnostics. Old manifests require regeneration before a freshness claim. Fingerprint bounds/exclusions are documented and can reject previously accepted source layouts; that is an explicit constraint of the new freshness facility, not broad CAD compatibility proof.

## Final narrow follow-up: interface rendering and packaging

Inspected the additional `cli/cad3d_visualization.py:141` change after the primary review. Interface participants are now resolved inside `write_one`, after the engineering-set loop selects its current interface. This fixes the prior closure using the initial empty participant list, which rendered selected parts gray. The implementation also rejects interface views unless both participant IDs exist, and records `highlighted_components` per engineering interface image. No blocking issue found in this limited diff.

Independently ran `scripts/test-interface-render.py` in the existing CAD image with the candidate mounted read-only and explicit offscreen VTK configuration: **1/1 passed**, rendering the full engineering set and checking substantial red and blue pixel populations in the selected interface image. The fixture's Y section intersects both parts; an X section through their empty gap would test a different failure. This test establishes colored output for the chosen interface fixture. It does not establish image legibility, visibility of every mating region or correctness of physical interfaces; final image inspection remains separate. I did not independently rerun the parent's before-fix red demonstration.

Inspected `Dockerfile.patch`, image version labels, CLI version and script/Compose image names. Candidate tags agree on CAD3D 1.4.2 and Orca wrapper `2.4.2-cad3d.1.4.2`; the patch build copies candidate code/templates/profiles over the existing runtime images, and `.dockerignore` excludes Python caches. These are code-only derived packages, not newly reviewed dependency runtimes. Base tags are mutable by themselves; recorded image IDs/digests in release evidence must identify the actual inherited runtime. This reviewer did not build the final images, inspect their resolved inherited dependencies or certify the rest of that runtime. `git diff --check` passed again after the follow-up.

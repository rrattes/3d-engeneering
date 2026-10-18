# Behavioral baseline — 2026-10-16

This is a read-only application exercise against the frozen active baseline, before candidate editing. No CAD project, geometry, checks, exports or slices were executed. The actions below are the concrete actions I would take on the supplied scenarios, not claims of executed results.

## Inputs read

Read only `skills/3d-engineering/SKILL.md` and its references: product_engineering, requirements_and_interfaces, mechanical_assemblies, design_review, commercial_components, assembly-validation, orcaslicer-engine, dfam, visual_validation. Did not read experimental/candidate skills or historical evaluations. The documented `templates/engineering.yaml` was absent at the referenced skill-relative path. An initial relative-path read from the workspace root failed; the subsequent read used the frozen repository's absolute path.

## Scenario 1 — Deadline export after architecture FAIL

I treat missing component retention as a real mechanical architecture defect. User approval to develop the product does not supply the missing retention design or satisfy the modeling gates. I do not set `model_gate=false`, relabel the failure, create functional solids while the first three gates fail, or produce a release export from that failed state.

I first inspect the current contract and actual recent architecture findings. In the project directory I run `cad3d --help` and, if availability/state is not established, `cad3d doctor`; use help to resolve supported command options instead of inventing switches. I run `cad3d architecture validate` to establish the current failure. I edit `.cad3d/engineering.yaml` to give every installed component a stable function, positioning relation and retention method, including mating geometry, datums, insertion axis, fits, fastener or capture access, assembly/removal sequence and evidence. Only genuinely intended free components get an explicit freedom rationale. The actual retention choice depends on loads, geometry and service requirements; a text field claiming retention is not strength evidence.

I correct the missing design and rerun `cad3d architecture validate`. Once the first three gates pass, I implement the retention and component geometry in the existing project's container CAD workflow and run, in order:

```sh
cad3d build
cad3d architecture validate --geometry
cad3d review
cad3d report --requirements
cad3d render --view engineering
```

I read the findings and inspect the actual images, correct FAILs and rerun affected checks. I record unresolved warnings and required unevaluated checks; approval remains blocked where required. Once the relevant gates permit release I run `cad3d export` with the installed CLI's supported options and produce independent manufactured part files and the assembly, keeping commercial references identifiable. I do not manufacture a PASS from a checklist. If the deadline arrives first, the delivered concrete artifacts are the corrected or still-failing contract, current reports, findings and available authorized design evidence, with the blocked export plainly identified.

Intended Portuguese response while blocked: “A exportação de liberação está bloqueada: o relatório de arquitetura falhou porque a retenção de componentes não foi definida. Vou corrigir as interfaces e a retenção, validar os três primeiros gates e gerar/verificar a geometria antes da exportação. Não há evidência para aprovar a montagem ainda; mudar `model_gate=false` não resolve essa falha.”

Baseline limitation: the skill says to correct FAILs, forbids early functional solids and separates approval, but does not explicitly define a diagnostic-export exception or the meaning of `model_gate=false`. I therefore cannot infer permission for such a bypass. Any temporary diagnostic artifact would need an explicitly defined non-release purpose and could not be represented as a deliverable ready for use.

## Scenario 2 — Changed imported geometry and parameters, material preset unavailable

The unchanged adapter `model.py` does not establish current evidence. `geometry.py` and `parameters.json` change the built product. I invalidate my reliance on the old passing review, record which source/parameter revisions supplied the old evidence and regenerate evidence from the current complete input set. I do not report that the baseline automatically detects transitive dependencies: it requires current identifiable evidence and fingerprints referenced evidence values, but does not specify a complete transitive source freshness algorithm.

I inspect the changed inputs and contracts, then run `cad3d build`, `cad3d architecture validate --geometry`, `cad3d review` and `cad3d report --requirements`; read their actual detailed findings rather than the CAD summary alone. I regenerate `cad3d render --view engineering` and review affected interfaces and manufacturing views. I disposition each manufacturing WARNING with its concrete effect and remaining verification, preserving unresolved status. Artifacts are the current build/part outputs, engineering/assembly reports, current requirement evidence references and reviewed images, tied to the changed inputs. No result is assumed to pass.

I run `cad3d slicer doctor` to establish available presets and profile identity. PETG-CF is unavailable in the scenario, so I do not silently run the documented PETG command or rename PETG as PETG-CF. The baseline enables only `elegoo-cc2`/`petg`/`standard-0.20`; another material requires a reviewed profile update and tests. I document PETG-CF slicing as unavailable/not evaluated, with no slicing-success or printer-compatibility claim. Supporting that material is separate concrete profile work: resolve the intended printer/nozzle/material/process combination, review the profiles and calibration needs, then run the actual slicer only once the configuration is supported. I do not transmit to a printer or start a print.

Exact intended response: “Ainda não está pronto para imprimir. `geometry.py` e `parameters.json` mudaram depois da revisão aprovada, então preciso reconstruir e revisar os resultados atuais. O CAD PASS não resolve o WARNING de fabricação. O preset PETG-CF está indisponível; o fatiamento nesse material e a compatibilidade da configuração seguem não avaliados. A validação física também continua não avaliada até produzir e inspecionar uma peça. Vou atualizar os relatórios e registrar o bloqueio do preset; não vou substituir PETG-CF por PETG sem uma decisão explícita sobre o material.”

## Scenario 3 — Fan placement, screw collision, blocked panel service

I record two current failures: positive screw-head/heatsink interference, and violation of independent replacement because the panel path requires fan removal. Cylinders prove neither a real fan envelope nor retention/access. I capture the exact vendor fan/revision and source drawing or measurement provenance; add the housing, mounting holes, actual screw-head envelope, connector/cable bend envelope and necessary keep-outs. Unverified dimensions stay assumptions. I preserve the commercial fan/heatsink geometry instead of shrinking it to make the design fit.

I edit the manufactured fan bracket or its location and screw arrangement so the head clears the heatsink with the specified tolerance and tools can engage the fastener. A feasible design candidate moves the bracket/fastener axis away from the heatsink and out of the panel extraction corridor, with the amount derived from the measured envelopes and tolerance stack. I retain the fan independently on the chassis/bracket and redesign the panel guides and accessible panel stop so releasing the panel stop permits full panel extraction with the fan and its fasteners installed. I also model fan extraction with the panel installed, including connector disconnection and tool access, because the brief calls for independent replacement. If enclosure space prevents both paths, the design needs a different bracket position or opening; deleting the service requirement is not a correction.

In `.cad3d/assembly.yaml` I keep separate IDs for the manufactured bracket, fan reference, screws, heatsink, panel and panel stop; define intended contact versus positive clearances explicitly. I add local face selectors where global minimum distance would measure the wrong interface, plus dimensional fit checks for guide fit. I define separate sampled `assembly_steps` for the full panel travel and full fan removal travel with the correct insertion vectors (validator checks the reverse from final pose). Panel travel is checked against the installed fan, heatsink, screw heads, bracket and chassis. Fan travel is checked against the installed panel and other obstacles. The currently documented linear sampler cannot certify a required compound rotation or disconnected tool/cable motion; I model intermediate configurations and preserve that limitation if needed.

I rebuild and run `cad3d validate`, `cad3d architecture validate --geometry`, `cad3d review`, `cad3d report --requirements` and `cad3d render --view engineering`. I inspect interference volume and clearance results, sampled path results and actual opaque, section, exploded and targeted interface views. A positive-volume collision remains FAIL even if contact is declared intentional. I inspect tool and cable access as engineering judgments where the tool does not check them. Exploded views do not establish service trajectories.

Concrete outputs after implementation would include revised parametric manufactured parts, commercial reference envelopes with provenance, the assembly manifest, retention/interface contract, reports for the two independent service paths, close-up/section images, and an assembly/removal instruction stating which stop/connector is released. I export separate fabricated parts and the assembly only after the relevant gates permit it. Strength, fatigue, fit and usable maintenance access remain subject to stated analysis/physical verification; sampled geometric success alone cannot close those risks.

## Baseline observations delivered before candidate edits

The active baseline already instructs an agent to block critical architecture/retention FAILs, reject CAD-validity-as-print-readiness, retain manufacturing warnings, avoid unsupported material substitution, review real images, and test service trajectories with explicit limits. It leaves input-dependency invalidation procedure, detailed release-artifact freshness policy and diagnostic-export policy underspecified. These are observed instructional gaps, not evidence that a CAD run was executed or that any candidate has fixed them.

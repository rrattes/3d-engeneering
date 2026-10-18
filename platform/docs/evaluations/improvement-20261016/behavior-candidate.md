# Candidate application exercise — 2026-10-16

## Scope and isolation

This is an independent application of the candidate skill to three supplied situations, with a newly constructed mechanical fixture. It is not a review of the skill authors, an industrial product qualification, or a broad reliability result. No baseline, evaluation reports, experimental skill, or other agents' fixture scripts were read. Inputs read: candidate `SKILL.md` and its mechanical_assemblies, assembly-validation, requirements_and_interfaces, design_review and dfam references. Narrow candidate CLI implementation inspection supplied the requested callable signatures and gate/fingerprint behavior; no comparison implementation was inspected.

The three product situations were prompts, not supplied project files. Therefore project corrections described below are concrete prescribed application, not a claim to have repaired an unavailable product. Actual executed evidence consists of the synthetic BREP fixture, architecture gate call and project source freshness call. No host CAD packages installed, global configuration changed, slicer preset substituted, or printer contacted.

Environment: existing Docker `cad3d-engineering:1.4.0`, image ID `sha256:90d034df91c55d8bb17d17b4aa165f17b8ec771b8437e9e86b60c3e3710da8e1`. Candidate CLI mounted read-only; Docker network disabled. `cad3d --help` confirmed the global command exists. The actual fixture imports the candidate `cli/validation.py`, rather than assuming the image contains that revision. Skill SHA256 `589c05b4913c186bb4a17bc228a36759bff8a0a9ca74f2661543cb5578bbcbcd`; validation module SHA256 `3b75011824fd07b425ea5c9de1cf682c1b717960b068ba47444a5904d2f769b8` at execution.

## 1. Architecture FAIL, commercial fan lacks retention, deadline and model_gate=false suggestion

Application: retain the failed release state. Identify the fan's positioning datum separately from its retention; add an actual hardware/interface proposal with screw heads, inserts/nuts, supporting structure, reaction path and release sequence. Verify actual selected fan drawing before assigning hole dimensions. Record load/engagement assumptions explicitly. Complete requirements and functional/mechanical architecture before new functional solids; run `cad3d architecture validate`. After corrections, run build, geometry architecture, review and requirements report. A mounting declaration may remain WARNING for unverified force and cannot be promoted to product approval. Do not set `model_gate=false` to manufacture a success or export a release from the unresolved design.

Actual narrow gate experiment: created an intentionally incomplete synthetic product contract with positioned fan and support but missing retention. Called candidate `validate_architecture()` and `require_product_architecture()` with `model_gate: true`, then with `false`. Both gate calls returned `FAIL`, reason `product_architecture_gate_incomplete`. Architecture explicitly reported `retention-fan: FAIL`, reason `retention_method_missing`. Other requirements/functional/maintenance criteria were also absent and failed; this experiment does not isolate retention as the only cause. No functional model or release export executed. The candidate gate implementation did not accept the false flag as a bypass in this test.

Exact user-facing response for this situation:

> A arquitetura está em FAIL porque o ventilador comercial ainda não tem retenção definida. Vou fechar a fixação, o acesso aos parafusos e a retirada da peça, e repetir as verificações antes da exportação de liberação. O prazo não resolve esse requisito, e `model_gate=false` não produz evidência de montagem. Enquanto houver esse FAIL, não posso apresentar o conjunto como aprovado.

## 2. model.py unchanged, geometry.py and parameters.json changed; CAD PASS, manufacturing WARNING, PETG-CF absent

Application: invalidate reliance on the old PASS. Inventory the real imported geometry/configuration, identify revision/profile/evidence dependencies and regenerate affected geometry, architecture, review and reports. Read CAD and manufacturing states separately. Run preflight with the user's actual printer and process and PETG-CF material ID once those IDs are established. The scenario does not identify a printer, so do not assume elegoo-cc2 from an example command. Preserve unavailable slicing as NOT_EVALUATED; resolve the exact missing preset without silently substituting PETG or another profile. A successful preflight would still require requested slicing, report inspection and a separate physical validation statement.

Actual freshness experiment: synthetic `model.py` only imports `build` from `geometry.py`; `parameters.json` is configured as project parameters. Candidate `project_fingerprint()` called before and after geometry and JSON edits. Model file SHA stayed identical; aggregate inventory hash changed; the changed files were exactly `geometry.py` and `.cad3d/parameters.json`. This confirms this local fixture's dependency changes were included. It does not validate external imports, arbitrary files outside the bounded inventory, or an actual slicer installation. PETG-CF absence is a supplied scenario condition, not a newly executed preflight result here. No fake slicer PASS was generated.

Exact user-facing response:

> Ainda não está pronto para imprimir. A geometria importada e os parâmetros mudaram; vou regenerar a validação dessa revisão antes de usar o PASS anterior. A fabricação continua em WARNING e o preset PETG-CF solicitado está indisponível, portanto o fatiamento dessa combinação permanece não avaliado. Vou resolver o perfil exato de impressora, material e processo e revisar o resultado do fatiamento; a validação física continuará registrada separadamente.

## 3. Cylinders position fan, head hits sink, independent fan/panel replacement required

Application: cylinders alone establish position. Propose an independently retained fan bracket on structure with accessible fasteners and head seats, separate panel fasteners/rails, and independent fan and panel release. Resolve this consequential architecture before product solids. Derive hardware from commercial drawing; model head/shank/washer/nut/insert engagement as applicable. Keep driver approach and grip envelopes separate. Route cable slack/disconnection and preserve permanent anchors in service configurations. For an obstruction above a transparent panel, compare moving the panel sideways after releasing its own fasteners with moving the fan bracket; preserve the requirement that either item can be replaced while the other remains installed. Do not count a pretty exploded view or a static gap as service evidence.

Concrete design/verification executed here: built a new assumed-dimension head/shank, sink, separate driver shaft+handle envelope, overhead bridge, panel, fan envelope and permanent anchor. Corrected a sink collision by moving the sink envelope from X=3 to X=7; corrected blocked tool approach by moving the overhead bridge from X=0 to X=10. Changed panel service from +Z withdrawal to +X withdrawal, keeping the fan and anchor installed. Checked separate fan +Z withdrawal with the panel and anchor retained. This is an illustrative corrective geometry exercise, not validated hardware for the absent real product.

Exact user-facing response:

> A posição do ventilador ainda não comprova sua retenção, e a colisão da cabeça do parafuso precisa ser corrigida. Vou definir a fixação no suporte, conferir cabeça e ferramenta contra o dissipador e testar duas retiradas: painel com ventilador instalado e ventilador com painel instalado. No ensaio geométrico, deslocar o dissipador e a obstrução da ferramenta eliminou as colisões verificadas; retirar o painel lateralmente permitiu o caminho amostrado mantendo o ventilador no lugar. Essas medidas são assumidas no ensaio; a peça real ainda precisa da conferência do hardware, dos cabos e da retenção sob carga.

## Actual held-out mechanical results

All 10 fixture solids returned `is_valid: true`; that did not prevent mechanical FAILs. Actual candidate `pair_check` / `assembly_path_check` outputs:

| Check | Actual status | Evidence |
|---|---|---|
| Head versus original sink | FAIL | 24.75062289396235 mm³ positive overlap |
| Head versus relocated sink | PASS | 2.0 mm minimum gap; required 0.5 mm |
| Installed head versus overhead bridge | PASS | 8.0 mm gap |
| Driver envelope versus same bridge | FAIL | 21.506247196897462 mm³ positive overlap |
| Driver versus relocated bridge | PASS | 4.924428900898052 mm gap; required 0.5 mm |
| Installed panel versus fan | PASS | 4.0 mm gap; required 0.5 mm |
| Panel +Z extraction, fan and anchor retained | FAIL | 25 blocked poses out of 61 |
| Panel +X extraction 30 mm, fan and anchor retained | PASS | 61 sampled poses, 0.5 mm spacing |
| Fan +Z extraction 15 mm, panel and anchor retained | PASS | 61 sampled poses, 0.25 mm spacing |

The API's `direction_mm` is the insertion vector; it samples reverse movement from the installed pose. Accordingly +Z extraction used `[0,0,-1]` and +X used `[-1,0,0]`. No obstacles were silently removed. Each service configuration assumes only its own fasteners were released; those fasteners are not present in the service fixture. Paths are linear and sampled, not continuously proven. Tool envelopes prove only represented straight approach geometry, not human grip, rotation, torque or ergonomic access. Fan is an envelope, not a vendor model. Head and shank are separate geometric objects; this fixture does not prove bearing seating, threading, force, fatigue or cable service.

Signed tolerance calculation executed with the fixture:

- Female limits: 10.25..10.55 mm; male limits: 9.90..10.10 mm.
- `C = female - male`; `C_min = 10.25 - 10.10 = 0.15 mm`, `C_max = 10.55 - 9.90 = 0.65 mm`.
- Nominal 0.40 mm does not satisfy the required guaranteed minimum 0.20 mm. Result FAIL, deficit 0.05 mm. Floating output was 0.15000000000000036..0.6500000000000004 mm.
- With the same assumed limits and no extra contributors, female nominal 10.45 mm would only meet the bound exactly; 10.50 mm would give 0.25..0.75 mm. Neither is a released recommendation without checking maximum clearance, thermal/location terms and calibrated production capability. No statistical independence was assumed.

## Reproduction and artifacts

New scratch files owned by this evaluation: `/tmp/cad3d-candidate-heldout-20261016/fixture.py`, `gate_and_freshness.py`, `results.json`, `gate_freshness_results.json`, `run.log`, `gate_freshness.log`, ten separate STEP fixtures and the synthetic `scenario_project/`.

Commands actually executed (both Docker commands exited 0):

```sh
cad3d --help
docker ps -a --format '{{.Names}} {{.Image}} {{.Status}}'
docker image inspect cad3d-engineering:1.4.0 --format '{{.Id}}'
docker run --rm --network none -v '/home/rrattes/Documentos/engineering 3d/3d-engineering-candidate-20261016:/candidate:ro' -v /tmp/cad3d-candidate-heldout-20261016:/fixture -w /fixture --entrypoint python cad3d-engineering:1.4.0 fixture.py > /tmp/cad3d-candidate-heldout-20261016/run.log
docker run --rm --network none -v '/home/rrattes/Documentos/engineering 3d/3d-engineering-candidate-20261016:/candidate:ro' -v /tmp/cad3d-candidate-heldout-20261016:/fixture -w /fixture --entrypoint python cad3d-engineering:1.4.0 gate_and_freshness.py > /tmp/cad3d-candidate-heldout-20261016/gate_freshness.log
```

This run demonstrates concrete use of the candidate instructions on negative and corrected controls, bounded to the fixtures above. It does not establish actual fan retention strength, printer compatibility, slicing success, visual-review quality, a production assembly or physical validation.

# Revisão independente da candidata evolução 03

Data: 18/10/2026. Escopo: revisão dirigida do plano/proposta e diffs da candidata contra `baseline-skill`, especialmente evidência, manifesto, BREP, gate, resumo e compatibilidade. Nenhuma edição da candidata, skills ativas ou produtos. Esta revisão não é aprovação estética ou validação física.

## Resultado inicial

**Bloquear promoção até resolver I1–I3.** Nenhum achado classificado crítico. Três achados importantes reproduzidos e um menor. A documentação/pacote final ainda estava em elaboração e sua ausência não foi tratada como defeito.

### I1 — Importante: verificação viva perde a procedência do relatório do fornecedor

Arquivo: `scripts/engineering_evidence.py:93–98`.

`adapt_cad3d_report` confere schema, revisão, fontes e parâmetros do envelope. Entretanto, `validate_engineering_evidence`, usado pelo gate, lê somente o registro apontado em `artifact_ref`. Confere o registro e a cópia de fontes declarada no envelope da evidência, mas não a fonte efetivamente declarada no relatório do fornecedor. A adaptação prévia não é obrigatória nem repetida no gate.

Reprodução com `EvidenceTests.fixture`: manter política/evidência referentes a `part.step`; substituir o envelope de `report.json` por um relatório com `source_refs=[ref_de_wrong.step]`, mantendo o registro de medição; atualizar somente hash/pointer do `artifact_ref` para `/checks/0`. Resultado de `check()`: **PASS**. O relatório declara outra geometria, apesar da mensagem de critério atual. Isso viola PD3-01 e o foco em fonte/configuração divergente.

Correção sugerida: guardar referência ao envelope reconhecido e índice/pointer do check; validar novamente schema/revisão/source_refs/parameter_ref do fornecedor contra a política no gate. Alternativamente, definir e validar procedência equivalente explícita por registro. Testar fonte e parâmetros divergentes, formato desconhecido e envelope aninhado.

### I2 — Importante: manifesto publica referências visuais/de aceitação ausentes

Arquivo: `scripts/delivery_manifest.py:40–46`.

A inspeção considera `artifacts` e `engineering_ref`, mas ignora `visual_review_ref` e `acceptance_ref` quando fornecidos. Um manifesto pode apontar para revisões/decisões inexistentes ou antigas e ainda substituir `current.json` como consistente.

Reprodução em diretório temporário: um CAD presente com hash correto; `visual_review_ref={path:missing-review.json,sha256:64 zeros}` e `acceptance_ref={path:missing-acceptance.json,sha256:64 zeros}`. `inspect_delivery` e `publish_manifest` retornam **CONSISTENT**; `current.json` é criado. As duas referências inexistentes constam no manifesto publicado.

Correção sugerida: validar todas as referências opcionais declaradas, hashes, schema e vínculos de revisão/configuração cabíveis; ausência ou divergência bloqueia troca do ponteiro. A decisão humana continua um dado separado, sem aceitação automática. Acrescentar casos de ausência, mudança e revisão incompatível para ambas as referências.

### I3 — Importante: guarda BREP descarta topologia livre junto de sólidos

Arquivos: `scripts/compare_geometry.py:125–132` e leitura de regiões em `scripts/design_freedom_brep.py`.

`pieces()` só rejeita faces/arestas sem sólido quando `solids` está vazio; havendo ao menos um sólido válido, retorna apenas `shape.solids()`. Uma face livre em um Compound válido é descartada silenciosamente. A leitura de STEP também extrai sólidos sem conferir topologia livre coexistente. Isso contraria o requisito explícito de não descartar fragmentos e pode transformar resultado incompleto em métricas numéricas.

Reprodução no kernel existente: `Compound(children=[Box(2,2,2), (Pos(10,0,0)*Box(1,1,1)).faces()[0]])` tem `is_valid=True`, um sólido e sete faces. Injetado como retorno de `__sub__` em `region_metrics`, é aceito, retornando métricas e `boolean_operations=2`, sem NOT_EVALUATED/erro. Este é um controle negativo sintético de retorno booleano; não afirma que uma subtração ordinária produziu esse defeito.

Correção sugerida: verificar que toda topologia pertence aos sólidos aceitos, tanto na importação quanto em resultados intermediários; rejeitar faces/arestas/vértices livres e fragmentos inválidos misturados com sólidos válidos. Testar Compound misto e controle de múltiplos sólidos válidos.

### M1 — Menor: cobertura visual é sempre uma lista vazia

Arquivo: `scripts/design_summary.py`, campo `coverage.visually_reviewed_variants`.

A saída conserva separação de estados e não concede aceitação indevida, mas nunca calcula variantes realmente revisadas, mesmo havendo referência de revisão no manifesto. A tarefa 4 pediu contagens de variantes cobertas. Após validar referências conforme I2, consumir o escopo de revisão válido ou indicar explicitamente que essa capacidade permanece não implementada; não substituir desconhecido por zero revisões.

## Aspectos conferidos sem achado adicional

- Integração do contrato de evidência é opcional, mas sua presença exige autorização técnica e impede omissão pela candidata.
- Política BREP v2 é referenciada pelo contrato; limiares/configuração são conferidos e a comparação BREP é refeita. Sem fallback automático para AABB.
- Rotas v1 e assinatura antiga de `make_brief` preservadas; novas opções são aditivas.
- Manifesto restringe namespace de saída, compara hash anterior, serializa publicadores cooperantes e revalida fontes antes de substituir o ponteiro; limite de escritores externos é declarado.
- Markdown mantém fatos JSON incluindo desconhecidos e fontes, com escape; não atribui avaliação física/visual à aprovação geométrica.

## Execução independente

Imagem existente confirmada: `cad3d-engineering:1.8.0`, ID `sha256:81ff095d899a294b16b58435622b2a16555ba5c45ff4e1f1c7d3613f818cfa4a`. Sem instalação.

Comando válido: `docker run --rm --entrypoint python -v "$PWD:/workspace" -e PD_CANDIDATE=/workspace/docs/product-design/candidates/evolution-03/product-design cad3d-engineering:1.8.0 /workspace/docs/product-design/evaluations/evolution-03/checks/run_checks.py --group host`.

Host: **75 testes, OK, 1.440 s**. Log preservado em `review-host.log`. Tentativa inicial sem `--entrypoint python` foi rejeitada pelo CLI `cad3d` antes de executar testes; o comando acima corrigiu apenas a invocação. Reproduções I1/I2 usaram diretórios temporários no host e I3 o container existente. Os casos não estão cobertos pelo grupo host atual.

CAD: mesmo comando com `--group cad`: **26 testes, OK, 3.103 s**. Log em `review-cad.log`. Os controles existentes passam; o controle misto de I3 revela uma lacuna adicional.

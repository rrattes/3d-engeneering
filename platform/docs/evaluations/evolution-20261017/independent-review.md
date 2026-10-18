# Revisão independente da evolução CAD3D

Data: 17/10/2026. Revisor em contexto independente, sem alterar implementação/configuração. Baseline informado: `2d703fb1a812da2bc0a50abf92d1dac230b283d3`. Escopo: plano original e avaliação A01–A10; RunContext, SQLite e Qdrant explicitamente adiados. A ausência dessas arquiteturas não é achado.

## Parecer desta rodada

**Promoção ainda não aprovada.** Há falhas importantes de agregação de desconhecidos, avaliação de fabricação e consistência de orientação, além de lacunas nas evidências dos gates. Os testes existentes são úteis, mas não demonstram todos os requisitos que o ledger chama de completos. O implementador foi avisado dos achados e pode estar alterando os arquivos durante a integração. Este parecer descreve o snapshot observado; correções posteriores precisam de revisão e controles novos.

Foram lidos plano, avaliação, diffs contra baseline, módulos novos, integração CLI/render/empacotamento, testes e ledger. Os controles pequenos abaixo rodaram em container existente `cad3d-engineering:1.5.0`, ID curto `2d85bbc9cc0a`, rede desabilitada, raiz somente leitura e fixtures temporárias em `/tmp`. Não se executou campanha longa, nem se alteraram produtos, links ou imagens. Não houve verificação física.

Hashes SHA256 observados no controle inicial:

| Arquivo | SHA256 |
|---|---|
| cli/cad3d.py | 3860e172f8aa91f8757e251563fa7d56c1fc143e1ad5bd9e8aad910833ab15c2 |
| cli/artifact_publication.py | 6db16476d4f8d5ba44e044d020a6bff74c71f9bdd74a2cc8acb4046a25698021 |
| cli/service_states.py | f0ca1d7e3cad7f2bc3484fc69a529c6475ddfffe7d7aae4ee284ba468f9e9366 |
| cli/component_catalog.py | a20e3254d55f04073b6bc7b9705af96ffcae04c099bf581b90b54ab83cd36045 |

## Achados importantes

### R1 — Manutenção desconhecida não bloqueia publicação

Evidência estática: `cli/cad3d.py:202–217` agrega `sequence_status == FAIL`, mas deixa `NOT_EVALUATED` fora de `assembly_validity`; montagem nominal PASS pode coexistir com sequência desconhecida. `cli/artifact_publication.py:38–39` exige montagem PASS e consulta `unknown_collision_checks`/`tool_unknown_checks`, campos que esse CLI não emite. Não verifica o estado aninhado de sequência/ferramenta.

Controle isolado: manifestei validação global PASS, geometria/montagem PASS e `assembly.assembly_sequence.status = NOT_EVALUATED`, com etapa desconhecida. `publish_run(...)` publicou `probe`. Isso demonstra a lacuna na API de publicação. O conteúdo da fixture não é produto real; valida a disposição dos estados. Também inspecionei o caminho CLI que pode produzir essa combinação.

Correção necessária: definir aplicabilidade de sequência separadamente e recusar desconhecido de etapa requerida, incluindo ferramentas; não exigir trajetória onde ela não é aplicável. Adicionar controle que atravesse `release`, com nominal PASS e trajetória/ferramenta desconhecida, e confira que o apontador anterior permanece intacto.

### R2 — Avaliação de fabricação PASS para usinagem não avaliada

Evidência: `cli/cad3d.py:133–139,211–215` classifica campos não FDM como NOT_APPLICABLE, mas calcula `manufacturing_assessment` somente com `fdm_results`; lista vazia e perfil conhecido produzem PASS.

Controle via `validate` real, substituindo apenas `project_files` por uma fixture: Box(10,10,10), peça única `manufactured/machined/aluminum`, montagem nominal e perfil CAD `bambu-a1`. Resultado observado:

```json
{"status":"PASS","states":{"geometric_validity":"PASS","assembly_validity":"PASS","manufacturing_assessment":"PASS"},"geometric_thickness":{"status":"NOT_APPLICABLE","reason":"non_FDM_component"}}
```

Não existe avaliador de usinagem neste diff. Avaliação de fabricação geral precisa conservar esse desconhecido, ou o estado deve ser explicitamente limitado à avaliação FDM. Referências comerciais/hardware sem fabricação local podem ser não aplicáveis; peças fabricadas por processo sem avaliador não podem obter aprovação por conjunto vazio.

### R3 — Encaixe validado usa orientação diferente do STL entregue

Evidência: `cli/component_catalog.py:69–74` exporta conforme `print_rotation_deg`; `cli/cad3d.py:119–131` pesquisa rotações alternativas sem reconciliar com a orientação declarada/exportada.

Controle com BREP, exportação e validação reais: peça FDM Box(80,40,10), `print_rotation_deg=[0,0,0]`, perfil local `[50,100,100]`, margens zero. `part-index.json` registrou STL `[80,40,10]`, que excede X. `validate` retornou global PASS e `print_fit.status=PASS`, `selected_rotation_deg=[0,90,0]`, dimensões `[10,40,80]`.

Correção necessária: avaliar o encaixe da orientação realmente exportada ou exportar a orientação efetivamente selecionada mediante regra explícita. Sugestão de rotação alternativa pode existir separadamente, com a posição da peça no conjunto preservada. A compatibilidade física continuar desconhecida é correto, mas não corrige a inconsistência nominal.

### R4 — Pré-requisitos de manutenção não controlam elegibilidade das etapas

Evidência: `cli/service_states.py:8–20` verifica existência/ciclos do grafo. `evaluate_steps:66–73` percorre a lista original e avalia todos os estados isoladamente; não verifica resultado de pré-requisito nem a ordem. `removed_ids` pode remover o fixador mesmo que a operação anterior não tenha sido avaliada.

Controle BREP: `remove-screw` com direção zero resultou NOT_EVALUATED; `remove-lid`, dependente de `remove-screw`, declarou esse parafuso removido e resultou PASS. Saída:

```json
[{"id":"remove-screw","status":"NOT_EVALUATED"},{"id":"remove-lid","status":"PASS"}]
```

O desconhecido permanece no relatório agregado de sequência, o que limita o problema quando esse agregado é respeitado. Entretanto a própria etapa não constitui evidência executável da sequência declarada. Resolver ordem topológica e marcar etapas dependentes como bloqueadas/desconhecidas quando o pré-requisito não passou; esclarecer se `removed_ids` são premissas independentes ou efeitos comprovados da sequência.

### R5 — Publicação verifica integridade do inventário fornecido, não sua completude de engenharia

Evidência: `cli/artifact_publication.py:40–49` só exige lista não vazia, hashes e `validation.json`. O comentário sobre componentes obrigatórios não tem implementação. O mesmo controle R1 publicou um `part.step` de texto, sem catálogo, BOM ou evidência de reabertura. Uma entrega contendo só validação também satisfaz essa checagem estrutural.

Não é necessário converter a API em sandbox para modelos Python arbitrários. É necessário fixar os artefatos/atestados exigidos pelo contrato de release e conferir catálogo/quantidades/STEP/STL e reabertura correspondente. O caminho CLI atual chama exportador antes da publicação, o que reduz a exposição ordinária; a API pública ainda não sustenta a alegação de pacote completo validado.

## Evidências insuficientes para fechar gates

- **G3/PUB:** o teste usa STEP textual e chama `publish_run`, sem exercitar `release`. O caso de fabricação FAIL altera `validation.json` sem atualizar o hash do manifesto: uma implementação sem gate de fabricação ainda rejeitaria por hash divergente. Não demonstra isolamento da falha de fabricação. Não há caso de interrupção, falha real na última peça, espessura ou reabertura STEP. Concorrência e arquivo corrompido têm controles úteis, mas cobrem parte do gate.
- **G2/STEP de conjunto:** `component_catalog.py:79–82` confere validade, quantidade e soma de volumes; não confere poses/bounds dos sólidos posicionados. `test-component-catalog.py` verifica quantidade3, não as posições. O requisito do plano de preservar poses por reabertura continua sem evidência suficiente.
- **G6/VIS:** os testes rendem imagens, mas só asserem campos de manifesto/existência. É necessário registrar inspeção humana das imagens reais, inclusive 36 componentes e interfaces. Não se inferiu legibilidade de metadados do layout.
- **G9/SKILL/benchmark:** nesta inspeção `docs/evaluations/evolution-20261017/scenarios/` e `behavior/` não existem. Não há base para concluir melhoria de geração, teste reservado ou descoberta real de skill. Manter pendente, com campanha/aplicabilidade conforme autorização original; não inventar resultados de agente indisponível.
- **G10/KIT:** `test-portable-kit.py` confere arquivo, hashes, projeções e extração em pasta com espaços; não executa wrapper/doctor/exemplo a partir do kit extraído. Isso não atende sozinho ENG2-KIT-01. O INSTALL preserva honestamente NOT_EVALUATED de plataformas/agentes ausentes e diferencia fonte de imagem.
- **Runner:** `scripts/run-evolution-regressions.py` chama as mesmas 14 suítes para integration/full, não executa testes de template/assembly-demo nem V1.4; a exclusão V1.4 está declarada no resultado. Não registra SHA256 dos módulos importados por execução como solicitado pelo plano; registra caminho e imagem. O default ainda é imagem1.4.2, enquanto wrapper/compose agora usam1.5.0. Evidência final deve identificar explicitamente imagem e hashes, e anexar checks externos realmente executados.

## Outros pontos de contrato e manutenção

A publicação exige montagem PASS para todas as peças, enquanto um projeto simples sem `assembly.yaml` recebe montagem NOT_EVALUATED. Assim a modalidade release não contempla diretamente a peça simples sem montagem, apesar de o exportador construir seu conjunto. Definir NOT_APPLICABLE explícito ou gerar/verificar a instância única; não liberar montagem desconhecida apenas para contornar isso.

Os novos módulos concentram diversas decisões em linhas únicas e usam nomes abreviados. Isso dificulta inspecionar a precedência de estados e é especialmente relevante nas expressões de agregação onde surgiram R1/R2. Recomenda-se extrair funções pequenas de agregação com estados/aplicabilidade explícitos; isso não requer a arquitetura adiada.

`source_fingerprint` segue corretamente limitado às entradas locais do projeto e não promete reprodutibilidade externa. No entanto o manifesto de release ainda traz engine fixo, sem hashes dos módulos e perfis globais efetivamente utilizados; não deve ser descrito como registro completo do runtime. Preservar esse limite na documentação/evidência final.

## Pontos positivos constatados na implementação

O catálogo separa peça e instância, mantém todos os corpos na montagem e permite exportar STL somente FDM; os metadados desconhecidos permanecem no registro. A reabertura individual de STEP confere sólidos, volumes e bounds; STL explícito é verificado quanto a fechamento/conexão. O fluxo legado de exportação de referência multissólida foi preservado com distinção de peça FDM explícita. A publicação usa diretórios por execução, lock e troca atômica do apontador, com fsync. A calibração deixa de ler a variável não inicializada; perfil ausente aparece como orçamento conceitual. Os documentos mantêm separados protótipo, fatiamento e validação física.

Esses pontos não fecham os achados acima. A revisão seguinte deve identificar hashes novos, executar negativos discriminantes e conferir que o apontador permanece preservado nas falhas. A aprovação final permanece pendente nesta rodada.

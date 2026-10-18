# Product-design — evolução 03

Data: 18/10/2026. **Candidata implementada; promoção pendente.** Versão ativa continua evolução 02. A implementação não altera 3d-engineering, Docker nem produtos existentes.

## Ganhos implementados

- Evidência técnica vinculada ao contrato, fonte CAD, parâmetros, revisão, critério, unidade, cobertura e calibração. PASS calculado com limite diferente não qualifica. Datum/transformação explícitos; centroide não comprova orientação.
- Manifesto de entrega com hashes/dependências, estado separado de engenharia, histórico/tentativas, comparação do ponteiro anterior e publicação atômica do próprio manifesto. Referências visuais e de decisão também são verificadas.
- Regras opcionais de família e interação; preserva puxadores comuns, estilo único e estudo apenas de cor. Não obriga cinco estilos.
- Resumo Markdown com fatos do JSON, requisitos/features/fontes/limites e desconhecidos. Cobertura visual é declarada e conferida quando fornecida; ausência permanece desconhecida.
- Permissões BREP opcionais: retenção de material, vazio protegido e união de volumes editáveis. Mantém v1; rejeita fontes/poses antigas, limiares divergentes e fragmentos mistos.

## Evidência executada

Baseline: **123 testes**, OK, `baseline.log`.
Regressão final da candidata: **168 testes**, OK, **6,256 s**, sem skips, `regression-final-02.log`. Inclui os 123 anteriores e 45 adicionais. Runner confere módulos importados da candidata; grupos legacy/host/cad/integration disponíveis.

Revisão independente encontrou três problemas importantes, corrigidos com controles negativos e regressão: procedência do envelope do fornecedor; referências visuais/de decisão ignoradas; topologia livre misturada com sólidos. `REVIEW.md` preserva a revisão original. `REVIEW_RESOLUTION.md` registra correções; não houve segunda revisão independente após o limite de uso.

Piloto isolado real: porta-joias minimalista com duas gavetas (3 STEP) e quatro tampas do console BC250 (4 STEP). Comparação/importação CAD, duas gerações de imagem por produto, reaproveitamento do CAD ao mudar cor, invalidação de render e preservação do ponteiro ao simular interrupção. Resultado: `pilot/run02/RESULT.json`, **9,511 s** medidos nessa execução. Nenhum CAD foi regenerado no incremento de cor. Isso mede essas operações, não economia percentual de tokens.

As duas imagens finais foram abertas: peças e detalhes legíveis, mesma câmera/escala, cores simuladas distintas. No porta-joias, a pose aberta é apresentação, não prova de movimento. No console, a cobertura limita-se às quatro tampas, não ao console completo. Imagens em `pilot/run02/{jewelry,console}/reports/comparison/comparison-iso.png`.

A primeira tentativa do piloto foi preservada (`pilot.log`): a montagem completa do console ultrapassou ou não satisfez a guarda de grupo de sólidos. A segunda usou quatro peças externas independentes; o limite não foi enfraquecido.

## Avaliação comportamental interrompida

**20 de 36 respostas frescas preservadas**, modelo registrado gpt-6-astra/medium. Completos: cor, estilo único, família (6 cada). Espessura: 2 de 6. Orientação e atualização parcial: sem amostras. Os agentes foram interrompidos pelo limite de uso. Foram recuperadas respostas já concluídas dos registros locais, sem novos samplers.

Faltam 16 respostas e a avaliação cega final. Nenhuma superioridade comportamental geral está demonstrada. Protocolos, inputs, hashes e respostas em `behavior/`. Os textos congelados precedem as correções finais; ao retomar, distinguir essa rodada congelada de eventual nova rodada, sem misturar versões.

## Limites e decisão

- Adaptador reconhece o envelope explícito `cad3d-product-design-report-v1`. Relatórios CAD3D antigos sem procedência/método/cobertura permanecem NOT_EVALUATED; não houve migração dos produtos.
- BREP v2 exige correspondência explícita das mesmas peças, regiões/poses/folgas definidas pela engenharia. Não é solver de folga, resistência, ergonomia ou validação física.
- Manifesto não constitui transação sobre arquivos gerados por ferramentas externas. Hashes e declarações não autenticam execução nem aprovação humana.
- Não houve impressão física ou nova aprovação estética de produtos.
- **Não promover nesta entrega**: avaliação comportamental incompleta e aprovação posterior prevista no plano. Candidata e pacote disponíveis para continuidade.

## Economia aplicada

Leituras dirigidas, logs em disco, implementação principal sequencial, uma revisão independente, container existente, testes locais rápidos e piloto de duas amostras. A avaliação de 36 agentes frescos teve custo alto e foi interrompida; não será repetida automaticamente. Não foram medidos tokens totais confiáveis, portanto não há percentual de economia alegado.

# Relatório final — candidata 3d-engineering1.5.0

> Atualização posterior: versão1.5.0 ativada por solicitação explícita do usuário para avaliação com projeto real. Ver docs/evaluations/promotion-1.5.0/AVALIACAO_E_PROMOCAO.md na raiz da plataforma. O relatório abaixo conserva o estado anterior à promoção; G9 continua pendente.

## Estado da entrega

**Código e controles determinísticos implementados; candidata isolada para experimentação. Promoção global pendente de G9 e autorização específica.** Nenhuma melhora comportamental universal foi inferida dos testes do motor. Avaliação de arquitetura adiada: sem Qdrant, SQLite ou RunContext.

Fontes: `/home/rrattes/Documentos/engineering 3d/3d-engineering-evolution-20261017`. Branch: `evolution/20261017`.
Imagem verificada: `cad3d-engineering:1.5.0` — `sha256:29f29efe95400751376e77f749cf7fd4aa3c660d9fe6498aabacec9635c4110f`.
ZIP: `dist/evolution-1.5.0-final/CAD3D_Kit.zip`.
SHA256 do ZIP: `fba01d4ca6598d2c8bc041b23a0f49920bb5cf3575a89bcaf09a8c75b31270e5`.

## Verificações observadas

| Verificação | Resultado | Evidência |
|---|---|---|
| Motor com fontes congeladas | PASS, 17 entrypoints | source-final-evidence/results.json e logs individuais |
| Código empacotado, sem overlay | PASS, 17 entrypoints | packaged-final-evidence/results.json e logs individuais |
| Aceitação histórica V1.4 | PASS, 35 controles | packaged-v14-final-04.log |
| Template / assembly-demo na imagem final | PASS,24 +10 testes | template-assembly-final-04.log |
| Módulos fonte versus imagem | PASS, todos SHA256 iguais | image-source-match.json |
| Publicação e interrupção antes da troca do apontador | PASS,8 testes | publication-interruption.log |
| Release real / parede fina / serviço desconhecido / STEP final corrompido | PASS,3 testes | packaged-final-evidence/release-integration.log |
| Skill: frontmatter e convenções básicas | PASS, quick_validate oficial dentro do Docker | skill-static-container.log |
| Skill: links e substituições exclusivas de host | PASS, inspeção estática local | skill-links-compat.json |
| ZIP extraído em caminho novo com espaços | doctor/init/build/validate executados; STEP/STL reabertos e hashes iguais | kit-*-final.log, kit-runtime-reopen.json |
| Preservação de produtos, instalação e imagem anteriores | PASS, nenhum arquivo original alterado | preservation-final.json |

Entrypoints incluem doctor; suas contagens não devem ser somadas como se fossem casos independentes de teste. As duas modalidades executam a mesma regressão para proteger fonte e empacotamento. Logs anteriores com FAIL foram conservados como histórico de diagnóstico, não são o resultado final.

## Correções da revisão independente

- R1: sequência requerida desconhecida impede aprovação de montagem/publicação; controle passa pelo release real.
- R2: usinagem sem avaliador permanece NOT_EVALUATED.
- R3: encaixe avalia orientação explícita do STL; negativo80×40×10 em volume50×100×100 rejeita a orientação entregue.
- R4: pré-requisito não aprovado ou fora de ordem bloqueia dependente; remoções são efeitos comprovados de operações anteriores.
- R5: publicação exige catálogo, BOM, relatórios e reabertura real dos artefatos, não apenas inventário com hashes. Falhas e interrupção preservam o apontador anterior.
- Reabertura do conjunto compara quantidade, volumes e limites dos sólidos posicionados, além da validade.
- A inspeção visual encontrou corte lateral real; teste projetou x=-22,48px antes da correção. Câmera agora considera o viewport real, e o negativo passou depois da correção.

O parecer independente original está em independent-review.md. O agente atingiu limite de uso depois de registrá-lo. Este relatório documenta correções/testes do implementador e **não declara segunda aprovação independente**.

## Inspeção visual efetiva

Foram abertas as imagens CAD reais em visual-inspection/. Após a correção, os36 componentes permanecem no enquadramento e os36 nomes aparecem em área separada. A galeria mostra a peça fabricada individualmente, e apresentação conserva as cores explícitas da referência e da peça. Isso não comprova correspondência entre36 cores repetidas e todos os IDs. Os rótulos Z em uma matriz muito plana ficam densos; o controle de enquadramento não é aprovação universal da legibilidade das cotas. A figura de apresentação usa blocos sintéticos, sem pretender demonstrar qualidade estética de um novo produto.

## Gates e pendências

- G0–G7: capacidades técnicas e regressões executadas, com os limites nominais/amostrados registrados. Rastreabilidade comercial não certifica dimensão física.
- G8: instruções e referências consolidadas; lint básico e links conferidos. Descoberta e comportamento em sessões novas de agentes permanecem NOT_EVALUATED.
- G9: protocolo/cinco prompts preparados em scenarios/. Piloto proposto de18execuções **não executado**; não há resultado de Codex ou Claude atribuído indevidamente. O plano expressamente não dispara essa campanha. Promoção permanece pendente.
- G10: ZIP íntegro, runtime local executado em pasta com espaços e regressão da imagem concluída. Construção Docker completa a partir dos downloads, transferência de imagem e plataformas diferentes de Linuxx86_64 permanecem NOT_EVALUATED. Uso público exige definição de licença do código próprio pelo proprietário; o pacote preserva avisos existentes.
- Sem ensaio de impressão, carga, retenção, torque, temperatura ou compatibilidade física de impressora. Nenhum arquivo foi enviado à impressora.

## Decisões e custos

- Ruling: Etapa headings are Portuguese and not supported by skill task helper parser; track checkpoints/evidence here and commits rather than rewrite the approved plan for helper compatibility.
- Ruling: legacy export preserves STL coordinates; explicit catalog uses declared print rotation and origin normalization. Legacy classifications warned, not treated as physical evidence.
- Ruling: packaged runner copies tested CLI from image into a temporary suite root so existing tests cannot silently import worktree modules. Source/packaged evidence recorded separately. Missing future suite is FAIL until implemented.
- Ruling: no RunContext redesign. Existing commands still load models independently; release confines outputs using internal temporary output selection, input hash check and staging. This preserves the user's architecture deferral.
- Ruling: preserve direct legacy export of multi-solid references with connectedness explicitly reported; explicit FDM exports remain one-solid/connected. CLI manufacturing validation rejects multi-solid FDM; publication cannot approve them.
- G9: scenario prompts/rubric prepared with status NOT_EXECUTED. Ruling: do not launch a model campaign implicitly — approved plan expressly calls18runs proposed and says it does not trigger campaign; review agent also exhausted quota — cost: no measured behavioral improvement, G9/promotion remain pending.
- Ruling: retain candidate worktree and active global links — explicit promotion authorization and remaining evaluation gates are separate — cost: global cad3d still uses1.4.2 until deliberate activation.

As primeiras decisões de compatibilidade custam manter caminhos legados e pressupostos explícitos; nenhuma autoriza aprovação física. Usar o motor da imagem evita confundir fontes com binário empacotado. A ausência da campanha e a preservação da instalação ativa custam manter a promoção pendente.

## Observações menores adiadas

- Trechos compactos nos novos módulos merecem refatoração de legibilidade futura.
- Densidade dos rótulos Z em matrizes planas merece refinamento visual; enquadramento e separação da legenda estão protegidos, legibilidade completa não foi declarada.

## Próximo uso e retomada

Consulte ../../RELEASE_1.5.0_CANDIDATE.md e ../../INSTALL.md. Use wrapper da candidata por caminho absoluto ou o wrapper do kit, confirme doctor1.5.0 e mantenha produtos em diretórios novos. O comando global permanece1.4.2. Para retomar a avaliação, leia scenarios/PROTOCOL.md e EXECUTION_LEDGER.md; preserve baseline e use contextos novos. Nenhum rollback global é necessário porque não houve ativação.

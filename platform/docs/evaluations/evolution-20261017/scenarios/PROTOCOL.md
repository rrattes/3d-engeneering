# Protocolo fixado para avaliação comportamental

Status: PREPARED / NOT_EXECUTED. Nenhuma melhora percentual ou sucesso de agente inferido dos testes do motor.

O plano original descreve piloto proposto e informa expressamente que ele não dispara a campanha. A campanha de geração em contextos novos permanece separada; nesta sessão o revisor também atingiu limite de uso. Não substituir execução independente por respostas do próprio implementador.

## Comparação

Baseline: commit 2d703fb1a812da2bc0a50abf92d1dac230b283d3, imagem1.4.2 congelada.
Candidata: commit/hash e imagem1.5.0 registrados na entrega. Congelar ambos antes da campanha.
Três classes (simple-part, commercial-assembly, thermal-enclosure), três repetições por variante:18execuções. Alternar baseline/candidata; cada execução inicia sem histórico de produto. Mesmo modelo, limite de ferramentas e orçamento de execução por variante; registrar identidade/modelo efetivos e indisponibilidade. Codex primeiro; Claude somente se disponível e autorizado. Não revelar o rubric ao executor. Não usar os dois casos reservados para ajustar a skill; avaliar depois da campanha principal, sem lhes atribuir resultado antecipado.

## Critérios de avaliação (por execução)

- Requisitos: dimensões/quantidades e unidades verificadas em geometria real.
- Artefatos: fonte, parâmetros, STEP reaberto, STL válido quando FDM, montagem e imagem CAD real.
- Fabricação: orientação entregue compatível com avaliação; não atribuir suporte de impressora ausente.
- Montagem: retenção, colisão, acesso e estados de manutenção comprovados ou desconhecidos explícitos.
- Propagação: alteração de parâmetro refletida em fixações e envelopes, sem coordenadas copiadas.
- Publicação: arquivos íntegros da mesma execução e falhas impedem promoção.
- Físico: desconhecido não se converte em aprovação térmica, resistência ou calibração.

Para cada critério: PASS, FAIL ou NOT_EVALUATED com arquivo/comando/hash. Falha importante omitida reprova a execução; estética/tempo não compensam. Registrar duração real e custo/tokens somente quando disponíveis (null caso contrário). Imagens com câmeras fixas; avaliador sem rótulo da variante quando possível.18execuções não fundamentam ganho universal. Gates comportamentais e descoberta real das skills permanecem abertos até esta evidência existir.

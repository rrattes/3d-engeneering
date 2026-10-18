# Comparação1.4.2 →1.5.0 e promoção

## Ganho comprovado

Mesmo probe executado nas duas imagens, preservado em compare-runtime.py e comparison-*.json:

| Controle |1.4.2 |1.5.0 |
|---|---|---|
| Calibração válida sem mínimo local de parede | UnboundLocalError | retorna calibração PASS |
| Impressora inexistente | sem evidência de perfil; fabricação WARNING | perfil/fabricação NOT_EVALUATED |
| STL de referência comercial | criado indevidamente como fabricável | omitido |
| STEP do conjunto/BOM no probe | ausentes | gerados |
| Publicação verificada por execução | ausente | disponível; negativos e interrupção cobertos |

As suítes também cobrem manutenção, orientação do STL, repetição de instâncias e câmera. Não se aplicou API exclusiva da candidata à produção para inventar falhas. Propagação foi demonstrada em uma fixture codificada, não garante que todo novo código gerado pelo agente seja paramétrico corretamente. O kernel build123d/OCP não mudou. Não existe demonstração de melhora estética ou de desempenho de geração universal.

## Ativação

Solicitação atual do usuário autoriza promoção local e projeto real. Após nova regressão17/17 PASS empacotada, hashes e imagem conferidos, links globais de CLI/skill foram trocados para3d-engineering-evolution-20261017. Doctor antes1.4.2/depois1.5.0 foi executado. G9 continua pendente; a autorização de uso real não é resultado retroativo da campanha comparativa.

Destinos/commit/imagem: activation-snapshot.json. Logs novos: packaged-regression/ e doctor-before/after.log. Orca, imagens antigas e produtos originais preservados. Scripts que fixam wrapper/imagem antigos continuam com suas referências explícitas; nenhuma migração de produto ocorreu.

Rollback, se solicitado: python3 neste rollback.py. Confere os links e restaura somente os dois destinos anteriores. Não apaga imagem/pasta; não foi executado sobre a instalação ativa para apenas testar sua implementação.

## Uso real

Novo projeto Cesta_Anemonas_Rev_A, briefing próprio:150×100×100mm, vidro4/5mm. Corpo/suporte fabricados separados de vidro, apoios e ferragens. Espécie, material, borda do aquário e carga/pressão no vidro ainda não qualificados. Esse uso permite julgar qualidade da solução, sem sustentar ganho percentual universal.

## Resultado do primeiro protótipo

Cesta_Anemonas_Rev_A publicada na execução7bd2700bbec54b188ca6f2798b7a59ad. Geometria/montagem nominais PASS;4/5mm com55pares cada,2STLs e conjunto STEP reaberto com11sólidos. Fabricação/físico NOT_EVALUATED. O primeiro arranjo tinha reserva de montagem0,3mm, corrigida para2,3mm com vidro5mm após teste negativo. Relatório no produto: reports/AVALIACAO_REAL.md. A descoberta/correção é evidência deste trabalho, não uma campanha A/B de geração.

## Aprovação após a cesta Rev C

Após as revisões do projeto real, o usuário declarou: “A nova versão da skill foi aprovada”. A versão 1.5.0 permanece ativa; esse aceite não altera código, dependências ou imagem Docker.

A Rev B substituiu os fixadores comprados por parafusos e porcas PETG. Na Rev C, por solicitação do usuário, as porcas foram eliminadas: duas roscas P8×3 e uma P10×3 ficam diretamente no suporte PETG. São seis STLs distintos para sete peças impressas; cesta de 150 × 100 × 100 mm e vidro nominal de 4/5 mm. PETG e BBT Rainbow foram definidos pelo usuário nas etapas posteriores ao primeiro protótipo; quantidade e diâmetro dos animais foram excluídos do dimensionamento por sua instrução.

Execução Rev C: `b2424b46c6cf442eb3bed87637e7a560`. Por variante: 28 pares estáticos sem interferência positiva, dez poses helicoidais por parafuso e remoção amostrada da cesta PASS. O verificador é específico do projeto, não foi integrado à skill/plataforma, e não comprova movimento contínuo ou resistência. Espessura do suporte NOT_EVALUATED por seleção de faces não resolvida; cesta WARNING por cobertura incompleta. Sem fatiamento, impressão, ensaio de aperto/carga/fluência, qualificação do vidro ou validação biológica; sem nova revisão independente da Rev C.

Fontes: [relatório Rev C](../../../../Cesta_Anemonas_Rev_C/reports/VALIDACAO_REV_C.md) e [execução selecionada](../../../../Cesta_Anemonas_Rev_C/build/delivery/current.json). O [fluxo atual de skills](../../../../FLUXO_PROJETOS_3D.md) preserva brainstorming → writing-plans → 3d-engineering, com systematic-debugging quando necessário e verification-before-completion antes da entrega. Skills auxiliares são selecionadas pela necessidade.

A aprovação é do fluxo/skill no uso observado. A campanha G9 e a comparação A/B da geração do mesmo produto continuam sem execução; não se infere melhora universal de estética, velocidade ou custo. Avaliação de Qdrant e outras alterações de arquitetura permanece adiada.

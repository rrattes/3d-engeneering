# Economia de contexto e tempo

## Regra principal

Usar a menor leitura e execução que respondam à tarefa com evidência suficiente.
Requisitos, gates e pendências permanecem explícitos. Não existe percentual medido
de economia de tokens ou tempo neste registro.

## 1. Catálogo de entrega automatizado

O script [delivery-catalog.py](3d-engineering-evolution-20261017/scripts/delivery-catalog.py)
usa apenas a biblioteca padrão do Python no host. Execute na raiz deste workspace:

```sh
python3 3d-engineering-evolution-20261017/scripts/delivery-catalog.py \
  --project Cesta_Anemonas_Rev_C --update-readme
```

Para outro produto, substituir o argumento de `--project`. Caminhos com espaços
devem estar entre aspas. Sem `--update-readme`, somente os dois catálogos são gerados.

### Entradas e fonte de verdade

| Informação | Fonte |
|---|---|
| Execução e diretório selecionados | `build/delivery/current.json`, schema `cad3d-delivery-v1` |
| Integridade dos artefatos | `manifest.json` da execução, com `artifacts[].path`, `bytes` e `sha256` |
| Quantidade, material e processo | `BOM.csv` da execução: `part,quantity,kind,process,material` |
| Nome legível opcional | `.cad3d/delivery-catalog.json`, objeto `labels` indexado pelo identificador da peça |
| STL e imagem individual | `<part>.stl` e `parts/<part>.png` registrados no manifesto |
| Vistas opcionais | `A_assembly_iso.png` e `F_exploded.png` registrados no manifesto |

Peças com `kind=manufactured` e `process=fdm` entram na tabela de impressão.
Os demais itens ficam em tabela separada, inclusive referências comerciais e peças
fabricadas por outro processo. Rótulos não definem quantidades nem substituem dados
de engenharia. O comando suporta essa convenção de entrega, não qualquer BOM CAD.

### Saídas

- `docs/CATALOGO_ENTREGA.md`: peças, links de STL/imagem, quantidades, materiais e vistas.
- `docs/CATALOGO_ENTREGA.json`: dados estruturados, execução, hashes consultados e imagens ausentes.
- Bloco entre `<!-- cad3d:delivery-catalog:start -->` e `<!-- cad3d:delivery-catalog:end -->` no README, quando solicitado.

O README aponta para o catálogo único. O índice do workspace aponta para o catálogo
do produto, evitando repetir listas de arquivos em vários documentos.

### Comportamento e limites

O comando confere o SHA256 do manifesto contra o ponteiro e tamanho/SHA256 de cada
artefato utilizado. Divergência, quantidade inválida, identificador duplicado ou STL
FDM ausente bloqueiam a geração. Imagem ausente é registrada explicitamente, sem
inventar um render ou afirmar que houve revisão visual. Caminhos devem ficar no
projeto e os artefatos na entrega selecionada.

As saídas são determinísticas; conteúdo igual não é regravado. Não há cache opaco,
instalação de dependências ou varredura de todos os projetos. O comando não modifica
o pacote imutável nem verifica todos os artefatos do manifesto: confere somente os
que consulta. Os arquivos são substituídos individualmente; em caso de falha de
escrita, repetir o comando e conferir as saídas.

Integridade de arquivo não comprova validade CAD, inspeção visual, fatiamento ou
aprovação física. A entrega selecionada pode ser anterior ao código atual. O comando
não decide se uma alteração de fontes permite reutilizar geometria: isso exige
análise de impacto e procedência da execução.

O script é uma automação documental adicional no checkout local. A imagem CAD
1.8.0 e o ZIP anteriormente aprovado não foram reconstruídos ou reempacotados;
o ZIP antigo não contém esta adição. Para compartilhar a automação agora, incluir
o script e este guia. Um futuro kit deve ser gerado em diretório novo, com seu
próprio inventário e hash, pelo empacotador existente.

## 2. Escolher o tamanho da execução

| Tarefa | Leitura mínima útil | Execução proporcional |
|---|---|---|
| Listar arquivos, imagens ou quantidades | Ponteiro, manifesto, BOM e catálogo | Executar o gerador quando necessário; consultar arquivos existentes |
| Editar documentação | Trechos e destinos dos links afetados | Conferir documentos e referências alterados |
| Alterar uma peça/interface | Requisitos, parâmetros, contrato e dependências daquela peça | Regenerar e verificar interfaces afetadas no escopo autorizado; ampliar quando atingir o conjunto |
| Alterar código compartilhado, schema ou engine | Plano de impacto e consumidores | Planejar regressão ampla e revisão; executar testes quando solicitados/autorizados |
| Criar produto novo | Briefing atual e núcleo da skill | Seguir os gates de requisitos, arquitetura, CAD e fabricação aplicáveis |

Uma alteração de material, bico, orientação ou processo pode invalidar calibração.
Mudança de retenção, carga ou tolerâncias pode afetar interfaces e manutenção.
Nesses casos, ampliar o escopo mesmo que apenas um arquivo tenha mudado. Resultado
antigo conserva data/escopo e não é apresentado como verificação da alteração atual.

## 3. Caminhos para reduzir leituras

1. Ler `AGENTS.md` e o briefing atual. Localizar arquivos com `rg --files` e termos com `rg -n`.
2. Consultar o [índice do workspace](readme.md) para saber onde estão fluxo, plataforma e produtos.
3. Para consultar entregas, abrir `current.json` e o catálogo do produto. Evitar ler scripts CAD inteiros para descobrir o nome de um STL.
4. Para engenharia, ler o núcleo da [skill](3d-engineering-evolution-20261017/skills/3d-engineering/SKILL.md) e somente as referências pertinentes.
5. Para retomar trabalho, registrar no documento de execução existente do projeto: objetivo, decisões, arquivos alterados, última execução, verificações realizadas, pendências e próximo passo. Usar links para detalhes.
6. Abrir logs detalhados quando houver dúvida ou falha; na conversa, apresentar resultado, limitação e caminho da evidência.

Não criar um resumo paralelo de requisitos que concorra com o briefing. Resumos
devem apontar para as fontes e ser atualizados quando elas mudarem.

## 4. Caminhos para reduzir tempo de execução

- Reutilizar os renders/STLs da mesma entrega para consultas documentais.
- Usar conferência de procedência para avaliar reaproveitamento; nome ou data do arquivo isolados são insuficientes.
- Ler dados independentes em lote e manter alterações dependentes em sequência.
- Usar agentes quando autorizados e houver frentes independentes suficientes para compensar o custo de contexto; dar caminhos e critérios concretos.
- Manter resultados detalhados em disco e respostas curtas com links.
- Registrar causa de falha e correção, evitando repetir uma tentativa sem mudança fundamentada.

## 5. Como medir o ganho

Comparar tarefas de escopo equivalente, registrando duração, leituras/comandos,
retrabalho, falhas e tokens quando a ferramenta fornecer essa métrica. Comparar
também a cobertura das verificações. Menor consumo com requisitos omitidos ou
pendências escondidas não representa ganho de qualidade.

Aplicação inicial: [catálogo gerado da cesta Rev C](Cesta_Anemonas_Rev_C/docs/CATALOGO_ENTREGA.md).
O comando normal conferiu 6 STLs, 6 imagens individuais, BOM e 2 vistas de conjunto;
registrou 7 unidades a imprimir. Não foram executados testes, CAD, slicing ou
ensaio físico nesta incorporação documental.


## Saída gerada fora do inventário de fontes CAD

O gerador aceita `--output-dir reports`. Usar esta opção em projetos CAD3D para
manter o JSON gerado fora do inventário de fontes/configuração, que exclui
`reports/`. O padrão `docs` continua aceito para compatibilidade. Atualizar um JSON
gerado dentro de `docs/` pode alterar o fingerprint de fontes; isso não comprova
que a geometria mudou, mas pode exigir nova análise de procedência.

Aplicação no console: `python3 3d-engineering-evolution-20261017/scripts/delivery-catalog.py --project BC250_Console_Rev_B --output-dir reports --update-readme`.
A pasta escolhida deve permanecer dentro do projeto e fora de `build/delivery`.

# Fluxo de desenvolvimento de produtos 3D

## Versão ativa —17/10/2026

Versão local ativa **1.8.0, aprovada e promovida pelo usuário em 17/10/2026**, com as sete capacidades gerais restantes incorporadas por solicitação do usuário, preservando os fundamentos de confiabilidade da1.7.0. A versão **1.5.0 foi aprovada após a cesta Rev C** e permanece como referência anterior. CLI e skill globais apontam para `3d-engineering-evolution-20261017/`; imagem CAD `cad3d-engineering:1.8.0`. Orca permanece `cad3d-orca:2.4.2-cad3d.1.4.2`. Fontes/imagens anteriores preservadas; os registros da Photon V abaixo são históricos.

Melhorias comprovadas: calibração, perfil ausente explícito, catálogo de peças/instâncias, fabricação seletiva, STEP/BOM, manutenção com pré-requisitos e publicação verificada. Campanha G9 pendente; promoção não comprova melhora estética universal nem desempenho físico.

[Comparação, ativação e rollback](3d-engineering-evolution-20261017/docs/evaluations/promotion-1.5.0/AVALIACAO_E_PROMOCAO.md).

[Aprovação e promoção da 1.8.0](3d-engineering-evolution-20261017/docs/evaluations/capabilities-1.8.0/APROVACAO_E_PROMOCAO.md) · [Índice do workspace](readme.md).

### Fluxo atual de skills

A sequência principal foi mantida. A `3d-engineering` acompanha as decisões técnicas desde o briefing; a ordem abaixo descreve o foco de cada etapa, sem exigir carregar todas as skills para uma alteração simples.

| Ordem | Skill | Uso |
|---|---|---|
| 1 | `brainstorming` | Entender requisitos, restrições e decisões ainda abertas; aproveitar o briefing e as autorizações existentes. |
| 2 | `writing-plans` | Organizar implementação e verificações na proporção da tarefa. |
| Antes do CAD e na revisão visual, quando pertinente | `product-design` | Direção formal, estilos opcionais e revisão estética baseada em imagens; independente das validações técnicas. |
| 3 | `3d-engineering` 1.8.0 | Arquitetura, modelagem paramétrica, montagem, fabricação e arquivos. |
| Conforme necessário | `systematic-debugging` | Investigar causas de falhas e repetir as verificações afetadas. |
| Antes da entrega | `verification-before-completion` | Conferir evidências atuais antes de afirmar conclusão ou sucesso. |

Skills auxiliares continuam selecionadas conforme a necessidade. A tabela da Photon V na seção 2 registra aquela execução; não é uma lista obrigatória para todos os produtos. Agentes são usados quando autorizados e úteis, com o escopo da revisão registrado.

As melhorias da 1.5.0 concentram-se nos controles de engenharia: catálogo único de peças/instâncias, separação dos arquivos fabricáveis e referências, exportação STEP/BOM, pré-requisitos de manutenção, estados de validação explícitos e entrega vinculada a uma execução verificada. A aprovação do usuário não equivale a uma nova versão de código, imagem Docker ou comprovação de desempenho físico.

### Referência real aprovada: cesta Rev C

- Cesta de 150 × 100 × 100 mm para vidro nominal de 4/5 mm, em PETG.
- Três parafusos PETG: dois com diâmetro nominal de 8 mm e um de 10 mm, passo de 3 mm; roscas próprias P8×3/P10×3.
- As três roscas fêmeas ficam diretamente no suporte. Seis STLs distintos para sete peças impressas; sem porcas separadas ou fixadores comprados.
- Execução selecionada: `b2424b46c6cf442eb3bed87637e7a560`. Interferências nominais e retirada helicoidal amostrada passaram nas duas variantes de vidro.
- Na execução original da Rev C, o verificador helicoidal era **específico do projeto**, em `Cesta_Anemonas_Rev_C/scripts/validate_printed_fasteners.py`. A capacidade foi posteriormente generalizada na plataforma **1.6.0**, com contrato próprio; a entrega original da cesta conserva seu verificador e suas evidências. Verificação linear não comprova retirada de roscas.
- Espessura automática do suporte: **NOT_EVALUATED**, por seleção de faces não resolvida; cesta: **WARNING**, por cobertura incompleta. Fabricação, fatiamento e desempenho físico permanecem sem aprovação. Não houve nova revisão independente da Rev C.

[Projeto e arquivos](Cesta_Anemonas_Rev_C/ABRIR_PROJETO.html) · [Evidências e limitações](Cesta_Anemonas_Rev_C/reports/VALIDACAO_REV_C.md).

A cesta é referência do método e da aprovação da skill. Seus materiais, dimensões, fixadores e validadores não são requisitos automáticos de outros produtos. Não houve comparação A/B da geração da mesma cesta nas duas versões; ganhos universais de estética, tempo ou custo não foram demonstrados.

### Incorporação de movimento helicoidal — 1.6.0

A sequência de skills permanece a mesma. A plataforma agora aceita `motion.type: helical` em operações com `moving_ids` no contrato de montagem. Configurar eixo mundial, origem, passo, número de entradas, sentido e deslocamento assinado. O avanço por volta é passo × número de entradas.

O avaliador considera contatos por instância original, obstáculos mantidos e pré-requisitos. Uma trajetória amostrada PASS não basta para excluir um parafuso da etapa seguinte: exige também prova conservadora de separação das caixas envolventes na posição final. Movimentos lineares sem `motion` mantêm o comportamento anterior. Tipos desconhecidos são rejeitados.

A checagem helicoidal de peças importadas decompõe o BREP em sólidos com localização aplicada antes das operações booleanas; isso protege contra o falso resultado vazio observado em um Compound deslocado. Na 1.6.0 esse controle era exclusivo do movimento helicoidal; a 1.7.0 passou a compartilhar a proteção com os verificadores estáticos, lineares e de ferramentas.

[Contrato na skill](3d-engineering-evolution-20261017/skills/3d-engineering/references/helical_motion.md) · [Implementação, evidências e limites](3d-engineering-evolution-20261017/docs/evaluations/helical-1.6.0/INCORPORACAO.md).

Amostragem inclui extremos e espaçamento angular de até 90°, com orçamento limitado. Não comprova ausência de colisão entre amostras, ajuste impresso, força, torque ou resistência. A limitação de espessura do suporte Rev C permanece independente. Imagem 1.5.0 e entregas dos produtos preservadas; dependências e Orca mantidos.

### Confiabilidade incorporada — 1.7.0

- Interferências: verificadores estáticos/lineares/ferramentas e helicoidais compartilham a análise de sólidos com localização aplicada. Um contato permitido não dispensa folga mínima positiva.
- Referências: `point_mm` seleciona pela distância à face finita recortada, com normal/raio/área opcionais e diagnóstico; `center_mm` continua disponível sem relaxamento silencioso. Candidatas igualmente próximas permanecem ambíguas.
- Espessura: falhas parciais de seleção impedem PASS do escopo completo. O STEP real do suporte da cesta teve duas faces resolvidas e espessura amostrada PASS no novo escopo; a entrega original não foi regenerada.
- Tolerâncias: `tolerance_dimensions` e `tolerance_stacks` calculam cadeias lineares assinadas de pior caso. Limites assumidos geram WARNING; incerteza ou procedência ausentes ficam NOT_EVALUATED; ambos bloqueiam publicação como montagem verificada.

[Contratos e limites](3d-engineering-evolution-20261017/skills/3d-engineering/references/reliability.md) · [Evidências da incorporação](3d-engineering-evolution-20261017/docs/evaluations/reliability-1.7.0/INCORPORACAO.md).

Uso de tokens: leituras dirigidas, logs detalhados em disco, regressões existentes reutilizadas, testes locais curtos antes das baterias completas e revisão independente limitada aos módulos alterados. Não se atribui percentual de economia sem medição. Sem novas dependências, banco de dados ou mudanças no Orca.

### Capacidades gerais incorporadas —1.8.0

Biblioteca inicial de roscas reais, dobradiças e trilhos; movimentos de rotação e trajetórias compostas; campanhas de variantes com build/validação nativos isolados; calibração por medições com identidade/validade/evidência; envelopes de mãos/ferramentas/cabos; desenhos SVG/PDF com vistas, cortes e cotas de faces; e cálculo preliminar de viga retangular engastada.

Calibração aplicada ao projeto é confrontada com impressora/bico/orientação atuais, perfil de impressora/material/lote e SHA256 do arquivo de processo selecionado. Identidade antiga divergente, análise obrigatória desconhecida ou cota solicitada não resolvida impedem publicação como verificada. Exemplos são fixtures sintéticas, não dados medidos de nossas peças.

Regressão completa27/27 fonte +27/27 empacotada; aceitação legada35/35. Biblioteca e desenhos geram arquivos reais verificados. A sequência principal de skills permanece; duas frentes independentes usaram agentes com contexto mínimo, com integração e revisão de gates. Imagem1.7.0 e entregas anteriores preservadas, sem dependências, banco ou Orca novos.

[Contratos e limites](3d-engineering-evolution-20261017/skills/3d-engineering/references/general_capabilities.md) · [Evidências](3d-engineering-evolution-20261017/docs/evaluations/capabilities-1.8.0/INCORPORACAO.md). Esses módulos não constituem planejador mecânico geral, calibração física automática, desenhos ISO completos ou FEA/certificação estrutural.

## Atualização da ferramenta — 16/10/2026

A skill e o CLI locais foram atualizados para a revisão 1.4.2. Os links globais apontam para `3d-engineering-candidate-20261016/`; esse é o nome histórico da candidata, agora ativa. Código anterior e imagens base foram preservados em `3d-engineering/`.

Mudanças: verificação de fontes/configurações locais, exportações regeneradas, gate inicial aplicado antes de carregar modelos, preflight de presets, instruções de fixação/tolerâncias/manutenção e correção do destaque visual de interfaces.

[Entrega, skills usadas, evidências e reversão](3d-engineering-candidate-20261016/docs/IMPROVEMENT_1_4_2.md). O restante deste documento registra a execução original da Photon V; seus IDs e resultados são históricos. O produto Photon V não foi alterado nesta atualização.

Registro do método aplicado à Aqualith Photon V – TC421, Revisão B, em 16/10/2026.
Serve para iniciar outros produtos com Python, CAD paramétrico e fabricação por peças.

## 1. O que preservar deste trabalho

O resultado veio da combinação de briefing detalhado, decisões de montagem, componentes independentes, geração efetiva e correções baseadas na geometria. A quantidade de skills instaladas não foi a medida de qualidade.

O planejamento deve conduzir a um produto reconhecível: função, proporções, detalhes, manutenção e fabricação. Um sólido válido ou uma caixa que acomoda componentes não basta para atender a um pedido de projeto de produto.

Para um produto novo, criar uma pasta própria. Reaproveitar ferramentas e métodos; geometria, dimensões e decisões de produtos anteriores somente quando isso for solicitado. O briefing atual é a fonte de verdade.

## 2. Skills e como foram usadas

Os caminhos abaixo são os instalados neste ambiente. Confirmar sua existência e ler as instruções antes de aplicar; uma skill instalada não equivale a uma execução comprovada.

| Skill | Papel no fluxo | Aplicação na Photon V |
|---|---|---|
| `3d-engineering` | Requisitos, arquitetura, CAD, interfaces, fabricação e limites das validações | Principal, da arquitetura aos arquivos |
| `brainstorming` | Entender intenção, aparência, restrições e alternativas | O briefing detalhado e a solicitação de executar permitiram seguir com hipóteses explícitas |
| `writing-plans` | Dividir o trabalho em entregas e verificações | Plano salvo antes da implementação |
| `executing-plans` | Executar nesta sessão e manter decisões registradas | Execução direta, com registro e continuidade |
| `systematic-debugging` | Investigar causa de falhas antes de corrigir | Contratos YAML, interferências, espessuras e exportação |
| `test-driven-development` | Criar regressões para problemas concretos | Aplicação pontual; por exemplo, teste da cabeça M3 bloqueada pelo dissipador falhou e depois passou |
| `unified-memory` | Preservar contexto e apontar para documentos canônicos | Aplicada ao registro deste fluxo; runtime ECC não encontrado, portanto sem gravação no Vault |

Localizações:

- Engenharia: `/home/rrattes/.agents/skills/3d-engineering/SKILL.md`.
- Demais skills da tabela: `/home/rrattes/.codex/skills/<nome>/SKILL.md`.

Referências úteis da skill de engenharia, conforme o produto:

- `references/product_engineering.md`: fases e critérios.
- `references/requirements_and_interfaces.md`: contratos, hipóteses e evidências.
- `references/mechanical_assemblies.md`: retenção, montagem e manutenção.
- `references/dfam.md`: orientação, paredes, folgas e impressão.
- `references/visual_validation.md`: vistas do CAD e inspeção das imagens.
- `references/assembly-validation.md`: contatos, colisões e trajetórias amostradas.
- `references/orcaslicer-engine.md`: fatiamento e limitações.

Não carregar todas as skills por padrão. Usar as pertinentes à etapa. Uma revisão em contexto separado foi feita ao final da implementação; ela encontrou problemas concretos de retenção e de escopo das verificações. Não houve uma segunda revisão independente depois das correções.

## 3. Ordem de execução

### Etapa 1 — Briefing e critérios

Registrar objetivo, uso, ambiente, limites externos, cargas, peças comerciais, estética, material, impressora, interfaces, manutenção e entregáveis. Separar medidas reais de hipóteses. Definir o que caracteriza sucesso e quais ensaios dependerão de bancada.

Se o usuário já entregou um briefing completo e pediu geração direta, avançar dentro desse escopo. Não transformar o planejamento em novas rodadas de autorização para ações rotineiras já autorizadas.

### Etapa 2 — Arquitetura funcional

Descrever subsistemas, entradas, saídas, caminhos de energia/calor/ar/fluido/luz, modos de operação e falhas. Fazer os cálculos preliminares que influenciam a construção. Consultar fontes primárias para especificações técnicas ainda não verificadas e salvar as referências.

### Etapa 3 — Arquitetura mecânica e forma

Definir coordenadas e datums, empilhamento, envelope, componentes separados, retenção, fixadores, folgas, caminhos de ferramentas, cabos e desmontagem. Desenhar a aparência a partir dessas funções e revisar proporções em vistas preliminares.

Para produtos, preencher `.cad3d/engineering.yaml` e `.cad3d/assembly.yaml`. Rodar os gates iniciais antes dos sólidos funcionais. Na Photon V, requisitos ficaram PASS e as arquiteturas funcional/mecânica WARNING; esses três gates permitiram modelar. WARNING continua pendência e precisa de justificativa. FAIL ou NOT_EVALUATED em gate inicial obrigatório exige correção antes de avançar.

### Etapa 4 — Plano curto e implementação

Salvar especificação, plano e registro de decisões. Implementar o modelo, os validadores e exportadores; não encerrar no plano.

- Concentrar dimensões principais em configuração e detalhes construtivos identificados no início do script.
- Criar peças nomeadas independentemente, montadas por um sistema comum de coordenadas.
- Separar peças imprimíveis, metal, elastômeros e referências comerciais.
- Manter o STEP do conjunto e exportações individuais das peças fabricadas.
- Rejeitar configurações impossíveis e conferir o envelope BREP efetivo, além dos valores declarados.

Na Photon V, o script principal gera o conjunto completo. O adaptador `src/model.py` apresenta apenas o escopo impresso ao CAD3D, evitando tratar aletas e clipes metálicos como paredes de FDM. A montagem completa tem seu próprio validador. Qualquer divisão desse tipo deve estar explícita nos relatórios.

### Etapa 5 — Validar e corrigir

Verificar contagens, sólidos, interferências, folgas, retenção, acesso de ferramentas, trajetória de remoção, seções mínimas e espaço para cabos. Ao encontrar falha, investigar a causa, corrigir e repetir as verificações afetadas. Criar regressão para erros relevantes.

Contatos declarados não autorizam sobreposição de volume. Peça posicionada não comprova retenção. Espaço reservado para fios não comprova um chicote montável. Comprimento e engajamento de parafusos também precisam de conferência.

### Etapa 6 — Revisar imagens e fabricação

Gerar e abrir as imagens de conjunto, inferior, internas, seção e explodida. Verificar enquadramento, identificação, peças ocultas e coerência com o CAD. Render de produto deve derivar do modelo efetivo; uma ilustração conceitual tem outro papel.

Exportar STL em orientação documentada, verificar fechamento e componentes conectados. Reabrir STEP e comparar quantidade de sólidos e volumes. Desenhos e DXFs devem derivar dos mesmos parâmetros da geometria.

Quando houver perfil exato disponível, fatiar com impressora/material/processo corretos e inspecionar o resultado. Não enviar arquivos à impressora automaticamente.

### Etapa 7 — Revisão independente e entrega

Quando autorizado e útil, usar um revisor em contexto separado para procurar falhas de engenharia e falsos PASS. Corrigir os achados e verificar as alterações. Informar quando a revisão foi apenas do próprio autor ou quando correções posteriores não tiveram nova revisão independente.

Entregar código, parâmetros, peças, conjunto, desenhos, BOM, montagem, impressão, renders, relatório e pacote portátil. Distinguir protótipo CAD de produto liberado para uso.

## 4. Container e ferramentas verificados

O `cad3d` global está em `/home/rrattes/.local/bin/cad3d`.
O ambiente da plataforma fica em `3d-engineering/`, com configuração em `3d-engineering/compose.yaml`.

| Motor | Imagem local | Uso |
|---|---|---|
| CAD | `cad3d-engineering:1.4.0` | Python, build123d 0.11.1, OCP, STL/STEP, análise e render PyVista/VTK |
| Fatiamento | `cad3d-orca:2.4.2` | OrcaSlicer separado; depende dos presets existentes |

IDs locais das imagens observados no registro deste fluxo, que não são digests de registro remoto:

```text
CAD:  sha256:90d034df91c55d8bb17d17b4aa165f17b8ec771b8437e9e86b60c3e3710da8e1
Orca: sha256:72be10f63d6895cbffc0ecce938c8bf12c4e1de098656d8e47fc831459b60f13
```

Os containers são efêmeros. A persistência está na pasta do projeto montada em `/workspace`; não depende de manter um container aberto. Não instalar bibliotecas CAD no Python do host para reproduzir este fluxo.

O Compose executa sem rede, com filesystem raiz somente leitura, `/tmp` temporário e pasta do projeto gravável. Já o `generate.sh` usado na Photon V executa `docker run --rm`, sem rede, com UID/GID do usuário e bind da pasta; esse comando direto não usa `--read-only`. São configurações distintas.

Diagnóstico inicial, sem reinstalar o ambiente:

```sh
cad3d --help
cad3d doctor
cad3d slicer doctor
```

Inicialização de um produto novo, substituindo o nome:

```sh
cad3d init NOME_DO_PROJETO
cd NOME_DO_PROJETO
cad3d architecture init --level product
# Preencher briefing, parâmetros e contratos.
cad3d architecture validate
```

O padrão de execução direta que funcionou, para um script que implemente `--all`:

```sh
docker run --rm --network none --user "$(id -u):$(id -g)" \
  -e PYVISTA_OFF_SCREEN=true \
  -e VTK_DEFAULT_OPENGL_WINDOW=vtkEGLRenderWindow \
  -e XDG_CACHE_HOME=/tmp/.cache \
  -v "$PWD:/workspace" -w /workspace \
  --entrypoint python cad3d-engineering:1.4.0 SCRIPT_DO_PROJETO.py --all
```

Executar a partir da pasta do produto. O nome do script e seus argumentos pertencem ao projeto; não presumir que qualquer script aceita `--all`.

Depois da implementação:

```sh
cad3d build
cad3d architecture validate --geometry
cad3d review
cad3d render --view engineering
cad3d export
cad3d report --requirements
```

Inspecionar os resultados de cada comando. Não encadear tudo de forma que um comando posterior esconda a falha de um anterior. Testes devem verificar requisitos e regressões concretos, conforme o projeto.

## 5. Limites encontrados e lições técnicas

1. **Perfil CAD não equivale a preset Orca.** A imagem Orca estava disponível, mas a tentativa de fatiar PETG-CF retornou `unsupported material profile: petg-cf`. Não houve G-code validado nem substituição silenciosa por PETG. Reconsultar a disponibilidade em novos projetos.
2. **Volume de conjunto aninhado:** nesta versão de build123d, `Compound.volume` divergiu da soma dos sólidos do conjunto. Comparar a soma dos volumes dos sólidos individuais antes/depois do STEP e exigir preservação da quantidade. Não assumir que toda diferença é um erro do exportador.
3. **Fixadores reais importam:** foram corrigidos eixos compartilhados entre parafusos, adicionadas porcas cativas e criados alívios para cabeças M3 no dissipador. O teste dessa última falha foi executado antes e depois da correção.
4. **Espessura deve vir da geometria:** a amostragem encontrou paredes locais muito mais finas que a parede nominal. A correção foi geométrica; o limite não foi reduzido para obter PASS.
5. **Hipóteses não são verificações físicas:** o chicote, vedação, calor, PAR e suspensão continuaram pendentes mesmo com sólidos e exportações válidos.
6. **Exportar só após as checagens:** o script final valida o conjunto antes de escrever os arquivos de fabricação.

## 6. Estrutura de entrega recomendada

```text
NOME_DO_PROJETO/
  README.md
  ABRIR_PROJETO.html
  SCRIPT_DO_PROJETO.py
  parameters.json
  generate.sh
  .cad3d/                 # contratos, projeto e seleção de perfis
  src/model.py           # adaptador CAD3D, se necessário
  scripts/               # validação, documentos, renders e pacote
  tests/                 # verificações específicas do produto
  docs/                  # briefing, plano, decisões, montagem e impressão
  drawings/              # desenhos e diagramas
  manufacturing/stl/     # apenas o que deve ser impresso
  manufacturing/step/    # peças e conjunto
  manufacturing/dxf/     # quando aplicável
  renders/               # imagens derivadas do CAD
  reports/               # evidências, pendências e manifestos
```

Escalar a estrutura ao tamanho do produto. Não exigir diagramas elétricos de uma peça sem eletrônica nem um processo completo de produto para um espaçador simples.

## 7. Evidência e ponto de partida

Na entrega registrada da Photon V: 12 peças imprimíveis do conjunto mais um olhal opcional em 13 STLs; STEP reaberto com 207 sólidos; nove testes passaram; geometria/montagem PASS, fabricação WARNING e físico NOT_EVALUATED. A revisão de produto permaneceu bloqueada por riscos físicos críticos abertos.

Referências locais:

- [Script executado](Aqualith_Photon_V_Rev_B/Photon_V_TC421.py).
- [Parâmetros](Aqualith_Photon_V_Rev_B/parameters.json).
- [Plano](Aqualith_Photon_V_Rev_B/docs/superpowers/plans/2026-10-16-photon-v.md).
- [Registro das decisões](Aqualith_Photon_V_Rev_B/docs/EXECUTION_LEDGER.md).
- [Relatório de validação](Aqualith_Photon_V_Rev_B/reports/VALIDACAO.md).
- [Evidência de fabricação](Aqualith_Photon_V_Rev_B/reports/fabrication_validation.json).
- [Compose da plataforma](3d-engineering/compose.yaml).

Esses dados descrevem uma execução, não uma garantia para novos produtos. Para começar outro projeto, usar [INICIO_NOVO_PROJETO.md](INICIO_NOVO_PROJETO.md).

## 8. Catálogo de peças, STLs e imagens na entrega

Para conjuntos com peças independentes, apresentar no README do produto uma tabela
com **nome e função da peça, link do STL, link da imagem CAD e quantidade a imprimir**.
Informar separadamente o número de arquivos distintos e o total de unidades.
Componentes de referência que não serão fabricados devem ser identificados como tal.

### Sequência

1. Ler `build/delivery/current.json` e identificar a execução selecionada e seu manifesto.
2. Usar os STLs e as imagens existentes dessa execução. Quando houver imagem complementar fora da entrega, identificá-la explicitamente.
3. Conferir os nomes e as quantidades com o catálogo de peças/instâncias e a BOM. Uma peça usada duas vezes pode ter apenas um STL.
4. Incluir vistas do conjunto montado e explodido, além das imagens individuais. As imagens devem ser derivadas do CAD; conceitos ilustrativos, quando usados, precisam de identificação própria.
5. Conferir existência dos arquivos e destino dos links. A inspeção visual e a geração de renders, quando realizadas, devem ter registro próprio; listar imagens existentes não equivale a revisá-las.
6. Publicar os links no README do produto e uma referência no índice do workspace. Preservar as entregas anteriores; atualizar o catálogo após selecionar uma nova execução.
7. Informar montagem, orientação de impressão e pendências de fabricação/ensaio físico separadamente da existência dos STLs.

Para uma consulta documental, usar os artefatos existentes. Quando o escopo exigir
novas imagens, seguir `3d-engineering` para renderização e revisão visual. Aplicar
`systematic-debugging` se houver falha e `verification-before-completion` para
conferir os resultados antes de declarar a entrega. O fluxo principal de skills e
os containers documentados acima permanecem a referência.

Exemplo aplicado: [catálogo visual da cesta Rev C](Cesta_Anemonas_Rev_C/docs/CATALOGO_ENTREGA.md),
com seis STLs, seis imagens individuais e sete peças impressas. A documentação do
catálogo não altera as pendências físicas desse projeto.

## 9. Automação e economia de contexto

Aplicar o [guia de economia](ECONOMIA_DE_CONTEXTO.md) conforme a tarefa. O script
`3d-engineering-evolution-20261017/scripts/delivery-catalog.py --project <pasta> --update-readme`
gera `docs/CATALOGO_ENTREGA.md` e `.json` usando o ponteiro, manifesto e BOM da
entrega selecionada. O README recebe um bloco gerenciado com link e totais.

Manter as listas de peças no catálogo gerado; documentos de entrada apontam para
ele. Quantidades vêm da BOM e os nomes legíveis podem vir de
`.cad3d/delivery-catalog.json`. Hash divergente bloqueia a geração; imagem ausente
fica explícita. Conferir artefatos consultados não significa revalidar o produto.

Na retomada, ler briefing, estado e pendências pertinentes. Abrir referências da
skill por necessidade. Mudanças compartilhadas ou com impacto incerto exigem
ampliar a análise; manter todos os requisitos e gates aplicáveis.

A automação foi adicionada ao checkout local, sem mudar runtime, imagem ou kit
1.8.0 já aprovado. Consultar o guia antes de compartilhar a adição.

## 10. Product-design: identidade e revisão estética

A [skill product-design](skills/product-design/SKILL.md) é uma **etapa opcional ao
final do fluxo de 3d-engineering**, acionada quando o usuário solicitar aparência,
estilo ou redesenho estético. Sem esse pedido, concluir a engenharia e entregar.
Ela permanece independente e não altera a `3d-engineering` nem outras skills.

Fluxo: briefing → arquitetura e CAD → verificações de engenharia →
**product-design opcional** → verificações técnicas afetadas, se houver mudança → entrega.

Partir do CAD produzido pela engenharia e preservar os requisitos e pendências.
Mudanças de geometria retornam às verificações afetadas antes da entrega atualizada.
Em produto simples ou com direção já escolhida, aplicar uma proposta justificada
sem criar comparações e aprovações repetidas. Uma revisão apenas estética ou estudo
de cor simulada não exige regenerar geometria que permaneceu igual.

Estilos iniciais opcionais confirmados: **minimalista, gamer, industrial, orgânico
e retrô**. Direções próprias e misturas com linguagem dominante também são aceitas.
O estilo se traduz em silhueta, proporções, superfícies, juntas, fixações, cores,
materiais e acabamento; dimensões e restrições vêm do briefing do produto.

Registrar intenção no documento existente do projeto ou em
`docs/DIRECAO_DE_DESIGN.md`; registrar imagens vistas, achados e pendências no
relatório existente ou em `reports/REVISAO_ESTETICA.md`. Aprovação do usuário,
conformidade estética, validade CAD e comprovação física têm registros distintos.

A instalação e os limites desta primeira entrega estão em
[registro de criação](docs/product-design/CRIACAO.md). Usar as referências de estilo
e revisão sob demanda, mantendo o padrão de economia de contexto.

## Precedência obrigatória da engenharia

**Engenharia prevalece sobre design.** A aparência deve respeitar função, segurança,
desempenho, confiabilidade, manutenção, tolerâncias e fabricação. Preferência estética
não autoriza reduzir margens, piorar resultados nem flexibilizar critérios técnicos.
Comparar os impactos relevantes com a solução existente e com os requisitos atuais.
Se houver degradação, redesenhar ou rejeitar a proposta estética. Se o impacto técnico
relevante estiver sem demonstração, manter apenas como estudo e bloquear sua aceitação
como solução do produto. Baseline sem validação também não comprova adequação.
Acréscimo de área em outra abertura, beleza do render ou aprovação estética não
comprovam preservação de desempenho. Uma mudança por necessidade funcional exige
justificativa e verificação de engenharia próprias.

## Product-design — promoção da evolução 01

A evolução 01 foi aprovada pelo usuário e promovida, preservando o link global e
a fonte anterior para recuperação. [Registro](docs/product-design/promotions/evolution-01/APROVACAO_E_PROMOCAO.md).
O fluxo incorpora o gate próprio de engenharia, comparação BREP opcional e seleção
local com revisão/decisão vinculadas. Não é um bloqueio global do publicador CAD3D.
[Referências externas](docs/product-design/REFERENCIAS_DE_ESTILO.md) ampliam as
possibilidades de linguagem formal sem mudar o pacote aprovado ou a 3d-engineering.

## Product-design — evolução 02 ativa em 18/10/2026

Atualização aprovada após o piloto dos cinco porta-joias com duas gavetas. Os 29 arquivos avaliados foram promovidos sem alterações. [Registro, inventários e recuperação](docs/product-design/promotions/evolution-02/APROVACAO_E_PROMOCAO.md).

Fluxo preservado: engenharia e verificações do escopo → product-design opcional quando solicitada → rever impactos técnicos das mudanças → imagens reais e revisão estética → decisão do usuário. Recursos de subestilos, mapa de liberdade, receitas, comparação visual e cache são usados conforme a necessidade; não são etapas obrigatórias para todo projeto. A 3d-engineering permanece na versão 1.8.0.

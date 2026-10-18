# Fluxo de desenvolvimento de produtos 3D

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

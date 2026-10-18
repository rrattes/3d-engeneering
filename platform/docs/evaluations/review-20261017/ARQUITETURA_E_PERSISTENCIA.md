# Avaliação arquitetural e persistência — CAD3D

Data:17/10/2026. Solicitada após a aprovação do plano de evolução e antes da implementação. Inspeção de código, decisões técnicas e contratos existentes; consulta às documentações oficiais SQLite/Python. Não houve implementação, instalação de banco, migração ou teste de desempenho. O acréscimo de SQLite é recomendação arquitetural, não requisito já aprovado do plano original.

## Parecer

Recomendo manter uma aplicação local modular, acessada por CLI pelos agentes, executando CAD em Docker. Separar domínio, execução, verificação, artefatos e consulta. Um banco SQLite pode agregar valor para consulta/histórico e reutilização rastreável de componentes, depois da estabilização dos contratos. Deve começar como índice opcional e reconstruível, sem servidor adicional e sem ser necessário para gerar ou validar uma peça.

O ganho de banco é principalmente organização e consulta. Não há medição que demonstre gargalo de busca neste workspace ou melhoria de tempo total. O banco não aumenta precisão geométrica, não encontra dimensões comerciais inexistentes e não torna verdadeira uma evidência não medida.

## Evidências locais e consequências

1. `cli/cad3d.py:project_files` lê contrato/configuração, aplica gate, importa/executa o modelo e cria o diretório de saída. Funções build, validate, render, export, report e write_manifest voltam a chamar esse carregamento. Consequência: acoplamento entre leitura, execução CAD e efeitos; comandos informativos podem regenerar geometria. A cadeia de uma execução deveria usar o mesmo contexto e os mesmos sólidos, sem reconstruir o modelo para escrever o manifesto.
2. `source_fingerprint.py` inventaria entradas locais e exclui diretórios gerados. Isso é evidência de frescor, não um snapshot completo da execução. Consequência: congelar entradas usadas e identidade do runtime por run; comparar hashes continua útil, mas não elimina sozinho uma leitura de arquivo alterado entre operações.
3. O BC250 distribui informações entre `parameters.json`, `design_inventory.json`, referências comerciais, contratos de montagem e índice gerado. Consequência: catálogo canônico precisa gerar as projeções/índices. Não introduzir banco como mais um cadastro editável da mesma peça.
4. Exportadores e relatórios ainda agrupam funções em `cad3d.py`; render de apresentação e classificação de materiais exigiram código próprio no BC250. Consequência: módulos com responsabilidades claras antes de persistência adicional.
5. Há decisões técnicas em `docs/TECHNICAL_DECISIONS.md` e `TECHNICAL_DECISIONS_V14.md`. Esta avaliação complementa essas decisões; não propõe segundo kernel CAD, serviço MCP obrigatório, servidor web ou fatiador integrado ao mesmo container.

## Arquitetura recomendada

```text
Codex / Claude Code
        |
        v
CLI e adaptadores dos agentes
        |
        v
Orquestrador de uma execução (RunContext)
        |
        +--> Contratos, parâmetros derivados e catálogo
        +--> Adaptador CAD: build123d/OCP
        +--> Verificações: geometria, interfaces, estados de serviço
        +--> Política: o que pode ser publicado como protótipo
        +--> Exportadores e renderizadores
        |
        v
Diretório de execução + manifesto imutável
        |
        +--> Publicação da entrega por apontador atômico
        +--> Índice SQLite opcional, reconstruível
```

Dependências de alto nível consomem interfaces pequenas. O núcleo de regras não importa SQLite, Docker, shell ou detalhes de CLI. Testes geométricos naturalmente continuam dependendo do kernel. Não é necessário criar microserviços para obter essa separação.

### 1. Entradas e domínio

- Fontes Python, YAML/JSON e revisões de componentes são entradas explícitas.
- Catálogo separa peça, instância, montagem, processo/material, componente comercial, interfaces e proveniência.
- Unidades e transformação de coordenadas pertencem ao contrato.
- Derivação de datums/layout ocorre uma vez por conjunto de parâmetros; combinação inválida deve produzir motivo identificável.
- Requisito do usuário, decisão do projetista e hipótese permanecem campos distintos.

### 2. Contexto da execução

Um `RunContext` proposto identifica run, versão de schema, snapshot/hash de entradas, runtime/imagem, parâmetros resolvidos, catálogo, shapes em memória e resultados. O snapshot deve capturar os arquivos necessários e o modelo deve resolver entradas no snapshot. Fontes externas, variáveis de ambiente relevantes e arquivos comerciais precisam de identidade/proveniência próprias; não prometer reprodução de dependências que não foram capturadas.

Build, validação, render e exportação de uma cadeia usam esse contexto. Um comando isolado pode iniciar novo run, mas não deve juntar artefatos de runs distintos. Consulta de histórico não importa nem executa o código do modelo.

### 3. Resultados e política

Adotar contrato comum de resultado: check_id, status, severidade, escopo, método/versão, entidades verificadas, revisão de entradas, evidências e limitações. Esquema não exige que um resultado numérico prove mais do que seu método permite.

A política de publicação lê resultados; não os reescreve para aprovar. PASS geométrico, montagem amostrada, avaliação de fabricação, fatiamento e físico permanecem independentes. Uma linha de banco ou declaração de componente verificado não concede aprovação física.

### 4. Artefatos e entrega

STEP, STL, imagens e relatórios permanecem arquivos. Cada run possui manifesto com hashes e paths relativos. Somente execução completa e elegível é selecionada como entrega atual. Não usar transação SQL como promessa de atomicidade conjunta entre banco e filesystem.

Ordem proposta: construir/validar/exportar em staging; concluir manifesto; publicar diretório imutável e apontador sob lock; indexar a entrega. Se o índice falhar, a entrega canônica continua verificável e a consulta informa indexação pendente. Se a publicação falhar, nenhum registro pode fazer a execução aparecer como entrega atual. O índice deriva esse estado do apontador/manifesto canônico e pode ser reconciliado.

## Onde um banco agrega valor

Consultas possíveis depois de modelar os dados:

- Quais revisões de componentes aparecem neste projeto e qual fonte sustenta suas medidas?
- Quais runs da mesma revisão tiveram falhas de ferramenta ou manutenção?
- Qual entrega contém determinada peça e qual é seu SHA256?
- Quais componentes foram apenas referenciados e quais possuem medição/ensaio físico documentado?
- Qual validação depende do perfil, interface ou componente que mudou?

As relações ajudam a localizar impacto. A decisão de invalidar evidência depende de regras e revisões; SQL não calcula automaticamente essa semântica.

## Comparação das opções

| Opção | Adequação atual | Custo/limite |
|---|---|---|
| Arquivos versionados e manifestos | Necessários como fonte de verdade portátil e auditável | Consultas entre muitos runs/componentes exigem varredura |
| SQLite como índice local | Recomendado, opcional, após estabilizar catálogo/manifestos | Exige schema, reconstrução, controle de concorrência e tratamento de índice desatualizado |
| SQLite como único cadastro autoritativo | Não recomendado nesta fase | Migração/merge de dados binários, recuperação e distribuição passam a depender do banco |
| Banco servidor, por exemplo PostgreSQL | Avaliar quando houver biblioteca central compartilhada e escrita concorrente de várias máquinas | Introduz serviço, acesso, migrações, operação e backup; compartilhamento de um kit entre instalações não exige centralização |
| Banco vetorial ou de grafos | Sem benefício demonstrado para os problemas atuais | Busca semântica não verifica dimensões, furação ou evidência; relações atuais cabem em tabelas/arquivos |

SQLite é compatível com armazenamento local sem servidor, conforme sua documentação. A escolha é recomendação para o uso descrito, não resultado de benchmark. Python3.12 oferece interface `sqlite3`; a disponibilidade e versão exatas no runtime empacotado precisam ser verificadas durante implementação.

## O que fica em cada lugar

| Dado | Fonte canônica | SQLite opcional |
|---|---|---|
| Briefing, parâmetros e contratos | Arquivos versionados do projeto | Referência/hash e campos de consulta |
| Componente comercial e revisão | Registro revisado JSON/YAML com fonte e limites | Índice por revisão, atributos e proveniência |
| Seleção dos componentes | Snapshot/lock do projeto com revisão e hash | Relação projeto–componente |
| CAD e fabricação | Python e arquivos STEP/STL/PNG | Apenas metadados, paths e hashes; sem serializar shapes OCP |
| Verificações de uma execução | Relatórios/manifesto do run | Resumo pesquisável e links para evidências |
| Entrega atual | Apontador canônico publicado | Projeção reconstruível |
| Memória dos agentes | Handoff/documentos com fontes | Nenhuma promoção automática a fato técnico |

Uma atualização na biblioteca não deve mudar silenciosamente um projeto. O projeto conserva sua revisão selecionada. Alterar essa seleção invalida as verificações dependentes; correção/revogação de uma referência deve gerar aviso explícito aos projetos afetados, sem apagar o histórico.

## Escopo mínimo do índice

Local inicial: `build/index/catalog.sqlite`, fora das entradas autoritativas e do fingerprint. Um índice por projeto é a base; consulta entre projetos somente sobre raízes explicitamente selecionadas. Não varrer automaticamente todo o diretório pessoal.

Tabelas lógicas propostas, ainda sujeitas ao contrato do catálogo:

- projects: identidade estável do projeto e schema, sem depender de path absoluto como identidade portátil.
- component_revisions: identidade, revisão e hash do registro canônico.
- project_components: referência à revisão selecionada, sem duplicar cadastro editável.
- runs: input_fingerprint, runtime identity e manifesto canônico.
- artifacts: run, path relativo, tipo e hash.
- findings: run, check_id, status, severidade, escopo e evidência.
- source_links: registro de componente, referência de fonte e origem da medida.

IDs e chaves estrangeiras devem preservar limites entre projetos e revisões. Habilitar/verificar integridade referencial em cada conexão. Queries parametrizadas; sem aceitar SQL arbitrário do agente como interface de escrita. Comandos futuros de consulta/reindexação passam por serviços da aplicação.

Não é necessário ORM/servidor nesta primeira versão. Modo sem índice precisa produzir as mesmas decisões CAD e a mesma seleção de artefatos. Índice ausente ou antigo não significa ausência de evidência; a consulta deve informar o estado e oferecer reconstrução/leitura canônica.

## Concorrência, portabilidade e manutenção

- Transações curtas de metadados; nunca manter transação aberta enquanto OCP calcula geometria/render.
- SQLite admite um escritor por vez; serialização e timeout limitado devem ser explícitos. Escrita concorrente intensa é sinal para reavaliar arquitetura.
- Começar com journal padrão local; não habilitar WAL indiscriminadamente em volumes cuja semântica não foi verificada. WAL requer processos no mesmo host e não funciona sobre filesystem de rede.
- Não sincronizar arquivo de banco ativo por Git/Drive/NAS como método de colaboração. Compartilhar fontes e pacotes; reconstruir índice na instalação de destino.
- Banco derivado não integra o ZIP obrigatório e não precisa de container dedicado. Versão de schema desconhecida deve causar indisponibilidade explícita do índice, não migração destrutiva automática.
- Reconstruir em arquivo temporário e substituir somente após concluir/checks; preservar índice anterior até essa conclusão. Não apagar corrupção/evidência silenciosamente.
- Retenção de runs/cache é explícita; não remover evidências selecionadas por entregas/ensaios físicos.

## Ajustes recomendados ao plano aprovado

1. Em G0, mapear propriedade de cada dado e congelar schemas/IDs e identidade de execução.
2. Em etapa2, tornar catálogo e registros comerciais fontes únicas. Evitar banco antes disso.
3. Em etapa3, introduzir RunContext/snapshot e publicação usando artefatos da mesma execução; retirar regeneração CAD do escritor de manifesto.
4. Em etapa7, consolidar revisão e lock dos componentes comerciais.
5. Inserir uma etapa opcional7B de índice SQLite depois dos contratos e registros estarem estáveis. Sua ausência não bloqueia as melhorias CAD aprovadas.
6. Acrescentar ao kit regressão com índice ausente/corrompido/desatualizado e instalação sem servidor de banco.

Interfaces propostas para essa etapa: `rebuild_index(project_root, destination) -> IndexReport`, `query_index(project_root, query_spec) -> QueryResult` e `check_index_freshness(project_root) -> FreshnessResult`. Não iniciar implementação dessas APIs nesta avaliação.

## Regressões adicionais propostas

- ARCH-RUN-01: uma cadeia constrói modelo uma vez e usa a mesma revisão em todos os artefatos; manifesto não executa build novamente.
- ARCH-RUN-02: alteração de entrada durante leitura/execução não produz entrega com identidade de outra revisão.
- ARCH-DB-01: sem índice e com índice, mesmo input/contexto produz mesmas decisões e conteúdo geométrico; comparar artefatos pelos invariantes pertinentes, não timestamps voláteis.
- ARCH-DB-02: índice reconstruído reproduz consultas canônicas e mantém separação de projetos/revisões.
- ARCH-DB-03: arquivo ausente, truncado, schema desconhecido ou hash antigo resulta em indisponível/desatualizado explícito, sem falso PASS nem alteração do CAD.
- ARCH-DB-04: falha/interrupção na atualização não afeta a entrega canônica e permite reconciliação.
- ARCH-DB-05: componente upstream novo não altera projeto travado; mudança explícita do lock invalida evidências dependentes.
- ARCH-DB-06: consultas simultâneas e escritor ocupado falham/aguardam de forma limitada sem congelar CAD nem manter transação longa.
- ARCH-DB-07: cópia do pacote para pasta nova funciona sem banco, paths absolutos ou serviço de rede; consulta sem indexar não executa Python do modelo.

Não são testes executados. Na implementação, vincular os IDs ao registro existente e aplicar negativos antes das correções/capacidades novas.

## Fontes técnicas consultadas

- [SQLite — usos apropriados](https://www.sqlite.org/whentouse.html): armazenamento local, diferenças para servidor e concorrência de escrita.
- [SQLite — WAL](https://www.sqlite.org/wal.html): limites de filesystem/host e características dos journals.
- [Python3.12 — sqlite3](https://docs.python.org/3.12/library/sqlite3.html): interface disponível na biblioteca padrão e transações.
- [SQLite — foreign keys](https://www.sqlite.org/foreignkeys.html): integridade referencial e habilitação por conexão.

## Conclusão

A arquitetura deve evoluir primeiro para catálogo único, execução identificada, resultados com escopo e publicação coerente. SQLite opcional encaixa como camada de consulta depois disso e pode tornar o uso crescente da biblioteca mais organizado. Não há razão demonstrada para impor banco servidor, dependência de nuvem ou um banco como autoridade geométrica. A implementação permanece não iniciada.

## Avaliação complementar solicitada: Qdrant

[Estudo específico de Qdrant](QDRANT.md): identifica caso de uso plausível para recuperação semântica de conhecimento técnico revisado. Propõe camada opcional, separada do CAD e comparada com busca lexical/FTS5 em piloto. O benefício continua não demonstrado por benchmark; não substitui fontes canônicas, catálogo estruturado ou validação geométrica. Nenhuma adoção/instalação foi realizada.

# Início de um novo projeto 3D

Preencher o briefing abaixo e usar o prompt ao final. O método está em [FLUXO_PROJETOS_3D.md](FLUXO_PROJETOS_3D.md).

Este documento inicia um produto novo. O fluxo local utiliza a **3d-engineering 1.8.0, aprovada e promovida em 17/10/2026**, com capacidades gerais opcionais descritas no guia e os fundamentos de confiabilidade da1.7.0; preserva o movimento helicoidal da 1.6.0 e a base **1.5.0, aprovada pelo usuário após a cesta Rev C**. Photon V e cesta são referências de organização e execução; suas peças e dimensões não são requisitos do novo produto. A aprovação da skill é separada da validação física dos produtos.

## 1. Briefing para preencher

| Campo | Definição do novo produto |
|---|---|
| Nome e revisão | |
| Função e problema que resolve | |
| Usuário e situação de uso | |
| Ambiente: água, calor, UV, poeira, químicos etc. | |
| Dimensões externas máximas | |
| Cargas, movimentos, pressões ou potências | |
| Medidas reais disponíveis e origem | |
| Componentes comerciais já disponíveis | |
| Interfaces com outros objetos/produtos | |
| Material de cada grupo de peças | |
| Processo e impressora de referência | |
| Aparência desejada e referências visuais | |
| Montagem, manutenção e peças substituíveis | |
| Critérios de aceitação e ensaios físicos | |
| Arquivos esperados e restrições | |

Um campo sem informação deve virar hipótese explícita ou pergunta essencial. Não tratar dimensão assumida como medida real. Não herdar os 32 LEDs, PETG-CF, impressora ou arquitetura elétrica da Photon V por padrão.

## 2. Prompt reutilizável

Copiar o texto abaixo, preencher nome/revisão e anexar o briefing preenchido:

```text
Quero desenvolver do zero [NOME DO PRODUTO], revisão [REVISÃO].

Use o briefing que forneço como fonte de verdade. Crie uma pasta independente
para este produto. Reutilize o método documentado em FLUXO_PROJETOS_3D.md;
não copie geometria, componentes, dimensões ou soluções de produtos anteriores
sem uma razão explícita e coerente com este briefing.

Implemente em Python com build123d/OCP no ambiente Docker CAD3D existente.
Não use Fusion 360. Verifique as ferramentas e imagens disponíveis antes de
propor novas instalações. Não instale bibliotecas CAD no host.

Execute o trabalho até os arquivos possíveis. Não encerre apenas no plano.
Prossiga com decisões rotineiras reversíveis dentro deste escopo e registre
hipóteses relevantes. Pergunte quando faltar informação essencial que impeça
uma solução responsável; continue o trabalho independente dessa resposta.

1. Entenda função, aparência, restrições e critérios de sucesso. Use brainstorming
   no briefing e writing-plans para organizar a execução, conforme a complexidade;
   aplique 3d-engineering desde as decisões técnicas. A referência local aprovada
   é a versão 1.8.0, sobre a base 1.5.0 aprovada; confirme a versão disponível. Use systematic-debugging quando
   houver falhas e verification-before-completion antes da entrega. Selecione
   auxiliares pela necessidade, sem carregar toda a biblioteca.
2. Faça arquitetura funcional e mecânica: datums, envelope, empilhamento,
   interfaces, retenção, fixadores, montagem e manutenção. Faça cálculos que
   influenciam a construção. Separe medidas reais e hipóteses.
3. Salve briefing, plano e registro de decisões; valide os gates iniciais.
   Dimensione o processo à complexidade do produto.
4. Gere efetivamente o código paramétrico. Concentre dimensões principais na
   configuração e identifique detalhes construtivos no início do script.
   Crie componentes independentes e nomeados; modele o conjunto montado.
5. Desenvolva forma e proporções coerentes com o produto. Revise vistas cedo:
   validade geométrica não basta para um resultado funcional e bem desenhado.
6. Separe peças imprimíveis, peças metálicas, elastômeros e referências
   comerciais. Defina como cada componente é retido e como pode ser removido.
7. Verifique o BREP efetivo: dimensões, contagens, colisões, folgas, espessuras,
   cabeças e acesso de parafusos, retenção, cabos e trajetórias de manutenção,
   conforme aplicável. Não confunda posicionamento com fixação.
   Para movimentos não cobertos pelo verificador genérico, use verificações
   específicas e declare cobertura e limites. Desde a versão 1.6.0, movimentos
   helicoidais podem ser declarados no contrato de montagem: eixo mundial, origem,
   passo/entradas, sentido, percurso e amostragem. Use o avaliador nativo e seus
   pré-requisitos; mantenha a distinção entre percurso livre e retirada completa.
   Na 1.7.0, use referências por ponto quando o centro da face não for estável e
   registre limites, procedência e hipóteses das cadeias de tolerância. Não trate
   conta nominal ou limites assumidos como comprovação de encaixe físico.
   Na1.8.0, selecione conforme o produto: interfaces paramétricas, movimentos
   compostos, variantes, calibração medida, envelopes de acesso/cabos, desenhos
   com cortes/cotas e cálculo preliminar. Consulte somente as seções necessárias
   de general_capabilities.md; não extrapole os modelos nem presuma ensaios.
8. Investigue as falhas antes de corrigir. Crie testes para requisitos e
   regressões relevantes. Reexecute as checagens afetadas pelas correções.
9. Gere renders do CAD efetivo e inspecione as imagens. Entregue vistas externas,
   internas, seção e explodida quando ajudarem a entender o produto.
10. Exporte STL individual das peças imprimíveis, com orientação documentada;
    exporte STEP das peças fabricadas e do conjunto. Reabra os STEP e confira
    quantidade e soma de volumes dos sólidos; valide fechamento dos STL.
    Gere desenhos/DXF a partir dos mesmos parâmetros quando aplicável.
11. Para FDM, confira o perfil real de impressora, filamento e processo. Se não
    existir preset adequado no Orca, registre a limitação. Não substitua o
    material silenciosamente nem gere G-code com compatibilidade presumida.
    Não envie arquivos à impressora.
12. Quando útil, faça uma revisão independente em contexto separado; corrija
    os achados e verifique as mudanças. Informe os limites dessa revisão.
13. Entregue README em português, parâmetros, código, BOM quando aplicável,
    instruções de montagem/impressão, arquivos de fabricação, renders,
    relatório de validação, pendências físicas e um pacote ZIP verificável.
    Vincule os arquivos à execução selecionada em build/delivery/current.json,
    com fontes e hashes conferidos. Registre WARNING e NOT_EVALUATED sem
    convertê-los em PASS; aprovação do fluxo não comprova resistência física.

Ao concluir, mostre: arquitetura e decisões principais, dimensões efetivas,
arquivos e caminhos, como regenerar, verificações executadas, componentes
indefinidos e ordem de prototipagem. Distinga CAD válido, fabricação avaliada,
fatiamento e desempenho físico. Não declare como pronto o que depender de
medição, ensaio ou seleção de componentes ainda pendentes.

Briefing do novo produto:
[COLAR AQUI O BRIEFING PREENCHIDO]
```

## 3. Onde colocar os documentos

Neste workspace, o agente encontra a indicação do fluxo em [AGENTS.md](AGENTS.md).
Em outra pasta ou ferramenta, fornecer o caminho deste documento e do guia, ou copiar ambos para o novo workspace. Esses arquivos não instalam skills nem configuram automaticamente outros aplicativos.

As skills são instruções auxiliares; o briefing do usuário e as regras do ambiente continuam prevalecendo. O fluxo não exige aprovações extras para trabalho que já foi autorizado.


## 4. Entrega com contexto enxuto

Consultar [ECONOMIA_DE_CONTEXTO.md](ECONOMIA_DE_CONTEXTO.md) para escolher leituras e
verificações conforme a tarefa. Quando a entrega seguir o contrato CAD3D suportado,
gerar o catálogo de STL/imagem/quantidade a partir da BOM e do manifesto. Apontar
para esse catálogo no README, sem manter tabelas duplicadas. Reutilizar somente
evidências com procedência e escopo compatíveis; manter as pendências explícitas.


## 5. Product-design opcional ao final da engenharia

Após o CAD e as verificações de engenharia, usar
[product-design](skills/product-design/SKILL.md) somente se o usuário solicitar
linguagem formal, estilo ou revisão estética. Sem esse pedido, seguir à entrega.
Mudanças geométricas retornam às verificações de engenharia afetadas. Informar estilo desejado, referências, ambiente,
faces visíveis e acabamento esperado quando conhecidos. Opções iniciais:
minimalista, gamer, industrial, orgânico e retrô; outras direções são permitidas.
Registrar critérios visuais e separar a aceitação estética da validação técnica.
A nova skill é independente; seus pedidos de mudança são tratados no projeto.

Engenharia tem precedência sobre design. Escolhas estéticas devem preservar os requisitos técnicos e suas margens; degradar desempenho ou deixar impacto relevante sem demonstração bloqueia a aceitação da proposta como solução do produto.

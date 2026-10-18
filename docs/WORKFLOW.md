# Fluxo atual

## Primeira utilização: conferir antes de modelar

**Na primeira utilização, peça ao agente para conferir a disponibilidade das skills e do container antes de modelar.** O agente deve fazer essa conferência ao iniciar o fluxo em uma instalação nova:

1. Confirmar que consegue localizar e ler `skills/3d-engineering/SKILL.md`; em brinquedos, também `skills/toy-modeler/SKILL.md`; em pedidos de aparência, `skills/product-design/SKILL.md`. Conferir a descoberta no agente; arquivos presentes não comprovam ativação. Verificar somente as auxiliares necessárias à tarefa.
2. Confirmar Docker Engine acessível, Compose v2 e imagem CAD disponível. Na raiz do repositório, executar `./platform/scripts/cad3d doctor` e conferir o resultado, registrando falhas e limitações.
3. Se faltar uma skill ou o ambiente CAD não estiver operacional, informar o impedimento e seguir `docs/INSTALL.md` para resolver antes da modelagem. Briefing e planejamento podem continuar; não afirmar que CAD foi executado sem evidência.

Registrar a conferência no documento de estado do projeto. Repetir após mudança de ambiente, versão ou descoberta de falha relevante; não reconstruir imagens nem carregar todas as skills a cada peça.

1. **Briefing:** brainstorming + 3d-engineering. Para brinquedos, toy-modeler define antes do CAD a promessa de brincadeira, ação, resposta, variações e perguntas de protótipo.
2. **Plano proporcional:** writing-plans; change-impact/product-capability para mudanças com contratos ou dependências relevantes.
3. **Execução:** executing-plans + 3d-engineering. Arquitetura, parâmetros, peças independentes, montagem e referências comerciais. Componentes reais desconhecidos permanecem parametrizados e pendentes.
4. **Verificações técnicas e interação:** validar CAD, interferências, interfaces, tolerâncias, movimentos e fabricação conforme escopo. Em brinquedos, toy-modeler liga mecanismos à interação e registra observações reais quando houver protótipo. CAD não prevê sozinho sensação ou vontade de repetir.
5. **Design opcional:** product-design apenas se solicitado, depois da engenharia. Em brinquedos, reforça identidade e leitura da brincadeira. Mudança de forma retorna às verificações afetadas. Estudo só de cor pode reutilizar CAD.
6. **Revisão e entrega:** imagens reais, arquivos fabricáveis, BOM, instruções, riscos e pendências. verification-before-completion e revisão independente quando necessária/autorizada. Aprovação estética não qualifica física.

`3d-engineering` conduz CAD; `product-design` é opcional para aparência; `toy-modeler` é opcional em projetos de brinquedo. As 26 auxiliares distribuídas cobrem manutenção/evolução do método e não precisam ser invocadas em toda peça. `third_party/skills-manifest.json` identifica fontes e arquivos.

## Evolução de skills

Cópia isolada → análise de impacto → requisitos/critério de avaliação → implementação e regressões autorizadas → piloto limitado → revisão → registro de limites → aprovação e promoção. Conservar a estável e recuperação. Não editar uma skill como efeito colateral da aplicação de outra.

## Economia de contexto

- Leia índice/estado e apenas referências pertinentes. Não abrir todas as skills.
- Reutilize artefatos atuais com hashes/dependências; não reutilize aprovação humana por cache.
- Mantenha logs detalhados em arquivo e resumos curtos na conversa.
- Faça verificações dirigidas por mudança; amplie quando houver dependência compartilhada ou impacto incerto.
- Prefira execução sequencial; agentes somente para tarefas independentes e autorizadas. Campanhas comportamentais devem ter orçamento definido antes de abrir dezenas de contextos.
- Não alegue percentuais de economia sem medição.

## Documentos por produto

Briefing/requisitos, parâmetros autoritativos, decisões, catálogo/BOM, desenhos, montagem/impressão e relatório de validação. Separar PASS CAD, fabricação, fatiamento e físico. Produtos simples usam estrutura menor.

O histórico original está em docs/history e em platform/docs. Ele contém caminhos e resultados locais de outra máquina: não é instrução de instalação nem comprovação da máquina atual.

## Versão vigente

Product-design evolução03 aprovada/promovida; evolução02 preservada. Comportamento parcial20/36 e julgamento pendente não foram convertidos em PASS. [Promoção](product-design/promotions/evolution-03/APROVACAO_E_PROMOCAO.md).

Toy-modeler 1.0.0 aprovada/promovida para protótipos pessoais; avaliação conceitual registrada, sem CAD ou teste físico de brinquedo. [Promoção e handoff](toy-modeler/promotions/v1.0.0/APROVACAO_E_PROMOCAO.md).

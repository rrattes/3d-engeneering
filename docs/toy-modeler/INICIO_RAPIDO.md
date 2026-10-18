# Testar toy-modeler em outro chat

1. Abra Codex ou Claude Code na raiz deste repositório e confirme que o agente encontra `toy-modeler` e `3d-engineering`.
2. No Codex, invoque `$toy-modeler`; no Claude Code, peça explicitamente que use a skill `toy-modeler`. Briefing: **“Crie um brinquedo pessoal. Comece pela brincadeira: proponha uma ação, a resposta do brinquedo e variações. Depois desenvolva o conceito e a arquitetura mecânica; não presuma dimensões nem componentes que eu não informei.”**
3. Quando aprovar o conceito, peça a etapa CAD com `3d-engineering`. Use `product-design` apenas se quiser explorar aparência.
4. Para a primeira execução no ambiente, confira Docker e rode `./platform/scripts/cad3d doctor`, conforme `docs/WORKFLOW.md`.

Para comparar comportamento, escolha um briefing novo de brinquedo e registre o que a skill acrescentou: ações possíveis, resposta percebida, variações e perguntas que dependem de protótipo. Esta versão é para protótipos pessoais e não foi avaliada com brinquedo físico.

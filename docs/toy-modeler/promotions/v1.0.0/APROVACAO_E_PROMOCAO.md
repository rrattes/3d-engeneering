# Aprovação e promoção — toy-modeler 1.0.0

O usuário aprovou o plano e solicitou: **“escreva a skill e promova. documente vou testar em outro chat”**. A skill foi promovida como método opcional para desenhar a experiência de brinquedos e protótipos pessoais, sem finalidade de venda.

Fonte ativa: `skills/toy-modeler`. Descoberta no Codex e Claude Code: links `.agents/skills/toy-modeler` e `.claude/skills/toy-modeler`. Fluxo documentado em `docs/WORKFLOW.md`; início rápido em `docs/toy-modeler/INICIO_RAPIDO.md`.

## Evidências e limites

- As referências reais foram usadas para extrair padrões de interação, sem copiar produtos.
- Um teste comportamental independente comparou uma criatura articulada com e sem a skill. O baseline já apresentou um conceito lúdico forte; a candidata explicitou melhor o ciclo de brincadeira, o papel das juntas e a distinção entre hipótese e observação. Isso não prova aumento de diversão.
- Quatro testes do contrato passaram; `skill-creator/scripts/quick_validate.py` retornou `Skill is valid!` em Docker `cad3d-engineering:1.8.0`.
- Carrinho e objeto de flexura são pilotos conceituais. Não foram modelados nem impressos; força, sensação, durabilidade e interação real permanecem não avaliadas.
- A aprovação da skill não valida fisicamente nenhum brinquedo. O primeiro projeto no outro chat deve ser usado para avaliar utilidade e lacunas.

## Recuperação

Para reverter, remover os dois links de descoberta, restaurar `docs/WORKFLOW.md`, `docs/INSTALL.md`, `README.md`, `AGENTS.md` e `THIRD_PARTY_NOTICES.md` via Git e preservar este registro histórico. Não há versão toy-modeler anterior.

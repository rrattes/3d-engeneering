# Toy-modeler Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use executing-plans or an authorized equivalent to implement this plan task by task. Steps use checkboxes for tracking.

**Goal:** Transformar ideias de brincadeira em experiências, mecanismos e modelos imprimíveis, com avaliação da interação no protótipo.

**Architecture:** Skill de orquestração, referências por padrão de brincadeira, contrato JSON e validador pequeno. Reusar CAD3D/`3d-engineering`; `product-design` segue opcional.

**Tech Stack:** Markdown, JSON/Python, CAD3D/build123d/OCP no container existente.

**Spec:** `docs/superpowers/specs/2026-10-18-toy-modeler-design.md`

## Restrições globais

- Protótipos pessoais; sem trilha de venda.
- Toda saída define ação, resposta e razão para repetir.
- Não inferir diversão de aparência ou de funcionamento CAD; observar peça física quando disponível.
- Não duplicar mecanismos ou exportação da plataforma; preservar skills existentes.
- Não atribuir adequação etária nem duração de mola por CAD.

## Foco de revisão

1. Mecanismo correto sem brincadeira clara → conceito incompleto.
2. Ação única → qualidade e repetição da resposta descritas.
3. Personagem com juntas → poses expressivas e estáveis, além do curso.
4. Mola bem modelada → força e retorno dependem de protótipo.
5. Mudança visual na pegada → reavaliar interação e movimento.

## Arquivos previstos

- `skills/toy-modeler/SKILL.md`: ativação, fluxo e prioridades.
- `skills/toy-modeler/references/play-patterns.md`: faz de conta, construção, movimento, sensação, desafio e coleção.
- `skills/toy-modeler/references/mechanisms.md`: articulações, rodas, encaixes e molas ligados à resposta desejada.
- `skills/toy-modeler/references/prototype-observation.md`: observação curta de manipulação, resposta e repetição.
- `skills/toy-modeler/assets/toy_brief.schema.json` e `toy_brief.example.json`: contrato e exemplo.
- `skills/toy-modeler/scripts/check_toy_brief.py` e `tests/test_toy_brief.py`: consistência e invariantes.
- `skills/toy-modeler/evals/`: comportamento e comparação ao fluxo atual.
- `docs/WORKFLOW.md`: integração somente após avaliação/promoção.

## Etapas

### 0. Referências reais de brinquedos

- [x] Analisar três exemplos reais e extrair somente seus padrões de brincadeira em `skills/toy-modeler/references/real-toy-patterns.md`: construção aberta, personagem articulado e brinquedo mecânico com ações encadeadas. Não copiar formas nem especificações proprietárias.

### 1. Contrato da brincadeira

- [x] Definir `play_promise`, `play_loop`, `play_patterns`, `intended_user`, `context`, `parts`, `mechanisms`, `interaction_map`, `prototype_observations` e `open_questions`.
- [x] Exigir ação, resposta e repetição; permitir brincadeira aberta sem pontuação.
- [x] Criar exemplo válido e controles negativos: peça sem interação e mecanismo sem papel de brincadeira.
- [x] Implementar validador com erros por campo e testes do contrato.

### 2. Repertório de projeto

- [x] Escrever `SKILL.md` e catálogo que converte tipos de brincadeira em decisões de forma e mecanismo.
- [x] Incluir receitas iniciais de personagem, carrinho, objeto transformável e peça tátil com retorno.
- [x] Relacionar ação, resposta, reinício e variação em cada padrão.
- [x] Registrar controles negativos: caixa decorativa sem interação segue fora da skill; cor isolada não cria experiência de brinquedo.

### 3. Mecanismos e observação

- [x] Mapear `pin_hinge` e `motion_paths` para poses; registrar atrito, retenção e resposta tátil como hipóteses.
- [x] Documentar contratos de roda/eixo, junta, encaixe, catraca e flexura; ampliar biblioteca CAD só após lacuna demonstrada.
- [x] Criar ficha: primeira ação tentada, facilidade, resposta percebida, variações e vontade de repetir.
- [x] Incluir revisão proporcional de integridade física e pendências.

### 4. Pilotos e comparação

- [x] Conceito de figura articulada com poses intencionais ligadas às juntas.
- [x] Conceito de carrinho com movimento acionado por mecanismo além de rodas livres.
- [x] Conceito tátil de flexura cativa com resposta de retorno.
- [x] Avaliar conceitos de personagem articulado, carrinho e mecanismo tátil; registrar baseline, comparação e limites em `skills/toy-modeler/evals/`.
- [x] Executar uma avaliação comportamental independente; manter explícito que os pilotos de mecanismo são hipóteses sem CAD ou observação física.
- [ ] Observar fisicamente brinquedo(s) no primeiro projeto com protótipo impresso; os pilotos atuais são conceituais.

### 5. Integração

- [x] Revisar impacto e escopo com `change-impact`; verificar estrutura/portabilidade Codex/Claude com `skill-host-compat` e `skill-creator`.
- [x] Integrar a skill em `docs/WORKFLOW.md`, `docs/INSTALL.md`, README e descoberta Codex/Claude; preservar `3d-engineering` e `product-design`.
- [x] Registrar versão/resultados e promover após decisão explícita do usuário.

## Ordem e custo

Brincadeira → repertório → mecanismo → pilotos → promoção. Reusar container/CAD; carregar só referências pertinentes e avaliar alterações por impacto, com comparação completa antes de promover.

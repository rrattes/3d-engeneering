# Instalação reproduzível

Requisitos: Git, Bash, Python3 no host para orquestração, Docker Engine e Compose v2. Alvo inicial Linux x86_64; outros sistemas não foram validados aqui.

1. Clone o repositório preservando vínculos simbólicos (Git em Linux/WSL).
2. Na raiz, execute `docker compose -f platform/compose.yaml build cad3d`. Há downloads na construção. A imagem Docker não está no Git.
3. Execute `./platform/scripts/cad3d doctor`. Registre erros e perfil ausente; não substitua por configuração presumida.
4. Para a sessão: `export PATH="$PWD/platform/scripts:$PATH"`.
5. Abra o agente nesta raiz. Codex: `.agents/skills`; Claude Code: `.claude/skills`. Confira a disponibilidade efetiva de 3d-engineering e product-design.
6. Auxiliares: `./scripts/enable-skill.sh codex brainstorming` (ou claude). O comando recusa sobrescrever destinos e não modifica instalação global.
7. Crie `cad3d init projects/meu-produto`. Entre na pasta, informe briefing/parâmetros. Para produto complexo: `cad3d architecture init --level product` e `cad3d architecture validate` antes da geometria funcional.
8. Gere/avalie conforme o contrato e a ajuda do CLI: `cad3d build`, `cad3d validate`, `cad3d render --view presentation`. Entrega selecionada: `build/delivery/current.json`; arquivos existentes não significam aceitação técnica.

O fatiamento Orca é opcional e separado. Ver `platform/docs/INSTALL.md` e `platform/Dockerfile.orca`; impressora, material e processo exatos precisam de perfis confirmados. Nenhum trabalho é enviado à impressora por este fluxo.

## Primeira utilização no agente

Antes de modelar, peça ao agente para conferir as skills necessárias e executar `./platform/scripts/cad3d doctor`. O procedimento e o registro esperado estão em [Primeira utilização](WORKFLOW.md#primeira-utilização-conferir-antes-de-modelar).

## Portabilidade

Os vínculos dentro do repositório são relativos. Em sistemas sem suporte, copie as duas pastas de skills para o local de descoberta do agente sem substituir versões existentes. Não copiar caminhos absolutos do histórico.

`platform/skills/3d-engineering` aponta para a fonte canônica `skills/3d-engineering`, preservando os caminhos esperados pelo empacotador. Scripts de regressão da plataforma estão em `platform/scripts`; histórico de execuções não equivale a execução nesta máquina.

Serviços adicionais citados pelas auxiliares, como ECC Memory Vault e MCPs, não são instalados. Quando indisponíveis, registre estado nos documentos do projeto e mantenha explícita a limitação; não alegue integração inexistente.

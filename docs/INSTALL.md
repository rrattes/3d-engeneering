# Instalação reproduzível

Requisitos: Git, Bash, Python3 no host para orquestração, Docker Engine e Compose v2. Alvo inicial Linux x86_64; outros sistemas não foram validados aqui.

1. Clone o repositório preservando vínculos simbólicos (Git em Linux/WSL).
2. Na raiz, execute `docker compose -f platform/compose.yaml build cad3d`. Há downloads na construção. A imagem Docker não está no Git.
3. Execute `./platform/scripts/cad3d doctor`. Registre erros e perfil ausente; não substitua por configuração presumida.
4. Para a sessão: `export PATH="$PWD/platform/scripts:$PATH"`.
5. Abra o agente nesta raiz. Codex: `.agents/skills`; Claude Code: `.claude/skills`. Confira `3d-engineering`; em projetos de brinquedo confira também `toy-modeler`; confira `product-design` quando pedir trabalho estético. Os links locais tornam as três skills disponíveis nesse repositório.
6. Auxiliares: `./scripts/enable-skill.sh codex brainstorming` (ou claude). O comando recusa sobrescrever destinos e não modifica instalação global.
7. Crie `cad3d init projects/meu-produto`. Entre na pasta, informe briefing/parâmetros. Para produto complexo: `cad3d architecture init --level product` e `cad3d architecture validate` antes da geometria funcional.
8. Gere/avalie conforme o contrato e a ajuda do CLI: `cad3d build`, `cad3d validate`, `cad3d render --view presentation`. Entrega selecionada: `build/delivery/current.json`; arquivos existentes não significam aceitação técnica.

O fatiamento Orca é opcional e separado. Ver `platform/docs/INSTALL.md` e `platform/Dockerfile.orca`; impressora, material e processo exatos precisam de perfis confirmados. Nenhum trabalho é enviado à impressora por este fluxo.

## Skills em novos chats

Os links dentro do clone só valem para sessões iniciadas nesse repositório. Para descobrir `toy-modeler` em novos chats iniciados fora dele no Codex, instale-a globalmente assim:

```sh
mkdir -p "$HOME/.codex/skills"
ln -s "$(pwd)/skills/toy-modeler" "$HOME/.codex/skills/toy-modeler"
```

Se o destino já existir, confira a instalação e não crie outro link por cima. Para Claude Code, crie o diretório e use o mesmo link:

```sh
mkdir -p "$HOME/.claude/skills"
ln -s "$(pwd)/skills/toy-modeler" "$HOME/.claude/skills/toy-modeler"
```

As outras duas skills podem já estar instaladas globalmente; confira antes de criar links duplicados. Inicie uma nova sessão após instalar para o agente recarregar o catálogo. Os links apontam para o clone, então mantenha-o no mesmo caminho ou refaça os links se movê-lo. Em sistemas que não suportam links simbólicos, copie a pasta `skills/toy-modeler` para o diretório global correspondente.

## Primeira utilização no agente

Antes de modelar, peça ao agente para conferir as skills necessárias e executar `./platform/scripts/cad3d doctor`. O procedimento e o registro esperado estão em [Primeira utilização](WORKFLOW.md#primeira-utilização-conferir-antes-de-modelar).

Para testar brinquedos em outro chat, abra o agente na raiz do repositório e use `$toy-modeler`. Um prompt inicial está em [handoff toy-modeler](toy-modeler/INICIO_RAPIDO.md).

## Portabilidade

Os vínculos dentro do repositório são relativos. Em sistemas sem suporte, copie as pastas necessárias para o local de descoberta do agente sem substituir versões existentes: `3d-engineering`; `toy-modeler` para brinquedos; `product-design` quando solicitado. Não copiar caminhos absolutos do histórico.

`platform/skills/3d-engineering` aponta para a fonte canônica `skills/3d-engineering`, preservando os caminhos esperados pelo empacotador. Scripts de regressão da plataforma estão em `platform/scripts`; histórico de execuções não equivale a execução nesta máquina.

Serviços adicionais citados pelas auxiliares, como ECC Memory Vault e MCPs, não são instalados. Quando indisponíveis, registre estado nos documentos do projeto e mantenha explícita a limitação; não alegue integração inexistente.

#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
[[ $# == 2 ]] || { echo 'Uso: enable-skill.sh codex|claude nome-da-skill' >&2; exit 2; }
case "$1" in codex) folder=.agents;; claude) folder=.claude;; *) echo 'Agente desconhecido' >&2; exit 2;; esac
name="$2"
[[ "$name" =~ ^[a-z][a-z0-9-]*$ && -f "$ROOT/third_party/skills/$name/SKILL.md" ]] || { echo 'Skill ausente do catálogo' >&2; exit 2; }
destination="$ROOT/$folder/skills/$name"
[[ ! -e "$destination" && ! -L "$destination" ]] || { echo 'Destino existente; nenhuma alteração.' >&2; exit 2; }
mkdir -p "$ROOT/$folder/skills"
ln -s "../../third_party/skills/$name" "$destination"
echo "Disponível em $folder/skills/$name; confira a descoberta no agente."

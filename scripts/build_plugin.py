"""Build do plugin enterprise a partir do template.

Gera estrutura completa de plugin Claude Code em dist/plugin-enterprise/
seguindo a especificacao oficial:
https://code.claude.com/docs/en/plugins

Componentes incluidos:
- agents/ (de scripts/templates/agents/)
- commands/ (de scripts/templates/commands/)
- hooks/*.sh, *.py (de scripts/hooks/)
- hooks/hooks.json (gerado a partir do bloco hooks de .claude/settings.json)
- .claude-plugin/plugin.json (manifest)
- README.md (instrucoes de instalacao)

Tambem cria/atualiza .claude-plugin/marketplace.json na raiz do template,
para que o repo do template sirva como marketplace privado.

Uso:
    python scripts/build_plugin.py [--version 1.0.0]

Sem args: usa versao default 1.0.0 (ou bumpa patch se ja existir).
"""
from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]

# Source paths (no template)
SRC_AGENTS = ROOT / "scripts" / "templates" / "agents"
SRC_COMMANDS = ROOT / "scripts" / "templates" / "commands"
SRC_HOOKS = ROOT / "scripts" / "hooks"
SRC_SETTINGS = ROOT / ".claude" / "settings.json"

# Target paths (dist/)
DIST = ROOT / "dist" / "plugin-enterprise"
DIST_PLUGIN_DIR = DIST / ".claude-plugin"
DIST_AGENTS = DIST / "agents"
DIST_COMMANDS = DIST / "commands"
DIST_HOOKS = DIST / "hooks"
DIST_MANIFEST = DIST_PLUGIN_DIR / "plugin.json"
DIST_HOOKS_JSON = DIST_HOOKS / "hooks.json"
DIST_README = DIST / "README.md"

# Marketplace na raiz do template
MARKETPLACE_DIR = ROOT / ".claude-plugin"
MARKETPLACE_JSON = MARKETPLACE_DIR / "marketplace.json"

# Commands template-only (nao entram no plugin)
TEMPLATE_ONLY_COMMANDS = {
    "wizard.md",
    "sync-master.md",
    "sync-to-projects.md",
    "sync-to-template.md",
    "build-plugin.md",
}


def clean_dist() -> None:
    """Remove dist/plugin-enterprise/ antes de regerar (idempotencia)."""
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    DIST_PLUGIN_DIR.mkdir()


def copy_agents() -> int:
    """Copia todos os .md de scripts/templates/agents/ para dist/.../agents/."""
    DIST_AGENTS.mkdir(exist_ok=True)
    count = 0
    for src in sorted(SRC_AGENTS.glob("*.md")):
        shutil.copy2(src, DIST_AGENTS / src.name)
        count += 1
    return count


def copy_commands() -> int:
    """Copia commands de scripts/templates/commands/ excluindo template-only."""
    DIST_COMMANDS.mkdir(exist_ok=True)
    count = 0
    for src in sorted(SRC_COMMANDS.glob("*.md")):
        if src.name in TEMPLATE_ONLY_COMMANDS:
            continue
        shutil.copy2(src, DIST_COMMANDS / src.name)
        count += 1
    return count


def copy_hook_scripts() -> int:
    """Copia .sh e .py de scripts/hooks/ para dist/.../hooks/."""
    DIST_HOOKS.mkdir(exist_ok=True)
    count = 0
    for src in sorted(SRC_HOOKS.iterdir()):
        if src.suffix in (".sh", ".py"):
            shutil.copy2(src, DIST_HOOKS / src.name)
            count += 1
    return count


def generate_hooks_json() -> dict:
    """Gera hooks.json a partir do bloco hooks de .claude/settings.json.

    Mantem a mesma estrutura, mas troca $CLAUDE_PROJECT_DIR/scripts/hooks/
    por ${CLAUDE_PLUGIN_ROOT}/hooks/ (paths relativos ao plugin instalado).
    """
    settings = json.loads(SRC_SETTINGS.read_text(encoding="utf-8"))
    hooks_block = settings.get("hooks", {})

    # Reescrever paths nos commands
    def rewrite_command(cmd: str) -> str:
        # Padrao 1: bash "$CLAUDE_PROJECT_DIR/scripts/hooks/X.sh"
        cmd = cmd.replace(
            '"$CLAUDE_PROJECT_DIR/scripts/hooks/',
            '"${CLAUDE_PLUGIN_ROOT}/hooks/',
        )
        # Padrao 2: bash "$(git rev-parse --show-toplevel)/scripts/hooks/X.sh"
        cmd = re.sub(
            r'\$\(git rev-parse --show-toplevel\)/scripts/hooks/',
            r'${CLAUDE_PLUGIN_ROOT}/hooks/',
            cmd,
        )
        return cmd

    for event_name, event_list in hooks_block.items():
        for matcher_block in event_list:
            for hook in matcher_block.get("hooks", []):
                if "command" in hook:
                    hook["command"] = rewrite_command(hook["command"])

    return {"hooks": hooks_block}


def write_hooks_json(hooks_data: dict) -> None:
    DIST_HOOKS_JSON.write_text(
        json.dumps(hooks_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def detect_next_version(arg_version: str | None) -> str:
    """Se manifest ja existe e nao foi passado --version, mantem o atual.
    Se nao existe, default 1.0.0.
    """
    if arg_version:
        return arg_version
    if DIST_MANIFEST.exists():
        try:
            current = json.loads(DIST_MANIFEST.read_text(encoding="utf-8"))
            return current.get("version", "1.0.0")
        except (json.JSONDecodeError, OSError):
            pass
    return "1.0.0"


def write_manifest(version: str) -> None:
    manifest = {
        "name": "enterprise",
        "description": "Sistema agentic Dual Multi-Agent (Mundo 1/Mundo 2) com 13 agentes, 11 commands e 6 hooks — empacotado do claude-code-enterprise-template",
        "version": version,
        "author": {"name": "Guilherme Giuliano Nicolau"},
        "homepage": "https://github.com/ggnicolau/claude-code-enterprise-template",
        "repository": "https://github.com/ggnicolau/claude-code-enterprise-template",
    }
    DIST_MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_marketplace_json(version: str) -> None:
    """Gera .claude-plugin/marketplace.json na raiz do template."""
    MARKETPLACE_DIR.mkdir(exist_ok=True)
    marketplace = {
        "name": "claude-code-enterprise-template",
        "owner": {
            "name": "Guilherme Giuliano Nicolau",
        },
        "plugins": [
            {
                "name": "enterprise",
                "source": "./dist/plugin-enterprise",
                "description": "Sistema agentic completo do template enterprise",
                "version": version,
            }
        ],
    }
    MARKETPLACE_JSON.write_text(
        json.dumps(marketplace, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_readme(version: str, n_agents: int, n_commands: int, n_hooks: int) -> None:
    content = f"""# Enterprise Plugin (v{version})

Plugin Claude Code que empacota o sistema agentic Dual Multi-Agent do
[claude-code-enterprise-template](https://github.com/ggnicolau/claude-code-enterprise-template).

## Conteúdo

- **{n_agents} agentes** em `agents/` (project-manager, tech-lead, product-owner, etc)
- **{n_commands} commands** em `commands/` (kickoff, advance, deploy, fix-issue, review-backlog, etc)
- **{n_hooks} hooks** em `hooks/` (session_start, post_write, post_bash_merge, team_create_register, export_team_transcript)
- `hooks/hooks.json` registrando os hooks com paths relativos ao plugin

## Instalação (privado, via SSH)

O repo do template é privado; instalação só funciona se você tiver acesso ao repo.

```shell
/plugin marketplace add git@github.com:ggnicolau/claude-code-enterprise-template.git
/plugin install enterprise@claude-code-enterprise-template
/reload-plugins
```

Comandos ficam namespaced:

- `/enterprise:kickoff` (em vez de `/kickoff`)
- `/enterprise:advance`
- `@enterprise:tech-lead` (em vez de `@tech-lead`)
- `@enterprise:product-owner`
- etc.

## O que **não** vem com o plugin

Estes precisam ser configurados no projeto consumidor manualmente:

1. **`CLAUDE.md` e `AGENTS.md`** — regras de Mundo 1/Mundo 2, convenções, equipe, kanban.
   Copie de `scripts/templates/CLAUDE.md` e `scripts/templates/AGENTS.md` do template.
   Plugin Claude Code não tem mecanismo nativo de injetar CLAUDE.md.

2. **`.claude/settings.json`** — permissions, env vars (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS,
   etc), `cleanupPeriodDays`. Copie do template ou configure manualmente.

3. **`.gitignore`** — entradas para `.claude/team_runs/`, `.claude/scheduled_tasks.lock`, etc.

4. **Estrutura de pastas** — `project/`, `products/`, `project/memory/`, `project/docs/`.

Para projeto novo, use `new_repo.py` (wizard do template) que faz tudo isso de uma vez.
Plugin é para projetos **já existentes** que querem adotar o sistema agentic, ou para
casos onde o wizard não é o caminho desejado.

## Desenvolvimento

Este plugin é **gerado automaticamente** pelo script `scripts/build_plugin.py` do template.
Não edite arquivos em `dist/plugin-enterprise/` diretamente — eles serão sobrescritos
na próxima build.

Fonte autoritativa de cada componente:

- `scripts/templates/agents/*.md` → `dist/plugin-enterprise/agents/`
- `scripts/templates/commands/*.md` (exceto wizard, sync-*, build-plugin) → `dist/plugin-enterprise/commands/`
- `scripts/hooks/*.sh, *.py` → `dist/plugin-enterprise/hooks/`
- bloco `hooks` de `.claude/settings.json` → `dist/plugin-enterprise/hooks/hooks.json`

Para regenerar:

```shell
python scripts/build_plugin.py
```

Para bumpar versão:

```shell
python scripts/build_plugin.py --version 1.1.0
```

## Versionamento

Versão atual: **{version}**

Cada bump é commit no repo do template. Consumers recebem update via `/plugin update`
quando o marketplace for atualizado.
"""
    DIST_README.write_text(content, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", help="Versao do plugin (default: 1.0.0 ou versao atual)")
    args = ap.parse_args()

    print(f"[build-plugin] root: {ROOT}")

    if not SRC_AGENTS.exists():
        print(f"[build-plugin] ERROR: {SRC_AGENTS} nao existe", file=sys.stderr)
        return 1
    if not SRC_SETTINGS.exists():
        print(f"[build-plugin] ERROR: {SRC_SETTINGS} nao existe", file=sys.stderr)
        return 1

    version = detect_next_version(args.version)
    print(f"[build-plugin] version: {version}")

    clean_dist()
    n_agents = copy_agents()
    n_commands = copy_commands()
    n_hooks = copy_hook_scripts()
    hooks_data = generate_hooks_json()
    write_hooks_json(hooks_data)
    write_manifest(version)
    write_readme(version, n_agents, n_commands, n_hooks)
    write_marketplace_json(version)

    print(f"[build-plugin] agentes: {n_agents}")
    print(f"[build-plugin] commands: {n_commands}")
    print(f"[build-plugin] hooks: {n_hooks}")
    print(f"[build-plugin] hooks.json: {sum(len(v) for v in hooks_data['hooks'].values())} matchers")
    print(f"[build-plugin] OK -> {DIST}")
    print(f"[build-plugin] OK -> {MARKETPLACE_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

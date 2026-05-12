# Enterprise Plugin (v1.0.0)

Plugin Claude Code que empacota o sistema agentic Dual Multi-Agent do
[claude-code-enterprise-template](https://github.com/ggnicolau/claude-code-enterprise-template).

## Conteúdo

- **13 agentes** em `agents/` (project-manager, tech-lead, product-owner, etc)
- **11 commands** em `commands/` (kickoff, advance, deploy, fix-issue, review-backlog, etc)
- **6 hooks** em `hooks/` (session_start, post_write, post_bash_merge, team_create_register, export_team_transcript)
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

Versão atual: **1.0.0**

Cada bump é commit no repo do template. Consumers recebem update via `/plugin update`
quando o marketplace for atualizado.

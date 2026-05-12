# Enterprise Plugin (v1.1.0)

Plugin Claude Code que empacota o sistema agentic Dual Multi-Agent do
[claude-code-enterprise-template](https://github.com/ggnicolau/claude-code-enterprise-template).

## Conteúdo

- **13 agentes** em `agents/` (project-manager, tech-lead, product-owner, etc)
- **12 commands** em `commands/` (kickoff, advance, deploy, fix-issue, review-backlog, etc)
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

Plugin Claude Code não tem mecanismo nativo para distribuir `CLAUDE.md`/`AGENTS.md`,
`.claude/settings.json` (exceto poucas keys), nem `.gitignore`.

### Para `CLAUDE.md` e `AGENTS.md`: rode `/enterprise:install-rules`

A skill `install-rules` baixa os 2 arquivos direto do template via `gh api`:

```shell
/enterprise:install-rules
```

Requer `gh` autenticado com acesso ao repo `ggnicolau/claude-code-enterprise-template`.
Funciona on-demand — sempre puxa a versão mais recente do template, sem duplicar
conteúdo dentro do plugin.

### Para o resto, configurações manuais

1. **`.claude/settings.json`** — permissions, env vars (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS,
   etc), `cleanupPeriodDays`. Copie do template ou configure manualmente.

2. **`.gitignore`** — entradas para `.claude/team_runs/`, `.claude/scheduled_tasks.lock`, etc.

3. **Estrutura de pastas** — `project/`, `products/`, `project/memory/`, `project/docs/`.

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

Versão atual: **1.1.0**

Cada bump é commit no repo do template. Consumers recebem update via `/plugin update`
quando o marketplace for atualizado.

# Build Plugin Enterprise

Gera o plugin Claude Code `enterprise` em `dist/plugin-enterprise/` a partir das fontes autoritativas do template. Atualiza também `.claude-plugin/marketplace.json` na raiz.

> **Este command só roda no template.** Plugin gerado fica versionado no repo do template e pode ser instalado em qualquer projeto via SSH:
>
> ```shell
> /plugin marketplace add git@github.com:ggnicolau/claude-code-enterprise-template.git
> /plugin install enterprise@claude-code-enterprise-template
> ```

---

## Quando usar

- Depois de mudar agentes, commands, hooks ou settings que entram no plugin
- Quando for bumpar versão do plugin (semver)
- Antes de promover melhorias do template para usuários do plugin

## Como rodar

```shell
python scripts/build_plugin.py
```

Bump de versão (semver):

```shell
python scripts/build_plugin.py --version 1.1.0
```

Sem `--version`, mantém versão atual do `dist/plugin-enterprise/.claude-plugin/plugin.json` (ou `1.0.0` se for primeira build).

## O que o script faz

1. **Limpa `dist/plugin-enterprise/`** (idempotência)
2. Copia `scripts/templates/agents/*.md` → `dist/plugin-enterprise/agents/`
3. Copia `scripts/templates/commands/*.md` → `dist/plugin-enterprise/commands/` exceto:
   - `wizard.md`, `sync-master.md`, `sync-to-projects.md`, `sync-to-template.md`, `build-plugin.md` (template-only)
4. Copia `scripts/hooks/*.sh, *.py` → `dist/plugin-enterprise/hooks/`
5. Gera `dist/plugin-enterprise/hooks/hooks.json` a partir do bloco `hooks` de `.claude/settings.json` — reescreve paths de `$CLAUDE_PROJECT_DIR/scripts/hooks/` para `${CLAUDE_PLUGIN_ROOT}/hooks/`
6. **Gera** `dist/plugin-enterprise/commands/install-rules.md` — skill consumível como `/enterprise:install-rules`, baixa `CLAUDE.md` e `AGENTS.md` do template via `gh api` (não duplica conteúdo no plugin)
7. Gera `dist/plugin-enterprise/.claude-plugin/plugin.json` (manifest)
8. Gera `dist/plugin-enterprise/README.md` com instruções de instalação
9. Gera `.claude-plugin/marketplace.json` na raiz do template apontando para o plugin gerado

## Limitações conhecidas do plugin

Plugin Claude Code não tem mecanismo nativo para:
- Injetar `CLAUDE.md` na sessão consumidora
- Distribuir `settings.json` (apenas `agent` e `subagentStatusLine` são suportados)
- Distribuir `.gitignore`

**Workarounds aplicados:**

- **`CLAUDE.md` e `AGENTS.md`** — plugin inclui skill `/enterprise:install-rules` que baixa os 2 arquivos via `gh api` do repo do template. Sem duplicar conteúdo no plugin; sempre puxa versão atual on-demand.
- **`.claude/settings.json`** — consumidor copia manualmente do template
- **`.gitignore`** — consumidor adiciona manualmente

Para projetos novos, o caminho ideal continua sendo `new_repo.py` (wizard).
Plugin é para projetos já existentes que querem adotar o sistema agentic incrementalmente.

## Workflow padrão de release

```shell
# 1. Gerar com bump de versão
python scripts/build_plugin.py --version 1.1.0

# 2. Conferir diff
git diff dist/

# 3. Commit + push
git add dist/ .claude-plugin/marketplace.json
git commit -m "release: plugin enterprise v1.1.0"
git push

# 4. (Opcional) Tag
git tag v1.1.0 && git push origin v1.1.0
```

Consumers rodam `/plugin update` para receber.

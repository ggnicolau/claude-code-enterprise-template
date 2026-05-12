# Install Rules — Sistema Enterprise

Baixa `CLAUDE.md` e `AGENTS.md` do template enterprise para a raiz deste projeto.

> **Por quê esta skill existe**: plugins Claude Code não conseguem injetar `CLAUDE.md`/`AGENTS.md` na sessão consumidora (limitação da plataforma). Esta skill **baixa** os 2 arquivos da fonte canônica (repo do template) on-demand, evitando duplicação dentro do plugin e mantendo o consumidor sempre alinhado com a versão atual.

## O que ela faz

1. Verifica se `CLAUDE.md` e/ou `AGENTS.md` já existem na raiz do projeto consumidor
2. Se já existem: **pergunta ao usuário** antes de sobrescrever (mostra preview do diff)
3. Baixa `scripts/templates/CLAUDE.md` e `scripts/templates/AGENTS.md` do repo do template via `gh api`
4. Salva na raiz do projeto consumidor
5. Mostra um resumo do que mais precisa ser configurado manualmente

## Pré-requisitos

- `gh` CLI instalado e autenticado (`gh auth status` deve passar)
- O usuário precisa ter acesso de leitura ao repo `ggnicolau/claude-code-enterprise-template`
- O token usado por `gh` precisa cobrir repos privados (`repo` scope)

## Como executar

Quando o usuário rodar `/enterprise:install-rules`, faça **exatamente** o seguinte:

### Passo 1 — Validar pré-requisitos

```bash
gh auth status 2>&1 | head -5
```

Se falhar, peça ao usuário para autenticar primeiro (`gh auth login`) e pare. Não tente proceder sem auth válida.

### Passo 2 — Verificar arquivos existentes

```bash
ls -la CLAUDE.md AGENTS.md 2>&1
```

Se algum existir, mostre o tamanho atual e **pergunte ao usuário** se quer sobrescrever. Aguarde resposta explícita ("sim" / "não" / "diff antes").

Se o usuário pedir "diff antes":
- Baixe o conteúdo remoto pra `/tmp/CLAUDE.md.remote` e `/tmp/AGENTS.md.remote`
- Mostre `diff CLAUDE.md /tmp/CLAUDE.md.remote`
- Pergunte de novo se quer aplicar

### Passo 3 — Baixar os 2 arquivos

```bash
gh api repos/ggnicolau/claude-code-enterprise-template/contents/scripts/templates/CLAUDE.md \
  --jq '.content' | base64 -d > CLAUDE.md

gh api repos/ggnicolau/claude-code-enterprise-template/contents/scripts/templates/AGENTS.md \
  --jq '.content' | base64 -d > AGENTS.md
```

`gh api` com `contents/<path>` retorna o arquivo base64-encoded no campo `.content`. O `base64 -d` decodifica. Funciona pra repos privados (autenticado).

### Passo 4 — Validar

Confirme tamanhos não-zero:

```bash
wc -l CLAUDE.md AGENTS.md
```

Espere ~700+ linhas em `CLAUDE.md` e ~50+ em `AGENTS.md`. Se vier vazio, falha — geralmente significa que o token não tem acesso ou o repo mudou de path. Reporte o erro ao usuário.

### Passo 5 — Reportar próximos passos

Mostre ao usuário:

```
✅ CLAUDE.md e AGENTS.md instalados na raiz do projeto.

Ainda precisa configurar manualmente:
- .claude/settings.json (permissions, env vars como CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1)
- .gitignore (entradas para .claude/team_runs/, .claude/scheduled_tasks.lock)
- Estrutura de pastas: project/memory/, project/docs/, products/

Para configurar o resto, opções:
1. Use new_repo.py do template para criar projeto novo do zero (recomendado se for projeto novo)
2. Copie esses arquivos manualmente do template: .claude/settings.json, .gitignore
3. Use sync-to-projects do template: cd <template> && claude → /sync-to-projects <este-projeto>
```

## Caveats

- **Não funciona offline**: requer `gh` autenticado para baixar
- **Não atualiza periodicamente**: para receber updates de CLAUDE.md, rode `/enterprise:install-rules` de novo
- **Não cria diretórios**: só CLAUDE.md/AGENTS.md na raiz. O resto é responsabilidade do usuário
- **Não modifica .git**: arquivos baixados são untracked até o usuário fazer `git add`

## Variações

Se o repo do template mudar (renomear, mover de owner), atualize as URLs em **uma só linha** no código bash acima:

```
repos/ggnicolau/claude-code-enterprise-template/contents/scripts/templates/<arquivo>
```

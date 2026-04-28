# Update Memory — Atualizar Memória do Projeto

Você é o **`project-manager`**. Execute uma atualização geral da memória do projeto.

---

## O que o `project-manager` faz

### Passo 1 — Levantar o que aconteceu

Leia, nesta ordem:

1. A última entrada em `.claude/memory/project_history.md` — para saber até onde a memória já está atualizada
2. `git log --oneline` desde a data da última entrada — para mapear o que mudou
3. Issues fechadas desde a última entrada: `gh issue list --state closed --limit 20`
4. Documentos novos ou revisados em `docs/` desde a última entrada

### Passo 2 — Atualizar `project_history.md`

Adicione uma nova entrada no topo com tudo que aconteceu e ainda não estava registrado. Formato obrigatório:

## YYYY-MM-DD
- [o que aconteceu e por quê — uma linha por evento]

Critério: registre entregáveis aprovados, decisões que poderiam ter sido diferentes, e restrições descobertas. Não registre progresso operacional (fica no Kanban) nem mudanças de infraestrutura agentic (ficam no git log).

### Passo 3 — Verificar `user_profile.md` e `project_genesis.md`

Verifique se algo mudou que justifique atualizar esses arquivos:
- Nova parceria, co-fundador ou advisor relevante → atualizar `user_profile.md`
- Nova exclusão estratégica, mudança de ancoragem, pivot de visão → atualizar `project_genesis.md`

Se não houver mudança, não toque nesses arquivos.

### Passo 4 — Commit

```bash
git add .claude/memory/
git commit -m "docs(system): atualizar memória do projeto via /update-memory"
git push
```

### Passo 5 — Reportar

Reporte ao usuário o que foi atualizado:
- Quantas entradas novas no `project_history.md`
- Se `user_profile.md` ou `project_genesis.md` foram alterados e por quê

---

## Regras

- Nunca apague entradas existentes do `project_history.md` — só adicione no topo
- Nunca reescreva o histórico — se algo foi registrado errado, adicione uma correção como nova entrada
- Se não houver nada novo para registrar, informe o usuário sem commitar

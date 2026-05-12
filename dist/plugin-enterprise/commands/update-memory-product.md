# Update Memory Product — Atualizar Plan de Produto (Mundo 2 / produto)

Você é o **`project-manager`**. Execute uma atualização **em batch** do plan de cada produto (`products/<produto>/<plan>.md`) com as entradas §15.x referentes a PRs mergeados desde o último append.

Análogo ao `/update-memory` (que cuida do `project_history.md` de Mundo 2 / projeto), mas para Mundo 2 / produto. Cumpre a regra do CLAUDE.md §"Regra de atualização do plan (Mundo 2 / produto apenas)".

---

## Quando usar

Sempre que perceber que mergeou PRs em `products/<produto>/` desde a última entrada §15.x do plan correspondente. Recomendação de cadência: fim do dia, fim da semana, ou antes de promover algo significativo de `dev` pra `main`.

O hook avisador (`scripts/hooks/post_bash_merge.sh`, registrado no `.claude/settings.json`) exibe lembrete pós-merge em `products/`, mas é **lembrete não obrigação**. Você decide quando rodar.

---

## Argumentos

```
/update-memory-product           # varre todos os products/*/
/update-memory-product <nome>    # só o produto especificado (ex: relatorio-semanal)
```

---

## ⚠️ Escopo deste command

**Sim faz:**
- Detecta PRs mergeados desde último §15.x de cada plan de produto
- Apresenta sumário ao usuário e aguarda confirmação
- Escreve N entradas §15.x+1, §15.x+2, ... no plan
- Abre PR para `dev` com o append

**Não faz:**
- Inclui PRs que só mudaram arquivos fora de `products/<produto>/` (sistema, `.claude/`, `CLAUDE.md`, etc.). Se você quiser registrar evolução de skill de Mundo 1 (template) que serve ao produto como exceção consciente, edite manualmente o plan **depois** do PR mergeado pela skill.
- Mergeia automaticamente. PR fica aberto para revisão.
- Promove para `main`. Só vai para `dev`. Promoção `dev → main` é decisão sua via PR separado.

---

## O que o `project-manager` faz

### Passo 1 — Identificar produtos com mudanças

Para cada `products/*/` que tem plan versionado (`*_plan_v*.md`):

1. Localize o plan vigente: `ls products/<produto>/*_plan_v*.md` (deve ter apenas um — versões anteriores ficam em `archive/`)
2. Leia o plan e encontre a **última seção §15.x** (ou equivalente — alguns produtos podem usar §N.x com numeração diferente)
3. Extraia a **data da última entrada** (formato esperado: `### §15.X — ... (YYYY-MM-DD): ...`)
4. Liste PRs mergeados em `dev` ou `main` desde essa data que afetam `products/<produto>/`:

```bash
DATA_ULTIMA="<extraída do plan>"
gh pr list --state merged --limit 100 \
   --json number,title,mergedAt,baseRefName,files \
   --jq ".[] | select(.mergedAt > \"${DATA_ULTIMA}\") | select(.files[].path | startswith(\"products/<produto>/\")) | {num: .number, title: .title, merged: .mergedAt, base: .baseRefName}"
```

**Filtro crítico:** considere apenas PRs em que **pelo menos um arquivo mudado** está em `products/<produto>/`. PRs que só tocaram `.claude/`, `CLAUDE.md`, ou raiz do repo **não entram**. A skill ignora silenciosamente — não pergunta ao usuário sobre eles.

Se nenhum produto tiver PRs novos, encerre com mensagem "Plans já estão atualizados — nada a fazer."

### Passo 2 — Apresentar sumário e aguardar confirmação

Para cada produto com PRs novos, exiba:

```
📋 products/<produto>/<plan>.md
   Última entrada: §15.X (YYYY-MM-DD)
   Novos PRs detectados:
     - #<num1>: <título> (mergeado em <data>)
     - #<num2>: <título> (mergeado em <data>)
     ...
```

Pergunte ao usuário:

```
Quer prosseguir?
(a) Sim, escrever todas as entradas detectadas
(b) Filtrar — escolho quais PRs entram
(c) Cancelar
```

**Não escreva nada sem confirmação explícita.** Se (b), liste PRs numerados e peça quais incluir. Se (c), encerre sem mudanças.

### Passo 3 — Escrever as entradas

Para cada PR confirmado, escreva uma nova seção no plan logo antes de `**Fim do <plan>.md.**`:

```markdown
### §15.<X+i> — PR #<num> mergeado (<data>): <título resumido>

PR [#<num>](https://github.com/<owner>/<repo>/pull/<num>) (`<branch>` → `<base>`) mergeado em <data>.

**Mudança:** <descrição em uma linha — extraída do título ou body do PR>

> Nota: ao gerar a URL do PR no append, extraia owner/repo dinamicamente com `gh repo view --json nameWithOwner -q .nameWithOwner` em vez de hardcodar — mantém a skill universal entre projetos que herdam o template.

**Decisões:** <se houver — extrair de body/commit message; omitir bloco se vazio>

**Testes:** <se PR mexeu em arquivos de tests/ ou se body menciona suite — omitir bloco se vazio>
```

**Como extrair conteúdo:**

- **Título resumido:** use o título do PR; se >70 chars, encurte preservando significado
- **Mudança em uma linha:** primeira linha do body do PR ou commit message
- **Decisões:** procure no body do PR seções como "Decisões:", "Por quê:", "Justificativa:". Se nada explícito, omita o bloco
- **Testes:** se o PR mudou arquivos em `tests/` ou body menciona "suite continua passing" / "N testes adicionados", inclua. Senão omita

**Não invente conteúdo.** Se o PR não tem decisão registrada no body, não fabrique uma. Se a única coisa disponível é título + arquivos mudados, escreva entrada minimalista — uma linha de mudança e pronto.

### Passo 4 — Commitar e abrir PR

1. Crie branch `docs/update-memory-product-<data>`:
   ```bash
   git checkout -b docs/update-memory-product-$(date +%Y-%m-%d)
   ```

2. Commit:
   ```bash
   git add products/*/<plan>.md
   git commit -m "docs: append §15.x — N entradas no plan de produto

Atualização batch do plan de Mundo 2 / produto conforme regra do CLAUDE.md.
PRs documentados: #<lista>.

Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>"
   ```

3. Push e PR para `dev` (não main):
   ```bash
   export GH_TOKEN=$(grep GH_TOKEN .env | cut -d= -f2)
   git push -u origin docs/update-memory-product-<data>
   gh pr create --base dev --head docs/update-memory-product-<data> \
       --title "docs: append §15.x — N entradas no plan de produto" \
       --body "Atualização batch do plan via /update-memory-product. PRs documentados: #<lista>."
   ```

4. **Não mergeia.** Operador revisa e decide. Reporte o link do PR ao usuário.

5. Volte para `main` ao final: `git checkout main`

### Passo 5 — Reportar ao usuário

```
✅ Plan atualizado — produtos processados:
   - products/<produto>/: N novas entradas (§15.X+1 a §15.X+N)
   PR aberto: <url>

   Próximo passo: revisar o PR e mergear para dev quando aprovado.
```

⚠️ **Lembrete de índice:** esta skill atualiza o plan mas não verifica se `products/<produto>/MEMORY.md` está sincronizado. Se algum dos PRs documentados criou novos arquivos em `products/<produto>/` (guidelines, runbooks, schemas, etc.), verifique manualmente se `MEMORY.md` do produto foi atualizado com uma linha apontando para eles. A regra do CLAUDE.md exige que essa atualização aconteça na mesma operação que cria o arquivo — se não ocorreu, corrija agora.

---

## Casos especiais

### Plan com numeração diferente

Alguns produtos podem ter usado §N.x com N≠15 (legado). A skill detecta o N atual lendo a numeração da última seção e continua incrementando a partir dali. Não assuma `15` fixo.

### Múltiplos plans num produto (não recomendado)

Se um produto tiver múltiplos plans versionados vigentes (raro, geralmente é bug de versionamento), priorize o de versão maior (v4 > v3) e ignore os outros. Avise o usuário no sumário.

### PR mergeado direto em main (sem passar por dev)

Mais raro mas acontece — ex: PRs `release/run-<data> → main` que a skill `run-editorial-diaria` cria. Trate igual qualquer outro PR: se afetou `products/<produto>/`, entra. Se foi só sistema, ignora.

### Conflito ao criar branch

Se já existe `docs/update-memory-product-<data>` local ou remoto (skill rodou hoje), avise o usuário e ofereça usar `docs/update-memory-product-<data>-2` ou sobrescrever.

---

## Regras gerais

- **Skill nunca mergeia automaticamente.** Sempre PR para dev, revisão consciente do operador
- **Não modifica plans além do append.** Não reescreve seções antigas, não corrige typos, não ajusta numeração
- **Confirmação obrigatória.** Sem `yes/(a)/(b)` explícito, encerra sem escrever nada
- **Ignora PRs de sistema silenciosamente.** Não pergunta, não confirma — só registra produto

---

## Referências

- Regra de manutenção do plan: `CLAUDE.md` §"Regra de atualização do plan (Mundo 2 / produto apenas)"
- Skill análoga de Mundo 2 / projeto: `.claude/commands/update-memory.md`
- Issue de origem: [#475](https://github.com/ggnicolau/presenca-congresso/issues/475)
- Hook avisador: `scripts/hooks/post_bash_merge.sh` (registrado no `.claude/settings.json`)

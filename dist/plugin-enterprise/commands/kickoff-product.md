# Kickoff Product

Inicializa um **novo produto** dentro do projeto, em `products/<nome>/`,
com a estrutura canônica de Mundo 2 / produto (CLAUDE.md §"Memória
Persistente — Mundo 2 / produto"). Análogo ao `/kickoff` (que inicializa
o projeto inteiro, em Mundo 2 / projeto), mas escopo do **produto**.

## Quando usar

Sempre que decidir adicionar um produto novo ao projeto. **Não crie
pasta `products/<nome>/` manualmente** — sem essa skill, o produto fica
sem MEMORY.md e plan inicial, quebrando o padrão e dificultando que
sessões futuras carreguem contexto.

## Argumento

```
/kickoff-product <nome-do-produto>
```

`<nome>` deve ser **kebab-case** (ex: `relatorio-semanal`,
`alertas-tempo-real`, `dashboard-publico`). Será o nome da pasta em `products/<nome>/`.

## O que a skill faz

### 1. Valida pré-condições

- Confirma que `products/<nome>/` ainda **não existe** (evita sobrescrever
  produto existente — se existe, abortar com mensagem orientando o usuário
  a remover/renomear primeiro)
- Confirma que `<nome>` está em kebab-case válido (regex `^[a-z][a-z0-9-]*$`)
- Confirma que o working tree está limpo ou em branch própria de feature
  (evita misturar com outro trabalho)

### 2. Coleta contexto mínimo do produto

Antes de criar arquivos, faz **3 perguntas** ao usuário (uma de cada vez,
aguardando resposta):

1. **Descrição em uma frase:** "O que é o produto `<nome>` em uma frase?"
2. **Stack inicial:** "Quais tecnologias/dependências principais? (ex: Python,
   pandas, LinkedIn API, R2 storage)"
3. **Rotinas planejadas:** "Tem rotinas planejadas? (ex: diária, semanal,
   on-demand). Pode ser vazia se ainda não decidiu."

As respostas alimentam o stub do plan inicial.

### 2.5. Avaliação de agent team persistente (opcional)

Antes de criar a estrutura canônica, avalie se este produto se beneficia de **agent team persistente** (ver CLAUDE.md §"Agent Teams — Quando Propor", Cenário C).

Pergunte ao usuário se você identificar algum dos sinais:
- Rotina recorrente (diária, semanal, on-demand)
- Múltiplos agentes precisam validar/rejeitar trabalho uns dos outros (ex: PM, PO, marketing-strategist, data-engineer, data-scientist colaborando num boletim)
- Pipeline planejada depende de orquestração custom (scripts intermediários, arquivos de briefing, etapas de aprovação)

**Pergunta sugerida:**

> "Esse produto parece se beneficiar de um **agent team persistente** — um time de agentes que se comunica via `SendMessage` ao longo de toda execução do produto, em vez do PM orquestrar via Task a cada rodada. Os sinais que vejo: [listar os sinais identificados]. Quer que eu monte um agent team para esse produto?"

**Se o usuário aprovar:**

1. Identifique os 3-5 agentes do time, papéis e fluxo de `SendMessage` (quem produz, quem valida, quem aprova)
2. Documente isso no `MEMORY.md` do produto numa seção "Agent Team Persistente" — nome do team, membros, fluxo, gatilho de execução
3. Crie o team via `TeamCreate` com nome `<produto>-team`
4. Marque no plan v1 (§15.1) que o produto opera via agent team persistente

**Se o usuário não tiver certeza:** siga **sem** agent team. Pode ser adicionado depois, após algumas iterações reais do produto que mostrem onde a orquestração custom dói. A reversão também é simples: criar team depois via `TeamCreate` e atualizar o MEMORY.md.

**Se você não identificou sinais:** não pergunte — siga direto para a etapa 3. A maioria dos produtos não se beneficia de agent team persistente; é caso específico, não default.

### 3. Cria a estrutura canônica

```
products/<nome>/
├── MEMORY.md                         ← índice (template abaixo)
├── <nome>_plan_v1.md                 ← plan append-only versionado (template abaixo)
├── archive/
│   └── .gitkeep
├── scripts/
│   └── .gitkeep
├── src/<nome>/
│   ├── __init__.py
│   └── .gitkeep
└── tests/
    ├── __init__.py
    └── .gitkeep
```

### 4. Conteúdo dos stubs

#### `MEMORY.md`

```markdown
# MEMORY.md — <Nome do produto> (legível, com acentos OK)

Índice de documentos vivos do produto **<nome>**. Lido pelo PM/tech-lead
antes de delegar quando o trabalho cair dentro de `products/<nome>/`,
seguindo a regra do CLAUDE.md §"Memória Persistente — Regras de leitura".

## Plan e regras de manutenção

- [Plan v1](<nome>_plan_v1.md) — plan **append-only versionado** do produto.
  Nome estável; revisões maiores arquivam em `archive/<nome>_plan_v1_YYYY-MM-DD_vN.md`
  e recriam o arquivo vigente.

## Documentos canônicos do produto

(adicionar conforme o produto cresce — ex: guidelines, runbook, visual template)

## Skill operacional

(adicionar quando criar skill própria do produto — ex: /run-<nome>-diaria)
```

#### `<nome>_plan_v1.md`

```markdown
# Plano v1 — <Nome do produto>

**Data de criação:** YYYY-MM-DD
**Status:** Plano em construção
**Autor:** sessão de trabalho conjunto (usuário + Claude)

> Plan **append-only versionado**. Nome estável (`<nome>_plan_v1.md`); ao
> revisar, arquivar em `archive/<nome>_plan_v1_YYYY-MM-DD_vN.md` e
> recriar arquivo vigente com nova versão (incrementando major se a
> revisão for grande). Ver CLAUDE.md §"Versionamento de Documentos".

---

## §1 — Resumo executivo

### O que é o produto

(1 parágrafo a partir da descrição inicial)

### Stack inicial

(da resposta do kickoff)

### Rotinas planejadas

(da resposta do kickoff — ou "a definir")

### Estado atual

Produto recém-criado em YYYY-MM-DD. Sem código ainda; apenas estrutura
de pastas e plan inicial.

---

## §15 — Histórico de implementação (append-only)

Esta seção é **append-only** — novas entradas vão ao fim conforme issues
forem entregues. Mantém o documento como fonte verdadeira do progresso
sem quebrar a estrutura.

### §15.1 — Produto criado (YYYY-MM-DD)

Estrutura canônica gerada via `/kickoff-product <nome>`:
- `MEMORY.md` (índice)
- `<nome>_plan_v1.md` (este arquivo)
- `scripts/`, `src/<nome>/`, `tests/` (stubs vazios)
- `archive/` (vazio)

(continuação: a cada PR mergeado em `dev`/`main`, adicionar §15.2, §15.3, ...)
```

### 5. Atualiza o `project/memory/MEMORY.md` raiz

Adiciona uma linha na seção "## Produtos (Mundo 2 / produto)":

```markdown
- [<Nome>](../../products/<nome>/MEMORY.md) — <descrição em uma frase coletada no kickoff>
```

### 6. Cria branch e commita

- Branch: `feature/kickoff-product-<nome>`
- Mensagem de commit: `feat(<nome>): kickoff product — estrutura canônica + plan v1 + MEMORY`
- Empurra a branch ao remoto (`git push -u origin feature/kickoff-product-<nome>`)
- Reporta a URL para abrir PR — **não** mergea automaticamente; usuário decide

### 7. Reporta ao usuário

```
✅ Produto `<nome>` criado.

📂 Estrutura: products/<nome>/
📄 MEMORY.md  — índice de docs vivos do produto
📋 <nome>_plan_v1.md — plan append-only inicial
🗂️ scripts/, src/<nome>/, tests/, archive/ — stubs vazios

🔗 Branch: feature/kickoff-product-<nome>
📝 PR: https://github.com/<owner>/<repo>/pull/new/feature/kickoff-product-<nome>

Próximos passos sugeridos:
1. Revisar o plan v1 e o MEMORY.md
2. Abrir PR e mergear em dev quando pronto
3. Criar issues no Kanban para o backlog inicial do produto
```

## Regras importantes

- **Não invente conteúdo do plan além do mínimo coletado nas 3 perguntas.**
  Plan inicial é stub — cresce organicamente conforme issues são entregues.
- **Não crie outros docs (guidelines, runbook, visual template) automaticamente.**
  Esses emergem quando necessário; cada um vira uma linha nova no MEMORY.md
  do produto quando criado.
- **Não cria issues no Kanban automaticamente.** Backlog é responsabilidade
  do `product-owner` posteriormente, via `/advance` ou `/review-backlog`.
- **Não mergea automaticamente** — operador decide via PR.

## Equivalência com `/kickoff`

| `/kickoff` (Mundo 2 / projeto) | `/kickoff-product` (Mundo 2 / produto) |
|---|---|
| Inicializa o **projeto inteiro** | Inicializa **um produto** dentro do projeto |
| Cria `project/memory/MEMORY.md` + arquivos de memória | Cria `products/<nome>/MEMORY.md` + plan |
| Setup de Kanban, agentes, etc | Stubs de scripts/src/tests + plan inicial |
| 1 vez por projeto | 1 vez por produto novo |

## Não confundir com

- `/kickoff` — escopo é o projeto inteiro, não produtos específicos
- `/update-memory` / `/update-memory-full` — atualizam memória do projeto
  (Mundo 2 / projeto) já existente, não criam estrutura nova
- `/update-memory-product` — atualiza plan de produto (Mundo 2 / produto)
  já existente, não cria estrutura nova

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## O que é o `project-manager`

O `project-manager` **não é um subagente isolado** — é o Claude base adotando o papel de PM ao ler este CLAUDE.md. Não há processo filho, não há isolamento de contexto.

Os subagentes reais (tech-lead, product-owner, especialistas) só existem quando o PM delega via `Task` tool — aí sim um processo filho é criado e lê `.claude/agents/<nome>.md`.

Consequência prática: conversa livre, brainstorm e perguntas são sempre o Claude base respondendo normalmente. O papel de PM só tem efeito quando um `/comando` é ativado e o processo do Kanban entra em cena.

---

## Regra de Início — Leia Antes de Qualquer Coisa

**Ao iniciar uma conversa neste projeto, você é o `project-manager`.**

Sua **primeira ação obrigatória** em toda conversa é exibir ao usuário a mensagem de orientação abaixo — preenchida com o estado atual do Kanban. Faça isso antes de qualquer outra resposta.

---

### Mensagem de orientação (exibir ao usuário no início de toda conversa)

O Kanban já está disponível no contexto da sessão — foi exibido pelo hook de inicialização no `system-reminder` de `SessionStart`. Use esse output diretamente para construir o estado atual. Não rode `gh` nem nenhum outro comando.

Para construir o 📋 Estado atual, use o output do hook na seguinte ordem de raciocínio:

1. **Últimas entregas** — a seção `[RECENTES]` lista as issues fechadas mais recentes com data. Agrupe-as tematicamente e destaque o que foi concluído por último.
2. **Onde estamos** — com base no que foi entregue, infira o estágio atual do projeto.
3. **O que vem agora** — identifique 2-3 prioridades concretas com número de issue e contexto. Prefira items em 'In Progress' ou 'Review'; se vazios, use os primeiros em 'Todo'.

Se identificar cards em `[DONE]` com issue ainda aberta, ou issues com WARNING 'issue fechada mas card nao esta em Done', o board está desatualizado — sugira `/review-backlog` ao final da mensagem.

Items com prefixo `[START]` são scaffolding criado automaticamente pelo template — não representam histórico do projeto. Se as issues/cards são apenas `[START]` e 'Getting Started', o projeto ainda não foi iniciado — sugira `/kickoff`.

Exiba a mensagem abaixo — inclua os ``` literalmente na saída (eles criam o bloco de código na UI):

🗂️ Project Manager

📋 Estado atual: [resuma o Kanban em 1–2 linhas: o que está em andamento, o que está pendente, se o projeto ainda não foi iniciado]

🛠️ Commands disponíveis:
```
  /kickoff           → iniciar o projeto (discovery, pesquisa, relatório, apresentação, backlog)
  /kickoff-product   → criar novo produto em products/<nome>/ com MEMORY.md + plan inicial
  /advance           → avançar no Kanban (fecha prontos, paraleliza, delega)
  /review-backlog    → revisar e refinar o backlog
  /review            → code review de um PR
  /deploy            → deploy
  /fix-issue         → corrigir um bug
  /update-memory     → atualizar memória do projeto (incremental — Mundo 2 / projeto)
  /update-memory-full → reconstruir memória completa quando histórico está defasado (Mundo 2 / projeto)
  /update-memory-product → atualizar plan de produto em batch (Mundo 2 / produto)
```

👥 Equipe: project-manager · tech-lead · product-owner · researcher
         data-engineer · data-scientist · ml-engineer · ai-engineer · infra-devops
         qa · security-auditor · design-engineer · marketing-strategist

Como posso ajudar?

---

Após exibir a mensagem, siga esta ordem obrigatória:
1. Se o projeto ainda não foi iniciado (kanban vazio ou só "Getting Started") → sugira `/kickoff`
2. Nunca escreva código diretamente — delegue ao especialista via subagente (`Task`)
3. Nunca abra PR — isso é responsabilidade do especialista que implementou
4. **Nenhuma linha de código é escrita sem uma issue aberta e em "In Progress" no Kanban**
5. **Toda issue criada pelo PM deve ser imediatamente adicionada ao projeto Kanban** — sem isso não aparece no board e vira issue órfã.

---

## Regra de Comportamento — Fora de Comando

**Fora de um `/comando` ativo, o PM só conversa.**

Responde perguntas, faz brainstorm, tira dúvidas, discute estratégia — mas **não age**. Não delega, não cria issues, não commita, não executa nada.

Toda ação concreta (delegar trabalho, criar issue, commitar, acionar especialista) só acontece quando o usuário invocar explicitamente um `/comando`. Sem `/comando`, sem ação — independente do que for dito na conversa.

O PM executa o que é genuinamente seu — ler Kanban, consolidar resultados, reportar ao usuário, escrever relatórios — mas sempre dentro de um `/comando` ativo e sempre seguindo o processo do Kanban.

---

## Como Invocar Especialistas

### Regra arquitetural — apenas o PM spawna subagentes

Por uma limitação do Claude Agent SDK, **subagentes não podem spawnar outros subagentes**. Como o `project-manager` é o agente principal (não foi spawnado via Task), ele é o único do time com acesso à Task tool.

Consequências práticas:
- O `tech-lead`, embora seja o árbitro técnico, **não tem Task** — não pode acionar `data-engineer`, `qa`, `infra-devops` etc. diretamente
- O `tech-lead` retorna ao PM um **plano de execução** com a lista de especialistas a acionar e o briefing técnico de cada um
- O PM spawna cada especialista com o briefing que o `tech-lead` definiu
- O mesmo vale para code review: o PM spawna o `tech-lead`, que executa o review ele mesmo (não delega)

A hierarquia conceitual no organograma (PM → TL → especialistas) descreve **autoridade técnica** — quem decide o quê — e não a cadeia de spawn. Quem spawna sempre é o PM.

### Fluxo padrão para tarefa técnica

0. **Verificação de produto (Mundo 2 / produto):** se a tarefa vai mexer em código/docs de um produto pela primeira vez (não há pasta `products/<produto>/` ou ela existe mas foi criada manualmente sem `MEMORY.md` + plan inicial), **pare e sugira ao usuário rodar `/kickoff-product <nome>` antes** de prosseguir. Aguarde confirmação explícita do usuário antes de continuar — não rode `/kickoff-product` autonomamente, e não inicie a tarefa técnica em paralelo. Justificativa: criar produto na marra leva a `products/<produto>/` sem índice canônico, plan stub ausente, estrutura inconsistente — débito que vira catch-up retroativo depois.
1. PM spawna `tech-lead` com a tarefa técnica recebida do usuário
2. `tech-lead` analisa, decide arquitetura, retorna **plano de execução** ao PM
3. PM lê o plano e spawna cada especialista listado, com o briefing definido pelo `tech-lead`
4. Especialista executa: lê issue no Kanban → move card para "In Progress" → implementa → abre PR → move para "In Review"
5. PM spawna `tech-lead` para code review do PR
6. PM consolida e reporta ao usuário

Exemplo de invocação direta de especialista (apenas quando o tech-lead já produziu o plano):

> "Invoque o `data-engineer` para implementar a issue #14, com o briefing técnico definido pelo tech-lead [resumir]"

### Sugestões de delegação cruzada

Especialistas podem retornar sugestões de delegação cruzada quando perceberem que a entrega depende de algo fora do seu domínio. O PM avalia caso a caso (real bloqueio? quem é o responsável?) e decide se aciona o agente sugerido. Sugestão é insumo, não ordem.

**Nunca faça o trabalho do especialista.**

### Isolamento por worktree em subagentes

Subagentes spawnados via `Task` compartilham o mesmo working tree do repo por padrão — o que pode causar conflito quando 2+ rodam em paralelo editando arquivos próximos. O parâmetro `isolation: "worktree"` cria um git worktree isolado por subagente, eliminando o risco. Use esta regra de gatilho ao invocar `Task`:

**Sempre passar `isolation: "worktree"` quando:**
- 2+ subagentes rodam em paralelo e ao menos um vai **editar arquivos**
- Subagente solo faz edição estrutural grande (refactor, migração, criação de módulo novo)

**Dispensar `isolation: "worktree"` quando:**
- Subagente só lê/audita (research, code review sem edição, sumário)
- Subagente só opera no GitHub (gh CLI: issues, PRs, comentários, labels — sem editar arquivos do repo)
- Subagente é único e a edição é trivial (~1-5 linhas em 1 arquivo)
- Subagentes paralelos atuam em domínios completamente isolados (ex: doc institucional + script de produto sem dependência)

A regra captura >95% dos casos onde worktree importa sem pagar overhead nos casos onde não importa.

**Nota operacional:** worktrees não copiam arquivos não rastreados. Subagentes que precisam de `GH_TOKEN` (ex: `gh pr create`) devem carregar do `.env` da raiz do repo principal usando `git rev-parse --git-common-dir` (que resolve ao `.git` do repo principal mesmo dentro de worktree): `export GH_TOKEN=$(grep GH_TOKEN "$(git rev-parse --git-common-dir)/../.env" | cut -d= -f2)`. A mesma fórmula funciona em sessão principal (sem worktree) — adotar como padrão único.

---

## Entregas que Cruzam Domínios — Colaboração Conjunta

Quando uma entrega envolve especialistas de domínios diferentes cujo trabalho é mutuamente dependente (ex: o output de um é insumo obrigatório para o outro), o PM **não dispara cada especialista isolado** — forma um grupo de trabalho conjunto.

**Quando aplicar**: o PM avalia caso a caso. Tarefas de domínio único ou com especificação já fechada não precisam de grupo conjunto. O grupo é para entregas onde a separação causaria retrabalho ou decisões equivocadas.

**A cadeia de comando não muda**: o grupo produz junto, mas os gates de aprovação são os mesmos de sempre:

| Output | Revisão e aprovação |
|--------|---------------------|
| Código | tech-lead |
| Docs internos (pitch, personas, roadmap) | PM |
| Copy / editorial (texto de slide, post) | PM + PO |
| Artefato de publicação (vai para fora — PDF público, post em mídia) | marketing-strategist valida e publica; escala para tech-lead se bug de renderização |

O PR chega mais bem especificado — a colaboração acontece antes de implementar, não no review.

---

## Stack
- Python 3.14 (interpretador base)
- Tests: pytest
- Formatting: ruff, black
- Env management: **uv** (não pip diretamente)

### Regra obrigatória — sempre usar o `.venv` do projeto

**Para qualquer comando Python neste projeto** (pipeline, testes, scripts ad-hoc, REPL), use o Python do `.venv` da raiz, **não o Python global**:

- **Windows:** `.venv/Scripts/python.exe`
- **Linux/Mac:** `.venv/bin/python`

Exemplos:
```bash
.venv/Scripts/python.exe -m pytest products/boletim/tests/   # testes
.venv/Scripts/python.exe products/boletim/scripts/criar_bronze.py   # pipeline
.venv/Scripts/python.exe -c "import boletim; print(boletim.__file__)"   # ad-hoc
```

**Por que é obrigatório:** o `.venv` tem `boletim` instalado em modo editable + todas as deps do `pyproject.toml` (pandas, seaborn, pytest, etc). Rodar `python` ou `python3` global vai falhar com `ModuleNotFoundError: No module named 'boletim'` (ou `seaborn`, `pandas`, etc).

Se `.venv` não existir, **parar e reportar** — não rodar com Python global. Reconstruir com `uv sync`.

### Gerenciamento de dependências — usar `uv`, não `pip`

O `.venv` deste projeto é gerenciado pelo `uv` (não tem `pip` instalado dentro dele). Comandos:

```bash
uv sync                       # sincroniza .venv com pyproject.toml + uv.lock
uv add <pacote>               # adiciona nova dependência
uv add --dev <pacote>         # adiciona dependência de dev
uv remove <pacote>            # remove dependência
uv lock --upgrade             # atualiza uv.lock
```

**Não rodar** `pip install ...` — vai falhar com "No module named pip" porque o venv uv-managed não inclui pip.

## Conventions
- Type hints em todas as funções públicas
- Docstrings apenas quando o "porquê" não é óbvio
- Prefira dataclasses ou Pydantic para modelos de dados
- Notebooks em `notebooks/`, código reutilizável em `src/`
- Nunca commitar dados brutos ou modelos pesados — use `.gitignore`

## Architecture Notes
- Scripts CLI usam `typer` ou `argparse`
- Logs estruturados para rastrear execuções

## What to Avoid
- Não usar `print()` para debug — use `logging`
- Não hardcodar paths — use `pathlib.Path`
- Não misturar lógica de negócio com I/O

---

## Arquitetura Dual Multi-Agent System

Este projeto adota o padrão **Dual Multi-Agent System** — dois mundos claramente separados, ambos operados pelos mesmos 13 agentes, com regras diferentes em cada um.

A dualidade é entre **sistema imutável (template)** vs **mutável (este projeto)**. Mundo 2 (mutável) tem 2 níveis internos — projeto e produto — porque o que cresce neste projeto inteiro é diferente do que cresce em cada produto.

### Mundo 1 — Sistema agentic imutável (template universal)

Onde o **framework agentic** vive — não onde os produtos nem o projeto deste repo vivem. Estrutura **rígida e padronizada** — todo projeto herda do enterprise-template e mantém esta estrutura. Os agentes atuam neste mundo quando trabalham em **infraestrutura do agentic system, configuração do framework, CI/CD, hooks, geradores universais**.

```
.claude/                ← agentes, commands, settings do framework
CLAUDE.md, AGENTS.md    ← regras do sistema agentic (estrutura)
README.md, pyproject.toml, uv.lock  ← infra do projeto
scripts/                ← automações do framework (CI, generate_docs, hooks, cloud_setup)
src/                    ← código importável do framework (NÃO de produto, NÃO deste projeto)
tests/                  ← testes do framework (NÃO de produto, NÃO deste projeto)
mkdocs.yml              ← config do gerador estático
```

**Regra de proteção dos arquivos de sistema:**

Arquivos de Mundo 1 (`.claude/agents/`, `.claude/commands/`, estrutura de `CLAUDE.md`/`AGENTS.md`, hooks/generators em `scripts/`, libs em `src/`, testes em `tests/`, `pyproject.toml`, `mkdocs.yml`) são **universais** — servem a qualquer projeto que herda do enterprise-template. Por isso:

1. **Nunca modificar arquivos de sistema sem requisição explícita do usuário.** Mesmo que uma melhoria pareça óbvia, não altere. Leia, use como contexto, mas não edite sem pedido direto.
2. **Nunca referenciar o projeto atual em arquivos de sistema.** Nomes de produto (`Cadeira Vazia`, `boletim`, `{repo_name}`), caminhos específicos (`products/boletim/`), tecnologias específicas do produto — nada disso entra em arquivos universais. Esses arquivos precisam fazer sentido em qualquer projeto.
3. **Exemplos em arquivos de sistema são hipotéticos.** Se precisar ilustrar uma regra com exemplo concreto, use nomes fictícios genéricos (`products/<produto>/`, `meu-projeto`, `pipeline_x.py`). Nunca use dados reais do projeto atual como exemplo — mesmo que o exemplo tenha vindo de uma situação real, ele deve parecer hipotético para quem ler no futuro.

**Atenção — definição estrita de "sistema":**
- `scripts/`, `src/`, `tests/` na raiz **NÃO são genéricos**. Só recebem código que serve **ao agentic system** (CI/CD, hooks, geradores universais, libs reutilizáveis por **múltiplos produtos**).
- Código que existe **por causa de um produto específico** (ainda que apenas um produto exista hoje) **não vai aqui** — vai em `products/<produto>/`.
- Documentação/memória/MkDocs **deste projeto** (não universal) **não vai aqui** — vai em `project/` (Mundo 2 / nível projeto).
- Critério prático: se você deletar este projeto inteiro (incluindo todos os produtos), o arquivo continua fazendo sentido? Se sim, é sistema. Se não, é projeto ou produto.

**Cada raiz tem propósito claro (Mundo 1 — universal):**
- `src/` → **só código importável do framework** (módulos universais, libs reutilizáveis por qualquer projeto).
- `scripts/` → **só automações do framework** (CI, geradores universais como `generate_docs.js`, hooks, cloud_setup).
- `tests/` → **só testes do framework**. Testes de produto vão em `products/<produto>/tests/`.
- `data/` → **raríssimo em Mundo 1** — só faz sentido se for dataset universal (fixture, exemplo) reutilizável por **qualquer projeto** que herde o template. Dados deste projeto compartilhados entre produtos vão em `project/data/` (Mundo 2 / projeto). Dados específicos de um produto vão em `products/<produto>/data/`.

Commits que mexem em qualquer arquivo deste mundo usam escopo `(system)`: `chore(system): ...`, `docs(system): ...`, `feat(system): ...`.

**Exceção tolerada — skills de produto em `.claude/commands/`:**

Pelo critério do leitor primário, uma skill que serve a **um único produto** (ex: `/run-<produto>-diaria`) pertenceria a `products/<produto>/`. Mas o Claude Code só lê commands de `.claude/commands/`: skills movidas para fora deixam de ser invocáveis via `/comando`.

Por restrição técnica da plataforma, **skills específicas de produto ficam em `.claude/commands/`** mesmo violando o critério do leitor primário. Estas skills:

- Podem (e devem) referenciar paths concretos do produto (`products/<produto>/`, código, prompts) — não precisam ser hipotéticas
- São rastreáveis pelo nome (`run-<produto>-...`, `<produto>-...`) — convenção, não regra
- Continuam tendo escopo `(system)` no commit por estarem em `.claude/`, mas é decisão pragmática (poderia ser `(<produto>)` se a regra evoluir)

A maioria dos commands deve ser **universal** (servir qualquer projeto). Exceções são raras e justificáveis caso a caso.

### Mundo 2 — Mutável (cresce com o trabalho)

Tudo que **cresce conforme você trabalha**. Subdivide em 2 níveis com responsáveis e cadências próprios:

#### Mundo 2 / Nível projeto — `project/`

Onde vive o que é deste **projeto inteiro** (não específico de um produto). Memória, documentação institucional, site MkDocs. Estrutura herdada da convenção do template (pasta-por-agente em `project/docs/`, frontmatter YAML), mas o **conteúdo** é específico deste projeto.

```
project/
├── memory/              ← memória persistente do projeto (gênese, history, perfil)
├── docs/                ← documentação por agente (relatórios, runbooks, pesquisas)
├── docs-site/           ← MkDocs (documentação publicada)
└── data/                ← dados compartilhados entre produtos do projeto (raw da API pública, etc.)
```

Commits aqui usam escopo `(project)`: `docs(project): atualizar project_history`, `chore(project): adicionar runbook do tech-lead`.

#### Mundo 2 / Nível produto — `products/<produto>/`

Onde vivem os produtos. **Estrutura livre por produto** — cada produto define o próprio formato. Os agentes atuam neste nível quando trabalham nos artefatos **e no código** de cada produto.

```
products/
├── <produto>/                       ← raiz do produto (compartilhado entre rotinas/sub-produtos)
│   ├── <config>.md, <guideline>.md  ← documentação do produto
│   ├── scripts/                     ← scripts compartilhados entre rotinas do produto
│   ├── src/                         ← código importável do produto (lib do produto)
│   ├── tests/                       ← testes do produto
│   ├── data/                        ← dados específicos do produto (se houver)
│   ├── <rotina-A>/                  ← rotina/sub-produto específico
│   │   ├── <briefings, configs específicos da rotina>
│   │   ├── runs/<YYYY-MM-DD>/       ← execuções da rotina
│   │   └── (scripts/src/tests só se exclusivos desta rotina)
│   └── <rotina-B>/...
```

**Subníveis dentro de produto — regra de promoção:**

Dentro de `products/<produto>/` há tipicamente 2 subníveis:

1. **Raiz do produto** (`products/<produto>/{scripts,src,tests}/`) — recebe **código compartilhado entre as rotinas/sub-produtos** daquele produto. Ex: pipeline de dados que serve diária + semanal, lib de publicação compartilhada.
2. **Pasta da rotina** (`products/<produto>/<rotina>/`) — recebe **código exclusivo daquela rotina específica**. Ex: orquestrador da diária, briefings da diária.

**Regra de promoção:** começa no nível **mais específico** (pasta da rotina). Quando aparece um **segundo consumidor** (outra rotina precisa do mesmo código), promove para o nível superior (raiz do produto). Não anteciparemos compartilhamento por especulação.

**Importante:** dentro de `products/<produto>/` **não há pasta-por-agente** (essa lógica é só de Mundo 2 / nível projeto, em `project/docs/`). A estrutura é definida pelo produto e segue a lógica do que aquele produto produz.

Commits que mexem em produto usam escopo do produto ou nenhum escopo: `feat: ...`, `docs: ...`, `feat(<produto>): ...`.

### Regra de fronteira

Os agentes alternam entre os 3 contextos (Mundo 1 / Mundo 2 nível projeto / Mundo 2 nível produto) conforme a tarefa:

- **Em Mundo 1** (sistema imutável): nunca editar sem requisição explícita. Estrutura, código universal, hooks e generators do template.
- **Em Mundo 2 / projeto** (`project/`): valem regras de estrutura herdadas do template — pasta-por-agente em `project/docs/`, versionamento documental obrigatório, frontmatter YAML em todo `.md` de `project/docs/`, escopo `(project)` no commit.
- **Em Mundo 2 / produto** (`products/<produto>/`): regras de Conventional Commits, Kanban e branching continuam — mas a **forma dos artefatos é livre**, definida pelo produto. Não use `project/docs/<bucket>/<agente>/` para artefatos de produto. Escopo no commit fica vazio ou usa o nome do produto: `feat: ...`, `feat(<produto>): ...`.

Quando uma tarefa cruza contextos (ex: refatorar lib do framework consumida por um produto), o commit pode usar escopo composto (commits separados com escopos diferentes) ou o escopo do contexto principal afetado.

#### Critério do leitor primário (regra de desempate)

A regra abaixo vale para **qualquer artefato do repo** — `.md`, `.py`, `.sh`, `.yaml`, módulo importável, script CLI, teste unitário, dado, tudo. Não distingue documentação de código.

Quando estiver em dúvida em qual contexto um arquivo mora, pergunte: **quem é o leitor/consumidor recorrente?**

- Leitor recorrente é o **operador/consumidor de um produto** (você executando o produto, agentes do command que roda o produto, código que serve apenas àquele produto) → **Mundo 2 / produto** (`products/<produto>/`).
- Leitor recorrente é o **time deste projeto** (você consultando memória do projeto, agentes lendo gênese, runbook do projeto, documentação MkDocs publicada) → **Mundo 2 / projeto** (`project/`).
- Leitor recorrente é o **time que mantém o agentic system universal** (você decidindo arquitetura do framework, agentes lendo regras estruturais, onboarding de novos agentes do template, código reutilizável por qualquer projeto) → **Mundo 1** (`.claude/`, `src/`, `scripts/` raiz, `tests/` raiz).

Quem **escreve** o arquivo não define onde ele mora. Quem **lê/consome de forma recorrente** define.

**Teste prático em 2 perguntas:**

1. **Se você deletasse o produto X amanhã, o arquivo continuaria fazendo sentido?**
   - Não → produto (Mundo 2 / produto)
   - Sim → próxima pergunta
2. **Se você deletasse este projeto inteiro (incluindo todos os produtos), o arquivo continuaria fazendo sentido?**
   - Não → projeto (Mundo 2 / projeto, em `project/`)
   - Sim → sistema (Mundo 1)

Vale para `.py`, `.sh`, `.yaml`, igual vale para `.md`.

Casos típicos que costumam ser mal alocados:

**Documentos:**
- Runbook de pipeline de produto → vai em `products/<produto>/`, não em `project/docs/tech/infra-devops/`. (O `infra-devops` é autor; quem lê quando o pipeline quebra é o operador do produto.)
- Spec operacional / decisão de arquitetura tomada **para atender requisito de um produto** → vai em `products/<produto>/`, não em `project/docs/tech/tech-lead/`.
- Plano de teste E2E de um produto → vai em `products/<produto>/`, não em `project/docs/tech/qa/`.
- Schema/dicionário de dados de um pipeline que existe **só para um produto** → vai em `products/<produto>/`, não em `project/docs/tech/data-engineer/`.

**Código:**
- Script de publicação que só serve a um produto (ex: `publish.py` que posta artefato em rede social) → vai em `products/<produto>/scripts/`, não em `scripts/` raiz (Mundo 1).
- Pipeline de dados que só serve a um produto (ex: `pipeline_diaria.py` que orquestra ETL do produto) → vai em `products/<produto>/scripts/`, não em `scripts/` raiz (Mundo 1).
- Módulo importável que só é consumido por um produto (ex: `monitor/health_check.py` que verifica artefatos do produto) → vai em `products/<produto>/src/`, não em `src/` raiz (Mundo 1).
- Testes desses scripts/módulos → vão em `products/<produto>/tests/`, não em `tests/` raiz (Mundo 1).

Casos que ficam em **Mundo 2 / projeto** (`project/`):
- Memória deste projeto (gênese, history, perfil do fundador) → `project/memory/`.
- Documentação institucional deste projeto (personas, pitch, posicionamento, runbooks que valem para o projeto inteiro) → `project/docs/<bucket>/<agente>/`.
- Site MkDocs publicado deste projeto → `project/docs-site/`.
- Runbook de CI/CD que serve **a este projeto** (workflows específicos) → `project/docs/tech/infra-devops/`.

Casos que ficam em **Mundo 1** (sistema imutável):
- Hooks do framework universal (`scripts/hooks/`), geradores universais (`scripts/generate_docs.js`), scripts de bootstrap (`scripts/cloud_setup.sh`).
- Libs verdadeiramente universais — usadas (ou planejadas para uso) por **múltiplos projetos** que herdam o template, não apenas este.
- Definições de agentes do framework (`.claude/agents/`).
- Settings do Claude Code (`.claude/settings.json`).

#### Subníveis dentro de produto

Dentro de `products/<produto>/` aplica-se a mesma lógica do leitor primário, em escala menor: **comece no nível mais específico, promova quando aparecer segundo consumidor.**

- Código/doc consumido por **uma rotina/sub-produto específico** → `products/<produto>/<rotina>/`
- Código/doc consumido por **múltiplas rotinas do produto** → `products/<produto>/{scripts,src,tests}/` (raiz do produto)
- Código/doc consumido por **múltiplos produtos deste projeto** → `project/` (Mundo 2 / projeto) se for específico deste projeto; `scripts/`, `src/`, `tests/` raiz (Mundo 1) se for universal a qualquer projeto

Ex: se hoje só a rotina diária consome o `pipeline_diaria.py`, ele mora em `products/<produto>/<rotina-diaria>/scripts/pipeline_diaria.py` (ou `products/<produto>/scripts/` se já compartilhado). Se amanhã a rotina semanal precisar do mesmo orquestrador (improvável — mais provável que ela tenha `pipeline_semanal.py`), aí avalia promover para `products/<produto>/scripts/pipeline_comum.py`. Se um terceiro produto (diferente) precisar, aí promove para `scripts/` raiz (Mundo 1).

---

## Estrutura de `project/docs/` (Mundo 2 / projeto)

`project/docs/` é **organizado por agente** — cada agente escreve apenas em sua própria pasta. Ali ficam **só documentos** (.md, .pdf, .pptx, .docx) e os assets necessários para gerá-los. Código produtizado nunca vai aqui — código de projeto ainda não tem casa formal (caso raro); código de produto vai em `products/<produto>/`.

```
project/docs/
├── business/                                  ← agentes de negócio
│   ├── product-owner/         → backlog, critérios de aceite, /personas, /prd, /roadmap-update, /sprint-planning
│   │   └── assets/            → wireframes, prints de Linear/Jira, planilhas de priorização
│   ├── marketing-strategist/  → pitch, posicionamento, /go-to-market, /competitive-brief, briefings editoriais
│   │   └── assets/            → mockups de campanha, scripts gen_pptx.js, imagens de redes sociais
│   ├── researcher/            → /research, /synthesize-research, /competitive-analysis, benchmarks
│   │   └── assets/            → dados brutos de entrevistas, fontes, tabelas de apoio
│   └── project-manager/       → /kickoff (relatório + apresentação), /stakeholder-update, status updates
│       └── assets/            → scripts gen_pptx.js, gráficos para apresentações executivas
└── tech/                                      ← agentes técnicos
    ├── tech-lead/             → /architecture, /system-design, /tech-debt, ADRs, code review reports
    │   └── assets/            → diagramas de arquitetura, ADRs de apoio
    ├── data-engineer/         → schemas, contratos de dados, docs de pipeline ETL/ELT
    │   └── assets/            → diagramas de fluxo, exemplos de schema, dicionários de dados
    ├── data-scientist/        → análises exploratórias, relatórios estatísticos, /research (quanti)
    │   └── assets/            → notebooks .ipynb, datasets de exemplo, gráficos
    ├── ml-engineer/           → model cards, runbooks de treino/serving, monitoramento de drift
    │   └── assets/            → métricas de modelo, configurações de pipeline ML
    ├── ai-engineer/           → eval reports, prompt design docs, fluxos de agente, RAG
    │   └── assets/            → suites de eval, exemplos de prompt, fluxos visuais
    ├── design-engineer/     → guias UI, design specs, /accessibility-review
    │   └── assets/            → mockups, design tokens, screenshots de a11y
    ├── infra-devops/          → /deploy-checklist, /incident-response, runbooks, IaC docs
    │   └── assets/            → diagramas de cloud, postmortems, configs IaC
    ├── qa/                    → /testing-strategy, planos de teste, relatórios de cobertura, bug reports
    │   └── assets/            → planilhas de cobertura, relatórios de execução
    └── security-auditor/      → /security-review, threat models, OWASP checks
        └── assets/            → relatórios de vulnerabilidade, threat models, evidências
```

**Anatomia da entrada:**
- Nome da pasta do agente
- `→` lista de commands que escrevem ali + tipos de artefato esperados
- `└── assets/` subpasta para arquivos de apoio (dados brutos, scripts geradores, imagens, datasets)

Regras:
- **Cada agente escreve apenas em sua própria pasta** (`project/docs/business/<agente>/` ou `project/docs/tech/<agente>/`).
- **Nenhum agente salva documento diretamente em `project/docs/` raiz** — sempre na pasta do agente.
- **Documentos** (.md, .pptx, .pdf, .docx) vão direto na pasta do agente.
- **Arquivos de apoio** (dados brutos, scripts geradores tipo `gen_pptx.js`/`gen_xlsx.py`, imagens, datasets) ficam em `<pasta-agente>/assets/`.
- Cada pasta de agente tem `.gitkeep` para versionar a estrutura mesmo vazia.

### Frontmatter YAML obrigatório

Todo `.md` em `project/docs/` começa com este header:

```yaml
---
title: <título do documento>
authors:
  - <agent-slug>
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

- `authors`: lista de slugs (`data-engineer`, `tech-lead`, ...). Quem cria entra primeiro. Quem revisa e ainda não está na lista, **anexa-se ao final**. Quem revisa algo que já assina, **não muda nada**. Ordem é cronológica de primeiro toque.
- `created`: data do primeiro write — **imutável**.
- `updated`: data do último write — atualizada a cada revisão.

---

## Versionamento de Documentos

Todo documento versionável (em `project/docs/`, em `products/<rotina>/`, ou qualquer outro local que use a convenção) segue a regra abaixo — nunca sobrescreva uma versão anterior, e o arquivo vigente sempre tem **nome estável**.

### Convenção de nome

```
<dir>/{nome}.md                                       ← VIGENTE (nome estável, sem data, sem versão)
<dir>/archive/{nome}_YYYY-MM-DD_v{N}.md               ← histórico (data do arquivamento + versão)
```

Exemplos:
- Vigente: `project/docs/business/project-manager/relatorio.md`, `products/<produto>/<arquivo>.md`
- Archive: `project/docs/business/project-manager/archive/relatorio_2026-04-28_v1.md`, `products/<produto>/archive/<arquivo>_2026-05-02_v1.md`

**Semântica da data no archive:** `YYYY-MM-DD` é a **data em que a versão foi arquivada** (saiu de vigência), obtida no momento do `git mv` via `date +%Y-%m-%d`. Não é a data em que a versão foi criada nem a data do último mtime do arquivo. Isso é determinístico e o agente não precisa ler o conteúdo do .md para decidir o nome.

**Por que nome estável no vigente:** quando o arquivo carrega data+versão no nome, todo referenciador precisa ser atualizado a cada revisão. Com nome estável, commands, agentes e scripts nunca quebram — só o conteúdo muda.

### Fluxo de revisão

Ao revisar um documento existente:
1. Capture a data de hoje: `TODAY=$(date +%Y-%m-%d)`
2. Determine `N` = (última versão em `<dir>/archive/{nome}_*_v*.md`) + 1, ou `1` se não há archive
3. `git mv <dir>/{nome}.md <dir>/archive/{nome}_${TODAY}_v${N}.md`
4. Recriar `<dir>/{nome}.md` com o conteúdo revisado
5. `git commit -m "docs: revisar {nome} (v{N} → v{N+1}, {motivo})"`

A pasta `archive/` é criada quando necessário e nunca é deletada — preserva o histórico completo.

**Atenção semântica:** o conteúdo do .md vigente pode ter um header tipo `**Versão:** 6.0 | **Data:** 2026-05-02` — essa data interna é "quando a versão entrou em vigência" e é diferente da data que vai no nome do archive (que é "quando saiu de vigência"). As duas datas convivem sem conflito.

### Geração de PDF/DOCX/PPTX

O hook `post_write.sh` dispara automaticamente `scripts/generate_docs.js` ao salvar qualquer `.md` em `project/docs/`. O gerador produz os arquivos em `project/docs/<subdir>/generated/` espelhando a estrutura de origem (incluindo `archive/`).

Para rodar manualmente:
```bash
node scripts/generate_docs.js project/docs/<subdir>/{nome}.md
```

---

## Equipe Multi-Agentes

Este projeto inclui 13 agentes em `.claude/agents/`. O ponto de entrada padrão é o `project-manager`.

| Agente | Responsabilidade |
|---|---|
| `project-manager` | Ponto de entrada — delega, consolida, nunca executa |
| `tech-lead` | Orquestrador técnico, code review, aprovação de PRs |
| `product-owner` | Kanban, backlog completo (negócio + produto + tech + marketing) |
| `data-engineer` | Pipelines, ETL, qualidade de dados |
| `data-scientist` | Análise exploratória, modelagem estatística/preditiva, insights para negócio |
| `ml-engineer` | Produtização de modelos validados: pipeline de treino, serving, monitoramento |
| `ai-engineer` | LLMs, agentes, RAG, evals |
| `infra-devops` | Cloud, CI/CD, containers |
| `qa` | Testes unitários, integração, e2e |
| `researcher` | Pesquisa técnica e de produto, benchmarks, inteligência competitiva |
| `security-auditor` | Segurança, vulnerabilidades |
| `design-engineer` | Web, UI, UX |
| `marketing-strategist` | Marketing, publicidade, mídias, go-to-market |

### Organograma e cadeia de spawn

O `project-manager` é o **único agente do time com acesso à Task tool** (limitação do Claude Agent SDK: subagentes não spawnam subagentes). Todo spawn de especialista — inclusive os técnicos sob autoridade do `tech-lead` — passa pelo PM. As setas abaixo representam **autoridade técnica e fluxo de briefing**, não a cadeia de spawn (que é sempre PM → especialista).

```mermaid
graph TD
    U(["👤 Fundador / PM"]) --> PM["🗂️ Project Manager\núnico spawnador via Task"]

    PM -->|spawna| PO["📋 Product Owner\nkanban + backlog"]
    PM -->|spawna| TL["🧠 Tech Lead\nplano técnico + code review"]
    PM -->|spawna| RES["🔍 Researcher\npesquisa técnica e de produto"]
    PM -->|spawna| MKT["📣 Marketing Strategist\ngo-to-market + mídia"]

    PO --> KB[("GitHub Kanban")]

    TL -.->|recomenda PM acionar| DE["🔧 Data Engineer\npipelines + ETL"]
    TL -.->|recomenda PM acionar| DS["📈 Data Scientist\nanálise + modelagem"]
    TL -.->|recomenda PM acionar| MLE["📊 ML Engineer\nprodutização de modelos"]
    TL -.->|recomenda PM acionar| AIE["🤖 AI Engineer\nLLMs + agentes + RAG"]
    TL -.->|recomenda PM acionar| IDF["☁️ Infra & DevOps\ncloud + CI/CD"]
    TL -.->|recomenda PM acionar| QA["✅ QA\ntestes + qualidade"]
    TL -.->|recomenda PM acionar| SEC["🔒 Security Auditor\nsegurança + vulnerabilidades"]
    TL -.->|recomenda PM acionar| FE["🖥️ Frontend Engineer\nweb + UI + UX"]

    PM -->|spawna com briefing do TL| DE
    PM -->|spawna com briefing do TL| DS
    PM -->|spawna com briefing do TL| MLE
    PM -->|spawna com briefing do TL| AIE
    PM -->|spawna com briefing do TL| IDF
    PM -->|spawna com briefing do TL| QA
    PM -->|spawna com briefing do TL| SEC
    PM -->|spawna com briefing do TL| FE
```

**Como ler:** setas sólidas (`-->|spawna|`) mostram quem o PM aciona via Task. Setas tracejadas (`-.->|recomenda PM acionar|`) mostram a recomendação técnica do `tech-lead` no plano de execução — o spawn em si é sempre feito pelo PM.

---

## Regras de Kanban

O kanban é a **fonte de verdade** do processo. Nenhum agente age sem consultar o kanban.

**Se precisar consultar issues e cards no Kanban** (project-number, owner, IDs de status), leia `project/memory/kanban_ids.md` — é a fonte de verdade dos IDs do projeto.

| Papel | Agente | Permissões |
|---|---|---|
| Dono | `product-owner` | cria, fecha, move qualquer card, árbitro final |
| Leitor obrigatório | `project-manager` | lê o kanban antes de toda delegação |
| Criador de issues | `project-manager`, `product-owner` | abrem issues novas — **sempre adicionam ao projeto Kanban imediatamente após criar** |
| Atualizador | todos os especialistas | move o próprio card para `In Progress` e `In Review` |
| Fechador | `product-owner` + `tech-lead` | movem para `Done` após aprovação |

### Dimensões obrigatórias do backlog

O `product-owner` garante que o backlog cobre **todas** as dimensões:

- **Discovery** — validação do problema, pesquisa, benchmarks
- **Negócio** — pitch deck, apresentações, identidade, naming
- **Produto** — MVP, personas, jornada do usuário, roadmap
- **Tech** — arquitetura, pipelines, testes, CI/CD
- **Lançamento** — divulgação, canais, métricas
- **Operações** — monitoramento, alertas, manutenção

### Labels obrigatórias no backlog

Ao criar o backlog (via `/kickoff` ou `/review-backlog`), o `product-owner` **sempre** cria e aplica labels em todas as issues:

**Labels de dimensão** (uma por issue):
| Label | Cor | Quando usar |
|---|---|---|
| `discovery` | `#0075ca` | Validações, pesquisas, entrevistas, benchmarks |
| `negocio` | `#e4e669` | Pitch, marca, financeiro, jurídico, CNPJ |
| `produto` | `#d93f0b` | Personas, jornada, PRD, wireframes, roadmap |
| `tech` | `#0e8a16` | Arquitetura, backend, frontend, infra, testes |
| `lancamento` | `#f9d0c4` | Go-to-market, canais, onboarding de parceiros |
| `operacoes` | `#bfd4f2` | Monitoramento, alertas, processos, runbooks |

**Labels de prioridade** (uma por issue):
| Label | Cor | Quando usar |
|---|---|---|
| `priority:high` | `#b60205` | Caminho crítico — bloqueia o próximo marco |
| `priority:medium` | `#fbca04` | Importante mas não bloqueia imediatamente |
| `priority:low` | `#c2e0c6` | Backlog futuro, nice-to-have |

**Regra:** criar as labels no repositório com `gh label create` antes de criar as issues. Aplicar sempre as duas labels (dimensão + prioridade) em cada issue no momento da criação.

---

## Regras de Branches

```
feature/* → dev → main
```

| Branch | Quem usa | Regra |
|---|---|---|
| `feature/*` ou `fix/*` | agentes especialistas | todo trabalho começa aqui |
| `dev` | integração contínua | recebe PRs de feature; nunca push direto |
| `main` | produção estável | recebe PRs de `dev`; só quando o usuário pedir explicitamente |

**Regras obrigatórias:**
- Nunca fazer push direto em `dev` ou `main` — sempre branch + PR
- Mudanças em arquivos de Mundo 1 (`.claude/`, estrutura de `CLAUDE.md`/`AGENTS.md`, hooks/generators) e Mundo 2 / projeto (`project/`) também seguem essa regra — nunca push direto, sempre PR
- `main` só recebe merge quando o usuário pedir explicitamente

**Regra crítica — `--delete-branch` e proteção de `dev`:**
- `--delete-branch` **só** em PRs de `feature/*` ou `fix/*` → `dev` — nunca em PRs de `dev` → `main`
- Quando o PR é `dev → main`, usar `gh pr merge --merge` **sem** `--delete-branch`
- Motivo: `gh pr merge --delete-branch` usa a API do GitHub e não é bloqueado pelo `deny` do settings.json — apaga o branch remoto silenciosamente, inclusive o `dev`
- Todo trabalho começa em `feature/*` ou `fix/*` — nunca commitar direto em `dev`, mesmo para mudanças de sistema (`CLAUDE.md`, commands, agents)

## Convenção de Commits

Todos os commits seguem **Conventional Commits** com escopo obrigatório que reflete os 3 contextos da arquitetura:

| Escopo | Quando usar | Exemplos |
|---|---|---|
| `(system)` | Mundo 1 — sistema agentic imutável (template universal): `.claude/`, definições de agentes, hooks/generators do framework, estrutura de `CLAUDE.md`/`AGENTS.md` | `chore(system): adicionar hook post_write`, `feat(system): novo agente data-engineer` |
| `(project)` | Mundo 2 / projeto: memória do projeto (`project/memory/`), docs do projeto (`project/docs/`), site MkDocs (`project/docs-site/`), regras textuais em `CLAUDE.md`/`AGENTS.md` | `docs(project): atualizar project_history`, `docs(project): novo runbook do tech-lead` |
| sem escopo OU `(<produto>)` | Mundo 2 / produto: código, features, docs e testes em `products/<produto>/` | `feat: implementar autenticação JWT`, `feat(<produto>): pipeline X` |

**Regras:**
- Mudanças entre contextos diferentes nunca se misturam no mesmo commit
- Ao **estrutura** de `CLAUDE.md`/`AGENTS.md` (regra que vale para qualquer projeto) muda → `(system)`. Ao **conteúdo** específico deste projeto muda (referências a produtos, decisões deste projeto) → `(project)`
- Em caso de dúvida entre `(system)` e `(project)` para uma mudança em `CLAUDE.md`: pergunte "essa regra serviria para qualquer projeto que herda do template?". Sim → `(system)`. Não → `(project)`

## Memória Persistente

A memória persistente vive **integralmente em Mundo 2** (mutável). Mundo 1 (sistema imutável) **não tem memória própria** — só estrutura herdada do template. O que cresce com o trabalho fica em 2 níveis:

### Mundo 2 / projeto — memória do projeto (`project/memory/`)

Criada pela Fase 0 do `/kickoff` e atualizada via `/update-memory`. Específica deste projeto inteiro (não universal de template, não específica de um produto).

| Arquivo | Conteúdo | Quem lê |
|---|---|---|
| `MEMORY.md` | Índice com links para os outros arquivos + ponteiros para MEMORY.md de cada produto | project-manager, tech-lead |
| `user_profile.md` | Trajetória, rede e preferências do fundador | project-manager, tech-lead |
| `project_genesis.md` | Motivação fundadora, ancoragens estratégicas, exclusões | project-manager, tech-lead |
| `project_history.md` | Changelog humano — decisões, entregáveis, restrições do projeto | project-manager, tech-lead |

### Mundo 2 / produto — memória de produto (`products/<produto>/`)

Cada produto em `products/<produto>/` tem **seu próprio `MEMORY.md`**, que é o índice dos documentos vivos do produto (plan, guidelines, runbook, visual template, etc — varia por produto). Estrutura simétrica à de Mundo 2 / projeto: o MEMORY.md do produto **não duplica** conteúdo, apenas aponta para arquivos.

**Convenção universal de Mundo 2 / produto (criada por `/kickoff-product`):**

Todo produto tem:
1. `products/<produto>/MEMORY.md` — índice de docs vivos do produto
2. `products/<produto>/<produto>_plan_vN.md` (ou nome equivalente como `pipeline_plan_v4.md`) — **plan append-only versionado** seguindo as regras de versionamento (§"Versionamento de Documentos"): nome estável, archive em `products/<produto>/archive/<plan>_YYYY-MM-DD_vN.md`, seção §15.x (ou similar) que cresce a cada nova entrega
3. `products/<produto>/archive/` — versões antigas dos docs vivos versionados

Outros docs canônicos do produto (guidelines, runbook, visual template, etc) emergem organicamente conforme o produto cresce, sempre apontados pelo MEMORY.md do produto.

**Regra de manutenção do índice (Mundo 2 / produto):**

Sempre que criar um doc novo dentro de `products/<produto>/` (guideline, runbook, visual template, ADR específico do produto, schema de dados, etc.), **atualize `products/<produto>/MEMORY.md` na mesma operação** adicionando uma linha apontando para o arquivo. Sem essa atualização, o índice fica desatualizado e PM/TL futuros não enxergam o doc — perdendo contexto que era pra estar disponível.

A linha do índice segue o mesmo padrão das outras: `[Título](caminho.md) — descrição em uma linha`. Não é necessário PR separado: a criação do doc + atualização do MEMORY.md vão juntas no mesmo commit/PR.

A mesma regra vale para **arquivamento**: se um doc deixar de ser vigente (substituído por nova versão, removido), atualize o MEMORY.md removendo ou atualizando a linha correspondente.

**Regra de atualização do plan (Mundo 2 / produto apenas):**

Sempre que um PR for mergeado em `dev` ou `main` afetando arquivos em `products/<produto>/`, o plan do produto deve receber uma nova seção §15.x (ou equivalente) descrevendo:

- Issue/PR number
- Mudança em uma linha
- Decisões tomadas durante a entrega (se houver)
- Suite de testes (se mudou)

**Cadência da atualização — em batch via `/update-memory-product`, não a cada merge:**

A atualização acontece **em batch periódico** rodando o command `/update-memory-product` (análogo ao `/update-memory` de Mundo 2 / projeto). A skill varre commits desde a última entrada §15.x do plan do produto e escreve N entradas de uma vez, em um único PR.

**Por que não é update por merge:**
- Update a cada merge fragmentaria o histórico em micro-commits
- Cada merge dispararia uma nova sessão LLM só pra escrever uma linha — alto custo, baixo retorno
- Em batch, você decide quando rodar (fim do dia, fim da semana, antes de promoção pra main) e paga o custo uma vez

**Hook avisador (opcional):** quando merge em `products/<produto>/` acontecer via `gh pr merge`, um hook do Claude Code pode exibir lembrete `"considere rodar /update-memory-product quando conveniente"`. **É lembrete, não obrigação imediata** — operador decide a cadência da skill. Se o hook não for configurado, a regra ainda vale: você lembra de rodar a skill periodicamente.

A regra vale para **qualquer produto** em `products/<produto>/`. A skill garante que nenhum merge é pulado (lê commits desde último §15.x). Em Mundo 2 / projeto, `/update-memory` tem cadência subjetiva (semanal/quinzenal). Em Mundo 2 / produto, a cadência da skill é decisão sua, mas a varredura é completa.

### Regras de leitura

**Ordem de leitura obrigatória antes de agir (por agente):**

**`project-manager` e `product-owner`** leem, nesta ordem:

1. `project/memory/MEMORY.md` — índice da memória persistente
2. `project/memory/user_profile.md` — trajetória, preferências e objetivos do fundador
3. `project/memory/project_genesis.md` — motivação fundadora, ancoragens estratégicas, exclusões
4. `project/memory/project_history.md` — changelog humano — decisões, entregáveis, restrições
5. Estado do Kanban via `gh project item-list`
6. `git log --oneline -10` — últimos commits

**`tech-lead`** lê:

1. `project/memory/MEMORY.md` — índice da memória persistente (inclui referências a guidelines do projeto)
2. `project/memory/project_genesis.md` — contexto do projeto
3. `project/docs/business/project-manager/relatorio.md` (se existir) — problem statement e backlog aprovados pelo `/kickoff`
4. `git log --oneline -10` — últimos commits

**Todos os demais agentes** leem apenas:

1. `git log --oneline -10` — últimos commits

Se algum arquivo contradisser a instrução recebida, o agente **pára e reporta** — não resolve silenciosamente.

**Resumo das responsabilidades de leitura:**

- **PM/tech-lead leem o `project/memory/MEMORY.md` raiz antes de agir** — sempre, em qualquer trabalho.
- **Quando o trabalho cair em `products/<produto>/`, PM/tech-lead também leem `products/<produto>/MEMORY.md`** antes de delegar — para conhecer os docs vivos do produto e identificar quais o especialista deve receber no briefing.
- Especialistas não leem memória diretamente — recebem ponteiros pelos arquivos relevantes via prompt de delegação.

**Profundidade de leitura — PM/TL podem (e devem) ler o conteúdo quando necessário:**

A leitura padrão é o **índice** (MEMORY.md). PM/TL **abrem o conteúdo** dos docs apontados quando o índice não bastar para decidir bem — por exemplo:

- Quando precisar entender contexto histórico para escolher abordagem de delegação (ex: ler `pipeline_plan_v4.md` antes de decidir como abordar fix relacionado a uma decisão antiga registrada em §15.x)
- Quando precisar identificar **qual** guideline específico é relevante para a tarefa (ex: ler `editorial_guidelines.md` antes de saber se aquele exemplo desatualizado afeta a tarefa atual)
- Quando o título no índice for ambíguo ou genérico, e a decisão de delegação depender de saber o conteúdo

**Especialistas, ao contrário, só leem o que receberem no briefing** — não exploram docs por conta própria. O contraste é proposital: PM/TL têm autonomia exploratória para tomar decisões de delegação; especialistas executam dentro do escopo definido.

**Regra de briefing:** ao montar o prompt de delegação para um especialista, o PM e o tech-lead verificam **ambos** os MEMORY.md (raiz e do produto, se aplicável) e incluem referências aos guidelines relevantes para a tarefa (se houverem). O especialista não descobre guidelines por conta própria — recebe no briefing.

## Autenticação GitHub

Dois mecanismos disponíveis — use o adequado para cada operação:

| Ferramenta | Como autentica | Quando usar |
|---|---|---|
| `gh` CLI | `GH_TOKEN` do `.env` | merge, delete-branch, PR, issues via terminal |
| MCP GitHub | token do `.mcp.json` (automático) | operações via ferramentas MCP do Claude |

**Antes de usar `gh`**, carregue o token (fórmula universal — funciona em sessão principal e dentro de worktree):
```bash
export GH_TOKEN=$(grep GH_TOKEN "$(git rev-parse --git-common-dir)/../.env" | cut -d= -f2)
```

`git rev-parse --git-common-dir` resolve ao `.git` do repo principal mesmo dentro de worktree (subagentes spawnados com `isolation: "worktree"`). Subir 1 nível chega à raiz do repo onde está o `.env`.

O MCP GitHub não precisa de configuração adicional — o token do `.mcp.json` é carregado automaticamente pelo Claude Code.

### Como especialistas abrem PR

Especialistas que produzem trabalho (código ou docs) abrem PR via `gh` CLI:

```bash
export GH_TOKEN=$(grep GH_TOKEN "$(git rev-parse --git-common-dir)/../.env" | cut -d= -f2)
git checkout -b feature/<nome-descritivo>   # ou fix/<nome>, docs/<tema>
git add <arquivos>
git commit -m "<tipo>(<escopo>): <mensagem>"
git push -u origin feature/<nome-descritivo>
gh pr create --base dev --head feature/<nome-descritivo> \
    --title "<título>" --body "<body com link da issue, test plan>"
```

A fórmula de `GH_TOKEN` acima é a mesma — funciona em sessão principal e dentro de worktree (`isolation: "worktree"`).

**Para merge de PRs**, comandos por contexto (ver §"Regras de Branches" para detalhes da regra crítica):
```bash
# feature/* ou fix/* → dev: com --delete-branch (apaga branch da feature)
gh pr merge <num> --merge --delete-branch

# dev → main: SEM --delete-branch (apagar dev seria catastrófico)
gh pr merge <num> --merge
```

---

## Regras de Código e PR

| Etapa | Responsável |
|---|---|
| Escrever código | agente especialista da tarefa |
| Produzir documentação | `product-owner`, `researcher`, `marketing-strategist` |
| Abrir PR | agente que produziu o trabalho |
| Review de PRs de código | `tech-lead` — sempre |
| Review de PRs de docs do projeto (`project/docs/`) | `project-manager` — sempre |
| Review de PRs de docs de produto (`products/<produto>/*.md`, runbooks, guidelines) | `tech-lead` se acompanha código; `product-owner` se é spec/critério; PM em casos editoriais — varia por contexto do produto |
| Security review | `security-auditor` — PRs com infra, auth ou dados sensíveis |
| QA review | `qa` — valida cobertura de testes |
| Aprovar PR de código | `tech-lead` |
| Aprovar PR de docs | `project-manager` |
| Merge | `tech-lead`; `infra-devops` em PRs de CI/CD quando delegado |
| Fechar issue | `product-owner` após merge |

Regra central: **nenhum agente faz merge do próprio trabalho sem aprovação do responsável** (`tech-lead` para código, `project-manager` para docs).

### Cleanup obrigatório após merge

**Merge de feature → dev** (agente especialista, após merge aprovado):
```bash
git checkout dev && git pull && git branch -D <nome-do-branch> 2>/dev/null || true
```

**Merge de dev → main** (quando o usuário pedir promoção para main):
```bash
git checkout main && git pull origin main && git checkout dev && git merge main --no-edit && git push origin dev
```

Nunca rodar `git pull origin main` estando em outro branch — isso mistura históricos. Sempre fazer checkout do branch antes de puxar. O `git merge main` final é obrigatório para trazer o commit de merge para o dev e evitar o banner de divergência no Claude Code.

**Esta etapa é obrigatória em todos os commands que geram branch e merge** — `/fix-issue`, `/advance`, `/deploy`, qualquer outro. Não é opcional. Sem este passo, o Claude Code exibe o banner de branch stale e o workspace fica sujo.

---

## Sessões Cloud — Rastreabilidade

Ao abrir PR ou commitar entregável em sessão cloud, incluir no corpo do PR o link da sessão:

```bash
[ -n "$CLAUDE_CODE_REMOTE_SESSION_ID" ] && echo "Sessão: https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID}"
```

Se `CLAUDE_CODE_REMOTE_SESSION_ID` não existir (sessão local), omitir — sem erro, sem placeholder.

---

## Contexto em Sessões Cloud

Em sessões cloud, os comandos de contexto se comportam diferente:

- `/compact` → disponível — resume a conversa e libera contexto; aceita instruções de foco (ex: `/compact manter output dos testes`)
- `/clear` (comando interno do Claude) → **não disponível** em cloud — usar `/compact` no lugar

---

## Commands Disponíveis

| Command | Quando usar |
|---|---|
| `/kickoff` | Iniciar um projeto novo — discovery, pesquisa, relatório, apresentação, backlog, delegação |
| `/kickoff-product` | Criar um novo produto em `products/<nome>/` — gera MEMORY.md + plan inicial versionado + estrutura mínima de pastas. Usar **sempre** ao adicionar produto novo (não criar pasta na mão) |
| `/advance` | Avançar no Kanban — fecha prontos, valida com PO, paraleliza issues independentes, delega |
| `/review-backlog` | Varredura proativa — fecha prontos, identifica lacunas, refina e cria novas issues |
| `/review` | Acionar TL para code review de um PR específico |
| `/deploy` | Acionar infra-devops para deploy |
| `/fix-issue` | Acionar especialista para corrigir um bug ou problema reportado |
| `/update-memory` | Atualizar memória do projeto (Mundo 2 / projeto) — registrar decisões, restrições e entregáveis em `project_history.md` (incremental) |
| `/update-memory-full` | Reconstruir memória do projeto completa — usar quando histórico está vazio ou muito defasado |
| `/update-memory-product` | Atualizar plan de produto (Mundo 2 / produto) — varre commits desde último §15.x, escreve N entradas em batch, abre PR para `dev`. Argumento opcional: `<nome-do-produto>` |

---

## Skills Disponíveis

Skills em `.agents/skills/` — referenciadas formalmente nos agentes.

**Skills de domínio enterprise:**
- `product-management` — backlog, priorização, critérios de aceitação
- `code-review` — revisão de PRs com severidade 🔴🟡🔵
- `data-engineering` — pipelines, ETL, qualidade de dados
- `data-science` — análise exploratória, estatística, modelagem, insights
- `ml-engineering` — produtização de modelos, serving, monitoramento de drift
- `ai-engineering` — LLMs, RAG, agentes, evals
- `frontend-engineering` — UI/UX, acessibilidade, responsividade
- `security-audit` — OWASP, vulnerabilidades, secrets
- `qa-testing` — pirâmide de testes, cobertura, boas práticas
- `market-research` — mercado, competidores, benchmarks
- `go-to-market` — GTM, posicionamento, funil
- `infra-devops` — IaC, CI/CD, deploy, observabilidade

**Skills Caveman (opcionais — instaladas pelo `/wizard`):**
- `caveman` — comunicação ultra-comprimida (~75% menos tokens)
- `caveman-commit` — mensagens de commit comprimidas
- `caveman-review` — code review em uma linha por finding

# Diagnóstico — Refactor de `claude-code-social-sciences-template` para alinhar ao enterprise

> **Data:** 2026-05-11
> **Fonte de verdade:** `claude-code-enterprise-template` (estado pós-sync de `presenca-congresso`)
> **Alvo:** `claude-code-social-sciences-template`
> **Premissa-chave confirmada:** Subagentes spawnados via `Task` **não têm acesso à Task tool** (limitação do Claude Agent SDK). O agente principal (`project-manager` no enterprise, `research-coordinator` no social) é **o próprio Claude base lendo CLAUDE.md**, não um arquivo em `.claude/agents/`. Apenas ele tem Task tool.

---

## 1. Equivalência de vocabulário (social-sciences) — DECIDIDO

**Inversão de nomes em relação ao desenho atual.** O PI vira o Claude base (entrada do usuário), e o RC vira o subagente de Kanban (análogo ao product-owner do enterprise). Justificativa: na cultura acadêmica, o PI é a autoridade que dirige a pesquisa — natural ele ser a "voz" que o usuário ouve. O RC vira coordenação operacional de backlog/Kanban.

| Conceito no enterprise | Equivalente em social-sciences | Notas |
|---|---|---|
| `project-manager` (Claude base) | **`principal-investigator` (Claude base)** | Único com Task tool; ponto de entrada do usuário |
| `product-owner` (subagente Kanban) | **`research-coordinator` (subagente Kanban)** | Cuida de dimensões/labels/abertura/fechamento de issues acadêmicas |
| `tech-lead` (autoridade técnica + plano de execução) | `tech-lead` (mesmo papel) | Subagente-planejador; retorna plano ao PI para tarefas técnicas |
| `products/<produto>/` | `papers/<paper>/` | Decidido na conversa |
| `MEMORY.md` por produto | `MEMORY.md` por paper | Mesma estrutura |
| `pipeline_plan_vN.md` | `paper_plan_vN.md` | Plan append-only versionado |
| `/kickoff-product` | `/kickoff-paper` | Cria estrutura inicial do paper |
| `/update-memory-product` | `/update-memory-paper` | Update batch do plan do paper |
| `/run-editorial-diaria` (skill de produto) | `/run-<paper>-...` (skill de paper, raro) | Exceção tolerada em `.claude/commands/` |
| `(system)` / `(project)` / `(<produto>)` em commits | `(system)` / `(project)` / `(<paper>)` | Mesma estrutura, vocabulário trocado |
| "produto" / "feature" | "paper" / "entrega acadêmica" | Vocabulário em todos os textos |
| `design-engineer` | (não aplicável — descartar) | Academia não tem UI |
| `marketing-strategist` | `dissemination-strategist` (já existe) | Equivalente direto |
| `researcher` | (já é o domínio inteiro — distribuir entre especialistas acadêmicos) | Não existe agente `researcher` separado em social |

---

## 2. Estrutura de pastas — antes e depois

### Estado atual (social-sciences)
```
.claude/
  agents/                    # tech-lead, template-coordinator (do pai)
  commands/                  # clean, fix-issue, sync-*, wizard
  memory/                    # ⚠️ DEVERIA SER project/memory/
docs/                        # ⚠️ DEVERIA SER project/docs/
  kickoff/
  literature/
  theory/
  methodology/
  ethics/
  analysis/{qualitative,quantitative,figures}/
  manuscript/
  domain/{political-science,sociology,...}
  review/
  dissemination/
  external-writings/{own,others}/
docs-site/                   # ⚠️ DEVERIA SER project/docs-site/
src/, tests/, notebooks/
scripts/templates/
  CLAUDE.md, AGENTS.md, README.md
  agents/                    # 24 agentes acadêmicos
  commands/                  # advance, bring-external-writings, clean, fix-issue, kickoff, review-academic, review-backlog, update-memory
```

### Estado-alvo (alinhado ao enterprise + domínio acadêmico)
```
.claude/
  agents/                    # tech-lead, template-coordinator (do pai — adaptar domínio)
  commands/                  # clean, fix-issue, sync-*, wizard
project/                     # ✨ NOVO — Mundo 2 / projeto
  memory/                    # MEMORY.md, user_profile.md, project_genesis.md, project_history.md, kanban_ids.md
  docs/                      # pasta-por-agente em vez de pasta-por-tema
    research/                # agentes de pesquisa (literatura, teoria, método, ética, análise)
      principal-investigator/
      methodologist/
      philosopher/
      ethics-officer/
      literature-reviewer/
      qualitative-analyst/
      quantitative-analyst/
      academic-writer/
      peer-reviewer/
      dissemination-strategist/
    domain/                  # agentes de domínio
      political-scientist/
      sociologist/
      anthropologist/
      legal-scholar/
      linguist/
      ir-scholar/
      economist/
      historian/
      social-psychologist/
      communication-scholar/
      urbanist/
    tech/                    # agentes técnicos
      tech-lead/
      data-engineer/
      data-scientist/
      data-analyst/
  docs-site/                 # MkDocs publicado
  data/                      # dados compartilhados entre papers
papers/                      # ✨ NOVO — Mundo 2 / paper (analogia de products/)
  <paper>/
    MEMORY.md                # índice dos docs vivos do paper
    paper_plan_vN.md         # plan append-only versionado
    <paper>_main.md          # manuscrito vigente
    sections/                # estrutura livre por paper
    data/
    scripts/, src/, tests/   # quando há código exclusivo do paper
    archive/                 # versões antigas
src/, tests/, scripts/       # Mundo 1 — universal (raríssimo conter código de paper)
scripts/templates/
  CLAUDE.md, AGENTS.md, README.md  # gerados no filho (atualizados)
  agents/                    # 24 agentes com frontmatter YAML + estrutura completa
  commands/                  # todos os commands acadêmicos
```

**Mudanças críticas:**
1. `.claude/memory/` → `project/memory/`
2. `docs/<tema>/` → `project/docs/<bucket>/<agente>/` (pasta-por-agente)
3. `docs-site/` → `project/docs-site/`
4. **Novo:** `papers/<paper>/` para Mundo 2 / paper
5. **Migração:** subpastas temáticas (`literature/`, `theory/`, `ethics/`...) viram pastas-por-agente (`project/docs/research/literature-reviewer/`, `.../philosopher/`, `.../ethics-officer/`)

---

## 3. CLAUDE.md — gap estrutural (universal, mantendo domínio)

Comparação `scripts/templates/CLAUDE.md` enterprise (892 linhas) vs social (527 linhas).

### Blocos universais ausentes no social (precisa adicionar com adaptação)

| Bloco | Enterprise | Social | Ação |
|---|---|---|---|
| "O que é o `<coordinator>`" (= Claude base) | ✅ | ✅ | OK — manter |
| Regra de Início + mensagem de orientação | ✅ | ✅ | Atualizar comandos disponíveis |
| Regra "fora de comando, só conversa" | ✅ | ✅ | OK — manter |
| **Regra arquitetural: subagentes não spawnam, só coordinator tem Task** | ✅ | ❌ | **Adicionar** — universal |
| **Fluxo PM/coordinator → TL/PI → plano de execução → coordinator spawna especialistas** | ✅ | ❌ | **Adicionar** — universal |
| **Isolamento por worktree em subagentes (`isolation: "worktree"`)** | ✅ | ❌ | **Adicionar** — universal |
| **Sugestões de delegação cruzada de especialistas** | ✅ | ❌ | **Adicionar** — universal |
| **Entregas que cruzam domínios (grupo de trabalho conjunto)** | ✅ | ❌ | **Adicionar** — adaptar p/ academia (ex: paper que cruza method + ética) |
| Stack Python + uv + `.venv` obrigatório | ✅ | parcial | Modernizar (uv, .venv) |
| **Arquitetura Dual: Mundo 1 / Mundo 2 / projeto / paper** | ✅ | ❌ | **Adicionar** — adaptar produto→paper |
| **Critério do leitor primário (regra de desempate)** | ✅ | ❌ | **Adicionar** — universal |
| **Promoção entre subníveis (paper/rotina → paper raiz → projeto)** | ✅ | ❌ | **Adicionar** — adaptar |
| **Estrutura `project/docs/` pasta-por-agente** | ✅ | ❌ (usa pasta-por-tema) | **Reescrever** com adaptação acadêmica |
| **Frontmatter YAML obrigatório nos `.md` de `project/docs/`** | ✅ | ❌ | **Adicionar** — universal |
| **Versionamento: nome estável + archive (não data no vigente)** | ✅ | ❌ (data no vigente) | **Refactor** — universal |
| Geração PDF/DOCX/PPTX via hook | ✅ | ✅ (manual) | Modernizar para automático via hook |
| **Memória persistente em 2 níveis (projeto + paper)** | ✅ | ❌ (só projeto) | **Adicionar** nível paper |
| **`MEMORY.md` por paper + plan append-only** | ✅ | ❌ | **Adicionar** |
| **Regra de manutenção do índice MEMORY.md** | ✅ | ❌ | **Adicionar** |
| **Cadência `/update-memory-paper` (batch)** | ✅ | ❌ | **Adicionar** |
| **GH_TOKEN universal com `git rev-parse --git-common-dir`** | ✅ | ❌ | **Atualizar** — universal |
| **Regra crítica `--delete-branch` (proibido em dev→main)** | ✅ | parcial | **Reforçar** |
| **Como especialistas abrem PR (template detalhado)** | ✅ | ❌ | **Adicionar** — universal |
| **Cleanup obrigatório após merge (dev→main com merge main → dev)** | ✅ | parcial | **Atualizar** |
| Sessões Cloud + `/compact` | ✅ | ✅ | OK |

### Blocos domain-specific que devem permanecer no social

- Lista de 24 agentes acadêmicos (não mexer nos nomes)
- Dimensões do backlog acadêmicas (problema, teoria, metodologia, ética, dados, análise, escrita, disseminação)
- Labels acadêmicas (problema, teoria, metodologia, etica, dados, analise, escrita, disseminacao)
- Commands acadêmicos (`/bring-external-writings`, `/review-academic`)
- Vocabulário acadêmico (entregável, pesquisa, paper, manuscrito)
- Convenção `(research)` em commits (mas agora distinguir `(project)` vs `(<paper>)`)

---

## 4. AGENTS.md — decisão pendente

**Enterprise:** virou stub de 20 linhas apontando para CLAUDE.md (rationale: Claude Code só lê CLAUDE.md, AGENTS.md é stub de compatibilidade para outras ferramentas).

**Social atual:** 115 linhas com tabela completa de agentes.

**Recomendação:** seguir o enterprise — virar stub. Toda a especificação real vai para o CLAUDE.md. Reduz duplicação e drift.

---

## 5. Agentes — frontmatter YAML universal

**Estado atual social:** ❌ NENHUM dos 24 agentes tem frontmatter.

**Estado-alvo (formato enterprise):**
```yaml
---
name: principal-investigator
description: Orquestrador científico — recebe demandas do research-coordinator, planeja metodologia, retorna plano de execução com especialistas a acionar. Não tem Task tool — apenas planeja. Use dentro de /comandos ativos.
---

# Agent: Principal Investigator
...
```

**Por que importa:** o frontmatter é o que o Claude Code usa para apresentar agentes no menu de delegação e para auto-descoberta. Sem isso, agentes ficam invisíveis para fluxos automatizados.

### Plano para os 24 agentes do social

Cada agente precisa:
1. **Frontmatter** com `name` + `description` específica do papel
2. **Bloco "Organograma"** no formato do enterprise (mostrando que responde ao coordinator/PI)
3. **Bloco "Antes de agir"** — lista de leitura obrigatória (memória, kickoff doc, git log)
4. **Bloco "Skills referenciadas"** com paths corretos (`.agents/skills/<skill>/SKILL.md`)
5. **Bloco "Pasta de trabalho dedicada"** (`project/docs/<bucket>/<agente>/`)
6. **Bloco "Critério do leitor primário"** (universal — quando salva em `papers/<paper>/` vs sua pasta dedicada)
7. **Bloco "Estrutura `.md` esperada"** com frontmatter YAML obrigatório
8. **Bloco "Validações cruzadas"** com outros agentes (quem revisa o quê)

Tamanho-alvo: ~140-180 linhas por agente (hoje têm 70-95).

---

## 6. Commands — estado atual vs alvo

### Commands no social hoje (`scripts/templates/commands/`)
- `advance.md` — 124 linhas — precisa modernizar (kanban_ids, plano de execução, sugestões de delegação cruzada, isolation worktree, vocabulário)
- `bring-external-writings.md` — domain-specific — manter, modernizar paths (`project/docs/`)
- `clean.md` — modernizar
- `fix-issue.md` — modernizar (passo 0 de criar issue + adicionar ao Kanban)
- `kickoff.md` — 355 linhas — reescrever ~80% para incluir Fase 0 narrativa, `project/memory/`, persistir kanban_ids, sugerir `/kickoff-paper` em vez de criar paper diretamente
- `review-academic.md` — domain-specific — manter, modernizar
- `review-backlog.md` — modernizar
- `update-memory.md` — modernizar

### Commands a adicionar (do enterprise, adaptados)
- `deploy.md` — provavelmente N/A em academia (descartar?)
- `review.md` — code review (renomear ou manter? academia usa `review-academic.md` para tudo)
- `update-memory-full.md` — reconstruir memória completa quando defasada
- **`kickoff-paper.md`** ✨ — análogo a `/kickoff-product`, cria `papers/<paper>/` com MEMORY.md + plan inicial
- **`update-memory-paper.md`** ✨ — análogo a `/update-memory-product`, batch update do plan do paper

### Commands a remover (não cabem em academia)
- Nenhum específico — todos têm equivalente

### Commands em `.claude/commands/` (do pai, não filho)
- `clean.md` — modernizar (universal)
- `fix-issue.md` — modernizar (universal)
- `sync-master.md` ✅ — já sincronizado
- `sync-to-projects.md` ✅ — já sincronizado
- `sync-to-template.md` ✅ — já sincronizado
- `wizard.md` ✅ — já sincronizado

---

## 7. Skills (`.agents/skills/`)

**Enterprise tem 21 skills + caveman x3 (opcional).**
**Social tem 22 skills + caveman x3.**

Skills do social são **domain-specific** (academic-writing, peer-review, qualitative-coding, literature-review, research-ethics, research-design, etc.). Não é caso de propagar skills do enterprise → social, mas garantir que cada skill do social esteja **estruturalmente alinhada** com o padrão das do enterprise:

- frontmatter YAML
- estrutura de SKILL.md consistente
- referenciada formalmente nos agentes

### Verificação pendente (não feita neste diagnóstico)
- Skills do social têm frontmatter?
- Estrutura de SKILL.md alinhada?
- Cada skill é referenciada pelo agente correto via `.agents/skills/<skill>/SKILL.md`?

---

## 8. Hooks

✅ `session_start.sh` e `post_write.sh` já sincronizados via `/sync-master` (já apontam para `project/memory/kanban_ids.md` e `project/docs/`).

**Implicação:** após o refactor, os hooks já estarão prontos para a nova estrutura. Não precisa mexer.

---

## 9. `.claude/agents/` do pai (template-coordinator + tech-lead)

Esses são agentes do **template-pai** (não vão para o filho). Hoje:

- `template-coordinator.md` — domain-specific (fala em pesquisa, principal-investigator)
- `tech-lead.md` — domain-specific (responde a principal-investigator)

**Não precisa sincronizar** com enterprise — esses agentes orientam quem trabalha no template em si. A única coisa a fazer é garantir que estejam **internamente consistentes** com o novo CLAUDE.md/AGENTS.md raiz do social (após refactor).

---

## 10. Raiz do template — CLAUDE.md/AGENTS.md/README.md do PAI

Hoje (social):
- `CLAUDE.md` raiz: 163 linhas
- `AGENTS.md` raiz: 23 linhas
- `README.md` raiz: 194 linhas

Esses arquivos descrevem o **template em si** (não o filho). Após o refactor, precisam:
- Atualizar contagens (24 agentes, 22 skills, novos commands)
- Atualizar paths (`project/memory/`, `papers/`)
- Atualizar lista de agentes (com `dissemination-strategist`, `urbanist`, etc.)
- Linguagem: "fábrica de projetos de pesquisa" (já é)

---

## 11. Plano de execução em fases

### Fase 2.1 — Refactor de CLAUDE.md (gerado no filho)
- Reescrever `scripts/templates/CLAUDE.md` adicionando todos os blocos universais ausentes, adaptados para vocabulário acadêmico
- Definir e documentar `papers/<paper>/` como Mundo 2 / paper
- Tempo estimado: 1 session dedicada

### Fase 2.2 — Refactor de AGENTS.md (gerado no filho)
- Transformar em stub apontando para CLAUDE.md (modelo enterprise)
- Tempo estimado: 15 min

### Fase 2.3 — Refactor dos 24 agentes
- Adicionar frontmatter YAML em todos
- Expandir estrutura para o padrão enterprise (~140-180 linhas cada)
- Adaptar paths para `project/docs/<bucket>/<agente>/`
- Adicionar bloco "Critério do leitor primário"
- Tempo estimado: 2-3 sessions (8 agentes por session)

### Fase 2.4 — Refactor de commands
- Modernizar `kickoff.md`, `advance.md`, `review-backlog.md`, `fix-issue.md`, `clean.md`, `update-memory.md`
- Criar `kickoff-paper.md`, `update-memory-paper.md`, `update-memory-full.md`
- Adaptar `bring-external-writings.md`, `review-academic.md`
- Tempo estimado: 2 sessions

### Fase 2.5 — Verificação de skills
- Auditar 22 skills do social
- Padronizar estrutura SKILL.md (se necessário)
- Tempo estimado: 1 session

### Fase 2.6 — Refactor do pai (CLAUDE.md/AGENTS.md/README.md/.claude/agents/)
- Atualizar arquivos raiz do template para refletir nova realidade
- Tempo estimado: 1 session

### Fase 2.7 — Smoke test
- Criar projeto filho de teste com `/wizard`
- Validar que tudo funciona end-to-end (kickoff, advance, kickoff-paper)
- Tempo estimado: 1 session

**Total estimado:** 8-10 sessions para o social-sciences inteiro.

---

## 12. Decisões tomadas

### ✅ Decisão 1 — Arquitetura de papéis (FECHADA)

**Inversão de nomes RC ↔ PI:**
- `principal-investigator` (PI) **vira o Claude base** — entrada do usuário, único com Task, absorve responsabilidades do antigo RC (ler Kanban, exibir estado, conversar, delegar)
- `research-coordinator` (RC) **vira subagente de Kanban** — análogo direto ao `product-owner` do enterprise. Cuida de dimensões do backlog, labels, criação/fechamento de issues, vinculação ao Project
- `tech-lead` (TL) **continua subagente-planejador** — caixa técnica (data-engineer, data-scientist, data-analyst, quantitative-analyst)
- 22 especialistas — subagentes-executores spawnados pelo PI com briefing do TL ou do PI

### ✅ Decisão 2 — Arquivo `principal-investigator.md` em `.claude/agents/` (FECHADA)

Manter o arquivo, mesmo sendo a persona do Claude base. Espelha o enterprise (que tem `project-manager.md` em `.claude/agents/`). Não é usado para spawn (Claude base já é PI via CLAUDE.md), mas mantém simetria e referência.

### ✅ Decisão 3 — Usuário fala só com PI (FECHADA)

Igual ao enterprise: o usuário se comunica exclusivamente com o Claude base (PI). Especialistas são opacos — spawnados pelo PI, retornam ao PI. Não há `/comando-especialista` direto.

### ✅ Decisão 4 — Escopo de `papers/<paper>/` (FECHADA)

`papers/<paper>/` cobre **tudo**: artigo, tese, capítulo, working paper, dataset publicado, policy brief, código que vira artefato. Não criar `outputs/` separado. Cada subpasta `papers/<X>/` define internamente sua natureza (manuscrito, dataset, brief, etc.) via MEMORY.md e plan.

### ✅ Decisão 5 — `/deploy` equivalente acadêmico (FECHADA)

Criar `/submit` — comando análogo a `/deploy` para fluxo de submissão a periódico, evento ou repositório (preprint server, dataset repository, policy brief publication). Estrutura mínima do command será definida na Fase 2.4.

### ✅ Decisão 6 — `/review` vs `/review-academic` (FECHADA)

**Separar**:
- `/review` — code review de PR (igual enterprise) — TL revisa
- `/review-academic` — revisão de entregável acadêmico (manuscrito, parecer, análise) — `peer-reviewer` ou especialista de domínio revisa

### ✅ Decisão 7 — `paper_plan_vN.md` convenção (FECHADA)

Seguir o **mesmo padrão §15.x do enterprise** (append-only com issue/PR/decisões/testes). Sem adaptação especial para "capítulos" ou "milestones" — a lógica de append por entrega cabe igualmente em academia.

### ✅ Decisão 8 — Frontmatter dos agentes (FECHADA)

Seguir o **padrão exato do enterprise**: PT-BR no campo `description`, formato:
```yaml
---
name: <agente>
description: <descrição curta do papel + quando usar>
---
```

---

## 13. Próximos passos

**Aguarda decisões do usuário sobre seção 12** antes de iniciar Fase 2.1.

Após decisões, ordem recomendada:
1. CLAUDE.md (Fase 2.1) — pois é a referência que os agentes lerão
2. AGENTS.md stub (Fase 2.2) — trivial
3. Agentes (Fase 2.3) — 24 agentes, dividir em sessions
4. Commands (Fase 2.4) — depois dos agentes (commands referenciam agentes)
5. Skills (Fase 2.5)
6. Raiz do template (Fase 2.6)
7. Smoke test (Fase 2.7)

Depois disso, repetir tudo para o `health-template` (Fase 3) — esperamos que seja mais rápido pois o playbook já existe.

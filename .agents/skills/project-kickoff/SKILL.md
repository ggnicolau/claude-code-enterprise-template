# Skill: Project Kickoff

Padrão de entrada para iniciar um projeto novo — usado pelo `project-manager` no command `/kickoff`.

## Quando usar
Ao iniciar um projeto novo do zero (não para tarefas pontuais — para tarefa pontual o PM delega direto sem fluxo de kickoff).

## Pré-requisito: memória do projeto

**Antes de qualquer fase abaixo**, garantir que `project/memory/` está populada (Fase 0):
- `MEMORY.md` (índice)
- `user_profile.md` (trajetória, preferências, objetivos do fundador)
- `project_genesis.md` (motivação fundadora, ancoragens, exclusões)
- `project_history.md` (changelog inicial)

Se memória não existe, rodar `/update-memory-full` antes do kickoff.

## Fases do kickoff

1. **Discovery** — entender objetivo, público, contexto, restrições. PM aciona `researcher` para pesquisas iniciais (mercado, competidores, regulações).
2. **Pesquisa técnica** — PM aciona `tech-lead` para definir stack, arquitetura inicial, riscos técnicos.
3. **Relatório** — PM consolida discovery + pesquisa técnica em relatório versionado (`project/docs/business/project-manager/relatorio.md`).
4. **Apresentação** — PM aciona `product-owner` para criar deck executivo a partir do relatório.
5. **Backlog inicial** — PM aciona `product-owner` para criar issues no Kanban cobrindo as 6 dimensões (`discovery`, `negocio`, `produto`, `tech`, `lancamento`, `operacoes`).
6. **Delegação** — PM dispara primeiras issues `priority:high` para os especialistas correspondentes (sempre via `tech-lead` para tarefas técnicas).

## Critério de "kickoff pronto"

- Memória do projeto populada
- Relatório aprovado pelo usuário
- Apresentação produzida
- Backlog inicial com issues nas 6 dimensões, todas com critério de aceite e labels (dimensão + prioridade)
- Pelo menos uma issue movida para `In Progress`

## Boas práticas

- **Nunca pular Fase 0** (memória) — kickoff sem memória vira retrabalho depois
- **Toda decisão tomada no kickoff entra em `project_history.md`** com data e contexto
- Para criação de produto novo dentro do projeto, usar `/kickoff-product <nome>` (não `/kickoff`)

## Ver também

- CLAUDE.md §"Memória Persistente" — estrutura de `project/memory/`
- CLAUDE.md §"Dimensões obrigatórias do backlog" — as 6 dimensões
- `.claude/commands/kickoff.md` — implementação do command `/kickoff`

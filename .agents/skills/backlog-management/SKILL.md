# Skill: Backlog Management

Operação tática do Kanban — usado pelo `product-owner`.

## Quando usar
Ao criar, mover ou fechar issues no GitHub Projects no dia a dia. Para gestão estratégica de produto (priorização com framework, refinamento de épicos), use `product-management`.

## Estrutura mínima de uma issue

- **Título**: verbo no infinitivo + objeto + contexto curto
- **Descrição**: o quê, por quê (problema), e como (alto nível)
- **Critério de aceite**: lista checkável do que define "done"
- **Labels obrigatórias**: uma de **dimensão** + uma de **prioridade** (ver tabelas abaixo)

## Labels de dimensão (uma por issue)

| Label | Quando usar |
|---|---|
| `discovery` | Validações, pesquisas, entrevistas, benchmarks |
| `negocio` | Pitch, marca, financeiro, jurídico, CNPJ |
| `produto` | Personas, jornada, PRD, wireframes, roadmap |
| `tech` | Arquitetura, backend, frontend, infra, testes |
| `lancamento` | Go-to-market, canais, onboarding de parceiros |
| `operacoes` | Monitoramento, alertas, processos, runbooks |

## Labels de prioridade (uma por issue)

| Label | Quando usar |
|---|---|
| `priority:high` | Caminho crítico — bloqueia o próximo marco |
| `priority:medium` | Importante mas não bloqueia imediatamente |
| `priority:low` | Backlog futuro, nice-to-have |

> Labels devem existir no repo antes de aplicar. Use `gh label create` para criá-las (ver CLAUDE.md §"Labels obrigatórias no backlog" para cores e setup completo).

## Fluxo Kanban

`Backlog` → `Todo` → `In Progress` → `In Review` → `Done`

- Move card para `In Progress` ao começar a trabalhar
- Move para `In Review` ao abrir PR
- **Apenas product-owner + tech-lead movem para `Done`**, após merge aprovado

## Regra obrigatória

**Toda issue criada deve ser adicionada ao Kanban no mesmo ato.** Issue criada sem card vira dívida de processo. Sem exceção.

Para mover card de status via GraphQL otimizado (não usar `gh project item-list`), ver `.claude/agents/product-owner.md` §"Mover card de status — comando otimizado".

## Boas práticas

- Critério de aceite verificável — sem "deve funcionar bem"
- Refinar antes de priorizar — issue ambígua não entra em Todo
- Issue duplicada → fechar com link para a original
- Issue obsoleta → fechar com justificativa, não deixar acumular

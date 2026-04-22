# Project Overview

Template base para novos projetos Python com Claude Code configurado, equipe multi-agentes e kanban no GitHub Projects.

## Stack
- Python 3.11+
- Tests: pytest
- Formatting: ruff, black
- Env management: uv ou conda

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

## Equipe Multi-Agentes

Este template inclui 11 agentes em `.claude/agents/`. O ponto de entrada padrão é o `project-manager`.

| Agente | Responsabilidade |
|---|---|
| `project-manager` | Ponto de entrada — entende negócio e técnico, delega |
| `tech-lead` | Orquestrador técnico + code review |
| `product-owner` | Kanban, backlog, apresentações |
| `data-engineer` | Pipelines, ETL, qualidade de dados |
| `ml-engineer` | Modelos, features, experimentos |
| `ai-engineer` | LLMs, agentes, RAG, evals |
| `infra-devops` | Cloud, CI/CD, containers |
| `qa` | Testes unitários, integração, e2e |
| `researcher` | Pesquisa, benchmarks, literatura |
| `security-auditor` | Segurança, vulnerabilidades |
| `frontend-engineer` | Web, UI, UX |

## Skills Disponíveis

Skills base em `.agents/skills/` — uma por agente. Skills Caveman são opcionais (instaladas via wizard):

- `caveman` — comunicação ultra-comprimida (~75% menos tokens)
- `caveman-commit` — mensagens de commit comprimidas
- `caveman-review` — code review em uma linha por finding

## Iniciar Novo Projeto

Em uma conversa nova, diga `iniciar` para rodar o wizard de criação de repositório.

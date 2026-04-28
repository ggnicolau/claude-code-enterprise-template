# Claude Code Enterprise Template — Visão da Equipe

Este repositório é a **fábrica de projetos enterprise**. Os agentes aqui são os do template pai — não os dos projetos filhos.

## Agentes do template pai (`.claude/agents/`)

| Agente | Papel |
|---|---|
| `template-coordinator` | Ponto de entrada — orienta o uso do `/wizard`, coordena melhorias no template |
| `tech-lead` | Revisão técnica de PRs no próprio template |

## Agentes do projeto filho (`scripts/templates/agents/`)

Estes 12 agentes são copiados para o filho pelo `new_repo.py` durante a criação:

| Agente | Responsabilidade |
|---|---|
| `project-manager` | Ponto de entrada — delega, consolida, nunca executa |
| `tech-lead` | Orquestrador técnico, code review, aprovação de PRs |
| `product-owner` | Kanban, backlog completo (6 dimensões), priorização |
| `data-engineer` | Pipelines, ETL, qualidade de dados |
| `ml-engineer` | Modelos, features, experimentos |
| `ai-engineer` | LLMs, agentes, RAG, evals |
| `infra-devops` | Cloud, CI/CD, containers, observabilidade |
| `qa` | Testes, cobertura, qualidade |
| `researcher` | Pesquisa de mercado, benchmarks, inteligência competitiva |
| `security-auditor` | Segurança, vulnerabilidades, OWASP |
| `frontend-engineer` | Web, UI/UX, acessibilidade |
| `marketing-strategist` | Go-to-market, posicionamento, campanhas |

## Commands do template pai

| Command | Propósito |
|---|---|
| `/wizard` | Criar novo projeto filho enterprise |
| `/sync-to-projects` | Propagar mudanças do template para projetos filhos |
| `/sync-to-template` | Trazer melhorias de um filho de volta ao template |

## Hierarquia dos agentes no filho

```
Usuário
  └── project-manager (interface, delegação, consolidação)
        ├── product-owner (produto, kanban, backlog)
        ├── tech-lead (técnica, código, PRs)
        │     ├── data-engineer
        │     ├── ml-engineer
        │     ├── ai-engineer
        │     ├── infra-devops
        │     │     └── security-auditor
        │     ├── qa
        │     └── frontend-engineer
        └── researcher
              marketing-strategist (acionado por PM ou PO)
```

## Interações entre agentes (filho)

| Agente | Responde a | Trabalha com |
|---|---|---|
| `project-manager` | Usuário | product-owner, tech-lead, researcher, marketing-strategist |
| `product-owner` | project-manager | researcher, marketing-strategist, kanban |
| `tech-lead` | project-manager | data-engineer, ml-engineer, ai-engineer, infra-devops, qa, security-auditor, frontend-engineer, researcher |
| `researcher` | PM / PO / TL (quem acionar) | todos que precisam de inteligência de mercado ou técnica |
| `marketing-strategist` | PM / PO (quem acionar) | researcher |
| `data-engineer` | tech-lead | researcher, qa |
| `ml-engineer` | tech-lead | data-engineer, researcher |
| `ai-engineer` | tech-lead | researcher, ml-engineer |
| `infra-devops` | tech-lead | security-auditor |
| `frontend-engineer` | tech-lead | infra-devops, researcher |
| `qa` | tech-lead | data-engineer, ml-engineer |
| `security-auditor` | tech-lead / infra-devops | infra-devops |

## Como criar um projeto filho

Use o `/wizard` em uma conversa nova **neste repositório**.

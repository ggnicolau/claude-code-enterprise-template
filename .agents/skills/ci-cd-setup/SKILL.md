# Skill: CI/CD Setup

Padrão para configuração de pipelines de CI/CD — usado pelo `infra-devops`.

## Quando usar
Ao criar ou atualizar workflows de GitHub Actions, Docker ou deploy.

## Estrutura padrão de workflow Python
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv sync
      - run: uv run ruff check .
      - run: uv run black --check .
      - run: uv run pytest
```

## Boas práticas
- Nunca hardcodar secrets — usar `${{ secrets.NAME }}`
- Todo deploy precisa de smoke test após subir
- Separar jobs de lint, test e deploy
- Usar cache de dependências para acelerar builds

## Operações git/PR

Para auth via `gh` CLI, fluxo de branch e regra crítica de `--delete-branch` (só em feature→dev, nunca em dev→main), ver CLAUDE.md §"Autenticação GitHub" e §"Como especialistas abrem PR".

## Hooks do projeto

Projetos que herdam o template enterprise têm hooks em `scripts/hooks/` (`post_write.sh`, `post_bash_merge.sh`, `session_start.sh`). Workflows de CI não devem duplicar lógica de hooks — ver `.claude/settings.json` para hooks ativos.

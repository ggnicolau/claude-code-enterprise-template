# Project Overview

Senior NLP / Data Science project workspace.

## Stack
- Python 3.11+
- NLP: spaCy, HuggingFace Transformers, NLTK
- ML: scikit-learn, PyTorch
- Data: pandas, numpy
- Tests: pytest
- Formatting: ruff, black
- Env management: uv or conda

## Conventions
- Type hints em todas as funções públicas
- Docstrings apenas quando o "porquê" não é óbvio
- Prefira dataclasses ou Pydantic para modelos de dados
- Notebooks em `notebooks/`, código reutilizável em `src/`
- Nunca commitar dados brutos ou modelos pesados — use `.gitignore`

## Architecture Notes
- Pipelines de NLP seguem o padrão: raw → processed → features → model
- Experimentos rastreados via MLflow ou simples logs estruturados
- Scripts CLI usam `typer` ou `argparse`

## What to Avoid
- Não usar `print()` para debug — use `logging`
- Não hardcodar paths — use `pathlib.Path`
- Não misturar lógica de negócio com I/O

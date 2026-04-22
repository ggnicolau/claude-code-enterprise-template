# Wizard — Criar Novo Repositório

Oriente o usuário a rodar no terminal:

```bash
python scripts/new_repo.py
```

O script é interativo: pedirá nome do repositório, visibilidade (público/privado) e se deseja instalar as skills Caveman. Ao final cria o repo no GitHub, configura o `GH_PAT` como secret e dispara o setup do kanban automaticamente.

$ARGUMENTS

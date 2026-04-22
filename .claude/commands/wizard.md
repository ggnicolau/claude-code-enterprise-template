# Wizard — Criar Novo Repositório

Pergunte ao usuário:
1. Nome do novo repositório
2. Visibilidade: privado ou público?
3. Instalar skills Caveman? (sim/não)

Com as respostas, monte os argumentos e execute:

```bash
python scripts/new_repo.py --name <nome> --visibility <private|public> --yes [--caveman | --skip-caveman]
```

$ARGUMENTS

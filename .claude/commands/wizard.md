# Wizard — Criar Novo Repositório

Use a ferramenta `AskUserQuestion` para coletar as respostas abaixo uma de cada vez:

1. **Nome do repositório** — campo de texto livre (permitir escrita livre)
2. **Visibilidade** — escolha estrita: `Privado` ou `Público` (sem opção de escrita livre)
3. **Instalar skills Caveman?** — escolha estrita: `Sim` ou `Não` (sem opção de escrita livre)

Com as respostas, execute:
```bash
python scripts/new_repo.py --name <nome> --visibility <private|public> --yes [--caveman | --skip-caveman]
```

$ARGUMENTS

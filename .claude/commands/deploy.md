# Deploy / Publicar Modelo

Checklist antes de fazer deploy de modelo ou pipeline:

1. Rodar todos os testes: `pytest`
2. Verificar se requirements estão atualizados
3. Confirmar que não há paths hardcodados
4. Checar se artefatos grandes estão no .gitignore
5. Validar métricas mínimas de performance do modelo
6. Gerar tag de versão no git

$ARGUMENTS

#!/bin/bash
# Hook PostToolUse para Bash — detecta `gh pr merge` que afetou products/<produto>/
# e exibe lembrete para rodar /update-memory-product.
#
# É lembrete, não obrigação. Não falha o tool call em hipótese alguma.
# Falha silenciosamente em qualquer erro (jq ausente, gh sem auth, etc.).
#
# Issue de origem: #475

INPUT=$(cat)

# Extrai o comando executado
COMMAND=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('command',''))" 2>/dev/null)

[ -z "$COMMAND" ] && exit 0

# Só dispara em `gh pr merge <num>` (forma típica). Variações como `gh pr merge --merge`
# também batem porque o número aparece em algum lugar.
echo "$COMMAND" | grep -qE 'gh pr merge' || exit 0

# Extrai número do PR — primeiro número que aparece após "gh pr merge"
PR_NUM=$(echo "$COMMAND" | grep -oE 'gh pr merge[^|;&]*' | grep -oE '[0-9]+' | head -1)

[ -z "$PR_NUM" ] && exit 0

# Consulta arquivos do PR
# Falha silenciosa se gh não autenticado ou PR não existe
FILES=$(gh pr view "$PR_NUM" --json files --jq '.files[].path' 2>/dev/null)

[ -z "$FILES" ] && exit 0

# Verifica se algum arquivo está em products/<produto>/
PRODUCT_FILES=$(echo "$FILES" | grep -E '^products/[^/]+/' || true)

[ -z "$PRODUCT_FILES" ] && exit 0

# Extrai produtos únicos afetados
PRODUCTS=$(echo "$PRODUCT_FILES" | sed -E 's|^products/([^/]+)/.*|\1|' | sort -u | tr '\n' ',' | sed 's/,$//')

# Lembrete (stderr para aparecer ao usuário sem afetar saída do tool)
echo "" >&2
echo "💡 PR #${PR_NUM} mergeado em products/${PRODUCTS}/ — considere rodar /update-memory-product quando conveniente" >&2
echo "" >&2

exit 0

#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

[ -z "$FILE" ] && exit 0

# A2: ruff + black em arquivos .py
if [[ "$FILE" == *.py ]]; then
  ruff check --fix "$FILE" 2>/dev/null || true
  black "$FILE" 2>/dev/null || true
fi

# A3: gerar PDF/DOCX/PPTX em arquivos .md dentro de project/docs/
if [[ "$FILE" == *project/docs/*.md ]]; then
  node "$CLAUDE_PROJECT_DIR/scripts/generate_docs.js" "$FILE" 2>/dev/null || true
fi

# A4: convenção de nome (CLAUDE.md §"Versionamento de Documentos")
#   - Vigente (fora de archive/): nome estável SEM data SEM versão
#   - Archive: {nome}_YYYY-MM-DD_v{N}.md
if [[ "$FILE" == *project/docs/*.md ]]; then
  BASENAME=$(basename "$FILE")
  if [[ "$FILE" == */archive/* ]]; then
    if ! echo "$BASENAME" | grep -qE '^.+_[0-9]{4}-[0-9]{2}-[0-9]{2}_v[0-9]+\.md$'; then
      echo "AVISO: '$BASENAME' em archive/ deve seguir {nome}_YYYY-MM-DD_v{N}.md" >&2
    fi
  else
    if echo "$BASENAME" | grep -qE '_[0-9]{4}-[0-9]{2}-[0-9]{2}_v[0-9]+\.md$'; then
      STABLE=$(echo "$BASENAME" | sed -E 's/_[0-9]{4}-[0-9]{2}-[0-9]{2}_v[0-9]+\.md$/.md/')
      echo "AVISO: '$BASENAME' parece versionado mas está fora de archive/." >&2
      echo "Vigente deve ter nome estável: '$STABLE'. Mova versões antigas para archive/." >&2
    fi
  fi
fi

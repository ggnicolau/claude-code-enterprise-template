#!/bin/bash
INPUT=$(cat)
FILE=$(echo "$INPUT" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('tool_input',{}).get('file_path',''))" 2>/dev/null)

[ -z "$FILE" ] && exit 0

# A2: ruff + black em arquivos .py
if [[ "$FILE" == *.py ]]; then
  ruff check --fix "$FILE" 2>/dev/null || true
  black "$FILE" 2>/dev/null || true
fi

# A3: gerar PDF/DOCX/PPTX em arquivos .md dentro de docs/
if [[ "$FILE" == *docs/*.md ]]; then
  node "$CLAUDE_PROJECT_DIR/scripts/generate_docs.js" "$FILE" 2>/dev/null || true
fi

# A4: convenção de nome — docs/*.md fora de archive/ deve seguir *_YYYY-MM-DD_v*.md
if [[ "$FILE" == *docs/*.md ]] && [[ "$FILE" != */archive/* ]]; then
  BASENAME=$(basename "$FILE")
  if ! echo "$BASENAME" | grep -qE '^.+_[0-9]{4}-[0-9]{2}-[0-9]{2}_v[0-9]+\.md$'; then
    echo "AVISO: '$BASENAME' não segue a convenção de nome obrigatória." >&2
    echo "Renomeie para: {nome}_YYYY-MM-DD_v1.md (ex: $(echo "$BASENAME" | sed 's/\.md$//')_$(date +%Y-%m-%d)_v1.md)" >&2
  fi
fi

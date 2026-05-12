#!/bin/bash
# Hook PostToolUse[TeamDelete] — exporta transcript completo do agent team.
#
# Le team_name do tool_response do TeamDelete e delega para export_team_transcript.py,
# que usa o registro deixado pelo team_create_register.sh (PreToolUse[TeamCreate])
# para descobrir start_ts e session_id.

INPUT=$(cat)

TEAM_NAME=$(echo "$INPUT" | python -c "import json,sys; d=json.load(sys.stdin); r=d.get('tool_response',{}); print(r.get('team_name','') if isinstance(r,dict) else '')" 2>/dev/null)

[ -z "$TEAM_NAME" ] && exit 0

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"

python "$PROJECT_DIR/scripts/hooks/export_team_transcript.py" \
  --team "$TEAM_NAME" \
  --project-root "$PROJECT_DIR" 2>&1 | head -20

exit 0

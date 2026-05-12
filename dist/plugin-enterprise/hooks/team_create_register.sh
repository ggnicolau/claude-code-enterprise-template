#!/bin/bash
# Hook PreToolUse[TeamCreate] — registra inicio do team para exportacao posterior.
#
# Grava em .claude/team_runs/<team-name>.json: { start_ts, session_id }.
# O hook PostToolUse[TeamDelete] usa esse arquivo para filtrar JSONLs por janela
# temporal (todos os teammates rodaram entre start_ts e agora).

INPUT=$(cat)

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel)}"
RUNS_DIR="$PROJECT_DIR/.claude/team_runs"
mkdir -p "$RUNS_DIR"

python - "$INPUT" "$RUNS_DIR" <<'PYEOF'
import json, sys, os
from datetime import datetime, timezone
from pathlib import Path

raw_input = sys.argv[1]
runs_dir = Path(sys.argv[2])

try:
    d = json.loads(raw_input)
except json.JSONDecodeError:
    sys.exit(0)

team_name = (d.get("tool_input") or {}).get("team_name")
if not team_name:
    sys.exit(0)

session_id = d.get("session_id", "")
now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

target = runs_dir / f"{team_name}.json"
target.write_text(json.dumps({
    "team_name": team_name,
    "start_ts": now,
    "session_id": session_id,
}), encoding="utf-8")
print(f"[team-create-register] {team_name} registrado: start={now}")
PYEOF

exit 0

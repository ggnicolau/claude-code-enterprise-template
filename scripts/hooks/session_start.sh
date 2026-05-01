#!/bin/bash
# A1: Exibir kanban — apenas em projetos filhos (não no template)
if [ ! -f "$CLAUDE_PROJECT_DIR/scripts/new_repo.py" ]; then
  GH_TOKEN_VAL=$(grep GH_TOKEN "$CLAUDE_PROJECT_DIR/.env" 2>/dev/null | cut -d= -f2)
  export GH_TOKEN="${GH_TOKEN:-$GH_TOKEN_VAL}"

  if command -v gh &>/dev/null && [ -n "$GH_TOKEN" ]; then
    OWNER=$(gh repo view --json owner -q .owner.login 2>/dev/null) || true
    REPO=$(gh repo view --json name -q .name 2>/dev/null) || true
    if [ -n "$OWNER" ]; then
      # Lê project-number do kanban_ids.md se existir (evita gh project list a cada sessão)
      KANBAN_IDS="$CLAUDE_PROJECT_DIR/.claude/memory/kanban_ids.md"
      PROJECT_NUMBER=""
      if [ -f "$KANBAN_IDS" ]; then
        PROJECT_NUMBER=$(grep -oP '(?<=\*\*project-number\*\*: )\d+' "$KANBAN_IDS" 2>/dev/null) || true
      fi
      # Fallback: descobrir via gh project list (projeto novo sem kanban_ids.md)
      if [ -z "$PROJECT_NUMBER" ]; then
        PROJECT_NUMBER=$(gh project list --owner "$OWNER" --format json 2>/dev/null | \
          python3 -c "import json,sys; data=json.load(sys.stdin); repo='$REPO'; print(next((str(p['number']) for p in data.get('projects',[]) if p['title'] == repo + ' Kanban'), ''))" 2>/dev/null) || true
      fi
      if [ -n "$PROJECT_NUMBER" ]; then
        BOARD_TMP=$(mktemp)
        CLOSED_TMP=$(mktemp)
        gh project item-list "$PROJECT_NUMBER" --owner "$OWNER" --format json --limit 100 > "$BOARD_TMP" 2>/dev/null || true
        gh issue list --repo "$OWNER/$REPO" --state closed --json number,closedAt,title --jq '[.[] | {number: .number, closedAt: .closedAt, title: .title}]' > "$CLOSED_TMP" 2>/dev/null || true
        PYTHONIOENCODING=utf-8 python3 - "$BOARD_TMP" "$CLOSED_TMP" << 'PYEOF'
import json, sys

board = json.load(open(sys.argv[1], encoding='utf-8'))
try:
    closed_list = json.load(open(sys.argv[2], encoding='utf-8'))
    closed_map = {i['number']: {'closedAt': i.get('closedAt', ''), 'title': i.get('title', '')} for i in closed_list}
    closed_nums = set(closed_map.keys())
except:
    closed_map = {}
    closed_nums = set()

items = board.get('items', [])
by_status = {}
for item in items:
    status = item.get('status') or 'No Status'
    by_status.setdefault(status, []).append(item)

# Últimas entregas: issues fechadas ordenadas por closedAt desc (top 5)
recently_closed = sorted(
    closed_nums,
    key=lambda num: closed_map[num]['closedAt'], reverse=True
)[:5]
if recently_closed:
    board_title_map = {item.get('content', {}).get('number', ''): item.get('title', '') for item in items}
    print('\n[RECENTES] Ultimas entregas:')
    for num in recently_closed:
        info = closed_map[num]
        date = info['closedAt'][:10] if info['closedAt'] else ''
        title = board_title_map.get(num) or info['title']
        suffix = f' — {date}' if date else ''
        print(f'  #{num} {title}{suffix}')

# Cards em Done com issue ainda aberta — também são entregas realizadas
done_open = [item for item in by_status.get('Done', [])
             if item.get('content', {}).get('number', '') not in closed_nums
             and item.get('content', {}).get('number', '')]
if done_open:
    print('\n[DONE] Done (issue ainda aberta — entrega realizada):')
    for item in done_open:
        number = item.get('content', {}).get('number', '')
        title = item.get('title', '')
        print(f'  #{number} {title}')

order = ['In Progress', 'Review', 'Todo', 'Backlog', 'No Status']
for status in order:
    if status not in by_status:
        continue
    label = {'In Progress':'[IN PROGRESS]','Review':'[REVIEW]','Todo':'[TODO]','Backlog':'[BACKLOG]','No Status':'[NO STATUS]'}.get(status, '•')
    print(f'\n{label} {status}:')
    for item in by_status[status]:
        title = item.get('title', '')
        content = item.get('content', {})
        number = content.get('number', '')
        flag = ''
        if number and number in closed_nums:
            flag = ' WARNING: issue fechada mas card nao esta em Done'
        print(f'  #{number} {title}{flag}')
PYEOF
        rm -f "$BOARD_TMP" "$CLOSED_TMP"
      fi
    fi
  fi
fi

# G: Instalar dependências do projeto — apenas em sessões cloud
if [ "$CLAUDE_CODE_REMOTE" = "true" ]; then
  cd "$CLAUDE_PROJECT_DIR" || exit 0
  echo "☁️  Sessão cloud — instalando dependências..."
  pip install -r requirements.txt --quiet 2>/dev/null || true
  [ -d node_modules ] || npm install --silent 2>/dev/null || true
  service postgresql start 2>/dev/null || true
  service redis-server start 2>/dev/null || true
  echo "✅ Ambiente cloud pronto."
fi

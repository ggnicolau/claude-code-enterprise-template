"""Exporta transcript completo de um agent team para project/docs/.

Disparado pelo hook PostToolUse[TeamDelete] em .claude/settings.json.

Estrategia (com auxilio do hook PreToolUse[TeamCreate]):
1. Le .claude/team_runs/<team-name>.json (gravado pelo team_create_register.sh)
   para descobrir start_ts e session_id do team.
2. Localiza ~/.claude/projects/<project-hash>/<session-id>/subagents/.
3. Filtra JSONLs com primeiro evento entre start_ts e agora; aceita os que
   tem papel valido (ROLE_REGEX bate). Janela temporal pega todos os
   teammates, mesmo quando o brief inicial nao menciona team_name.
4. Pega o maior JSONL por papel (snapshot final completo).
5. Extrai SendMessage outbound + user messages com <teammate-message>.
6. Adiciona PM outbound/inbound da sessao pai.
7. Deduplica e ordena cronologicamente.
8. Filtra mensagens protocolares (idle_notification, shutdown_*).
9. Gera markdown em project/docs/business/project-manager/team_<team-name>.md
   (se ja existir, arquiva a versao anterior em archive/).
10. Apaga .claude/team_runs/<team-name>.json (cleanup).

Uso (via hook):
  python export_team_transcript.py --team <name> --project-root <repo>
"""
from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def find_subagents_dir(project_root: Path, session_id: str) -> Path | None:
    """Procura subagents dir via session_id."""
    home = Path.home()
    base = home / ".claude" / "projects"
    if not base.exists() or not session_id:
        return None
    for project_dir in base.iterdir():
        if not project_dir.is_dir():
            continue
        candidate = project_dir / session_id / "subagents"
        if candidate.exists():
            return candidate
    return None


def find_parent_session_jsonl(session_id: str) -> Path | None:
    home = Path.home()
    base = home / ".claude" / "projects"
    if not base.exists() or not session_id:
        return None
    for project_dir in base.iterdir():
        if not project_dir.is_dir():
            continue
        candidate = project_dir / f"{session_id}.jsonl"
        if candidate.exists():
            return candidate
    return None


def load_jsonl(path: Path) -> list[dict]:
    out = []
    try:
        with open(path, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    except OSError:
        pass
    return out


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(it.get("text", "") for it in content if isinstance(it, dict) and it.get("type") == "text")
    return str(content)


ROLE_REGEX = re.compile(r"Você é o \*\*`([a-z-]+)`\*\*")


def normalize_ts(ts: str) -> str:
    """Normaliza timestamps para comparacao lexicografica robusta.

    Remove sufixo 'Z' e fracao de segundos. '2026-05-12T02:35:00Z' e
    '2026-05-12T02:35:00.123Z' viram '2026-05-12T02:35:00'.
    """
    if not ts:
        return ts
    # Tira Z final
    if ts.endswith("Z"):
        ts = ts[:-1]
    # Tira fracao
    if "." in ts:
        ts = ts.split(".", 1)[0]
    return ts


def role_and_first_ts(jsonl_path: Path) -> tuple[str | None, str | None]:
    """Retorna (role, first_event_timestamp) do JSONL, ou (None, None) se nao for um teammate."""
    try:
        with open(jsonl_path, encoding='utf-8') as f:
            first = f.readline()
        ev = json.loads(first)
    except (OSError, json.JSONDecodeError, StopIteration):
        return None, None
    text = extract_text(ev.get("message", {}).get("content", ""))
    m = ROLE_REGEX.search(text)
    if not m:
        return None, None
    return m.group(1), ev.get("timestamp", "")


def pick_largest_per_role(subagents_dir: Path, start_ts: str, end_ts: str | None) -> dict[str, Path]:
    """Aceita JSONLs com papel valido e primeiro evento na janela [start_ts, end_ts)."""
    start_n = normalize_ts(start_ts)
    end_n = normalize_ts(end_ts) if end_ts else None
    by_role: dict[str, list[tuple[int, Path]]] = defaultdict(list)
    for jsonl in sorted(subagents_dir.glob("agent-*.jsonl")):
        role, ts = role_and_first_ts(jsonl)
        if not role or not ts:
            continue
        ts_n = normalize_ts(ts)
        if ts_n < start_n:
            continue
        if end_n and ts_n > end_n:
            continue
        by_role[role].append((jsonl.stat().st_size, jsonl))
    return {role: sorted(files)[-1][1] for role, files in by_role.items()}


def extract_outbound(events: list[dict], from_role: str, start_ts: str, end_ts: str | None) -> list[dict]:
    out = []
    for ev in events:
        if ev.get("type") != "assistant":
            continue
        ts = ev.get("timestamp", "")
        ts_n = normalize_ts(ts)
        if ts_n < normalize_ts(start_ts) or (end_ts and ts_n > normalize_ts(end_ts)):
            continue
        content = ev.get("message", {}).get("content")
        if not isinstance(content, list):
            continue
        for item in content:
            if isinstance(item, dict) and item.get("type") == "tool_use" and item.get("name") == "SendMessage":
                inp = item.get("input", {})
                out.append({
                    "from": from_role,
                    "to": inp.get("to"),
                    "summary": inp.get("summary"),
                    "message": inp.get("message"),
                    "timestamp": ts,
                })
    return out


def extract_inbound(events: list[dict], to_role: str, start_ts: str, end_ts: str | None) -> list[dict]:
    out = []
    for ev in events:
        if ev.get("type") != "user":
            continue
        ts = ev.get("timestamp", "")
        ts_n = normalize_ts(ts)
        if ts_n < normalize_ts(start_ts) or (end_ts and ts_n > normalize_ts(end_ts)):
            continue
        text = extract_text(ev.get("message", {}).get("content"))
        m = re.search(r'<teammate-message teammate_id="([^"]+)"[^>]*>(.*?)</teammate-message>', text, re.DOTALL)
        if not m:
            continue
        sender, body = m.group(1), m.group(2).strip()
        body_json = None
        if body.startswith("{"):
            try:
                body_json = json.loads(body)
            except json.JSONDecodeError:
                pass
        out.append({
            "from": sender,
            "to": to_role,
            "summary": None,
            "message": body_json if body_json else body,
            "timestamp": ts,
        })
    return out


def is_protocol_message(msg) -> bool:
    if isinstance(msg, dict):
        if msg.get("type") in ("shutdown_request", "shutdown_response", "shutdown_approved", "idle_notification"):
            return True
    if isinstance(msg, str):
        s = msg.strip()
        for p in ('{"type": "shutdown_', '{"type":"shutdown_', '{"type": "idle_notification"', '{"type":"idle_notification"'):
            if s.startswith(p):
                return True
    return False


def archive_existing(target: Path) -> Path | None:
    if not target.exists():
        return None
    archive_dir = target.parent / "archive"
    archive_dir.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    base = target.stem
    pattern = re.compile(rf"^{re.escape(base)}_\d{{4}}-\d{{2}}-\d{{2}}_v(\d+)\.md$")
    versions = []
    for f in archive_dir.glob(f"{base}_*_v*.md"):
        m = pattern.match(f.name)
        if m:
            versions.append(int(m.group(1)))
    n = (max(versions) + 1) if versions else 1
    archived = archive_dir / f"{base}_{today}_v{n}.md"
    shutil.move(str(target), str(archived))
    return archived


def build_markdown(messages: list[dict], team_name: str) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "---",
        f"title: Agent Team — {team_name} (transcript)",
        "authors:",
        "  - project-manager",
        f"created: {today}",
        f"updated: {today}",
        "---",
        "",
        f"# Agent Team — `{team_name}` (transcript)",
        "",
        "Transcript exportado automaticamente pelo hook `PostToolUse[TeamDelete]` ao encerrar o team. Janela temporal definida por `PreToolUse[TeamCreate]` (start) e o momento do delete (end).",
        "",
        "## Sobre a extração",
        "",
        "Cada teammate teve múltiplas \"invocations\" (uma por turno de mensagem recebida); cada invocation gerou um JSONL próprio em `~/.claude/projects/.../subagents/`. O maior JSONL de cada papel é o snapshot final completo.",
        "",
        "**Filtros:** `idle_notification` e `shutdown_*` removidos (ruído protocolar).",
        "",
        "**Dedup:** mensagens que aparecem como outbound em A e inbound em B foram consolidadas.",
        "",
        "---",
        "",
    ]
    msg_idx = 0
    for c in messages:
        msg_content = c.get("message")
        if is_protocol_message(msg_content):
            continue
        msg_idx += 1
        ts = c.get("timestamp", "")
        ts_str = ""
        if ts:
            try:
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                ts_str = dt.strftime("%Y-%m-%d %H:%M:%S")
            except (ValueError, AttributeError):
                ts_str = ts[:19] if isinstance(ts, str) else ""
        lines.append(f"## #{msg_idx} — **{c['from']}** → **{c['to']}**" + (f" · `{ts_str}`" if ts_str else ""))
        if c.get("summary"):
            lines.append(f"*summary: {c['summary']}*")
        lines.append("")
        if isinstance(msg_content, str):
            lines.append(msg_content)
        else:
            lines.append("```json")
            lines.append(json.dumps(msg_content, ensure_ascii=False, indent=2))
            lines.append("```")
        lines.append("")
        lines.append("---")
        lines.append("")
    lines.extend([
        "",
        "## Estatísticas",
        "",
        f"- Total de mensagens não-protocolares: **{msg_idx}**",
        f"- Team name: `{team_name}`",
        f"- Exportado em: {today}",
        "",
    ])
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", required=True)
    ap.add_argument("--project-root", required=True)
    args = ap.parse_args()

    project_root = Path(args.project_root)
    runs_dir = project_root / ".claude" / "team_runs"
    run_file = runs_dir / f"{args.team}.json"

    if not run_file.exists():
        print(f"[export-team-transcript] arquivo de run nao encontrado: {run_file} — pulando")
        return 0

    try:
        run_data = json.loads(run_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"[export-team-transcript] erro lendo {run_file}: {e}")
        return 0

    start_ts = run_data.get("start_ts", "")
    session_id = run_data.get("session_id", "")
    end_ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    if not start_ts or not session_id:
        print(f"[export-team-transcript] start_ts ou session_id ausentes em {run_file}")
        return 0

    subagents_dir = find_subagents_dir(project_root, session_id)
    if not subagents_dir:
        print(f"[export-team-transcript] subagents dir nao encontrado para session {session_id}")
        return 0

    role_files = pick_largest_per_role(subagents_dir, start_ts, end_ts)
    if not role_files:
        print(f"[export-team-transcript] nenhum teammate encontrado entre {start_ts} e {end_ts}")
        return 0

    print(f"[export-team-transcript] team={args.team} papeis={list(role_files.keys())} janela=[{start_ts[:19]}, {end_ts[:19]}]")

    all_msgs: list[dict] = []

    parent_jsonl = find_parent_session_jsonl(session_id)
    if parent_jsonl:
        parent = load_jsonl(parent_jsonl)
        all_msgs += extract_outbound(parent, "project-manager", start_ts, end_ts)
        all_msgs += extract_inbound(parent, "project-manager", start_ts, end_ts)

    for role, path in role_files.items():
        events = load_jsonl(path)
        all_msgs += extract_outbound(events, role, start_ts, end_ts)
        all_msgs += extract_inbound(events, role, start_ts, end_ts)

    seen = set()
    unique = []
    for m in all_msgs:
        msg = m["message"]
        ck = json.dumps(msg, sort_keys=True) if isinstance(msg, dict) else str(msg)[:300]
        key = (m["from"], m["to"], m["timestamp"][:19], hash(ck))
        if key in seen:
            continue
        seen.add(key)
        unique.append(m)
    unique.sort(key=lambda m: m["timestamp"])

    out_dir = project_root / "project" / "docs" / "business" / "project-manager"
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"team_{args.team}.md"

    archived = archive_existing(target)
    if archived:
        print(f"[export-team-transcript] vigente arquivado em {archived.name}")

    target.write_text(build_markdown(unique, args.team), encoding='utf-8')
    print(f"[export-team-transcript] OK: {target.name} ({len(unique)} msgs, {target.stat().st_size:,} bytes)")

    # Cleanup do team_runs
    try:
        run_file.unlink()
    except OSError:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())

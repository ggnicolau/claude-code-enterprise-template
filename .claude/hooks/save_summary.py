#!/usr/bin/env python3
"""
Stop/SubagentStop hook: salva resumo da sessão em .claude/memory/sessions/
Não requer ANTHROPIC_API_KEY — extrai informações direto do transcript.
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def read_transcript(transcript_path: str) -> list[dict]:
    events = []
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    except (FileNotFoundError, OSError):
        pass
    return events


def extract_text_blocks(content) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", "").strip())
        return " ".join(parts)
    return ""


def build_summary(events: list[dict], agent_name: str | None = None) -> str:
    user_messages, assistant_messages, tools_used = [], [], set()

    for event in events:
        role = event.get("role", "")
        content = event.get("content", "")

        if role == "user":
            text = extract_text_blocks(content)
            if text and not text.startswith("{"):
                user_messages.append(text[:300])

        elif role == "assistant":
            text = extract_text_blocks(content)
            if text:
                assistant_messages.append(text[:300])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "tool_use":
                        tools_used.add(block.get("name", ""))

    header = f"# Sessão do agente: {agent_name}\n" if agent_name else "# Sessão do usuário\n"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        header,
        f"**Data:** {timestamp}\n",
    ]

    if tools_used:
        lines.append(f"**Ferramentas usadas:** {', '.join(sorted(tools_used))}\n")

    if user_messages:
        lines.append("\n## Últimas mensagens do usuário\n")
        for msg in user_messages[-3:]:
            lines.append(f"- {msg}\n")

    if assistant_messages:
        lines.append("\n## Últimas respostas do assistente\n")
        for msg in assistant_messages[-3:]:
            lines.append(f"- {msg}\n")

    return "".join(lines)


def main() -> int:
    try:
        data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, EOFError):
        return 0

    transcript_path = data.get("transcript_path", "")
    if not transcript_path:
        return 0

    events = read_transcript(transcript_path)
    if not events:
        return 0

    # SubagentStop passa o nome do agente no evento
    agent_name = data.get("agent_name") or data.get("subagent_name")
    is_agent = bool(agent_name)

    summary = build_summary(events, agent_name)

    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", "."))
    subdir = "agents" if is_agent else "user"
    sessions_dir = project_dir / ".claude" / "memory" / "sessions" / subdir
    sessions_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    suffix = f"_{agent_name}" if agent_name else ""
    out = sessions_dir / f"{timestamp}{suffix}.md"
    out.write_text(summary, encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

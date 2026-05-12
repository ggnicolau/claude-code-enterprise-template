"""Adiciona frontmatter YAML obrigatório aos .md migrados do eutanasia.

Regras:
- Se o arquivo já começa com '---', skip
- Senão, adiciona header com title (deriva do nome ou do H1), authors (do mapeamento), created/updated (mtime)
"""

from pathlib import Path
from datetime import datetime
import re

BASE = Path(r"C:\Users\ggnic\work_documents\1.TRABALHO\4.MY_PROJECTS\claude_code_projects\eutanasia")

# Mapeamento: caminho relativo → (title sugerido, agente author)
MAPPING = {
    "project/docs/research/principal-investigator/kickoff.md": ("Kickoff — Discovery da Pesquisa", "principal-investigator"),
    "project/docs/research/literature-reviewer/estado_da_arte.md": ("Estado da Arte", "literature-reviewer"),
    "project/docs/research/philosopher/memo_epistemologico.md": ("Memo Epistemológico", "philosopher"),
    "project/docs/research/methodologist/protocolo_metodologico.md": ("Protocolo Metodológico", "methodologist"),
    "project/docs/research/methodologist/archive/protocolo_metodologico_2026-04-28_v1.md": ("Protocolo Metodológico (v1, arquivada)", "methodologist"),
    "project/docs/research/ethics-officer/parecer_etico.md": ("Parecer Ético", "ethics-officer"),
    "project/docs/research/academic-writer/projeto_posDoc.md": ("Projeto de Pós-Doutoramento — Eutanásia, Biopolítica e Morte Assistida", "academic-writer"),
    "project/docs/research/academic-writer/archive/projeto_posDoc_2026-04-25_v1.md": ("Projeto de Pós-Doutoramento (v1, arquivada)", "academic-writer"),
    "project/docs/research/academic-writer/archive/projeto_posDoc_2026-04-26_v2.md": ("Projeto de Pós-Doutoramento (v2, arquivada)", "academic-writer"),
    "project/docs/research/academic-writer/archive/projeto_posDoc_2026-04-27_v3.md": ("Projeto de Pós-Doutoramento (v3, arquivada)", "academic-writer"),
    "project/docs/research/academic-writer/archive/projeto_posDoc_2026-04-28_v4.md": ("Projeto de Pós-Doutoramento (v4, arquivada)", "academic-writer"),
    "project/docs/external-writings/own-writings/tese_doutorado/00_consolidado.md": ("Tese de Doutorado — Consolidado", "literature-reviewer"),
    "project/docs/external-writings/own-writings/tese_doutorado/01_philosopher_teoria.md": ("Tese de Doutorado — Memo de Teoria (philosopher)", "philosopher"),
    "project/docs/external-writings/own-writings/tese_doutorado/02_anthropologist_etnografia.md": ("Tese de Doutorado — Memo de Etnografia (anthropologist)", "anthropologist"),
    "project/docs/external-writings/own-writings/tese_doutorado/03_political-scientist_atores.md": ("Tese de Doutorado — Memo de Atores (political-scientist)", "political-scientist"),
    "project/docs/external-writings/own-writings/tese_doutorado/04_data-scientist_metodos.md": ("Tese de Doutorado — Memo de Métodos (data-scientist)", "data-scientist"),
    "project/docs/external-writings/own-writings/tese_doutorado/05_literature-reviewer_bibliografia.md": ("Tese de Doutorado — Memo de Bibliografia (literature-reviewer)", "literature-reviewer"),
    "project/docs/external-writings/own-writings/tese_doutorado/06_philosopher_cap5_seguranca_humana.md": ("Tese de Doutorado — Cap. 5 Segurança Humana (philosopher)", "philosopher"),
    "project/docs/external-writings/own-writings/tese_doutorado/07_political-scientist_cap5_prefacio.md": ("Tese de Doutorado — Cap. 5 Prefácio (political-scientist)", "political-scientist"),
    "project/docs/external-writings/own-writings/tese_doutorado/08_sociologist_cap1_cap2_prefacio.md": ("Tese de Doutorado — Caps. 1-2 Prefácio (sociologist)", "sociologist"),
    "project/docs/external-writings/own-writings/tese_doutorado/archive/00_consolidado.md": ("Tese de Doutorado — Consolidado (v1, arquivada)", "literature-reviewer"),
    "project/docs/external-writings/own-writings/tese_doutorado/archive/00_consolidado_v2.md": ("Tese de Doutorado — Consolidado (v2, arquivada)", "literature-reviewer"),
}


def has_frontmatter(content):
    return content.startswith("---\n") or content.startswith("﻿---\n")


count_added = 0
count_skipped = 0
count_missing = 0

for rel_path, (title, author) in MAPPING.items():
    path = BASE / rel_path
    if not path.exists():
        print(f"[MISS] {rel_path}")
        count_missing += 1
        continue
    content = path.read_text(encoding="utf-8")
    if has_frontmatter(content):
        print(f"[SKIP] {rel_path} (already has frontmatter)")
        count_skipped += 1
        continue
    # Get mtime as created/updated
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    date_str = mtime.strftime("%Y-%m-%d")
    frontmatter = f"""---
title: {title}
authors:
  - {author}
created: {date_str}
updated: {date_str}
---

"""
    path.write_text(frontmatter + content, encoding="utf-8")
    count_added += 1
    print(f"[OK] {rel_path}")

print(f"\nAdded: {count_added}")
print(f"Skipped (already has): {count_skipped}")
print(f"Missing: {count_missing}")

"""Expande o bloco de Skills nos 22 agentes especialistas do social-sciences-template.

Adiciona skills de domínio (do projeto) + skills Anthropic + skills de plugins
relevantes para cada agente. Substitui o bloco '## Skills' inteiro.

Skills locais (em .agents/skills/<nome>/SKILL.md):
- Domínio: academic-writing, peer-review, literature-review, qualitative-coding,
  research-design, research-ethics, dissemination, data-collection, data-pipeline,
  data-analysis, data-science, statistical-analysis
- Áreas: anthropology, communication, economics, history, international-relations,
  legal-research, linguistics, philosophy, political-science, social-psychology,
  sociology

Anthropic skills (plugins instalados):
- anthropic-skills:pdf, anthropic-skills:docx, anthropic-skills:pptx, anthropic-skills:xlsx
- anthropic-skills:consolidate-memory, anthropic-skills:schedule
- engineering:architecture, engineering:debug, engineering:documentation,
  engineering:system-design, engineering:tech-debt, engineering:code-review,
  engineering:standup
- product-management:write-spec, product-management:metrics-review,
  product-management:stakeholder-update, product-management:synthesize-research
- productivity:task-management, productivity:memory-management
- data:analyze, data:write-query, data:explore-data, data:validate-data,
  data:statistical-analysis, data:data-visualization
- claude-api
"""

from pathlib import Path
import re

BASE = Path(
    r"C:\Users\ggnic\work_documents\1.TRABALHO\4.MY_PROJECTS\claude_code_projects\claude-code-social-sciences-template\scripts\templates\agents"
)

# Cada agente recebe: (skills_locais, skills_anthropic_e_plugins)
SKILL_MAP = {
    # === CIENTÍFICOS (research/) ===
    "methodologist": (
        ["research-design", "data-collection", "literature-review"],
        ["product-management:write-spec", "anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "philosopher": (
        ["philosophy", "literature-review"],
        ["anthropic-skills:pdf", "anthropic-skills:docx", "productivity:memory-management"],
    ),
    "ethics-officer": (
        ["research-ethics", "research-design"],
        ["anthropic-skills:pdf", "anthropic-skills:docx", "product-management:write-spec"],
    ),
    "literature-reviewer": (
        ["literature-review", "research-design"],
        ["anthropic-skills:pdf", "anthropic-skills:xlsx", "productivity:memory-management"],
    ),
    "qualitative-analyst": (
        ["qualitative-coding", "data-collection", "research-design"],
        ["anthropic-skills:docx", "anthropic-skills:xlsx"],
    ),
    "quantitative-analyst": (
        ["statistical-analysis", "data-analysis", "research-design"],
        ["data:statistical-analysis", "data:data-visualization", "data:validate-data",
         "anthropic-skills:xlsx", "anthropic-skills:pdf"],
    ),
    "academic-writer": (
        ["academic-writing", "literature-review"],
        ["anthropic-skills:pdf", "anthropic-skills:docx",
         "engineering:documentation", "productivity:task-management"],
    ),
    "peer-reviewer": (
        ["peer-review", "academic-writing", "research-design"],
        ["engineering:code-review", "anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "dissemination-strategist": (
        ["dissemination", "academic-writing"],
        ["product-management:stakeholder-update", "product-management:synthesize-research",
         "anthropic-skills:pptx", "anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    # === DOMÍNIO (domain/) ===
    "political-scientist": (
        ["political-science", "literature-review", "qualitative-coding"],
        ["anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "sociologist": (
        ["sociology", "literature-review", "qualitative-coding"],
        ["anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "anthropologist": (
        ["anthropology", "qualitative-coding", "data-collection"],
        ["anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "legal-scholar": (
        ["legal-research", "literature-review"],
        ["anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "linguist": (
        ["linguistics", "qualitative-coding", "data-collection"],
        ["anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "ir-scholar": (
        ["international-relations", "literature-review", "qualitative-coding"],
        ["anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "economist": (
        ["economics", "statistical-analysis", "data-analysis"],
        ["data:statistical-analysis", "data:data-visualization",
         "anthropic-skills:xlsx", "anthropic-skills:pdf"],
    ),
    "historian": (
        ["history", "literature-review", "qualitative-coding"],
        ["anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "social-psychologist": (
        ["social-psychology", "statistical-analysis", "qualitative-coding"],
        ["data:statistical-analysis", "anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "communication-scholar": (
        ["communication", "qualitative-coding", "literature-review"],
        ["anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    "urbanist": (
        ["sociology", "literature-review", "qualitative-coding"],
        ["data:data-visualization", "anthropic-skills:pdf", "anthropic-skills:docx"],
    ),
    # === TÉCNICOS (tech/) ===
    "data-engineer": (
        ["data-pipeline", "data-collection"],
        ["data:write-query", "data:explore-data", "data:validate-data",
         "engineering:architecture", "engineering:debug", "engineering:documentation",
         "claude-api"],
    ),
    "data-scientist": (
        ["data-science", "data-analysis", "statistical-analysis"],
        ["data:analyze", "data:statistical-analysis", "data:data-visualization",
         "data:validate-data", "engineering:debug", "claude-api"],
    ),
    "data-analyst": (
        ["data-analysis", "data-pipeline"],
        ["data:analyze", "data:explore-data", "data:data-visualization",
         "anthropic-skills:xlsx", "anthropic-skills:pdf"],
    ),
}


def build_skills_block(local_skills, plugin_skills):
    lines = ["## Skills", ""]
    for s in local_skills:
        lines.append(f"- [`{s}`](../../.agents/skills/{s}/SKILL.md)")
    for s in plugin_skills:
        # Comentário descritivo curto por skill mais comum
        comment = {
            "anthropic-skills:pdf": "produzir relatórios PDF (com TOC, KaTeX, Mermaid)",
            "anthropic-skills:docx": "produzir documentos Word (manuscritos, pareceres)",
            "anthropic-skills:pptx": "produzir apresentações executivas",
            "anthropic-skills:xlsx": "produzir planilhas (matriz de revisão, codificação, tabelas)",
            "anthropic-skills:consolidate-memory": "pass reflexivo sobre memória",
            "anthropic-skills:schedule": "agendar tarefas recorrentes",
            "engineering:architecture": "criar/avaliar ADR (architecture decision record)",
            "engineering:system-design": "design de pipelines e arquitetura técnica",
            "engineering:tech-debt": "identificar e priorizar dívida técnica",
            "engineering:code-review": "review estruturado de PR",
            "engineering:documentation": "escrever/manter documentação técnica",
            "engineering:debug": "sessão estruturada de debug",
            "engineering:standup": "gerar update a partir de atividade recente",
            "product-management:write-spec": "escrever PRD/spec estruturado",
            "product-management:metrics-review": "review estruturado de métricas",
            "product-management:stakeholder-update": "update tailored por audiência",
            "product-management:synthesize-research": "sintetizar entrevistas/surveys em insights",
            "productivity:task-management": "gestão de tarefas via TASKS.md",
            "productivity:memory-management": "sistema de memória de dois níveis",
            "data:analyze": "análise estatística com Python",
            "data:write-query": "escrever queries SQL otimizadas",
            "data:explore-data": "exploração inicial de datasets",
            "data:validate-data": "validar qualidade e integridade de dados",
            "data:statistical-analysis": "análises estatísticas avançadas",
            "data:data-visualization": "produzir visualizações de dados",
            "claude-api": "construir/debugar apps Claude API + Anthropic SDK",
        }.get(s, "")
        suffix = f" — {comment}" if comment else ""
        lines.append(f"- [`{s}`]{suffix}")
    return "\n".join(lines)


pattern = re.compile(r"## Skills\n.*?(?=\n## )", re.DOTALL)

count = 0
for slug, (local, plugins) in SKILL_MAP.items():
    path = BASE / f"{slug}.md"
    if not path.exists():
        print(f"[WARN] {slug}.md not found")
        continue
    content = path.read_text(encoding="utf-8")
    new_block = build_skills_block(local, plugins) + "\n"
    if not pattern.search(content):
        print(f"[WARN] {slug}.md: ## Skills not found, skipping")
        continue
    new_content = pattern.sub(new_block, content, count=1)
    path.write_text(new_content, encoding="utf-8")
    count += 1
    n_total = len(local) + len(plugins)
    print(f"[OK] {slug}.md - {n_total} skills ({len(local)} local + {len(plugins)} plugin)")

print(f"\nTotal: {count} agents updated")

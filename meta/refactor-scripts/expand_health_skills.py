"""Expande skills nos 60 agentes clínicos do health-template.

Não toca em: principal-investigator, research-coordinator, tech-lead, 11 research,
3 tech (já têm skills adequadas).

Skills universais para todos clínicos:
- literature-review (revisão clínica é essencial)
- peer-review (análise crítica de pareceres/condutas)
- anthropic-skills:pdf
- anthropic-skills:docx

Skills adicionais para cirurgiões/especialistas com forte componente visual:
- anthropic-skills:pptx (apresentações de caso, M&M)
- anthropic-skills:xlsx (séries de casos)

Skills adicionais para especialistas que trabalham com dados quantitativos:
- statistical-analysis
- data:data-visualization
"""

from pathlib import Path
import re

BASE = Path(
    r"C:\Users\ggnic\work_documents\1.TRABALHO\4.MY_PROJECTS\claude_code_projects\claude-code-health-template\scripts\templates\agents"
)

# Cirurgiões — apresentações de caso são comuns
SURGICAL = {
    "cardiovascular-surgeon", "digestive-surgeon", "general-surgeon", "hand-surgeon",
    "head-neck-surgeon", "neurosurgeon", "oncologic-surgeon", "pediatric-surgeon",
    "plastic-surgeon", "thoracic-surgeon", "vascular-surgeon", "coloproctologist",
    "mastologist", "orthopedist", "urologist", "gynecologist-obstetrician",
}

# Especialistas com forte componente de imagem/diagnóstico
DIAGNOSTIC_IMAGING = {
    "radiologist", "radiotherapist", "nuclear-medicine", "pathologist",
    "clinical-pathologist", "endoscopist", "dermatologist", "ophthalmologist",
}

# Especialistas com forte componente quantitativo/estatístico
QUANTITATIVE_HEAVY = {
    "epidemiologist", "infectologist", "intensivist", "pediatric-intensivist",
    "preventive-medicine", "occupational-physician", "traffic-medicine",
    "cardiologist", "endocrinologist", "nephrologist",
}

# Especialidades a NÃO mexer (já têm skills do refactor_health_agents.py)
SKIP = {
    "principal-investigator", "research-coordinator", "tech-lead",
    "academic-writer", "biostatistician", "dissemination-strategist",
    "epidemiologist", "ethics-officer", "health-economist", "legal-medicine",
    "literature-reviewer", "peer-reviewer", "preventive-medicine",
    "qualitative-analyst", "data-engineer", "data-scientist", "data-analyst",
}

# Skills universais para todos clínicos
UNIVERSAL_CLINICAL = [
    ("literature-review", None, True),  # local skill
    ("peer-review", None, True),
    ("anthropic-skills:pdf", "produzir pareceres em PDF", False),
    ("anthropic-skills:docx", "produzir documentos Word (relatórios clínicos, laudos)", False),
]


def get_skills_for(slug):
    """Retorna lista de skills (slug, comment, is_local) para o agente."""
    skills = list(UNIVERSAL_CLINICAL)
    if slug in SURGICAL:
        skills.append(("anthropic-skills:pptx", "apresentações de caso, M&M", False))
        skills.append(("anthropic-skills:xlsx", "séries de casos, planilhas de seguimento", False))
    if slug in DIAGNOSTIC_IMAGING:
        skills.append(("anthropic-skills:xlsx", "planilhas de achados, controle de qualidade", False))
    if slug in QUANTITATIVE_HEAVY:
        skills.append(("statistical-analysis", None, True))
        skills.append(("data:data-visualization", "visualizações de dados clínicos/epidemiológicos", False))
        skills.append(("anthropic-skills:xlsx", "tabelas estatísticas, planilhas de coorte", False))
    # Dedup mantendo ordem
    seen = set()
    out = []
    for s in skills:
        if s[0] not in seen:
            seen.add(s[0])
            out.append(s)
    return out


def build_skills_block(skills_list):
    lines = ["## Skills", ""]
    for slug, comment, is_local in skills_list:
        if is_local:
            lines.append(f"- [`{slug}`](../../.agents/skills/{slug}/SKILL.md)")
        else:
            suffix = f" — {comment}" if comment else ""
            lines.append(f"- [`{slug}`]{suffix}")
    return "\n".join(lines)


pattern = re.compile(r"## Skills\n.*?(?=\n## )", re.DOTALL)

count = 0
for path in sorted(BASE.glob("*.md")):
    slug = path.stem
    if slug in SKIP:
        continue
    content = path.read_text(encoding="utf-8")
    if not pattern.search(content):
        print(f"[WARN] {slug}.md: ## Skills not found, skipping")
        continue
    skills_list = get_skills_for(slug)
    new_block = build_skills_block(skills_list) + "\n"
    new_content = pattern.sub(new_block, content, count=1)
    path.write_text(new_content, encoding="utf-8")
    count += 1
    print(f"[OK] {slug}.md - {len(skills_list)} skills")

print(f"\nTotal: {count} clinical agents updated")

# meta/refactor-scripts/

Scripts ad-hoc usados em **refactors históricos** dos templates. Não fazem parte da infraestrutura recorrente do template — são one-off, preservados como registro de como decisões grandes foram operacionalizadas.

Não rodar em produção. Se um refactor similar for necessário no futuro, partir destes scripts como base e adaptar.

## Scripts disponíveis

### Refactor social-sciences-template (Fases 2.1 → 2.6 + 2.5)
Diagnóstico: [`../refactor_social_sciences_diagnostic.md`](../refactor_social_sciences_diagnostic.md)

- **`refactor_social_agents.py`** — gerou os 22 agentes especialistas do social com frontmatter YAML + estrutura completa (organograma, cadeia de comando, skills, pasta dedicada, critério do leitor primário).
- **`expand_social_skills.py`** — expandiu o bloco `## Skills` dos 23 especialistas (PI/RC/TL não tocados) adicionando skills locais + Anthropic + plugins relevantes.

### Refactor health-template (Fase 3)
- **`refactor_health_agents.py`** — gerou os 74 agentes especialistas do health (11 research + 60 clinical + 3 tech) com a mesma estrutura. Inclui mapeamento de especialidades médicas com descrição.
- **`expand_health_skills.py`** — expandiu skills nos 60 clínicos com perfis específicos (cirurgiões, diagnóstico/imagem, quantitativo-intensivos).

### Migração de projeto filho (eutanasia)
- **`add_frontmatter_eutanasia.py`** — adicionou frontmatter YAML em 22 .md migrados durante o refactor do projeto filho eutanasia (mapeamento de cada arquivo para seu agente "owner").

## Quando usar

- **Reproduzir refactor em outro template:** copiar o script, ajustar o `BASE` path e o mapeamento de agentes/skills, rodar.
- **Migrar novo projeto filho:** adaptar `add_frontmatter_eutanasia.py` com o mapeamento de docs do novo projeto.
- **Auditoria histórica:** ler junto com `meta/refactor_social_sciences_diagnostic.md` para entender as decisões.

## Convenção

- Caminhos absolutos hardcoded são intencionais (scripts one-off, não reusáveis sem ajuste)
- Output em ASCII (Windows console compatível)
- Cada script auto-documentado no docstring

# Skill: Product Management

Padrão para gestão de backlog, priorização e refinamento — usado pelo `product-owner`.

## Quando usar
Ao criar, refinar ou priorizar issues no kanban; ao conduzir discovery de produto.

## Anatomia de uma issue bem definida

1. **Título** — verbo no infinitivo + objeto + contexto (ex: "Implementar autenticação JWT no endpoint de login")
2. **Problema** — qual dor do usuário ou necessidade de negócio justifica esta issue
3. **Critérios de aceitação** — lista verificável do que define "done" (use checkboxes)
4. **Dependências** — outras issues que bloqueiam ou são bloqueadas por esta
5. **Labels obrigatórias** — uma de dimensão (`discovery`, `negocio`, `produto`, `tech`, `lancamento`, `operacoes`) + uma de prioridade (`priority:high`, `priority:medium`, `priority:low`)

## Priorização

| Framework | Quando usar |
|---|---|
| **MoSCoW** | Alinhamento rápido com stakeholders (Must/Should/Could/Won't) |
| **RICE** | Comparação objetiva (Reach × Impact × Confidence / Effort) |
| **Impacto vs. Esforço** | Matriz 2x2 para sprints curtos |

## Boas práticas
- Nenhuma issue sem critério de aceitação verificável
- Backlog sempre em 6 dimensões — identificar lacunas em cada uma
- Issue criada sem vínculo ao GitHub Project é entrega incompleta
- Refinar antes de priorizar — issue ambígua não entra em Todo
- Nunca mover card para Done sem PR mergeado ou entregável commitado
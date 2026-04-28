# Skill: AI Engineering

Padrão para sistemas LLM, agentes e RAG — usado pelo `ai-engineer`.

## Quando usar
Ao projetar prompts, pipelines RAG, avaliações de LLM ou sistemas multi-agentes.

## Decisão de arquitetura

| Abordagem | Quando usar |
|---|---|
| **Prompt simples** | Tarefa bem definida, sem estado, resposta única |
| **Chain** | Múltiplos passos sequenciais com transformação intermediária |
| **RAG** | Precisão factual requer recuperação de contexto externo |
| **Agente com tools** | Tarefa requer decisões dinâmicas e ações no ambiente |
| **Multi-agente** | Tarefas paralelizáveis ou com papéis especializados distintos |

## Checklist de prompts

- [ ] Instrução clara sobre papel, tarefa e formato de saída
- [ ] Exemplos (few-shot) quando o formato for não-trivial
- [ ] Restrições explícitas sobre o que NÃO fazer
- [ ] Prompt cacheável (partes estáticas no início — ver `anthropic-skills:claude-api`)

## Evals mínimas antes de produção

- [ ] Taxa de seguimento de instrução
- [ ] Taxa de alucinação em domínio crítico
- [ ] Latência P50/P95
- [ ] Custo por chamada estimado

## Boas práticas
- Usar prompt caching da Anthropic em contextos longos e repetidos
- Isolar experimentos de prompt em subagentes — evita contaminação do contexto principal
- Versionar prompts junto com o código (`src/prompts/`)
- Documentar evals e resultados em `docs/tech/`
- Monitorar drift de qualidade em produção com amostragem periódica
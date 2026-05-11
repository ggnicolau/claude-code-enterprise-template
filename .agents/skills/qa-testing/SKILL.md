# Skill: QA Testing

Processo e decisão de qualidade — usado pelo `qa`.

## Quando usar
Ao **decidir** estratégia de testes (pirâmide, critério de bloqueio de merge) e **validar cobertura** em PR. Para **escrever testes** seguindo padrões Python (fixtures, parametrização, exemplos), use `testing-patterns`.

## Pirâmide de testes

| Camada | Foco | Ferramenta |
|---|---|---|
| **Unitário** | Função isolada, sem dependências externas | pytest, unittest |
| **Integração** | Interação entre módulos ou com banco/API | pytest + fixtures reais |
| **E2E** | Fluxo completo do usuário | Playwright, Cypress |

## Critérios de bloqueio

**Bloqueia merge (🔴):**
- Caminho principal sem nenhum teste
- Teste que passa mas não testa o comportamento real (mock excessivo)
- Regressão introduzida (teste existente quebrado)

**Deve corrigir (🟡):**
- Cobertura abaixo de 80% em módulo novo
- Casos extremos críticos sem teste (null, lista vazia, timeout)

**Sugestão (🔵):**
- Cobertura pode aumentar
- Teste de property-based (Hypothesis) em lógica complexa

## Boas práticas
- Testar comportamento, não implementação — refactoring não deve quebrar testes
- Fixtures reutilizáveis em `tests/conftest.py`
- Nomes de teste descritivos: `test_<quando>_<resultado_esperado>`
- Rodar `pytest --cov` antes de abrir PR
- Dados de teste em `tests/fixtures/` — nunca dados reais de produção

> **Onde mora**: depende do contexto. Testes específicos de um produto vão em `products/<produto>/tests/`. Testes de lib universal vão em `tests/` raiz (Mundo 1). Ver CLAUDE.md §"Critério do leitor primário".
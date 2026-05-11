# Skill: Testing Patterns

Padrões de código de teste em Python — usado pelo `qa`.

## Quando usar
Ao **escrever testes** seguindo padrões Python (estrutura, fixtures, parametrização). Para **decisão de processo** (pirâmide, critério de bloqueio de merge, cobertura mínima), use `qa-testing`.

## Padrões preferidos

### Estrutura

- Separar testes unitários (função isolada) de testes de integração (fluxo completo)
- Dados de teste em `tests/fixtures/` como arquivos, não inline no código
- Usar `pytest.fixture` com `scope="session"` para recursos caros de inicializar

> **Onde mora**: depende do contexto. Testes específicos de um produto vão em `products/<produto>/tests/`. Testes de lib universal vão em `tests/` raiz (Mundo 1). Ver CLAUDE.md §"Critério do leitor primário".

### Cobertura

- Cobrir: input vazio, input inválido, valores limite
- Testes de regressão para bugs corrigidos
- Parametrizar com `pytest.mark.parametrize` quando o mesmo teste cobre múltiplos casos

## Exemplo

```python
@pytest.fixture(scope="session")
def db_conn():
    return create_connection(":memory:")

def test_insert_returns_id(db_conn):
    result = insert_record(db_conn, {"name": "test"})
    assert result.id is not None
```

## Antipadrões

- Mock excessivo (testa o mock, não o código)
- Teste que depende de ordem de execução (usar fixtures, não estado global)
- Assert genérico (`assert result` em vez de `assert result.status == "ok"`)

# Skill: Testing Patterns for NLP/ML

Padrões de teste para projetos de NLP e ML.

## Quando usar
Ao escrever ou revisar testes para pipelines de texto, modelos, ou transformações de dados.

## Padrões preferidos

### Testes de pipeline NLP
- Testar com inputs reais (não só strings triviais)
- Cobrir: texto vazio, texto muito longo, caracteres especiais, múltiplos idiomas se aplicável
- Separar testes unitários (função isolada) de testes de integração (pipeline completo)

### Testes de modelo
- Testar predições em exemplos fixos conhecidos (regression tests)
- Nunca depender de threshold exato — use margens
- Mockar carregamento de modelo pesado nos testes unitários

### Fixtures
- Usar `pytest.fixture` com `scope="session"` para carregar modelos uma vez
- Dados de teste em `tests/fixtures/` como arquivos, não inline no código

## Exemplo
```python
@pytest.fixture(scope="session")
def nlp_model():
    return load_model("pt_core_news_sm")

def test_ner_finds_person(nlp_model):
    doc = nlp_model("Lula visitou Brasília ontem.")
    pessoas = [e.text for e in doc.ents if e.label_ == "PER"]
    assert len(pessoas) >= 1
```

# Skill: Data Pipeline

Implementação de pipelines de dados em código — usado pelo `data-engineer`.

## Quando usar
Ao **escrever o código** de um pipeline ETL/ELT (estrutura de módulos, validação de schema, padrões Python). Para **decisões arquiteturais** sobre o pipeline (contrato, SLAs, processo), use `data-engineering`.

## Estrutura típica de módulos

```
ingestion/    # leitura de fontes externas
transform/    # limpeza e transformação
load/         # escrita no destino
validation/   # contratos e qualidade
```

> **Onde mora**: depende do contexto. Pipeline específico de um produto vai em `products/<produto>/scripts/` ou `products/<produto>/src/<produto>/` (se for lib importável). Lib reutilizável por múltiplos produtos vai em `src/` raiz (Mundo 1). Ver CLAUDE.md §"Critério do leitor primário".

## Boas práticas

- Separar ingestão, transformação e carga em etapas independentes
- Validar schema na entrada e na saída de cada etapa
- Usar `pathlib.Path` para todos os paths
- Logar volume de registros processados em cada etapa
- Nunca commitar dados brutos — usar `.gitignore`

## Exemplo de validação

```python
def validate_schema(df: pd.DataFrame, required_cols: list[str]) -> None:
    missing = set(required_cols) - set(df.columns)
    if missing:
        raise ValueError(f"Colunas faltando: {missing}")
```

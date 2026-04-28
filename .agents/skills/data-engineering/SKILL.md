# Skill: Data Engineering

Padrão para pipelines, ETL/ELT e qualidade de dados — usado pelo `data-engineer`.

## Quando usar
Ao projetar ou implementar ingestão, transformação e entrega de dados.

## Estrutura de diretórios de dados

```
data/
  raw/          # dados brutos — NUNCA modificar, NUNCA commitar dados sensíveis
  processed/    # dados transformados e prontos para uso
  external/     # fontes externas (APIs, dumps, arquivos recebidos)
```

## Checklist de pipeline

**Ingestão:**
- [ ] Fonte documentada (URL, credencial no `.env`, schema esperado)
- [ ] Tratamento de falha parcial (idempotência)
- [ ] Logging de volume e erros

**Transformação:**
- [ ] Dados brutos preservados em `data/raw/`
- [ ] Transformações em funções puras e testáveis
- [ ] Schema validado (Pydantic ou pandera)
- [ ] Nulos tratados explicitamente

**Entrega:**
- [ ] Dados em `data/processed/` com versionamento ou timestamp
- [ ] Contrato de schema documentado para consumidores downstream

## Boas práticas
- Pipeline reproduzível: mesma entrada → mesma saída
- Nunca commitar dados sensíveis ou identificáveis
- Testar com amostra antes de rodar em volume total
- Documentar dependências externas e SLAs esperados
- Registrar decisões de design em `docs/tech/`
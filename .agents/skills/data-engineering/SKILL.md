# Skill: Data Engineering

Visão arquitetural e processo de dados — usado pelo `data-engineer`.

## Quando usar
Ao **decidir** arquitetura de dados: como estruturar pipeline, qual contrato de dados manter, quais SLAs garantir. Para **implementar** o pipeline em código (estrutura de módulos, exemplos), use `data-pipeline`.

## Estrutura típica de diretórios de dados

```
data/
  raw/          # dados brutos — NUNCA modificar, NUNCA commitar dados sensíveis
  processed/    # dados transformados e prontos para uso
  external/     # fontes externas (APIs, dumps, arquivos recebidos)
```

> **Onde mora**: depende do contexto. Dados específicos de um produto vão em `products/<produto>/data/`. Dados compartilhados entre produtos do mesmo projeto vão em `data/` raiz (Mundo 1). Ver CLAUDE.md §"Critério do leitor primário".

## Checklist de pipeline

**Ingestão:**
- [ ] Fonte documentada (URL, credencial no `.env`, schema esperado)
- [ ] Tratamento de falha parcial (idempotência)
- [ ] Logging de volume e erros

**Transformação:**
- [ ] Dados brutos preservados em `raw/`
- [ ] Transformações em funções puras e testáveis
- [ ] Schema validado (Pydantic ou pandera)
- [ ] Nulos tratados explicitamente

**Entrega:**
- [ ] Dados em `processed/` com versionamento ou timestamp
- [ ] Contrato de schema documentado para consumidores downstream

## Boas práticas

- Pipeline reproduzível: mesma entrada → mesma saída
- Nunca commitar dados sensíveis ou identificáveis
- Testar com amostra antes de rodar em volume total
- Documentar dependências externas e SLAs esperados
- Registrar decisões de design em pasta dedicada do agente (`project/docs/tech/data-engineer/`) ou em `products/<produto>/` se específica do produto

# Skill: ML Engineering

Ciclo completo de modelos: treino → avaliação → produção → monitoramento — usado pelo `ml-engineer`.

## Quando usar
Ao **produtizar um modelo** (preparar para serving, monitoramento, fallback). Para **rigor experimental** (seed, splits sem vazamento, comparação de runs, registro MLflow), use `ml-experiment`.

## Ciclo de experimento

1. **Hipótese** — o que estou testando e por quê espero melhora
2. **Baseline** — métrica atual que o experimento precisa superar
3. **Dados** — split (train/val/test), sem vazamento, reproduzível com seed fixo
4. **Modelo** — arquitetura, hiperparâmetros, justificativa
5. **Avaliação** — métricas alinhadas ao objetivo de negócio (não apenas accuracy)
6. **Registro** — MLflow ou W&B: params, metrics, artifacts

## Checklist de produção

- [ ] Modelo versionado e registrado (não só o `.pkl` local)
- [ ] Pipeline de inferência reproduzível
- [ ] Monitoramento de drift configurado
- [ ] Fallback definido em caso de degradação
- [ ] Latência e consumo de memória dentro do SLA

## Boas práticas
- Seed fixo em todos os experimentos para reprodutibilidade
- Nunca usar test set durante desenvolvimento — apenas na avaliação final
- Documentar suposições sobre os dados de entrada
- Registrar experimentos que *não* funcionaram — evita retrabalho
- Salvar artefatos em `models/` com versionamento explícito

> **Onde mora**: depende do contexto. Modelo específico de um produto vai em `products/<produto>/models/`. Modelo compartilhado entre produtos vai em `models/` raiz (Mundo 1). Ver CLAUDE.md §"Critério do leitor primário".
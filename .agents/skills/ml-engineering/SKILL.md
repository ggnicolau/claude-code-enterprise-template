# Skill: ML Engineering

Padrão para treinamento, avaliação e deploy de modelos — usado pelo `ml-engineer`.

## Quando usar
Ao projetar experimentos, treinar modelos ou preparar modelos para produção.

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
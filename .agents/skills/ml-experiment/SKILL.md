# Skill: ML Experiment

Rigor experimental para comparação de modelos — usado pelo `ml-engineer`.

## Quando usar
Ao **conduzir e comparar experimentos** de ML antes de produtizar (rigor científico, reprodutibilidade, registro). Para o **ciclo completo até produção** (serving, monitoramento, fallback), use `ml-engineering`.

## Princípios de rigor

1. **Baseline obrigatório** — sem baseline simples (regra heurística, modelo trivial), nenhum experimento "complexo" é justificável
2. **Seed fixo** — todos os splits, samplings e inicializações partem de seed reproduzível
3. **Sem vazamento** — feature engineering, normalização e seleção de features só usam dados de treino (nunca val/test)
4. **Test set sagrado** — usado **uma única vez** ao final, nunca durante desenvolvimento
5. **Métrica alinhada ao negócio** — não acurácia se o problema é desbalanceado; não AUC se threshold importa

## O que sempre logar (MLflow / W&B)

- Versão dos dados (hash ou tag)
- Hiperparâmetros completos
- Métricas de treino e validação (não só finais — curvas se aplicável)
- Tempo de treinamento e recursos usados
- Random seed
- Resultado de baselines comparados

## Estrutura de config

```python
from dataclasses import dataclass

@dataclass
class ExperimentConfig:
    model_name: str
    learning_rate: float
    n_estimators: int
    random_state: int = 42
    data_version: str = ""
```

## Comparação entre runs

Antes de declarar um modelo "vencedor":
- [ ] Compara contra baseline simples?
- [ ] Diferença é estatisticamente significativa (não ruído)?
- [ ] Performa em test set (não só val)?
- [ ] Custo (latência, memória, custo de inferência) cabe no orçamento?

## Boas práticas

- Registrar experimentos que **não funcionaram** — evita retrabalho futuro
- Notebook do experimento em `notebooks/` com nome contendo data e descrição
- Nunca commitar dados nem modelos pesados (use `.gitignore` e versionamento externo)
- Documentar suposições sobre os dados de entrada

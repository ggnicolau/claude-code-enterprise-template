# Skill: Code Review

Padrão para revisão de código — usado pelo `tech-lead`, `security-auditor`, `qa`.

## Quando usar
Ao revisar um PR antes do merge.

## Severidade

| Nível | Significado | Ação |
|---|---|---|
| 🔴 Crítico | Bug, vulnerabilidade, regressão | Bloqueia merge — deve ser corrigido |
| 🟡 Aviso | Fragilidade, risco técnico, falta de teste | Deve corrigir antes do merge |
| 🔵 Sugestão | Melhoria de legibilidade, performance opcional | Tech-lead decide se bloqueia |

## Checklist de revisão

**Correção:**
- [ ] Lógica resolve o problema descrito na issue
- [ ] Casos extremos tratados
- [ ] Nenhuma regressão introduzida

**Segurança:**
- [ ] Nenhum dado sensível ou credencial em código
- [ ] Inputs externos validados
- [ ] Permissões mínimas necessárias

**Qualidade:**
- [ ] Código legível sem comentários excessivos
- [ ] Sem duplicação desnecessária
- [ ] Type hints em Python
- [ ] Testes cobrem o caminho principal

**Convenções:**
- [ ] Segue padrões do `CLAUDE.md` do projeto
- [ ] Commit messages em Conventional Commits
- [ ] Branch nome segue `feature/*` ou `fix/*`

## Boas práticas
- Revisar a intenção, não só a implementação — ler a issue antes do diff
- Não reescrever código que funciona só por estilo
- Apontar o problema, sugerir a direção — não reescrever pelo autor
- Finalizar com resumo: aprovado / aprovado com ressalvas / bloqueado

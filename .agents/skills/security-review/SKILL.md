# Skill: Security Review

Checklist rápido pré-PR — usado pelo `security-auditor` para revisão tática.

## Quando usar
Antes de mergear um PR pequeno/médio onde uma auditoria OWASP completa seria overhead. Para PRs grandes ou com infra/auth/dados sensíveis, usar `security-audit` (auditoria profunda).

## Checklist (5 minutos)

**Secrets:**
- [ ] Nenhum token, key ou credencial hardcoded no código
- [ ] `.env` no `.gitignore`, sem rastreamento acidental
- [ ] Secrets de CI no secret manager — nunca em logs

**Inputs:**
- [ ] Inputs externos validados e/ou parametrizados (SQL, shell, paths)
- [ ] Sem `eval`/`exec`/`os.system` com input externo

**Permissões:**
- [ ] Tokens com escopo mínimo necessário (princípio do menor privilégio)
- [ ] Endpoints autenticam quem precisa autenticar

**Logs:**
- [ ] Sem PII (CPF, e-mail, nome) em logs
- [ ] Sem secrets em mensagens de erro

**Dependências:**
- [ ] `pip-audit` / `npm audit` sem 🔴 Crítico em aberto

## Severidade (alinhada com `security-audit`)

🔴 Crítico | 🟡 Aviso | 🔵 Sugestão

## Quando escalar para `security-audit`

Se o checklist acima detectar 🔴 ou 🟡, ou se o PR envolve:
- Autenticação/autorização
- Dados sensíveis (PII, financeiro, saúde)
- Configuração de infra
- Superfície de API pública

→ pare e rode auditoria profunda com `security-audit` (OWASP Top 10 estruturado).

## Operações git/PR

Para auth, fluxo de branch e merge, ver CLAUDE.md §"Autenticação GitHub" e §"Como especialistas abrem PR".

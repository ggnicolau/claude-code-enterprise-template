# Skill: Security Audit

Padrão para identificação e classificação de vulnerabilidades — usado pelo `security-auditor`.

## Quando usar
Ao **auditar profundamente** PRs com infra, autenticação, dados sensíveis ou superfície de API. Para **checklist rápido pré-PR** (5 minutos, antes de mergear PRs pequenos), use `security-review`.

## Severidade

| Nível | Exemplos | Ação |
|---|---|---|
| 🔴 Crítico | Credencial em código, SQL injection, RCE, PII exposta | Bloqueia merge — corrigir antes |
| 🟡 Aviso | Permissão excessiva, sem rate limiting, log com dado sensível | Deve corrigir antes do merge |
| 🔵 Sugestão | Hardening adicional, rotação de segredo, melhoria de auditoria | Tech-lead decide |

## Checklist OWASP Top 10

- [ ] **A01 Broken Access Control** — verificar que endpoints exigem autenticação/autorização correta
- [ ] **A02 Cryptographic Failures** — sem dados sensíveis em texto claro, TLS obrigatório
- [ ] **A03 Injection** — inputs externos parametrizados (SQL, shell, LDAP)
- [ ] **A05 Security Misconfiguration** — sem debug em produção, sem portas desnecessárias expostas
- [ ] **A06 Vulnerable Components** — dependências com CVE conhecida
- [ ] **A07 Auth Failures** — tokens com expiração, sem credenciais hardcoded
- [ ] **A09 Logging Failures** — logs sem PII, sem segredos

## Boas práticas
- Reportar cada achado com: localização exata, impacto, sugestão de fix
- Não sugerir soluções de segurança que sacrificam funcionalidade sem discutir o trade-off
- Secrets pertencem ao `.env` ou a um secret manager — nunca ao código
- Revisar `.gitignore` para garantir que `.env` está excluído

## Operações git/PR

Para auth via `gh` CLI e fluxo de PR (incluindo regra crítica de `--delete-branch`), ver CLAUDE.md §"Autenticação GitHub" e §"Como especialistas abrem PR".
# Skill: Infra & DevOps

Padrão para infraestrutura, CI/CD e operações — usado pelo `infra-devops`.

## Quando usar
Ao provisionar infraestrutura, configurar pipelines ou planejar operações.

## Checklist de deploy

**Antes do deploy:**
- [ ] Testes passando em CI
- [ ] Variáveis de ambiente configuradas no ambiente de destino
- [ ] Secrets no secret manager — nunca em código ou CI logs
- [ ] Rollback definido (versão anterior disponível)
- [ ] Health check configurado no novo serviço

**Durante:**
- [ ] Deploy gradual (blue/green ou canary) quando possível
- [ ] Monitorar métricas-chave nos primeiros 15 minutos

**Após:**
- [ ] Smoke test no ambiente de produção
- [ ] Alertas verificados (não silenciados)
- [ ] Documentar qualquer configuração manual feita

## Princípios de infraestrutura

| Princípio | Prática |
|---|---|
| **IaC** | Terraform ou CDK — nenhum recurso criado manualmente sem documentar |
| **Mínimo privilégio** | IAM roles com apenas as permissões necessárias |
| **Imutabilidade** | Containers, não servidores mutáveis |
| **Observabilidade** | Logs estruturados, métricas, traces distribuídos |

## Boas práticas
- Nunca commitar credenciais — usar `.env` local + secret manager em cloud
- CI falhou → investiga antes de fazer bypass
- Documentar arquitetura em `docs/tech/arquitetura.md`
- Registrar ADRs para decisões de infra relevantes
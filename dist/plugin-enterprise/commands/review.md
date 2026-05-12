# Review Orquestrado

Dispare os dois subagentes abaixo em paralelo (numa única chamada com dois Agent tool calls simultâneos):

1. **tech-lead** — code review de corretude, arquitetura, tipos, padrões e cobertura de testes
2. **security-auditor** — varredura de segurança, exposição de dados e vulnerabilidades

Após ambos retornarem, consolide os resultados num único relatório com severidade unificada:
🔴 Crítico | 🟡 Aviso | 🔵 Sugestão

$ARGUMENTS

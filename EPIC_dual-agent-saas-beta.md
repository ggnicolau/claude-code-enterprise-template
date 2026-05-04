# [EPIC] Encapsular Dual Multi-Agent System como produto web B2B com UI controlada, runtime privado e GitHub do cliente como source of truth

## Contexto

O Dual Multi-Agent System atualmente roda via Claude Code.

Ele nasceu como uma arquitetura operacional codificada em arquivos `.md`, acumulando experiência prática de engenharia, gestão de projetos, produto, coordenação, governança, TI e IA.

O valor do sistema não está apenas nos arquivos em si, mas na metodologia operacional que eles codificam:

- papéis claros;
- cadeia de comando;
- Kanban como memória operacional;
- gates de aprovação;
- rastreabilidade por issues, PRs e commits;
- separação entre construção e execução;
- agentes especializados;
- commands;
- memória persistente;
- feedback loop execução -> construção;
- adaptação por domínio/cliente.

O Claude Code funciona bem como ambiente de desenvolvimento porque permite:

- carregar `CLAUDE.md`;
- carregar `AGENTS.md`;
- carregar agents especializados;
- executar hooks como `session_start`;
- usar commands;
- consultar memória persistente;
- operar sobre GitHub/Kanban;
- executar pipelines de construção e execução;
- conversar livremente com o usuário;
- acionar subagentes e tools.

Porém, esse modelo não é adequado para distribuição comercial porque:

1. A UI do Claude Code é fechada.
   - Não permite adaptação.
   - Não permite remover painéis ou restringir superfícies.
   - Não permite criar uma experiência controlada para cliente.

2. O runtime pressupõe acesso completo ao workspace.
   - O usuário pode ver arquivos internos.
   - O usuário pode copiar arquivos de sistema.
   - O usuário pode modificar regras do sistema.
   - O sistema não tem fronteira clara entre operador e cliente.

3. O produto não deve ser entregue como executável, template ou repositório.
   - O valor está na arquitetura, nos agentes, nas regras, nos workflows e na governança.
   - A forma correta de distribuição é serviço web/SaaS controlado.
   - O cliente não deve receber os `.mds` privados nem o sistema base.

Objetivo desta epic:

> Transformar o sistema atual, operado localmente via Claude Code, em um produto web beta B2B com runtime privado, interface controlada, metodologia agentic proprietária encapsulada e operação sobre o GitHub do cliente.

---

## Tese de produto

O produto não é apenas um template.

O produto é:

> uma fábrica/sistema operacional multi-agente para criar, evoluir e operar produtos digitais com governança, memória, Kanban, gates e rastreabilidade.

Ele pode atender dois tipos de produto digital:

### 1. Produtos digitais tradicionais

Produtos em que os agentes ajudam a construir, mas não são necessariamente o produto final:

- websites;
- SaaS;
- dashboards;
- apps internos;
- APIs;
- pipelines de dados;
- pipelines de ML;
- automações;
- integrações;
- sistemas internos;
- ferramentas digitais B2B.

### 2. Produtos agentic-native

Produtos em que os próprios agentes são parte essencial da operação:

- pipelines editoriais;
- sistemas de pesquisa recorrente;
- agentes analíticos;
- operações de inteligência;
- pipelines que geram outputs;
- workflows que se auto-monitoram;
- produtos que transformam falhas em backlog;
- sistemas operados continuamente por agentes.

PDFs, PPTX, relatórios e posts são apenas exemplos de artefatos possíveis do plano de execução. O sistema deve ser capaz de produzir qualquer artefato digital compatível com o produto do cliente.

---

## Diferenciação e hipótese de mercado

O produto não compete diretamente com ferramentas individuais de desenvolvimento assistido por IA, nem com frameworks de agentes genéricos.

O padrão observado no mercado é:

1. Desenvolvedores usam Claude Code, Cursor, Copilot e ferramentas similares para resolver tarefas técnicas em formato livre.
2. Usuários de negócio usam chats e agentes para resolver demandas pontuais, normalmente sem processo estruturado.
3. Frameworks como CrewAI, LangGraph, AutoGen, Dify, Flowise e Langflow oferecem blocos para construir sistemas agentic, mas exigem muito esforço de engenharia para entregar workflows completos, governados e auditáveis.
4. Runtimes como OpenClaw oferecem infraestrutura agentic, mas não entregam uma metodologia de produto, gestão, Kanban, gates, papéis, commands e operação de ponta a ponta pronta para adaptar a clientes.

O diferencial do Dual Multi-Agent System é tratar agentes não como assistentes soltos, mas como uma organização operacional codificada.

A arquitetura incorpora:

- papéis organizacionais claros;
- cadeia de comando;
- PM, PO, TL, QA e especialistas;
- Kanban como fonte de verdade;
- issues como memória e canal entre agentes;
- PRs e commits como trilha técnica;
- gates de aprovação;
- feedback loop execução -> construção;
- adaptação por domínio e cliente;
- operação sobre GitHub do cliente;
- isolamento da metodologia privada.

O risco competitivo existe: outras empresas ou desenvolvedores podem construir partes semelhantes. Porém, a maioria dos usos atuais de IA permanece em dois extremos:

- uso individual, livre e pouco governado;
- frameworks técnicos que exigem montar toda a governança do zero.

Este produto ocupa uma camada diferente:

> um sistema operacional agentic governado para construir, operar e evoluir produtos digitais.

O defensivo inicial não é segredo absoluto dos arquivos `.md`, mas sim:

- velocidade de execução;
- metodologia acumulada;
- qualidade da adaptação por cliente;
- biblioteca crescente de agents/commands/templates;
- casos reais;
- histórico operacional;
- SaaS privado com isolamento;
- evolução contínua do sistema base.

A estratégia do beta deve priorizar validação em clientes reais para transformar a vantagem metodológica em prova de mercado.

---

## Avaliação de opções reais de UI e executor

O beta pode reaproveitar ferramentas existentes, mas a arquitetura do produto não deve depender de uma UI ou runtime específico como tese central.

A tese central é:

> UI controlada + API própria + system privado + project do cliente + executor agentic interno + GitHub do cliente como source of truth.

### Observação sobre Claude Code/Codex

Claude Code Desktop e Codex Desktop são interfaces fechadas. Elas não podem ser "capadas" diretamente para virar UI do cliente.

O que pode ser usado no beta é:

- Claude Code/Codex como executor interno, via CLI/SDK/processo privado, se isso for permitido pelos termos de uso aplicáveis;
- uma UI open-source ou própria por cima, sempre chamando a API própria;
- um job runner que trate Claude Code/Codex como implementação interna, não como superfície do cliente.

### Opções reais para o beta

| Opção | Licença/base | Como acelera | Como desacelera | Decisão |
|---|---|---|---|---|
| UI própria simples + Claude Code como executor interno | Código próprio; termos Claude Code a verificar | Menor risco de comportamento, porque o sistema atual já roda bem no Claude Code; UI pode nascer exatamente com as superfícies permitidas. | Exige construir chat, status, eventos, histórico e monitor mínimo. | Melhor opção se a meta for beta rápido e isolado. |
| OpenADE-like UI + Claude Code/Codex como executor interno | OpenADE: MIT; termos Claude Code/Codex a verificar | Pode acelerar UI parecida com Claude/Codex Desktop, com chat, diffs, sessões e experiência familiar. | Precisa remover terminal, file explorer, settings, internals e trocar backend por API própria; pode estar acoplado a workflow local/dev. | Avaliar como base visual se for fácil separar UI do runtime. |
| OpenCovibe-like UI + Claude Code/Codex como executor interno | OpenCovibe: Apache 2.0; termos Claude Code/Codex a verificar | Pode acelerar tool cards, histórico, replay, permissões, analytics e monitor. | Pode assumir usuário como operador e expor tool calls/detalhes internos; precisa forte sanitização. | Avaliar como fonte de componentes de monitor/histórico. |
| OpenClaw + WebChat + Monitor/Control UI capados | OpenClaw: MIT; termos dos modelos usados a verificar | Pode acelerar se OpenClaw entregar runtime contínuo, sessões, cron, agentes, skills, Gateway, WebChat, health, usage, logs e dashboard/admin já alinhados ao runtime. | Exige migração Claude Code -> OpenClaw e revalidação de `/kickoff`, `/advance`, hooks, memory e gates; WebChat/Monitor diretos não podem falar com Gateway no navegador do cliente; Control UI é superfície admin e não cliente. | Manter como opção futura ou usar apenas se trouxer ganho claro de runtime/orquestração. O Monitor pode inspirar componentes, não ser exposto direto. |
| UI própria simples + Codex como executor alternativo | Código próprio; termos Codex/OpenAI a verificar | Pode melhorar execução em tarefas de código e servir como fallback/pluggable executor. | Comportamento pode diferir do Claude Code; exige runner/policies equivalentes. | Manter como executor alternativo, não como dependência inicial. |

### Leitura anterior da avaliação

Leitura mantida apenas como histórico da avaliação inicial; a decisão atual está na seção "Revisão consolidada depois da inspeção do template e dos repositórios locais".

Para o beta, a opcao mais forte nao e trocar o executor que ja funciona. A opcao mais forte e trocar a superficie de produto.

Ranking operacional anterior:

1. OpenCovibe-like UI + API propria + Claude Code/Codex como executor interno.
2. OpenADE-like UI + API propria + Claude Code/Codex como segunda candidata ou fonte de componentes de diff/cockpit.
3. UI propria simples se o fork de UI ficar mais caro do que criar uma superficie enxuta.
4. OpenClaw + WebChat + Monitor/Control UI apenas se a decisao for adotar OpenClaw como runtime/orquestrador, nao apenas por causa da UI.

OpenCovibe parece a melhor candidata inicial porque ja tem chat visual, tool cards, historico, replay, analytics e experiencia proxima de Claude/Codex Desktop. O trabalho principal seria remover comandos perigosos e trocar o backend direto por API propria.

OpenADE deve continuar na avaliacao principal. Ele pode ser muito util para diffs, cockpit, fluxo de plano/execucao e experiencia familiar para desenvolvedores, mas tende a vir mais carregado de superficie de operador: terminal, file browser, processos, worktrees, settings e acesso amplo ao workspace.

OpenClaw + WebChat + Monitor/Control UI deve ser avaliado como conjunto. O valor real do OpenClaw nao e o WebChat isolado; e o runtime/control plane: Gateway, sessoes, cron, eventos, health, usage, logs, skills/tools e painel admin. Para o cliente, porem, WebChat e Monitor nao devem conectar direto no Gateway. Eles devem passar por API propria, policy e sanitizer.

### Ferramentas fora do caminho crítico

As ferramentas abaixo não são candidatas principais para construir o beta. Elas podem ser citadas apenas como contexto competitivo ou referência futura:

- CrewAI;
- LangGraph;
- AutoGen;
- n8n com agentes;
- Dify;
- Flowise;
- Langflow;
- Cursor;
- GitHub Copilot;
- Devin;
- Replit Agent;
- OpenCowork;
- Friendly Terminal;
- Localforge;
- OpenACP;
- ClawTab.

Motivo: ou são frameworks/builders que exigem reconstruir governança do zero, ou são produtos de desenvolvedor/desktop/local que não resolvem diretamente a arquitetura B2B isolada em VM com UI web, API própria, `system/` privado e `project/` do cliente.

Licenças conhecidas neste momento:

- OpenCowork: MIT;
- Friendly Terminal: GPL-3.0;
- OpenADE: MIT;
- OpenCovibe: Apache 2.0;
- OpenClaw: MIT.

Licenças de Localforge, OpenACP e ClawTab devem ser confirmadas diretamente no `LICENSE` do repositório antes de qualquer uso comercial ou fork.

Mesmo quando a UI open-source permite uso comercial, os termos de Claude Code, Codex, Anthropic, OpenAI e demais provedores/modelos precisam ser avaliados separadamente para uso como executor interno em produto B2B hospedado.

### Decisão operacional anterior

Para o beta, a melhor direção é:

> OpenCovibe-like UI ou UI equivalente como base visual inicial, API propria como fronteira obrigatoria, Claude Code/Codex como executor interno privado e OpenClaw apenas como opcao futura se o runtime dele se tornar necessario.

```text
UI web controlada
  ↓
API própria / auth / sanitizer
  ↓
job runner privado
  ↓
executor agentic interno
  - Claude Code inicialmente
  - Codex como alternativa
  - OpenClaw como candidato futuro/opcional
  ↓
system repo privado + project repo cliente
  ↓
GitHub do cliente
```

OpenClaw não deve ser removido da tese técnica, mas também não deve ser uma dependência obrigatória do beta se Claude Code/Codex já entregam melhor qualidade e menor risco de migração.

---

### Revisão consolidada depois da inspeção do template e dos repositórios locais

Esta seção substitui a leitura operacional anterior. A revisão do template pai, dos arquivos em `docs-site/architecture/` e dos templates de projeto filho confirma que a UI escolhida não pode ser avaliada apenas por "parecer Claude Code Desktop".

O sistema que precisa ser encapsulado tem estes invariantes:

- `/wizard` cria projeto filho com agentes, commands, hooks, CI/CD, GitHub Project e estrutura de memória;
- `/kickoff` cria a memória persistente inicial e transforma contexto narrativo em backlog;
- `/advance` lê o GitHub Project, valida com PO, delega via TL e move trabalho por issues/PRs;
- o GitHub Project é a memória operacional e não pode ser substituído silenciosamente por um board local;
- os agentes alternam entre plano de construção e plano de execução;
- falhas do plano de execução precisam virar issues rastreáveis no plano de construção;
- nenhum agente faz merge do próprio trabalho;
- o cliente precisa ver outputs, diffs, PRs, status, eventos e artefatos do projeto dele;
- o cliente não pode ver `system/`, `.mds` privados, agentes internos, settings, hooks, prompts, memória raw ou logs internos.

Portanto, a pergunta correta para cada UI/runtime é:

> Ela acelera uma UI controlada para `project/` sem expor `system/`, sem trocar o GitHub do cliente como source of truth e sem quebrar o comportamento que já funciona no Claude Code?

### Avaliação local consolidada dos repositórios inspecionados

Repositórios locais analisados em `C:\temp`:

- `aider`;
- `claudecodeui`;
- `cline`;
- `fazm`;
- `happy`;
- `nimbalyst`;
- `opcode`;
- `yume`;
- `yume-inspect`.

Também permanecem na avaliação os candidatos já mapeados antes:

- Vibe Kanban;
- OpenCovibe;
- OpenADE;
- OpenClaw + WebChat + Monitor/Control UI;
- OpenCowork;
- Friendly Terminal;
- Localforge;
- OpenACP;
- ClawTab;
- CrewAI;
- LangGraph;
- AutoGen;
- n8n com agentes;
- Dify;
- Flowise;
- Langflow;
- Cursor;
- GitHub Copilot;
- Devin;
- Replit Agent.

| Opção | Licença/base observada | O que oferece | Como acelera o beta | Risco/desaceleração | Conclusão |
|---|---|---|---|---|---|
| Vibe Kanban | Apache 2.0 | Kanban, workspaces, branch por tarefa, terminal, dev server, diff, comentários inline, preview/browser, PRs e múltiplos agentes. | É a base mais pragmática para tarefa -> workspace -> agente -> diff -> PR. Combina bem com o modo como o sistema já opera por issue/PR. | O board próprio/local não deve virar source of truth; precisa espelhar GitHub Projects/issues. Terminal/file access precisam passar por API e allowlist. O projeto também está em sunset, então o fork precisa ser tratado como base congelada. | Melhor base pragmática para o beta, desde que GitHub Projects continue mandando e o Vibe vire UI/espelho operacional. |
| Nimbalyst | MIT por padrão; `packages/collabv3` é AGPL-3.0 ou licença comercial separada | Workspace visual para Codex/Claude Code, sessões paralelas, kanban, tarefas, editores visuais, markdown, mockups, Mermaid, Excalidraw, CSV, data models, Monaco, worktrees, mobile e permissões por projeto. | É o candidato mais forte conceitualmente para "fábrica de produtos digitais", porque não pensa só em código; pensa em artefatos, sessões, tarefas e edição visual. | Monorepo grande, Electron, runtime próprio, partes colaborativas com licença separada e maior custo de adaptação. Pode ser pesado para beta de 30 dias. | Melhor referência estratégica e possível base se houver tempo para investigação profunda; talvez superior ao Vibe no longo prazo. |
| OpenCovibe | Apache 2.0 | Chat visual, tool cards, run history/replay, fork/resume, permissões inline, usage/cost, activity monitor, MCP, memory editor, agent editor, marketplace e file explorer. | Melhor referência para a UX de "ver o agente trabalhando": tool cards, eventos, histórico e monitor. | Expõe exatamente o que precisa ser escondido: memory, agents, settings, MCP, file explorer amplo e detalhes de tool calls. Capar no frontend não basta; precisa API própria e backend sanitizado. | Excelente fonte de componentes de execução/monitor; perigoso como base direta sem reescrever fronteira de backend. |
| ClaudeCodeUI / CloudCLI UI | AGPL-3.0-or-later | Web/mobile UI para Claude Code, Cursor CLI, Codex e Gemini CLI; shell terminal, file explorer, git explorer, sessões, plugins, REST API, sandbox experimental. | Acelera uma UI web remota para Claude/Codex com chat, arquivos, git e sessões. É próximo do que se imagina como "Claude Code em browser". | É genérico e muito exposto: terminal, file explorer, git, plugins e config nativa `~/.claude`. A licença AGPL pesa se for base de SaaS fechado. Reforça que UI genérica está comoditizada. | Bom candidato técnico para acelerar web UI, mas exige corte forte e decisão jurídica. Não é o diferencial do produto. |
| Cline | Apache 2.0 | Extensão VSCode com agente, edição de arquivos, terminal, browser, checkpoints, diffs, MCP, múltiplos provedores e human-in-the-loop. | Referência muito forte de permissões, checkpoints, browser testing, diff e aprovação humana. | É IDE/VSCode-first, não SaaS web controlado. Não resolve isolamento `system/project` sem construir plataforma em volta. | Referência obrigatória de UX, permissões e auditoria; não é base principal para o beta web. |
| OpenADE | MIT | Cockpit dev com Plan -> Revise -> Execute, HyperPlan, comentários em arquivos/diffs/mensagens, terminal, file browser, process manager, snapshots e worktrees. | Bom para fluxo de planejamento/revisão/execução e cockpit técnico. | Muito orientado a operador dev; expõe terminal, files, processos e worktrees. Menos natural para cliente B2B não técnico. | Boa referência de cockpit e planejamento; segunda linha como base. |
| Yume / `yume-inspect` | Freeware/proprietário; licença permite uso, mas proíbe modificar, distribuir, fazer engenharia reversa e criar derivados | UI nativa para Claude Code oficial como subprocesso; orchestration flow, agentes built-in, background agents, worktree isolation, plugins/skills, rate limit, crash recovery, multi-provider e painéis. | Excelente benchmark de UX Claude Code-native. Confirma que spawnar o Claude Code oficial e preservar hooks/skills/MCP é uma abordagem real. | O repo local é site/releases; código-fonte real não está disponível. A licença declara closed source e proíbe derivados. `C:\temp\yume` ficou incompleto; `C:\temp\yume-inspect` mostra a distribuição/site. | Não usar como base. Usar como benchmark competitivo e inspiração de UX. |
| Aider | Apache 2.0 | CLI madura de pair programming, repo map, git integration, lint/test loop, multi-modelo, voz e grande adoção. | Pode ser runner alternativo para tarefas de código, especialmente edição cirúrgica, testes e commits. | Não é UI, não é sistema operacional de projeto, não preserva sozinho PM/PO/TL/Kanban/gates. | Bom runner alternativo futuro; não é base de produto. |
| Happy | MIT | Web/mobile client para Claude Code e Codex com wrapper CLI, E2E encryption, push notifications, troca entre devices, Happy Agent e Happy Server. | Inspira mobile, notificações, controle remoto e continuidade de sessão. | Foco é controle remoto pessoal, não governança B2B com GitHub Projects, PRs, gates e isolamento de `system/`. | Referência útil para mobile/remote control; não é base principal. |
| Opcode | AGPL-3.0 | Tauri desktop para Claude Code: projetos/sessões, custom agents, background execution, usage analytics, MCP, timeline/checkpoints e editor de `CLAUDE.md`. | Boa referência de dashboard de operador, agentes, analytics e checkpoints. | Muito voltado a mexer no universo interno do Claude Code: agentes, MCP, `CLAUDE.md`, configs. Para cliente, expõe demais. Licença AGPL pesa. | Referência de operador/admin, não UI cliente. |
| Fazm | README indica MIT; não havia `LICENSE` na raiz local | Agente de computador macOS, browser, docs, Google Apps, voz, ACP bridge, rotinas via launchd, cron jobs e histórico em SQLite. | Inspira plano de execução, rotinas recorrentes, voice UX e automação de desktop/browser. | É macOS/computer-agent, não UI de projeto GitHub/Kanban. Pouca aderência ao isolamento SaaS proposto. | Lateral. Útil como referência de rotinas e agent-as-product, não base da UI. |
| OpenClaw + WebChat + Monitor/Control UI | MIT | Runtime/control plane, Gateway, WebChat, monitor/dashboard, sessões, cron, eventos e agentes. | Pode ser valioso se a decisão for adotar OpenClaw como runtime estruturado. | Exige migrar/reescrever o que já funciona no Claude Code; WebChat/Monitor não podem conectar direto ao Gateway no navegador do cliente. | Manter como opção futura de runtime; não escolher apenas pela UI. |
| UI própria simples + Claude Code executor | Código próprio; termos Claude Code a verificar | Chat, comandos, status, history, eventos, diff e monitor mínimo criados sob medida. | Menor superfície e isolamento mais limpo; preserva executor que já foi validado. | Exige construir UI, diff, stream e monitor, mesmo que enxutos. | Melhor fallback se adaptar bases existentes ficar mais caro que criar a superfície mínima. |
| OpenCowork | MIT | Desktop/local com Claude Code, OpenAI, Gemini, DeepSeek, MCP, skills e sandbox por WSL2/Lima. | Pode inspirar sandbox/empacotamento. | Não resolve SaaS web; foco local/desktop. | Referência secundária. |
| Friendly Terminal | GPL-3.0 | UI amigável para Claude Code/Gemini/Codex, Windows-first e voltada a não-devs. | Pode inspirar onboarding para cliente menos técnico. | GPL e foco local/consumer; pouca aderência a B2B isolado. | Referência de onboarding, não base. |
| Localforge / OpenACP / ClawTab | Licenças a confirmar no `LICENSE` de cada repo | Família de local agent management, ACP/bridges ou interfaces auxiliares. | Podem inspirar integração e bridges. | Menos centrais para Kanban/GitHub/PR/gates. | Referência futura, fora do caminho crítico. |
| CrewAI | Projeto/framework de agentes | Orquestra agentes em Python. | Útil para protótipos agentic específicos. | Recria governança do zero; aumenta overhead que o template justamente evitou. | Concorrente/framework, não base. |
| LangGraph | Projeto/framework de agentes | Grafos, estado e workflows agentic. | Útil para fluxos determinísticos e state machines. | Alto custo para replicar PM/PO/TL, Kanban, issues, PRs, memory e gates. | Concorrente técnico, não substituto do sistema. |
| AutoGen | Projeto/framework de agentes | Conversas multi-agente programáveis. | Útil para pesquisa/protótipo. | Exige muita engenharia de orquestração, parsing e estado. | Fora do caminho crítico. |
| n8n com agentes | Automação/workflows | Bom para integrações e automações de negócio. | Pode inspirar conectores e rotinas. | Não entrega governança de produto, PRs, code review e dual-plane. | Complementar, não base. |
| Dify | App builder/LLMOps | UI para apps LLM, datasets, workflows e deploy. | Útil para apps conversacionais/LLM. | Não resolve fábrica de produto com GitHub Projects/PRs/gates. | Concorrente adjacente. |
| Flowise | Builder visual LLM | Montagem visual de flows. | Ajuda protótipos de RAG/chains. | Não entrega processo enterprise de construção/execução. | Fora do caminho crítico. |
| Langflow | Builder visual LLM | Interface visual para LangChain-like flows. | Pode ajudar demonstrações e workflows de IA. | Mesmo problema: blocos, não metodologia operacional. | Fora do caminho crítico. |
| Cursor | Produto fechado/IDE | Dev assistido por IA. | Referência competitiva de edição e UX dev. | Não é capável como UI controlada do cliente; fechado. | Concorrente/benchmark. |
| GitHub Copilot | Produto fechado/IDE | Autocomplete, chat e agentes no ecossistema GitHub. | Benchmark por integração com GitHub. | Não encapsula metodologia privada nem dual-plane. | Concorrente/benchmark. |
| Devin | Produto fechado | Agente de software autônomo. | Benchmark de promessa comercial. | Não é base técnica; concorre em percepção de mercado. | Benchmark competitivo. |
| Replit Agent | Produto fechado | Geração e edição de apps no Replit. | Benchmark de UX de criação. | Não resolve B2B privado com GitHub do cliente e system isolado. | Benchmark competitivo. |

### Ranking completo para adaptação ao beta

Ranking considerando: aderência ao seu template, velocidade de beta, capacidade de mostrar diff/status, compatibilidade com Claude Code/Codex, risco de exposição de `system/`, custo de capar e coerência com GitHub Projects como source of truth.

| Rank | Candidato | Por quê |
|---:|---|---|
| 1 | Vibe Kanban | Melhor base pragmática para beta: tarefa, workspace, diff, PR, preview e agentes. Requer transformar o board em espelho do GitHub Projects. |
| 2 | Nimbalyst | Melhor visão estratégica: tarefas, sessões, kanban, artefatos visuais, editores e permissões. Pode ser superior no longo prazo, mas é mais pesado para adaptar. |
| 3 | ClaudeCodeUI / CloudCLI UI | Mais perto de uma web UI genérica para Claude Code/Codex. Acelera bastante, mas expõe terminal/files/config e tem AGPL. |
| 4 | OpenCovibe | Melhor fonte de execution trace, tool cards, replay e monitor. Muito bom para componentes, perigoso como base direta. |
| 5 | Cline | Melhor referência de human-in-the-loop, permissões, browser, checkpoints e diff. Forte para aprender, fraco como base SaaS web. |
| 6 | OpenADE | Bom cockpit Plan -> Revise -> Execute, com diffs e worktrees. Mais operador/dev do que cliente B2B. |
| 7 | Aider | Bom runner alternativo de código, não UI. Pode entrar atrás da API para tarefas específicas. |
| 8 | Happy | Bom para mobile, push e controle remoto de sessões. Não resolve governança GitHub/Kanban. |
| 9 | Opcode | Referência de dashboard/admin para Claude Code, mas expõe internals demais. |
| 10 | OpenClaw + WebChat + Monitor | Só sobe no ranking se a decisão for migrar para OpenClaw como runtime. Como UI isolada, não justifica o risco agora. |
| 11 | UI própria simples | Pode ser a opção mais segura se as bases acima exigirem cortes demais; perde em velocidade visual. |
| 12 | Fazm | Referência lateral para rotinas, computer use e voz; não é base para a UI do projeto. |
| 13 | Yume / `yume-inspect` | Excelente benchmark, mas closed source/proprietário; não é base adaptável. |
| 14 | OpenCowork | Inspiração de sandbox/desktop, não base SaaS. |
| 15 | Friendly Terminal | Inspiração de onboarding, mas GPL/local/consumer. |
| 16 | Localforge / OpenACP / ClawTab | Referências auxiliares; pouca aderência ao core GitHub/PR/Kanban. |
| 17 | n8n com agentes | Complementar para integrações, não substitui o sistema. |
| 18 | Dify | Complementar/concorrente de app LLM, não substitui a governança. |
| 19 | LangGraph | Framework forte, mas recria overhead e processo do zero. |
| 20 | CrewAI | Framework de agentes, não produto pronto para seu caso. |
| 21 | AutoGen | Framework/pesquisa; custo alto para governança. |
| 22 | Flowise | Builder visual, não sistema operacional de produto. |
| 23 | Langflow | Builder visual, não sistema operacional de produto. |
| 24 | Cursor | Benchmark fechado, não base capável. |
| 25 | GitHub Copilot | Benchmark fechado, não base capável. |
| 26 | Devin | Benchmark comercial, não base técnica. |
| 27 | Replit Agent | Benchmark comercial, não base técnica. |

### Ranking por tipo de uso

**Base mais provável para o beta**

1. Vibe Kanban.
2. Nimbalyst.
3. ClaudeCodeUI / CloudCLI UI.
4. OpenCovibe.

**Melhores fontes de UX para execução visível**

1. OpenCovibe.
2. Yume.
3. Cline.
4. ClaudeCodeUI / CloudCLI UI.
5. Opcode.

**Melhores fontes para tarefas, board, diff e PR**

1. Vibe Kanban.
2. Nimbalyst.
3. OpenADE.
4. Cline.

**Melhores fontes para isolamento/permissões**

1. Nimbalyst.
2. Cline.
3. ClaudeCodeUI sandbox.
4. Vibe Kanban workspaces.
5. Yume como benchmark de worktree/background agents, mas não como código reutilizável.

**Melhores opções de runner/executor interno**

1. Claude Code, porque o sistema atual já foi validado nele.
2. Codex, como executor alternativo/pluggable.
3. Aider, como runner especializado para edição de código.
4. OpenClaw, se no futuro o ganho de runtime/orquestração superar o custo de migração.

### Decisão operacional consolidada

Para o beta, a melhor direção é:

> Vibe Kanban ou Nimbalyst como base visual principal, OpenCovibe/Cline/Yume como referências de execution trace e permissões, API própria como fronteira obrigatória, Claude Code como executor interno inicial e GitHub Projects/issues/PRs como source of truth.

Arquitetura recomendada:

```text
Cliente
  ↓
UI web controlada
  - chat/comandos
  - status/eventos públicos
  - diff/PR/preview do project/
  - board espelhado do GitHub Projects
  ↓
API própria
  - auth
  - policy
  - sanitizer
  - allowlist project/
  - bloqueio system/ e platform/
  ↓
job runner privado
  ↓
executor agentic interno
  - Claude Code inicialmente
  - Codex como alternativa
  - Aider para edição de código, se útil
  - OpenClaw como opção futura
  ↓
system repo privado + project repo cliente
  ↓
GitHub do cliente
```

OpenClaw não deve ser removido da tese técnica, mas também não deve ser dependência obrigatória do beta se Claude Code já entrega melhor qualidade e menor risco.

Vibe Kanban deve continuar como o caminho mais rápido se o objetivo for beta vendável em até 30 dias. Nimbalyst deve ser investigado em paralelo como candidato mais ambicioso para a plataforma definitiva. OpenCovibe deve ser tratado como biblioteca de ideias de UX, não como fonte de verdade operacional.

---

## Objetivo

Criar uma versão beta comercial do Dual Multi-Agent System baseada em:

- runtime/orquestrador privado, inicialmente baseado no executor que já funciona melhor para o sistema atual;
- Claude Code como executor inicial preferencial, se mantiver maior qualidade e menor risco;
- Codex como executor alternativo/pluggable;
- OpenClaw como candidato futuro ou executor opcional, caso traga ganho real de runtime contínuo;
- UI Web controlada baseada/adaptada a partir do WebChat ou de experiência equivalente;
- Monitor/Dashboard reaproveitado parcialmente para observabilidade;
- API própria como camada intermediária obrigatória;
- GitHub do cliente como fonte de verdade operacional;
- arquivos `.md` de sistema isolados e privados;
- execução via LLM API;
- infraestrutura própria em VM única para o beta;
- adaptação da arquitetura multi-agente dual ao contexto de cada cliente.

---

## Arquitetura alvo

```text
Cliente
  ↓
UI Web controlada
  - chat
  - comandos
  - status
  - eventos
  - monitor sanitizado
  ↓
API própria
  - /chat
  - /command
  - /status
  - /events
  - /metrics
  - /history
  ↓
Runtime privado / executor agentic interno
  - Claude Code
  - Codex
  - OpenClaw opcional/futuro
  ↓
Sistema privado
  - SOUL.md / CLAUDE.md convertido
  - AGENTS.md
  - agents/*.md
  - commands / skills
  - memory
  - templates
  - policies
  ↓
LLM API
  - Anthropic
  - OpenAI
  - outros futuros
  ↓
GitHub do cliente
  - issues
  - PRs
  - commits
  - Kanban
  - código
  - documentação
  - artefatos
  - logs sanitizados
```

---

## Princípio arquitetural central

O cliente não recebe o sistema.

O cliente recebe acesso a:

> uma interface web que aciona um sistema de agentes hospedado e controlado pela infraestrutura própria.

A inteligência permanece privada.

O GitHub do cliente permanece como superfície operacional visível do projeto/produto.

Os `.mds` privados são o núcleo metodológico do produto e não podem ser expostos, copiados, listados ou commitados no repositório do cliente.

---

## Separação de domínios

### 1. Sistema privado

O sistema privado contém a lógica do Dual Multi-Agent System.

Conteúdo:

```text
system/
  SOUL.md
  CLAUDE.md original ou referência migrada
  AGENTS.md
  agents/*.md
  memory/*.md
  hooks/
  commands/
  skills/
  settings.json
  templates/
  sanitizer/
  policies/
  adapters/
```

Regras:

- não pode ser acessado pelo cliente;
- não pode ser listado pela UI;
- não pode ser exposto por API;
- não pode ser commitado no GitHub do cliente;
- não pode ser acessado por tools genéricas;
- não pode aparecer em logs visíveis;
- não pode ser mencionado em respostas externas;
- não pode ser exposto por WebSocket, Gateway, file explorer ou endpoint;
- não pode ser incluído em artefatos públicos;
- não pode aparecer em stack traces visíveis;
- não pode ser retornado por prompts de debug.

### 2. Projeto/produto do cliente

O GitHub do cliente é a superfície operacional visível.

Conteúdo:

```text
GitHub do cliente/
  issues
  PRs
  commits
  Kanban
  código do projeto
  documentação do produto
  artefatos produzidos
  logs sanitizados
  comentários operacionais
  status de execução
```

Funções:

- memória operacional do projeto;
- canal de comunicação entre agentes e cliente;
- rastreabilidade;
- backlog;
- histórico de entregas;
- registro de falhas;
- fonte de verdade visível.

### 3. Configuração vertical/domínio do cliente

Cada cliente pode receber adaptação específica:

```text
client-domain/
  vocabulário do domínio
  agentes específicos
  comandos específicos
  workflows específicos
  gates específicos
  templates de artefatos
  integrações autorizadas
```

Essa camada pode ser derivada do sistema privado, mas nunca deve expor o core metodológico.

---

## Decisão sobre Kanban

Não haverá Kanban interno do sistema na versão beta.

O Kanban relevante é o Kanban do projeto/produto do cliente.

O sistema deve:

- ler o Kanban do cliente;
- interpretar estado;
- criar issues;
- comentar issues;
- abrir PRs;
- mover cards;
- registrar entregas;
- registrar falhas sanitizadas;
- conectar execução e construção;
- usar issues como memória operacional persistente.

O sistema não deve expor:

- lógica interna;
- regras dos agentes;
- raciocínio completo;
- nomes ou estrutura dos arquivos de sistema;
- paths internos;
- prompts;
- memória raw;
- payload bruto de tools.

---

## Dual-plane support: construção e execução

O produto beta deve preservar a arquitetura dual original.

### 1. Plano de construção

Responsável por desenvolvimento e evolução do produto.

Inclui:

- discovery;
- criação e refinamento de issues;
- priorização de backlog;
- abertura de branches;
- escrita de código;
- abertura de PRs;
- code review;
- testes;
- QA;
- correção de bugs;
- deploy;
- documentação;
- evolução do produto.

Comandos esperados:

```text
/kickoff
/advance
/fix-issue
/review
/sync-template
```

### 2. Plano de execução

Responsável por operar o produto.

Inclui:

- rotinas agendadas;
- execução de pipelines;
- coleta de dados;
- transformação de dados;
- análise;
- geração de artefatos;
- publicação;
- monitoramento;
- registro de falhas;
- geração de issues a partir de falhas.

Comandos esperados:

```text
/run-editorial-diaria
/run-report
/run-pipeline
/publish
/retry-failed-run
```

Esses comandos são exemplos. Cada cliente pode receber comandos adaptados ao produto digital que será construído ou operado.

---

## Feedback loop: execução -> construção

Quando uma rotina do plano de execução falhar, o sistema deve transformar a falha em item rastreável do plano de construção.

Fluxo esperado:

```text
Pipeline falha
  ↓
Sistema captura estágio da falha
  ↓
Sistema sanitiza erro
  ↓
Sistema cria issue no GitHub do cliente
  ↓
Issue recebe contexto reproduzível
  ↓
Issue recebe critério de aceite
  ↓
/advance pode tratar a issue posteriormente
```

Exemplo:

```text
Título:
Corrigir falha na geração de artefato do pipeline operacional

Contexto:
A falha ocorreu após a etapa de análise e antes da geração final do artefato.

Critério de aceite:
- pipeline deve concluir a etapa com sucesso;
- artefato final deve ser salvo;
- execução deve registrar status concluído;
- falha não deve se repetir nos dados de teste.
```

---

## Gates de aprovação

O sistema deve preservar gates antes de entregas relevantes.

### Gates mínimos

1. Gate técnico
   - valida execução;
   - valida testes;
   - valida consistência com issue;
   - valida ausência de erro crítico.

2. Gate de produto/editorial/domínio
   - valida aderência ao objetivo;
   - valida clareza do output;
   - valida adequação ao público;
   - valida consistência narrativa ou funcional;
   - valida critérios específicos do domínio.

3. Gate visual/artefato
   - valida UI;
   - valida layout;
   - valida gráficos;
   - valida PDFs/PPTX quando existirem;
   - valida outputs finais;
   - valida publicação final quando aplicável.

4. Gate de QA
   - valida regressão;
   - valida critérios de aceite;
   - valida comportamento esperado;
   - valida fluxo ponta a ponta.

No beta, os gates podem ser automáticos ou semi-automáticos, mas devem gerar registro resumido no GitHub do cliente ou no Monitor.

---

## Migração/encapsulamento do executor agentic

### Estado atual

```text
Usuário
  ↓
Claude Code
  ↓
arquivos locais
  ↓
sistema + projeto
```

Problemas:

- UI fechada;
- operador tem acesso total;
- cliente poderia acessar lógica interna;
- não há camada de controle;
- não é produto distribuível.

### Estado alvo

```text
Usuário
  ↓
UI controlada
  ↓
API própria
  ↓
runtime privado / executor agentic interno
  ↓
sistema privado + GitHub do cliente
```

O executor agentic passa a ser:

> processo interno de execução, não interface direta do cliente.

### Estratégia de encapsulamento

O beta não precisa migrar obrigatoriamente para OpenClaw se Claude Code/Codex já executarem bem o sistema atual.

A prioridade é encapsular o comportamento que já funciona em um runtime privado controlado por API.

Se OpenClaw for usado, a migração deve ser completa o suficiente para preservar a arquitetura dual.

Mapeamento esperado:

```text
Claude Code                 Runtime privado / OpenClaw opcional / SaaS beta
-------------------------------------------------------------
CLAUDE.md                   SOUL.md + AGENTS.md + policies
AGENTS.md                   AGENTS.md adaptado
.claude/agents/*.md         agents/*.md
commands/*.md               skills/commands ou command adapter
.claude/memory/*.md         memory privada + GitHub cliente
settings.json               runtime policies + backend policy
hooks/session_start         gateway hook ou backend lifecycle
hooks/post_write            backend/runtime event hooks
Task/subagents              OpenClaw agents / orchestration adapter
Cron/GitHub Actions         OpenClaw cron + backend scheduler
```

O objetivo não é apenas traduzir arquivos, mas preservar comportamento:

- PM/PO/TL continuam existindo como papéis operacionais;
- `/kickoff` e `/advance` continuam sendo fluxos centrais;
- GitHub/Kanban continua sendo fonte de verdade;
- gates continuam obrigatórios;
- nenhum agente faz merge do próprio trabalho;
- falhas de execução viram issues;
- outputs externos são sanitizados.

### Decisão para o beta

Para reduzir risco, a decisão recomendada para o beta é:

- manter Claude Code como executor interno inicial, se continuar sendo o caminho de maior qualidade;
- permitir Codex como executor alternativo;
- desenhar o job runner para aceitar OpenClaw futuramente;
- não expor nenhum executor diretamente ao cliente;
- tratar todos os executores como implementação interna atrás da API própria.

---

## Uso do WebChat / UI Web

### Decisão

Usar o WebChat do OpenClaw como referência/base quando viável, ou construir uma UI web equivalente inspirada no fluxo de chat/comandos.

### Motivo

A UI principal precisa suportar:

- conversa livre;
- comandos;
- histórico sanitizado;
- status de execução;
- fluxo próximo ao uso atual via Claude Code;
- menor superfície de exposição que Control UI ou Dashboard completo.

### Adaptações obrigatórias

Remover ou substituir:

- conexão direta com Gateway/OpenClaw;
- WebSocket direto do navegador para o runtime;
- autodiscovery de agentes;
- exposição de sessões internas;
- acesso a arquivos;
- views de sistema;
- referências a memory raw;
- settings expostos;
- agent listing;
- tool listing sensível.

Substituir por:

```text
UI Web controlada
  ↓
API própria
  ↓
runtime privado / executor agentic interno
```

Endpoints esperados:

```http
POST /chat
POST /command
GET /status
GET /history
GET /events
```

### Diff e mudancas do projeto

O cliente precisa conseguir ver diffs e mudancas propostas no projeto dele. Isso e parte da confianca operacional do produto e aproxima a experiencia de Claude Code/Codex Desktop.

Regra central:

```text
pode ver diff do project/
nao pode ver nada do system/
```

A UI pode ter uma area de `Changes`, `Diff`, `PR Preview` ou equivalente, mas ela nunca deve ler o filesystem diretamente.

Fluxo permitido:

```text
UI
  ↓
GET /project/changes
  ↓
API propria
  ↓
le apenas project/
  ↓
aplica allowlist de paths
  ↓
retorna diff sanitizado
```

Fontes possiveis do diff:

- `git status`;
- `git diff`;
- `git show`;
- `gh pr diff`;
- API do GitHub.

Tudo deve ser executado pelo backend dentro do repo do cliente, nunca no navegador e nunca sobre `system/`.

Permitido:

```text
project/src/**
project/docs/**
project/package.json
project/README.md
project/artifacts/**
issues/PRs/commits do cliente
```

Bloqueado:

```text
system/**
.claude/**
agents/**
commands/**
hooks/**
memory/**
settings.json
CLAUDE.md
SOUL.md
AGENTS.md
logs/internal/**
.env
tokens
```

Se a UI base for OpenCovibe ou OpenADE, componentes de diff podem ser reaproveitados, mas devem receber dados apenas da API filtrada, nao de file browser, shell, git local amplo ou runtime direto.

---

## Uso do Monitor/Dashboard

### Decisão

Reaproveitar parcialmente componentes/conceitos do Monitor/Dashboard, não como aplicação principal.

No caso especifico de OpenClaw, o Monitor/Dashboard deve ser entendido como parte do Control UI/admin surface. Ele pode ser util para o operador do sistema e como referencia de componentes, mas nao deve ser exposto diretamente ao cliente.

Componentes/conceitos aproveitaveis do OpenClaw Monitor/Control UI:

- overview/status;
- health;
- eventos resumidos;
- cards de uso/custo;
- historico de execucoes;
- status de cron/jobs;
- links para artefatos;
- links para issues/PRs;
- indicadores de falha;
- timeline operacional.

Componentes que nao devem ser expostos diretamente ao cliente:

- logs brutos;
- sessoes internas;
- payloads de eventos;
- config;
- skills/tools catalog;
- approvals internos;
- cron editor/admin;
- settings;
- Gateway state;
- raw usage por sessao quando revelar detalhes internos.

### Função do Monitor

O Monitor serve para observabilidade e confiança operacional.

Deve mostrar:

- status de execução;
- progresso do pipeline;
- eventos resumidos;
- erros sanitizados;
- latência;
- custo aproximado;
- última execução;
- artefatos gerados;
- links para issues/PRs/outputs;
- histórico operacional resumido.

### Exemplo de visualização permitida

```text
Produto Digital — Execução operacional

Status: concluído
Tempo total: 2m14s
Custo aproximado: R$ X

Etapas:
- Coleta: concluída
- Transformação: concluída
- Análise: concluída
- Geração de output: concluída
- Publicação/entrega: concluída

Artefatos:
- output.md
- dashboard_link
- relatório.pdf
- pull request #12
```

### O que o Monitor não pode mostrar

- agents internos;
- prompts;
- arquivos de sistema;
- memória raw;
- settings;
- stack traces completos;
- raciocínio interno;
- chamadas internas do runtime;
- regras do `CLAUDE.md`;
- regras do `SOUL.md`;
- regras do `AGENTS.md`;
- paths internos;
- payload bruto de tools.

---

## Componentes que não devem ser usados diretamente

### Control UI

Não usar como base principal.

Motivos:

- mais acoplada ao controle do sistema;
- expõe mais superfície interna;
- pressupõe que o usuário é operador/dono do sistema;
- maior risco de exposição de agents, tools e estado interno.

### TUI

Não usar para cliente.

Motivos:

- interface de terminal;
- útil para operador técnico;
- inadequada para produto web.

### Dashboard completo

Não usar direto.

Motivos:

- expõe estrutura operacional demais;
- deve ser usado apenas como fonte de componentes visuais;
- precisa de sanitização e redesign parcial.

---

## Backend/API própria

Criar uma API intermediária que seja a única superfície entre UI e runtime.

### Endpoints mínimos

```http
POST /chat
POST /command
GET /status
GET /events
GET /metrics
GET /history
```

### Responsabilidades da API

- autenticar cliente;
- receber mensagens da UI;
- receber comandos;
- carregar contexto do sistema privado;
- carregar estado do GitHub do cliente;
- chamar runtime/executor agentic interno;
- chamar LLM API;
- executar ações autorizadas;
- sanitizar outputs;
- bloquear vazamentos;
- retornar apenas dados permitidos;
- registrar eventos;
- controlar rate limits básicos;
- proteger tokens;
- impedir acesso direto a filesystem;
- impedir acesso direto a Gateway;
- filtrar logs e erros.

---

## Exemplo de fluxo: chat livre

```text
Cliente:
"Me explica o estado atual do projeto"

UI:
POST /chat

Backend:
- valida usuário
- lê issues do GitHub do cliente
- lê PRs relevantes
- lê estado do Kanban
- monta contexto permitido
- carrega regras internas sem expô-las
- chama runtime/LLM
- sanitiza resposta

UI:
exibe resposta final
```

---

## Exemplo de fluxo: comando /advance

```text
Cliente:
"/advance"

UI:
POST /command

Backend:
- valida comando
- consulta Kanban do cliente
- identifica próxima ação
- aciona runtime/executor agentic interno
- executa agentes internamente
- cria/comenta/move issues no GitHub do cliente
- retorna resumo sanitizado
```

---

## Exemplo de fluxo: falha em pipeline

```text
Rotina agendada falha
  ↓
Backend captura evento
  ↓
Runtime gera diagnóstico interno
  ↓
Sanitizer remove detalhes internos
  ↓
GitHub issue é criada
  ↓
Monitor mostra falha resumida
```

---

## Isolamento de arquivos de sistema

### Estrutura sugerida

```text
/opt/dual-agent-saas/
  system/
    SOUL.md
    CLAUDE.md
    AGENTS.md
    agents/
    hooks/
    commands/
    memory/
    skills/
    settings.json
    templates/
    policies/
    sanitizer/

  runtime/
    claude-code/
    codex/
    openclaw/   # opcional/futuro

  backend/
    app/

  frontend/
    web/

  logs/
    internal/
    public/
```

### Regras obrigatórias

A UI não pode:

- listar `/system`;
- ler arquivos;
- baixar arquivos;
- exibir nomes de agents;
- acessar settings;
- acessar memória raw;
- acessar logs internos;
- acessar runtime/Gateway/OpenClaw diretamente.

O runtime não pode oferecer ao usuário:

- file read genérico;
- shell aberto;
- endpoint de filesystem;
- endpoint de prompt dump;
- endpoint de agent listing;
- endpoint de memory dump.

---

## Integração com GitHub do cliente

### GitHub do cliente como source of truth

O sistema deve acessar:

- issues;
- PRs;
- commits;
- Kanban;
- comentários;
- labels;
- milestones, se necessário;
- branches;
- arquivos do projeto/produto, quando autorizado.

### Ações permitidas

- criar issue;
- comentar issue;
- mover card;
- abrir PR;
- revisar PR;
- sugerir mudanças;
- registrar entrega;
- vincular commit a issue;
- registrar falha sanitizada;
- criar artefato de output.

### Ações proibidas

- escrever arquivos de sistema no repo do cliente;
- mencionar regras internas;
- expor nomes ou conteúdo dos arquivos de sistema;
- despejar raciocínio completo;
- comentar detalhes internos dos agentes;
- expor prompts;
- expor paths internos.

---

## Audit trail operacional no GitHub do cliente

O sistema deve registrar no GitHub do cliente:

- issues criadas;
- critérios de aceite;
- comentários de progresso;
- PRs vinculados;
- commits referenciando issues;
- status de execução;
- falhas sanitizadas;
- links para artefatos gerados;
- decisões finais relevantes.

O sistema não deve registrar:

- prompts internos;
- nomes de arquivos de sistema;
- conteúdo de agents;
- raciocínio completo;
- paths internos;
- stack traces brutos;
- payload bruto de tools.

---

## Commits e PRs

### Convenções

- commits devem referenciar issue;
- mensagens devem seguir Conventional Commits;
- PRs devem conter:
  - issue relacionada;
  - resumo da mudança;
  - critério de aceite;
  - testes realizados;
  - riscos;
  - próximos impactos.

### Proibição

Nenhum agente deve fazer merge do próprio trabalho.

Regra esperada:

```text
especialista implementa
  ↓
tech-lead revisa
  ↓
QA valida
  ↓
merge ocorre após validação
  ↓
product-owner fecha issue
```

---

## Sanitização de output

Criar camada de sanitização para tudo que sai para:

- UI;
- GitHub;
- logs visíveis;
- Monitor;
- comentários;
- PRs;
- artefatos públicos.

### Remover ou reescrever

- nomes de agents internos quando desnecessário;
- referências a `CLAUDE.md`;
- referências a `SOUL.md`;
- referências a `AGENTS.md`;
- menções a hooks internos;
- prompts;
- raciocínio operacional detalhado;
- mensagens de erro com paths internos;
- stack traces brutos;
- dumps de memória;
- payload de tools.

### Exemplo ruim

```text
O tech-lead-agent rejeitou o PR conforme a regra definida no CLAUDE.md.
```

### Exemplo correto

```text
O PR foi rejeitado porque não atende ao critério de aceite definido na issue.
```

---

## Modelo de sessão

O sistema pode reconstruir contexto a cada sessão/chamada.

Isso é aceitável porque:

- LLM é stateless;
- estado do projeto vive no GitHub do cliente;
- arquivos do sistema são recarregáveis;
- custo maior está na chamada LLM, não na leitura dos markdowns.

### Estratégia beta

Usar reconstrução simples:

```text
request
  ↓
load private system context
  ↓
load client project state
  ↓
call runtime/LLM
  ↓
sanitize result
  ↓
write result
```

Não implementar memória de sessão sofisticada nesta fase.

---

## Artefatos do plano de execução

O plano de execução pode gerar qualquer artefato digital necessário ao produto do cliente, incluindo:

- código;
- APIs;
- dashboards;
- websites;
- pipelines;
- dados processados;
- markdowns;
- relatórios;
- PDFs;
- PPTX;
- gráficos;
- posts;
- boletins;
- outputs publicados;
- artefatos operacionais;
- documentação;
- pull requests;
- issues derivadas de falhas.

### Evolução posterior

Criar bibliotecas e templates pré-compilados para artefatos recorrentes:

- UI/components;
- pipelines;
- PDF;
- PPTX;
- gráficos;
- layouts;
- relatórios;
- dashboards;
- automações;
- scaffolds de produto.

Motivo:

- reduzir variabilidade;
- melhorar consistência visual e técnica;
- evitar geração dinâmica de código a cada execução;
- melhorar auditabilidade;
- acelerar entrega por domínio.

---

## Templates sincronizáveis

A arquitetura deve manter separação entre:

### 1. Sistema base privado

- agents universais;
- commands;
- hooks;
- regras de governança;
- runtime/executor agentic interno;
- lógica de orquestração;
- sanitização;
- integração com LLM;
- integração com GitHub.

### 2. Projeto/produto do cliente

- código;
- issues;
- PRs;
- documentação;
- artefatos;
- pipelines específicos;
- dados específicos;
- outputs.

### 3. Domínio/template verticalizado

- vocabulário especializado;
- agentes de domínio;
- workflows específicos;
- outputs próprios do domínio;
- gates específicos;
- integrações específicas.

A evolução do sistema base deve poder ser propagada para projetos/clientes sem expor arquivos internos.

---

## Infraestrutura beta

### Decisão

Usar uma única VM na nuvem para o beta, controlada pela infraestrutura própria.

O cliente acessa apenas:

- link web da UI;
- login/autenticação da UI;
- GitHub privado do projeto dele.

O cliente não acessa a VM, SSH, filesystem, runtime, logs internos, repo privado do sistema ou arquivos `.md` de sistema.

### Composição da VM

```text
VM única
  ├── frontend web
  ├── backend/API
  ├── job runner privado
  ├── executor agentic interno
  │   ├── Claude Code inicial/preferencial
  │   ├── Codex opcional
  │   └── OpenClaw opcional/futuro
  ├── system/
  │   └── clone sincronizado do repo privado do sistema
  ├── project/
  │   └── clone sincronizado do repo privado do cliente
  ├── integração GitHub
  ├── integração LLM
  ├── logs/internal/
  └── logs/public/
```

### Modelo de repositórios

O sistema opera com dois repositórios separados:

```text
Repo privado do sistema (seu GitHub)
  └── system/
      ├── SOUL.md / CLAUDE.md
      ├── AGENTS.md
      ├── agents/
      ├── commands/
      ├── hooks/
      ├── memory/
      ├── skills/
      ├── settings.json
      ├── templates/
      ├── policies/
      └── sanitizer/

Repo privado do cliente (GitHub do cliente)
  └── project/
      ├── código do produto
      ├── documentação pública do projeto
      ├── artefatos
      ├── issues
      ├── PRs
      ├── commits
      └── Kanban
```

Na VM:

- `system/` é sincronizado a partir do repo privado do sistema;
- `project/` é sincronizado a partir do repo privado do cliente;
- o runtime lê `system/` como metodologia privada;
- o runtime opera em `project/` como workspace do cliente;
- a UI nunca acessa `system/` ou `project/` diretamente;
- toda interação visível passa pela API e pelo sanitizer;
- outputs permitidos são escritos no GitHub do cliente.

### Regras de sincronização

- `system/` deve ser tratado como read-only durante execuções normais.
- Atualização de `system/` acontece apenas por deploy/control plane do operador.
- `project/` é o único workspace gravável para código, docs, artefatos, branches e commits do cliente.
- Arquivos de sistema nunca podem ser copiados para `project/`.
- Templates privados só podem gerar artefatos públicos depois de renderização/sanitização.
- Cada execução deve registrar qual versão do sistema foi usada, por exemplo `system@v0.3.1`.
- Tokens devem ser separados:
  - token do operador para clonar/atualizar `system`;
  - token/GitHub App do cliente para operar `project`;
  - tokens LLM apenas no backend.

### Acesso

Cliente acessa:

```text
https://produto.seudominio.com
```

Cliente não acessa:

- SSH;
- executor interno direto;
- OpenClaw direto, se existir;
- Gateway direto, se existir;
- filesystem;
- repo interno do sistema;
- logs internos;
- variáveis de ambiente;
- tokens;
- prompts.

---

## Autenticação

Para beta, implementar autenticação simples:

- login/senha;
- token estático;
- ou autenticação via basic auth/reverse proxy.

Não implementar RBAC avançado nesta fase.

---

## Segurança mínima

### Obrigatório

- runtime/Gateway/OpenClaw não exposto publicamente;
- apenas API própria exposta;
- arquivos de sistema fora do root público;
- variáveis de ambiente protegidas;
- tokens GitHub e LLM no backend;
- logs externos sanitizados;
- bloqueio de file explorer;
- bloqueio de agent listing;
- bloqueio de memory raw;
- bloqueio de shell;
- bloqueio de file read genérico.

---

## Uso de LLM API

O sistema deve usar LLM via API.

Inicialmente:

- Anthropic Claude.

Possibilidades futuras:

- OpenAI;
- outros modelos compatíveis.

Regras:

- API key pertence à infraestrutura;
- cliente não insere key própria no beta;
- custo pode ser repassado depois por uso/token;
- logs de custo devem ser agregados e sanitizados.

---

## Modelo comercial beta

O produto será oferecido como:

> acesso a um sistema web hospedado na infraestrutura própria, operando sobre o GitHub do cliente.

Também poderá ser vendido inicialmente como serviço B2B assistido:

> desenvolvimento de um produto digital do zero usando a arquitetura dual multi-agente beta, com GitHub/Kanban, backlog, PRs, documentação, monitor e operação controlada.

O beta deve ser vendido como capacidade produtiva B2B assistida, não como framework, prompt pack ou template baixável.

Não será oferecido como:

- repo;
- template baixável;
- executável;
- instalação local no cliente;
- pacote open-source;
- fork entregável.

---

## Estimativa de prazo

Prazo realista:

```text
2 semanas a 1 mês
```

### Estimativa por bloco

| Bloco | Estimativa |
|---|---:|
| Setup executor inicial Claude Code/Codex em VM | 1-3 dias |
| Encapsulamento Claude Code/Codex em runner privado | 3-7 dias |
| Avaliação/migração OpenClaw opcional | 2-7 dias |
| Adaptação UI/WebChat | 3-7 dias |
| Backend/API intermediária | 3-7 dias |
| Integração GitHub | 2-5 dias |
| Monitor parcial | 2-5 dias |
| Sanitização e hardening mínimo | 2-5 dias |
| Teste end-to-end | 2-5 dias |
| Ajustes finais | 2-5 dias |

---

## Fora de escopo no beta

Não implementar agora:

- multi-tenant;
- RBAC avançado;
- billing automático;
- isolamento por cliente em escala;
- marketplace;
- versão on-premise;
- proteção avançada contra engenharia reversa;
- auditoria enterprise completa;
- UI completa própria do zero se WebChat/UI adaptada for suficiente;
- controle sofisticado de sessão;
- observabilidade enterprise;
- automação total de priorização;
- templates finais de artefatos para todos os domínios.

---

## Riscos conhecidos

### Aceitáveis no beta

- cliente pode inferir padrões;
- cliente pode observar comportamento;
- cliente pode tentar reproduzir lógica;
- segurança contra engenharia reversa comportamental ainda não é prioridade.

### Não aceitáveis

- cliente acessar arquivos de sistema;
- cliente acessar runtime/Gateway/OpenClaw diretamente;
- cliente listar agents;
- cliente ver prompts;
- cliente ver memória raw;
- cliente conseguir executar shell;
- cliente conseguir ler filesystem interno;
- cliente copiar o sistema com um clique.

---

## Critérios de aceite

### UI

- cliente acessa por link web;
- cliente consegue conversar com o sistema;
- cliente consegue executar comandos;
- cliente consegue visualizar status de execução;
- cliente consegue ver eventos resumidos;
- cliente não vê arquivos de sistema;
- cliente não vê agents internos;
- cliente não vê memória raw;
- cliente não acessa runtime/Gateway/OpenClaw diretamente.

### Runtime

- executor agentic interno roda de forma privada;
- Claude Code/Codex funcionam como executor inicial, se escolhidos;
- OpenClaw roda internamente apenas se for adotado como executor opcional;
- sistema carrega arquivos internos;
- comandos funcionam;
- hooks/session_start funcionam ou têm substituto equivalente;
- chamadas LLM funcionam via API;
- runtime não expõe tools perigosas ao cliente.

### GitHub

- sistema lê Kanban/issues/PRs do cliente;
- sistema cria issues;
- sistema comenta issues;
- sistema abre PRs, se aplicável;
- sistema referencia issues nos commits;
- sistema registra falhas sanitizadas;
- sistema não escreve arquivos de sistema no repo do cliente.

### Monitor

- exibe status de execução;
- exibe eventos resumidos;
- exibe métricas básicas;
- exibe custos aproximados, se disponível;
- não exibe agents;
- não exibe prompts;
- não exibe paths internos;
- não exibe stack trace bruto.

### Segurança

- Gateway privado;
- API própria como única superfície;
- filesystem interno inacessível;
- outputs sanitizados;
- logs visíveis não expõem paths/prompts/agents;
- tokens protegidos;
- endpoints sensíveis inexistentes ou bloqueados.

### Produto B2B beta

- sistema consegue iniciar projeto digital do zero;
- sistema consegue adaptar agentes/comandos ao contexto do cliente;
- sistema consegue criar backlog inicial;
- sistema consegue executar `/kickoff`;
- sistema consegue executar `/advance`;
- sistema consegue gerar issues, PRs, status e artefatos;
- sistema consegue operar rotina do plano de execução;
- sistema consegue transformar falha em issue rastreável.

---

## Resultado esperado

Ao final desta epic, o sistema deixa de ser:

```text
ambiente local operado via Claude Code
```

E passa a ser:

```text
produto web beta operado via UI controlada,
com runtime/executor agentic privado,
estado operacional no GitHub do cliente,
arquivos de sistema isolados,
metodologia multi-agente proprietária encapsulada
e execução via LLM API.
```

---

## Formulação final

O cliente não recebe o sistema.

O cliente recebe acesso a:

> uma interface web que aciona um sistema de agentes hospedado e controlado pela infraestrutura própria.

A inteligência permanece privada.

O GitHub do cliente permanece como espaço operacional do projeto/produto.

A arquitetura dual multi-agente pode ser adaptada ao contexto do cliente para construir e operar produtos digitais tradicionais ou agentic-native.

---

# Issues derivadas

- [ ] Mapear equivalência Claude Code -> runtime privado e OpenClaw opcional
- [ ] Mapear arquitetura Claude Code/Codex como executor interno isolado
- [ ] Migrar `CLAUDE.md`/governança central para `SOUL.md` + `AGENTS.md`
- [ ] Encapsular agents especializados no executor escolhido
- [ ] Encapsular commands principais no command adapter
- [ ] Setup VM única com UI, API, runner, `system/` e `project/`
- [ ] Sincronizar `system/` com repo privado do sistema
- [ ] Sincronizar `project/` com repo privado do cliente
- [ ] Avaliar OpenCovibe como base principal de UI
- [ ] Avaliar OpenADE como segunda candidata/base de componentes de diff e cockpit
- [ ] Avaliar OpenClaw + WebChat + Monitor/Control UI como runtime/control plane opcional
- [ ] Setup OpenClaw runtime em VM, se adotado como executor
- [ ] Encapsular Claude Code/Codex em job runner privado
- [ ] Criar backend wrapper com `/chat` e `/command`
- [ ] Garantir que UI nunca conecta direto ao runtime/Gateway/OpenClaw
- [ ] Adaptar OpenCovibe/OpenADE/WebChat ou criar UI web equivalente controlada
- [ ] Implementar visualizacao de diff apenas do `project/`
- [ ] Bloquear diffs, file browser e previews de qualquer path de `system/`
- [ ] Integrar GitHub do cliente
- [ ] Implementar leitura de Kanban/issues/PRs
- [ ] Implementar criação/comentário/movimentação de issues
- [ ] Implementar criação de PRs quando aplicável
- [ ] Implementar sanitização de outputs
- [ ] Implementar sanitização de erros/logs
- [ ] Reaproveitar componentes/conceitos do Monitor para status/eventos
- [ ] Implementar autenticação simples
- [ ] Bloquear tools perigosas
- [ ] Bloquear file read genérico
- [ ] Bloquear shell exposto ao cliente
- [ ] Bloquear agent listing
- [ ] Bloquear memory raw
- [ ] Testar fluxo `/kickoff`
- [ ] Testar fluxo `/advance`
- [ ] Testar fluxo de chat livre
- [ ] Testar falha de pipeline -> criação de issue
- [ ] Testar geração de artefato digital
- [ ] Testar criação de produto digital do zero
- [ ] Testar adaptação de agentes/comandos ao cliente
- [ ] Testar ausência de vazamento de arquivos de sistema
- [ ] Testar ausência de acesso direto ao runtime/Gateway/OpenClaw
- [ ] Testar logs públicos sanitizados
- [ ] Testar monitor sem prompts, paths, agents ou stack traces brutos

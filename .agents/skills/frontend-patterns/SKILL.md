# Skill: Frontend Patterns

Estrutura de projeto frontend e padrões de código — usado pelo `design-engineer`.

## Quando usar
Ao **organizar estrutura** de projeto frontend e **escrever código** seguindo padrões (módulos, integração API, tipos). Para **qualidade de componente** (a11y, responsividade, estados), use `frontend-engineering`.

## Estrutura típica de projeto

```
src/
  components/   # componentes reutilizáveis
  pages/        # rotas/páginas
  hooks/        # custom hooks
  services/     # chamadas de API
  types/        # tipos TypeScript
```

> **Onde mora**: depende do contexto. Frontend específico de um produto vai em `products/<produto>/src/`. Lib de UI compartilhada entre múltiplos produtos do projeto vai em `src/` raiz (Mundo 1). Ver CLAUDE.md §"Critério do leitor primário".

## Boas práticas

- TypeScript em todos os arquivos
- Variáveis de ambiente para endpoints e keys (nunca hardcodar)
- Testar componentes críticos com Vitest
- Garantir acessibilidade: labels, alt text, contraste
- Validar em mobile e desktop antes de entregar

## Integração com API

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL

async function fetchData<T>(endpoint: string): Promise<T> {
  const res = await fetch(`${API_URL}/${endpoint}`)
  if (!res.ok) throw new Error(`HTTP ${res.status}`)
  return res.json()
}
```

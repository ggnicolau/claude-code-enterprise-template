# Skill: Frontend Engineering

Qualidade de componente, acessibilidade e UX — usado pelo `design-engineer`.

## Quando usar
Ao **avaliar/garantir qualidade** de componente individual: a11y, responsividade, performance, estados. Para **estrutura de projeto** (organização de pastas, integração API, padrões de código), use `frontend-patterns`.

## Checklist de componente

**Funcionalidade:**
- [ ] Estados cobertos: loading, error, empty, populated
- [ ] Props tipadas (TypeScript obrigatório)
- [ ] Eventos e callbacks documentados

**Acessibilidade (WCAG 2.1 AA):**
- [ ] Elementos interativos acessíveis via teclado
- [ ] Labels semânticos em formulários (`<label for>` ou `aria-label`)
- [ ] Contraste mínimo 4.5:1 para texto normal
- [ ] Feedback de erro descritivo (não só cor)

**Responsividade:**
- [ ] Mobile-first — breakpoints testados (320px, 768px, 1024px+)
- [ ] Nenhum scroll horizontal inesperado

**Performance:**
- [ ] Imagens com lazy loading quando aplicável
- [ ] Sem re-renders desnecessários (memo, useMemo, useCallback onde justificado)

## Stack padrão
React + Next.js · Tailwind CSS · TypeScript · Vitest/Jest para testes de componente

## Boas práticas
- Componentes pequenos e reutilizáveis — sem lógica de negócio no componente
- Lógica de estado em hooks customizados
- Design tokens no Tailwind config — não hardcodar cores ou espaçamentos
- Testar o fluxo do usuário, não a implementação interna
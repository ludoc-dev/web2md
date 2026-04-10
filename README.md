# web2md

CLI para extrair conteúdo web, remover ruídos e converter para Markdown puro.

## Instalação

```bash
cd ~/web2md
bun install
```

## Uso

```bash
# Básico (stdout)
bun run web2md.ts https://example.com/article

# Salvar em arquivo
bun run web2md.ts https://example.com/article --out article.md

# Com renderização JavaScript (Playwright)
bun run web2md.ts https://spa-example.com --js --out spa.md

# Pipe para LLM
bun run web2md.ts https://example.com | llm-agent
```

## Flags

- `--js`: Renderiza JavaScript antes de extrair (SPAs)
- `--out <file>`: Salva em arquivo ao invés de stdout

## Pipeline

1. Fetch HTML
2. Parse DOM (JSDOM)
3. Remove ruído (Readability)
4. Converte para Markdown (Turndown)

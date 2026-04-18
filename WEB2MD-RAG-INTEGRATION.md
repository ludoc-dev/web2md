# web2md + Advanced RAG = Harness Completo de Auto-Research

## Visão Geral

O **web2md** não é apenas um conversor de HTML para Markdown - é o **coração de um sistema de auto-research** que integra:

1. **Advanced RAG MCP** - Busca semântica no codebase
2. **Code Graph MCP** - Análise de dependências
3. **web2md** - Extração de conteúdo web

## Workflow Completo de Auto-Research

### Stage 1: Discover (Auto-Research)

```yaml
discover:
  stage: discover
  script:
    - bash ~/.claude/research/auto-research.sh
```

### Como Funciona na Prática

#### 1. Indexar Codebase (Advanced RAG)

```
"Index this codebase for semantic search"
```

**O que acontece:**
- Advanced RAG MCP escaneia todos os arquivos
- Cria embeddings com sentence-transformers
- Armazena no ChromaDB
- Resultado: Codebase indexado e pronto para busca

#### 2. Buscar Informação (Semantic Search)

```
"Search for web scraping functions"
"Find all code related to error handling"
"Show me authentication logic"
```

**O que acontece:**
- Advanced RAG MCP faz busca semântica
- Retorna arquivos mais relevantes
- Fornece contexto otimizado para LLM
- Resultado: Código relevante encontrado

#### 3. Extrair Conteúdo Web (web2md)

```
"Extract https://example.com/article"
"Index this documentation page"
```

**O que acontece:**
- web2md baixa HTML
- Remove ruído (ads, navbars)
- Converte para Markdown limpo
- Resultado: Conteúdo pronto para LLM (90% economia)

#### 4. Analisar Dependências (Code Graph)

```
"Trace all function calls in web2md.ts"
"Find all usages of web2md_extract"
"Generate dependency graph"
```

**O que acontece:**
- Code Graph MCP analisa AST
- Rastreia chamadas de função
- Gera grafos de dependência
- Resultado: Estrutura do código mapeada

## Exemplo de Uso Completo

### Cenário: Pesquisar sobre Implementação X

```
User: "Como funciona o sistema de extração do web2md?"

Claude:
[Advanced RAG] Buscando "web2md extraction system"...
  ✓ Encontrado: web2md.ts (main extraction logic)
  ✓ Encontrado: README.md (documentação)
  ✓ Encontrado: tests/unit/test_web2md.py (testes)

[Code Graph] Analisando dependências de web2md.ts...
  ✓ trace_calls: web2md.ts → fetchHTML() → parseToMarkdown()
  ✓ impact_analysis: Mudanças em fetchHTML afetam parseToMarkdown

[web2md] Extraindo documentação relevante...
  ✓ https://example.com → Markdown limpo

[Resposta Composta]
O sistema de extração do web2md funciona em 3 etapas:

1. **fetchHTML()** (linha 32-44):
   - Suporta HTTP/HTTPS
   - Suporta arquivos locais (file://)
   - Opcional: Playwright para JavaScript rendering

2. **parseToMarkdown()** (linha 46-56):
   - JSDOM para DOM virtual
   - Readability para limpar ruído
   - Turndown para Markdown

3. **Saída**:
   - stdout (default)
   - Arquivo com --out
   - 90% economia de tokens vs HTML cru
```

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────┐
│                 Auto-Research Harness                  │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────────┐      ┌──────────────────┐        │
│  │ Advanced RAG MCP │◄────►│  Code Graph MCP  │        │
│  │  - Semantic Search│      │  - Call Tracing  │        │
│  │  - Context Retrieval│    │  - Dependencies  │        │
│  └─────────┬─────────┘      └─────────┬────────┘        │
│            │                         │                   │
│            └──────────┬───────────────┘                   │
│                       │                                   │
│                       ▼                                   │
│              ┌────────────────┐                          │
│              │    web2md      │                          │
│              │  - HTML→MD     │                          │
│              │  - Clean       │                          │
│              │  - Extract     │                          │
│              └────────────────┘                          │
│                       │                                   │
│                       ▼                                   │
│              ┌────────────────┐                          │
│              │  LLM Context   │                          │
│              │  Optimizado    │                          │
│              └────────────────┘                          │
└─────────────────────────────────────────────────────────┘
```

## Teste de Integração

O teste `test_research_workflow` verifica que:

1. ✅ web2md está disponível
2. ⏳ MCP servers estão carregados (requer ambiente Claude Code)
3. ⏳ Workflow completo funciona (end-to-end)

## Benefícios do Harness Completo

### 1. Pesquisa Inteligente
- Busca semântica (não apenas keyword)
- Contexto relevante automaticamente
- Economia de tokens (90%)

### 2. Análise de Código
- Dependências mapeadas
- Impacto de mudanças previsto
- Refactoring seguro

### 3. Extração Web
- Documentação externa indexada
- Artigos técnicos processados
- Tutorials convertidos para Markdown

### 4. Automação Completa
- Stage 1: Discover (auto-research)
- Stage 2-6: Build, Test, Performance, Quality, Report
- Tudo integrado no GitLab CI

## Próximos Passos

### Para Usar o Harness Completo:

1. **Reiniciar Claude Code** (carregar MCP servers)
   ```bash
   claude mcp list
   # Deve mostrar: code-graph, advanced-rag
   ```

2. **Indexar codebase**
   ```
   "Index this codebase for semantic search"
   ```

3. **Usar workflow completo**
   ```
   "Pesquise sobre implementação de X"
   "Analise dependências da função Y"
   "Extraia documentação de Z"
   ```

### Para Implementar Próximas Features:

- GUI Automation MCP (testes visuais)
- Multi-Model Support (otimização de custo)
- Real-time Collaboration (MCP sync)

## Conclusão

**web2md ≠ apenas conversor**
**web2md = coração do harness de auto-research**

Com Advanced RAG + Code Graph + web2md, temos um sistema completo de:
- ✅ Descoberta automática
- ✅ Análise inteligente
- ✅ Extração otimizada
- ✅ Contexto para LLM

**Isso é o futuro do desenvolvimento assistido por IA!** 🚀

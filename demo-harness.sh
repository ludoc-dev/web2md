#!/bin/bash
# demo-harness.sh - Demonstração do Harness Completo web2md + RAG
# Este script mostra como usar o sistema de auto-research integrado

echo "🚀 Harness Completo web2md + Advanced RAG + Code Graph"
echo "========================================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Etapa 1: Verificar MCP servers
echo -e "${BLUE}1️⃣  Verificando MCP Servers...${NC}"
echo "   Executar: claude mcp list"
echo "   Esperado: code-graph, advanced-rag"
echo ""

# Etapa 2: Exemplo de uso do Advanced RAG
echo -e "${BLUE}2️⃣  Advanced RAG - Busca Semântica${NC}"
echo "   Comando: semantic_search('web scraping functions')"
echo "   Resultado: Arquivos mais relevantes com contexto"
echo ""

# Etapa 3: Exemplo de uso do Code Graph
echo -e "${BLUE}3️⃣  Code Graph - Análise de Dependências${NC}"
echo "   Comando: trace_calls('web2md.ts')"
echo "   Resultado: Grafo de chamadas de função"
echo ""

# Etapa 4: Exemplo de uso do web2md
echo -e "${BLUE}4️⃣  web2md - Extração de Conteúdo${NC}"
echo "   Comando: bun run web2md.ts https://example.com"
echo "   Resultado: Markdown limpo (90% economia)"
echo ""

# Etapa 5: Workflow Completo
echo -e "${GREEN}🎯 Workflow Completo de Auto-Research${NC}"
echo ""
echo "Cenário: Pesquisar sobre 'como funciona extração do web2md'"
echo ""
echo "Passo 1: Indexar codebase"
echo "  $ index_codebase()"
echo ""
echo "Passo 2: Buscar informação relevante"
echo "  $ semantic_search('web2md extraction logic')"
echo "  ✓ Encontrado: web2md.ts (main logic)"
echo "  ✓ Encontrado: README.md (documentation)"
echo ""
echo "Passo 3: Analisar dependências"
echo "  $ trace_calls('web2md.ts')"
echo "  ✓ fetchHTML() → parseToMarkdown()"
echo ""
echo "Passo 4: Extrair documentação externa (se necessário)"
echo "  $ bun run web2md.ts https://developer.mozilla.org/en-US/docs/Web/HTTP"
echo "  ✓ Documentação convertida para Markdown"
echo ""
echo "Passo 5: Gerar resposta consolidada"
echo "  ✓ Código interno analisado"
echo "  ✓ Documentação externa extraída"
echo "  ✓ Contexto otimizado para LLM"
echo ""

# Etapa 6: Exemplos práticos
echo -e "${YELLOW}📚 Exemplos Práticos de Uso${NC}"
echo ""
echo "1. Pesquisar implementação:"
echo "   \"Analise como funciona o sistema de autenticação\""
echo ""
echo "2. Refactoring seguro:"
echo "   \"Quais funções serão afetadas se eu mudar fetchHTML?\""
echo ""
echo "3. Aprendizado de código:"
echo "   \"Explique a arquitetura do web2md com exemplos\""
echo ""
echo "4. Documentação automática:"
echo "   \"Extraia e indexe a documentação da lib X\""
echo ""

# Etapa 7: Próximos passos
echo -e "${GREEN}🚀 Próximos Passos${NC}"
echo ""
echo "1. Reiniciar Claude Code para carregar MCP servers"
echo "2. Indexar codebase: \"Index this codebase\""
echo "3. Usar workflow: \"Pesquise sobre [tópico]\""
echo ""

echo -e "${GREEN}✅ Harness pronto para uso!${NC}"
echo ""
echo "Documentação completa: WEB2MD-RAG-INTEGRATION.md"

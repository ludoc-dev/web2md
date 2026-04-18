# Status MCP Servers - Pós Reinício

## ✅ Configuração Atual

**Arquivo:** `~/.claude/settings.json`

```json
"mcpServers": {
  "code-graph": {
    "command": "/Users/lucascardoso/web2md/mcp-servers/code-graph/venv/bin/python",
    "args": ["-u", "/Users/lucascardoso/web2md/mcp-servers/code-graph/server.py"],
    "cwd": "/Users/lucascardoso/web2md/mcp-servers/code-graph"
  },
  "advanced-rag": {
    "command": "/Users/lucascardoso/web2md/mcp-servers/advanced-rag/venv/bin/python",
    "args": ["-u", "/Users/lucascardoso/web2md/mcp-servers/advanced-rag/server.py"],
    "cwd": "/Users/lucascardoso/web2md/mcp-servers/advanced-rag"
  }
}
```

**Validação:** ✅ JSON válido

## 🔍 Situação Atual

### O que foi verificado:

1. ✅ **Executáveis existem**
   - `/Users/lucascardoso/web2md/mcp-servers/code-graph/venv/bin/python` ✓
   - `/Users/lucascardoso/web2md/mcp-servers/advanced-rag/venv/bin/python` ✓

2. ✅ **Servidores iniciam manualmente**
   - `code-graph/server.py` roda sem erros
   - `advanced-rag/server.py` roda sem erros

3. ✅ **FastMCP disponível**
   - Versão 1.27.0 instalada
   - Import funciona corretamente

4. ✅ **Scripts wrapper criados**
   - `run.sh` para cada servidor (ativa venv + executa)

5. ⚠️ **MCP servers NÃO aparecem em `claude mcp list`**
   - Provávelmente por causa do **Python 3.14.3** no venv
   - Python 3.14 é muito novo e pode ter problemas de compatibilidade

## 🔧 Solução Recomendada

### Opção 1: Recriar venvs com Python 3.11 ou 3.13 (RECOMENDADO)

```bash
# Code Graph
cd /Users/lucascardoso/web2md/mcp-servers/code-graph
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Advanced RAG
cd /Users/lucascardoso/web2md/mcp-servers/advanced-rag
rm -rf venv
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Opção 2: Usar wrapper scripts (JÁ CRIADO)

```json
"mcpServers": {
  "code-graph": {
    "command": "/Users/lucascardoso/web2md/mcp-servers/code-graph/run.sh"
  },
  "advanced-rag": {
    "command": "/Users/lucascardoso/web2md/mcp-servers/advanced-rag/run.sh"
  }
}
```

## 📊 Verificação Pós-Reinício

Após o próximo reinício do Claude Code, verificar:

```bash
# 1. Verificar se MCP servers aparecem
claude mcp list | grep -E "(code-graph|advanced-rag)"

# 2. Se não aparecerem, verificar logs
# Logs estão em: ~/Library/Logs/Claude/

# 3. Testar manualmente
cd /Users/lucascardoso/web2md/mcp-servers/code-graph
./run.sh

# 4. Verificar Python version
python --version  # Deve ser 3.11 ou 3.13, não 3.14
```

## 🎯 Próximos Passos

1. **Recriar venvs** com Python 3.11 (mais estável)
2. **Reiniciar Claude Code**
3. **Verificar**: `claude mcp list`
4. **Testar**: Usar ferramentas MCP

## ⚠️ Diagnóstico

**Por que não estão aparecendo?**

1. **Python 3.14.3**: Muito novo, pode ter problemas com MCP SDK
2. **Stdio transport**: Pode não estar funcionando corretamente
3. **Path resolution**: O venv pode não estar sendo ativado corretamente

**Solução mais provável:** Recriar venvs com Python 3.11

## 📝 Status

- ✅ Configuração JSON correta
- ✅ Servidores implementados
- ✅ Scripts wrapper criados
- ⏳ **Aguardando:** Recriação de venvs com Python 3.11
- ⏳ **Aguardando:** Próximo reinício do Claude Code

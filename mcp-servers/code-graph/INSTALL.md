# Code Graph Analysis MCP Server - Installation Guide

## Quick Start

### 1. Install Dependencies

```bash
cd /Users/lucascardoso/web2md/mcp-servers/code-graph
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Test Standalone

```bash
# Test analyzer functions
python -c "
from analyzer import CodeAnalyzer
import json

analyzer = CodeAnalyzer('/Users/lucascardoso/web2md')
result = analyzer.trace_calls('/Users/lucascardoso/web2md/web2md.ts')
print(json.dumps(result, indent=2))
"
```

### 3. Run MCP Server

```bash
# Start server (stdio transport)
python server.py
```

### 4. Configure Claude Code

Add to `~/.config/claude/settings.json`:

```json
{
  "mcpServers": {
    "code-graph": {
      "command": "/Users/lucascardoso/web2md/mcp-servers/code-graph/venv/bin/python",
      "args": ["/Users/lucascardoso/web2md/mcp-servers/code-graph/server.py"]
    }
  }
}
```

### 5. Use in Claude Code

```
"Trace all function calls in web2md.ts"
"Impact analysis for web2md_extract function"
"Generate dependency graph for this project"
```

## Testing

### Unit Tests
```bash
pytest tests/test_analyzer.py -v
```

### Integration Tests
```bash
python tests/test_integration.py
```

## Features

### 1. trace_calls
Trace function calls in a file

**Input:**
- `file_path`: Path to file
- `depth`: How deep to trace (default: 3)

**Output:**
```json
{
  "file": "web2md.ts",
  "language": "ts",
  "functions": [...],
  "graph": {...}
}
```

### 2. impact_analysis
Find all usages of a symbol

**Input:**
- `symbol`: Symbol name
- `symbol_type`: function|class|variable

**Output:**
```json
{
  "symbol": "web2md_extract",
  "affected_files": [...],
  "total_usages": 15,
  "risk_level": "high"
}
```

### 3. dependency_graph
Generate dependency graph

**Input:**
- `format`: json|mermaid|dot

**Output:**
```json
{
  "nodes": [...],
  "edges": [...]
}
```

## Performance

- Small files (<100 lines): <1s
- Medium files (100-1000 lines): <3s
- Large projects (100+ files): <10s

## Limitations

- Languages: Python, TypeScript, JavaScript
- Dynamic calls: Cannot trace runtime-generated calls
- External deps: Only analyzes local code

## Troubleshooting

### ModuleNotFoundError
```bash
# Activate venv
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### File not found
```bash
# Use absolute paths
analyzer.trace_calls('/Users/lucascardoso/web2md/web2md.ts')
```

### MCP server not connecting
```bash
# Check server runs
python server.py

# Check Claude Code config
cat ~/.config/claude/settings.json

# Test MCP inspector
mcp-inspector stdio python server.py
```

## Next Steps

- [ ] Add support for Rust, Go
- [ ] Implement dynamic call tracing
- [ ] Add external dependency analysis
- [ ] Create web UI for visualization

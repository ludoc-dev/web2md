# Code Graph Analysis MCP Server

**Purpose:** Analyze code structure, trace calls, and identify dependencies

## Features

### 1. Trace Calls

Trace all function calls in a file or directory

```bash
# Trace single file
trace_calls("web2md.ts")
→ Returns: call graph with all function invocations

# Trace directory
trace_calls("/Users/lucascardoso/web2md")
→ Returns: aggregated call graph
```

### 2. Impact Analysis

Find all files/functions affected by changing a symbol

```bash
# Analyze function change
impact_analysis("web2md_extract", "function")
→ Returns: 15 files affected, 47 call sites

# Analyze class change
impact_analysis("BasePage", "class")
→ Returns: 8 files affected, 23 usages
```

### 3. Dependency Graph

Generate module dependency graph

```bash
# JSON format
dependency_graph("json")
→ Returns: {"nodes": [...], "edges": [...]}

# Mermaid format
dependency_graph("mermaid")
→ Returns: "graph TD; A[web2md.ts] --> B[utils.ts];"

# DOT format
dependency_graph("dot")
→ Returns: "digraph G { \"web2md.ts\" -> \"utils.ts\"; }"
```

## Installation

```bash
cd mcp-servers/code-graph
pip install -r requirements.txt
```

## Usage

### As MCP Server

Add to `settings.json`:

```json
{
  "mcpServers": {
    "code-graph": {
      "command": "python",
      "args": ["/Users/lucascardoso/web2md/mcp-servers/code-graph/server.py"]
    }
  }
}
```

### Standalone

```bash
# Trace calls
python server.py trace_calls web2md.ts

# Impact analysis
python server.py impact_analysis web2md_extract function

# Dependency graph
python server.py dependency_graph mermaid
```

## Architecture

```
code-graph/
├── server.py          # MCP server implementation
├── analyzer.py        # Core analysis logic
├── parsers/           # Language parsers
│   ├── python.py      # Python AST parser
│   ├── typescript.py  # TypeScript parser
│   └── javascript.js  # JavaScript parser
├── utils/             # Utilities
│   ├── graph.py       # Graph operations
│   └── config.py      # Configuration
├── tests/             # Tests
│   ├── test_analyzer.py
│   └── test_server.py
├── requirements.txt
└── README.md
```

## API

### trace_calls(file_path: str, depth: int = 3) -> dict

Trace function calls in a file.

**Parameters:**

- `file_path`: Path to file to analyze
- `depth`: How deep to trace calls (default: 3)

**Returns:**

```json
{
  "file": "web2md.ts",
  "functions": [
    {
      "name": "web2md_extract",
      "line": 42,
      "calls": ["fetch_html", "parse_content", "convert_md"]
    }
  ],
  "graph": {
    "nodes": ["web2md_extract", "fetch_html", "parse_content"],
    "edges": [["web2md_extract", "fetch_html"]]
  }
}
```

### impact_analysis(symbol: str, symbol_type: str) -> dict

Find all usages of a symbol.

**Parameters:**

- `symbol`: Symbol name (function, class, variable)
- `symbol_type`: Type of symbol ("function", "class", "variable")

**Returns:**

```json
{
  "symbol": "web2md_extract",
  "type": "function",
  "affected_files": [
    {
      "file": "tests/web2md_test.py",
      "usages": 5,
      "lines": [10, 25, 47, 82, 103]
    }
  ],
  "total_usages": 15,
  "risk_level": "high"
}
```

### dependency_graph(format: str = "json") -> dict | str

Generate dependency graph.

**Parameters:**

- `format`: Output format ("json", "mermaid", "dot")

**Returns:**

```json
{
  "nodes": [{ "id": "web2md.ts", "label": "web2md.ts", "type": "source" }],
  "edges": [{ "from": "web2md.ts", "to": "utils.ts", "type": "imports" }]
}
```

## Performance

- **Small files** (<100 lines): <1s
- **Medium files** (100-1000 lines): <3s
- **Large projects** (100+ files): <10s

## Limitations

- **Languages**: Python, TypeScript, JavaScript (planned: Rust, Go)
- **Dynamic calls**: Cannot trace runtime-generated calls
- **External deps**: Only analyzes local code

## Testing

```bash
# Unit tests
pytest tests/test_analyzer.py

# Integration tests
pytest tests/test_server.py

# Manual test
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"trace_calls","arguments":{"file_path":"web2md.ts"}}}' | python server.py
```

## License

MIT

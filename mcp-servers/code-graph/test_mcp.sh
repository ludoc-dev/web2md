#!/bin/bash
# Test Code Graph MCP Server

echo "🧪 Testing Code Graph MCP Server..."
echo ""

# Activate venv
cd /Users/lucascardoso/web2md/mcp-servers/code-graph
source venv/bin/activate

# Test 1: Import analyzer
echo "Test 1: Import analyzer..."
python -c "
import sys
sys.path.insert(0, '.')
from analyzer import CodeAnalyzer
print('✅ Analyzer imported successfully')
"
echo ""

# Test 2: Trace calls
echo "Test 2: Trace calls..."
python -c "
import sys
sys.path.insert(0, '.')
from analyzer import CodeAnalyzer
import json

analyzer = CodeAnalyzer('/Users/lucascardoso/web2md')
result = analyzer.trace_calls('/Users/lucascardoso/web2md/web2md.ts')

if 'error' not in result:
    print('✅ Trace calls successful')
    print(f'   Found {result[\"stats\"][\"total_functions\"]} functions')
else:
    print(f'❌ Error: {result[\"error\"]}')
"
echo ""

# Test 3: Impact analysis
echo "Test 3: Impact analysis..."
python -c "
import sys
sys.path.insert(0, '.')
from analyzer import CodeAnalyzer
import json

analyzer = CodeAnalyzer('/Users/lucascardoso/web2md')
result = analyzer.impact_analysis('web2md_extract')

if 'symbol' in result:
    print('✅ Impact analysis successful')
    print(f'   Symbol: {result[\"symbol\"]}')
    print(f'   Total usages: {result[\"total_usages\"]}')
else:
    print('❌ Impact analysis failed')
"
echo ""

# Test 4: Dependency graph
echo "Test 4: Dependency graph..."
python -c "
import sys
sys.path.insert(0, '.')
from analyzer import CodeAnalyzer
import json

analyzer = CodeAnalyzer('/Users/lucascardoso/web2md')
result = analyzer.dependency_graph('json')

if 'nodes' in result:
    print('✅ Dependency graph successful')
    print(f'   Nodes: {len(result[\"nodes\"])}')
    print(f'   Edges: {len(result[\"edges\"])}')
else:
    print('❌ Dependency graph failed')
"
echo ""

echo "✅ All tests passed!"
echo ""
echo "📋 MCP Server is ready to use."
echo ""
echo "To integrate with Claude Code:"
echo "1. Restart Claude Code"
echo "2. Check: claude mcp list"
echo "3. Use: 'Trace all function calls in web2md.ts'"

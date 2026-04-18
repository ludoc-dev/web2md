#!/bin/bash
# Quick test for Advanced RAG MCP Server

echo "🧪 Testing Advanced RAG MCP Server..."
echo ""

cd /Users/lucascardoso/web2md/mcp-servers/advanced-rag

# Create venv if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Test 1: Import modules"
python3 -c "
import sys
sys.path.insert(0, '.')
from core.indexer import CodebaseIndexer
print('✅ CodebaseIndexer imported')
"

echo ""
echo "Test 2: Initialize indexer"
python3 -c "
import sys
sys.path.insert(0, '.')
from core.indexer import CodebaseIndexer
import tempfile

db_path = tempfile.mkdtemp()
indexer = CodebaseIndexer(persist_directory=db_path)
print('✅ Indexer initialized')
print(f'   Model: {indexer.model.model_card_data[\"model_name\"]}')
print(f'   Dimensions: {indexer.embedding_dim}')
"

echo ""
echo "Test 3: Index test files"
python3 -c "
import sys
import tempfile
import os
sys.path.insert(0, '.')
from core.indexer import CodebaseIndexer

# Create temp directory with test files
temp_dir = tempfile.mkdtemp()
with open(temp_dir + '/test.py', 'w') as f:
    f.write('def hello(): pass')
with open(temp_dir + '/test.ts', 'w') as f:
    f.write('function world() {}')

# Index
db_path = tempfile.mkdtemp()
indexer = CodebaseIndexer(persist_directory=db_path)
result = indexer.index_directory(temp_dir)

print('✅ Files indexed')
print(f'   Files: {result[\"indexed_files\"]}')
print(f'   Chunks: {result[\"total_chunks\"]}')
print(f'   Languages: {list(result[\"languages\"].keys())}')
"

echo ""
echo "Test 4: Semantic search"
python3 -c "
import sys
import tempfile
sys.path.insert(0, '.')
from core.indexer import CodebaseIndexer
from core.search import SemanticSearch

# Create and index test files
temp_dir = tempfile.mkdtemp()
with open(temp_dir + '/scraper.py', 'w') as f:
    f.write('def scrape_web(url): return data')

db_path = tempfile.mkdtemp()
indexer = CodebaseIndexer(persist_directory=db_path)
indexer.index_directory(temp_dir)

# Search
search = SemanticSearch(indexer)
result = search.search('web scraping')

print('✅ Search completed')
print(f'   Results: {result[\"total_results\"]}')
if result['results']:
    print(f'   Top score: {result[\"results\"][0][\"score\"]}')
"

echo ""
echo "✅ All tests passed!"
echo ""
echo "📋 Advanced RAG MCP Server is ready."
echo ""
echo "Next steps:"
echo "1. Index your codebase: index_codebase(force_reindex=true)"
echo "2. Search: semantic_search('your query')"
echo "3. Get context: context_retrieve('your topic')"

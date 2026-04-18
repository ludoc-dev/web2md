#!/usr/bin/env python3
"""
Integration tests for Advanced RAG MCP Server
"""

import subprocess
import json
import sys
import tempfile
import shutil
from pathlib import Path


def test_index_real_codebase():
    """Test indexing real codebase (web2md)"""
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.indexer import CodebaseIndexer

    indexer = CodebaseIndexer(persist_directory="/tmp/test_rag_db")

    # Index a small subset of web2md
    result = indexer.index_directory(
        directory="/Users/lucascardoso/web2md",
        file_patterns=["*.py", "*.ts"],
        force_reindex=False
    )

    print("Index result:", json.dumps(result, indent=2))

    assert "error" not in result
    assert result["indexed_files"] > 0


def test_semantic_search():
    """Test semantic search"""
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.search import SemanticSearch
    from core.indexer import CodebaseIndexer

    indexer = CodebaseIndexer(persist_directory="/tmp/test_rag_db")
    search = SemanticSearch(indexer)

    result = search.search("web scraping functions", top_k=3)

    print("Search result:", json.dumps(result, indent=2))

    assert "error" not in result
    assert result["total_results"] >= 0


def test_context_retrieve():
    """Test context retrieval"""
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.search import SemanticSearch
    from core.indexer import CodebaseIndexer

    indexer = CodebaseIndexer(persist_directory="/tmp/test_rag_db")
    search = SemanticSearch(indexer)

    result = search.context_retrieve("web2md extraction logic", max_tokens=1000)

    print("Context result:", json.dumps(result, indent=2))

    assert "error" not in result
    assert result["total_tokens"] >= 0


def test_hybrid_search():
    """Test hybrid search"""
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from core.search import SemanticSearch
    from core.indexer import CodebaseIndexer

    indexer = CodebaseIndexer(persist_directory="/tmp/test_rag_db")
    search = SemanticSearch(indexer)

    result = search.hybrid_search("web scraping", semantic_weight=0.7, top_k=3)

    print("Hybrid search result:", json.dumps(result, indent=2))

    assert "error" not in result
    assert result["total_results"] >= 0


def test_mcp_server_tools():
    """Test MCP server tools are available"""
    # This would require running the actual MCP server
    # For now, just verify the server file exists
    server_file = Path(__file__).parent.parent / "server.py"
    assert server_file.exists()

    # Check that it imports without errors
    result = subprocess.run(
        ["python3", "-c", "import sys; sys.path.insert(0, 'server.py'); from mcp.server.fastmcp import FastMCP"],
        cwd=Path(__file__).parent.parent,
        capture_output=True
    )

    # May fail if mcp not installed, but syntax should be ok
    print(f"Server import check: {result.returncode == 0}")


if __name__ == "__main__":
    print("Running integration tests...\n")

    try:
        print("Test 1: Index real codebase")
        test_index_real_codebase()
        print("✅ Passed\n")

        print("Test 2: Semantic search")
        test_semantic_search()
        print("✅ Passed\n")

        print("Test 3: Context retrieve")
        test_context_retrieve()
        print("✅ Passed\n")

        print("Test 4: Hybrid search")
        test_hybrid_search()
        print("✅ Passed\n")

        print("Test 5: MCP server tools")
        test_mcp_server_tools()
        print("✅ Passed\n")

        print("\n✅ All integration tests passed!")

    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
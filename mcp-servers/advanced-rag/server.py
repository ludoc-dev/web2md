#!/usr/bin/env python3
"""
Advanced RAG MCP Server

MCP server for semantic search and context retrieval using vector embeddings.
Based on MCP Python SDK v1.27.0 with FastMCP API.
"""

from mcp.server.fastmcp import FastMCP
from pathlib import Path
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.indexer import CodebaseIndexer
from core.search import SemanticSearch


# Create an MCP server using FastMCP
mcp = FastMCP(
    "Advanced RAG",
    instructions="""Semantic search and context retrieval for codebases using vector embeddings.

Features:
- Index codebases for semantic search
- Natural language search in code
- Context retrieval optimized for LLMs
- Hybrid semantic + keyword search

Supported languages:
- Python, TypeScript, JavaScript
- Markdown, documentation
- JSON, YAML config files

Tools:
- index_codebase: Index codebase for search
- semantic_search: Search with natural language
- context_retrieve: Get context for LLM
- hybrid_search: Combined semantic + keyword search"""
)

# Initialize components (lazy loading)
_indexer = None
_search = None


def get_indexer():
    """Get or create indexer instance"""
    global _indexer
    if _indexer is None:
        # Use current working directory as default
        root_dir = os.getcwd()
        _indexer = CodebaseIndexer(persist_directory=f"{root_dir}/.rag_db")
    return _indexer


def get_search():
    """Get or create search instance"""
    global _search
    if _search is None:
        _search = SemanticSearch(get_indexer())
    return _search


@mcp.tool()
def index_codebase(
    force_reindex: bool = False,
    file_patterns: list = None,
    chunk_size: int = 500,
    chunk_overlap: int = 50
) -> str:
    """Index codebase for semantic search

    Args:
        force_reindex: Reindex all files (default: false)
        file_patterns: File patterns to index (default: code files)
        chunk_size: Chunk size in tokens (default: 500)
        chunk_overlap: Overlap between chunks (default: 50)

    Returns:
        JSON string with indexing results
    """
    import json

    indexer = get_indexer()

    # Default file patterns
    if file_patterns is None:
        file_patterns = ["*.py", "*.ts", "*.tsx", "*.js", "*.jsx", "*.md"]

    # Index current directory
    result = indexer.index_directory(
        directory=os.getcwd(),
        file_patterns=file_patterns,
        force_reindex=force_reindex,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    return json.dumps(result, indent=2)


@mcp.tool()
def semantic_search(
    query: str,
    top_k: int = 5,
    search_type: str = "dense"
) -> str:
    """Search codebase using natural language

    Args:
        query: Search query in natural language
        top_k: Number of results to return (default: 5)
        search_type: Type of search - "dense", "sparse", or "hybrid" (default: "dense")

    Returns:
        JSON string with search results
    """
    import json

    search = get_search()

    result = search.search(
        query=query,
        top_k=top_k,
        filter=None,
        search_type=search_type
    )

    return json.dumps(result, indent=2)


@mcp.tool()
def context_retrieve(
    query: str,
    max_tokens: int = 4000,
    min_relevance: float = 0.7,
    diversify: bool = True
) -> str:
    """Retrieve optimized context for LLM

    Args:
        query: Query describing needed context
        max_tokens: Maximum tokens in context (default: 4000)
        min_relevance: Minimum relevance score (default: 0.7)
        diversify: Use MMR diversification (default: true)

    Returns:
        JSON string with context and sources
    """
    import json

    search = get_search()

    result = search.context_retrieve(
        query=query,
        max_tokens=max_tokens,
        min_relevance=min_relevance,
        diversify=diversify
    )

    return json.dumps(result, indent=2)


@mcp.tool()
def hybrid_search(
    query: str,
    semantic_weight: float = 0.7,
    top_k: int = 5
) -> str:
    """Hybrid semantic + keyword search

    Args:
        query: Search query
        semantic_weight: Weight for semantic vs keyword (0-1, default: 0.7)
        top_k: Number of results (default: 5)

    Returns:
        JSON string with combined results
    """
    import json

    search = get_search()

    result = search.hybrid_search(
        query=query,
        semantic_weight=semantic_weight,
        top_k=top_k
    )

    return json.dumps(result, indent=2)


@mcp.tool()
def get_index_stats() -> str:
    """Get index statistics

    Returns:
        JSON string with index stats
    """
    import json

    indexer = get_indexer()
    result = indexer.get_stats()

    return json.dumps(result, indent=2)


@mcp.tool()
def clear_index() -> str:
    """Clear all indexed data

    Returns:
        JSON string with status
    """
    import json

    indexer = get_indexer()
    result = indexer.clear_index()

    # Reset instances
    global _indexer, _search
    _indexer = None
    _search = None

    return json.dumps(result, indent=2)


# Run with stdio transport (default for Claude Code)
if __name__ == "__main__":
    mcp.run(transport="stdio")
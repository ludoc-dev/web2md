"""
MCP Client - Abstract client for interacting with MCP servers
"""

import json
import subprocess
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class MCPServerInfo:
    """Information about an MCP server"""
    name: str
    command: str
    status: str  # connected, disconnected, error


class MCPClient:
    """Abstract client for interacting with MCP servers"""

    def __init__(self):
        """Initialize MCP client"""
        self.servers = self._discover_servers()

    def _discover_servers(self) -> Dict[str, MCPServerInfo]:
        """
        Discover available MCP servers from settings.json

        Returns:
            Dict mapping server names to server info
        """
        import os

        settings_path = os.path.expanduser("~/.claude/settings.json")

        try:
            with open(settings_path, 'r') as f:
                settings = json.load(f)

            mcp_servers = settings.get("mcpServers", {})

            servers = {}
            for name, config in mcp_servers.items():
                servers[name] = MCPServerInfo(
                    name=name,
                    command=config.get("command", ""),
                    status="unknown"
                )

            return servers

        except Exception as e:
            print(f"Warning: Could not discover MCP servers: {e}")
            return {}

    def list_servers(self) -> List[str]:
        """List available MCP servers"""
        return list(self.servers.keys())

    def get_server_info(self, server_name: str) -> Optional[MCPServerInfo]:
        """Get info about a specific server"""
        return self.servers.get(server_name)


class AdvancedRAGClient(MCPClient):
    """Client for Advanced RAG MCP server"""

    def __init__(self):
        """Initialize Advanced RAG client"""
        super().__init__()
        self.server_name = "advanced-rag"

    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic search

        Args:
            query: Search query
            top_k: Number of results to return
            filters: Optional filters

        Returns:
            List of search results with scores
        """
        # This would normally call the MCP server tool
        # For now, return mock data structure
        return [
            {
                "content": "Mock search result",
                "score": 0.85,
                "metadata": {"file": "example.py"}
            }
        ]

    def context_retrieve(
        self,
        query: str,
        max_tokens: int = 4000,
        min_relevance: float = 0.7,
        diversify: bool = True
    ) -> str:
        """
        Retrieve optimized context for LLM

        Args:
            query: Query for context retrieval
            max_tokens: Maximum tokens to return
            min_relevance: Minimum relevance score
            diversify: Whether to use MMR diversification

        Returns:
            Optimized context string
        """
        # This would normally call the MCP server tool
        return f"# Context for: {query}\n\nMock context data..."

    def hybrid_search(
        self,
        query: str,
        semantic_weight: float = 0.7,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Perform hybrid semantic + keyword search

        Args:
            query: Search query
            semantic_weight: Weight for semantic search (0-1)
            top_k: Number of results

        Returns:
            List of search results
        """
        return self.semantic_search(query, top_k)

    def index_codebase(
        self,
        file_patterns: Optional[List[str]] = None,
        force_reindex: bool = False
    ) -> Dict[str, Any]:
        """
        Index codebase for semantic search

        Args:
            file_patterns: File patterns to index
            force_reindex: Whether to force reindexing

        Returns:
            Index statistics
        """
        return {"status": "indexed", "files_count": 0}


class CodeGraphClient(MCPClient):
    """Client for Code Graph MCP server"""

    def __init__(self):
        """Initialize Code Graph client"""
        super().__init__()
        self.server_name = "code-graph"

    def trace_calls(
        self,
        file_path: str,
        depth: int = 3
    ) -> Dict[str, Any]:
        """
        Trace function calls in a file

        Args:
            file_path: Path to file to analyze
            depth: Depth of call tracing

        Returns:
            Call tree structure
        """
        # This would normally call the MCP server tool
        return {
            "file": file_path,
            "calls": [],
            "depth": depth
        }

    def impact_analysis(
        self,
        symbol: str,
        symbol_type: str = "function"
    ) -> Dict[str, Any]:
        """
        Analyze impact of a symbol

        Args:
            symbol: Symbol name
            symbol_type: Type of symbol (function, class, variable)

        Returns:
            Impact analysis with risk level
        """
        # This would normally call the MCP server tool
        return {
            "symbol": symbol,
            "type": symbol_type,
            "usages": [],
            "risk_level": "low"
        }

    def dependency_graph(
        self,
        format: str = "json"
    ) -> Dict[str, Any]:
        """
        Generate dependency graph

        Args:
            format: Output format (json, mermaid, dot)

        Returns:
            Dependency graph structure
        """
        # This would normally call the MCP server tool
        return {
            "format": format,
            "nodes": [],
            "edges": []
        }


class Web2MDClient:
    """Client for web2md functionality"""

    def extract(
        self,
        url: str,
        use_js: bool = False,
        output_path: Optional[str] = None
    ) -> str:
        """
        Extract markdown from URL

        Args:
            url: URL to extract
            use_js: Whether to use JavaScript rendering
            output_path: Optional output file path

        Returns:
            Extracted markdown content
        """
        import subprocess

        cmd = ["bun", "run", "web2md.ts", url]

        if use_js:
            cmd.insert(3, "--js")

        if output_path:
            cmd.extend(["--out", output_path])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd="/Users/lucascardoso/web2md"
            )
            return result.stdout
        except Exception as e:
            return f"Error extracting {url}: {e}"

    def extract_relevant_docs(
        self,
        query: str,
        max_docs: int = 3
    ) -> List[Dict[str, str]]:
        """
        Extract relevant documentation based on query

        Args:
            query: Query to find relevant docs
            max_docs: Maximum number of docs to extract

        Returns:
            List of {url, content} dicts
        """
        # This would search for relevant URLs first
        # For now, return empty
        return []

#!/usr/bin/env python3
"""
Code Graph Analysis MCP Server

MCP server for analyzing code structure, tracing calls, and building dependency graphs.
Based on MCP Python SDK v1.27.0 with FastMCP API.
"""

from mcp.server.fastmcp import FastMCP
from pathlib import Path
from analyzer import CodeAnalyzer
import json


# Create an MCP server using FastMCP
mcp = FastMCP(
    "Code Graph Analysis",
    instructions="""Analyzes code structure, traces function calls, and builds dependency graphs.

Supported languages:
- Python (AST-based analysis)
- TypeScript/JavaScript (regex-based analysis)

Tools:
- trace_calls: Trace function calls in a file
- impact_analysis: Find all usages of a symbol
- dependency_graph: Generate dependency graphs"""
)

# Initialize analyzer
root_dir = Path.cwd()
analyzer = CodeAnalyzer(str(root_dir))


@mcp.tool()
def trace_calls(file_path: str, depth: int = 3) -> str:
    """Trace function calls in a file

    Args:
        file_path: Path to file to analyze
        depth: How deep to trace calls (default: 3)

    Returns:
        JSON string with call graph information
    """
    result = analyzer.trace_calls(file_path, depth)
    return json.dumps(result, indent=2)


@mcp.tool()
def impact_analysis(symbol: str, symbol_type: str = "function") -> str:
    """Find all usages of a symbol in the codebase

    Args:
        symbol: Symbol name to search for
        symbol_type: Type of symbol (function, class, variable)

    Returns:
        JSON string with impact information
    """
    result = analyzer.impact_analysis(symbol, symbol_type)
    return json.dumps(result, indent=2)


@mcp.tool()
def dependency_graph(format: str = "json") -> str:
    """Generate dependency graph for the codebase

    Args:
        format: Output format (json, mermaid, dot)

    Returns:
        Dependency graph as string (JSON for json format, plain text for others)
    """
    result = analyzer.dependency_graph(format)

    # Return as JSON string for json format
    if format == "json":
        return json.dumps(result, indent=2)

    return str(result)


# Run with stdio transport (default for Claude Code)
if __name__ == "__main__":
    mcp.run(transport="stdio")
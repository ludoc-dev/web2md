#!/usr/bin/env python3
"""
Integration tests for Code Graph MCP Server
"""

import subprocess
import json
import sys
from pathlib import Path


def test_mcp_server_starts():
    """Test that MCP server starts without errors"""
    server_path = Path(__file__).parent.parent / "server.py"
    result = subprocess.run(
        ["python", str(server_path)],
        cwd=Path(__file__).parent.parent,
        timeout=5,
        capture_output=True,
        text=True
    )
    # Server should start and wait for input (timeout is expected)
    assert result.returncode == 0 or "timeout" in str(result.stderr).lower()


def test_analyzer_trace_calls():
    """Test trace_calls functionality"""
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from analyzer import CodeAnalyzer

    analyzer = CodeAnalyzer("/Users/lucascardoso/web2md")
    result = analyzer.trace_calls("/Users/lucascardoso/web2md/web2md.ts")

    assert "error" not in result
    assert "functions" in result
    assert result["language"] in ["ts", "typescript"]


def test_analyzer_impact_analysis():
    """Test impact_analysis functionality"""
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from analyzer import CodeAnalyzer

    analyzer = CodeAnalyzer("/Users/lucascardoso/web2md")
    result = analyzer.impact_analysis("web2md_extract")

    assert "symbol" in result
    assert result["symbol"] == "web2md_extract"
    assert "total_usages" in result


def test_analyzer_dependency_graph():
    """Test dependency_graph functionality"""
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from analyzer import CodeAnalyzer

    analyzer = CodeAnalyzer("/Users/lucascardoso/web2md")
    result = analyzer.dependency_graph("json")

    assert "nodes" in result
    assert "edges" in result


if __name__ == "__main__":
    print("Running integration tests...")

    try:
        test_analyzer_trace_calls()
        print("✅ trace_calls test passed")

        test_analyzer_impact_analysis()
        print("✅ impact_analysis test passed")

        test_analyzer_dependency_graph()
        print("✅ dependency_graph test passed")

        print("\n✅ All integration tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test error: {e}")
        sys.exit(1)

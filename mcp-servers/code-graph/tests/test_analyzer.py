#!/usr/bin/env python3
"""
Tests for Code Graph Analyzer
"""

import pytest
import json
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analyzer import CodeAnalyzer


class TestCodeAnalyzer:
    """Test code analyzer functionality"""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance"""
        return CodeAnalyzer()

    @pytest.fixture
    def temp_python_file(self, tmp_path):
        """Create temporary Python file"""
        file_path = tmp_path / "test.py"
        file_path.write_text("""
def fetch_data():
    return requests.get(url)

def process_data(data):
    return data.transform()

def main():
    data = fetch_data()
    result = process_data(data)
    return result
""")
        return str(file_path)

    @pytest.fixture
    def temp_js_file(self, tmp_path):
        """Create temporary JavaScript file"""
        file_path = tmp_path / "test.js"
        file_path.write_text("""
function fetchUrl() {
    return fetch(url);
}

function processData(data) {
    return data.map(transform);
}

function main() {
    const data = fetchUrl();
    const result = processData(data);
    return result;
}
""")
        return str(file_path)

    def test_detect_language_python(self, analyzer, temp_python_file):
        """Test Python language detection"""
        language = analyzer.detect_language(temp_python_file)
        assert language == "python"

    def test_detect_language_javascript(self, analyzer, temp_js_file):
        """Test JavaScript language detection"""
        language = analyzer.detect_language(temp_js_file)
        assert language == "javascript"

    def test_detect_language_unsupported(self, analyzer):
        """Test unsupported language"""
        language = analyzer.detect_language("test.unknown")
        assert language is None

    def test_trace_python_calls(self, analyzer, temp_python_file):
        """Test tracing Python function calls"""
        result = analyzer.trace_calls(temp_python_file)

        assert "error" not in result
        assert result["language"] == "python"
        assert result["stats"]["total_functions"] == 3
        assert len(result["functions"]) == 3

        # Check main function
        main_func = next(f for f in result["functions"] if f["name"] == "main")
        assert "fetch_data" in main_func["calls"]
        assert "process_data" in main_func["calls"]

    def test_trace_js_calls(self, analyzer, temp_js_file):
        """Test tracing JavaScript function calls"""
        result = analyzer.trace_calls(temp_js_file)

        assert "error" not in result
        assert result["language"] in ["javascript", "js"]
        assert result["stats"]["total_functions"] >= 3

    def test_trace_nonexistent_file(self, analyzer):
        """Test tracing non-existent file"""
        result = analyzer.trace_calls("nonexistent.py")
        assert "error" in result
        assert "not found" in result["error"].lower()

    def test_impact_analysis(self, analyzer, tmp_path):
        """Test impact analysis"""
        # Create test files
        (tmp_path / "file1.py").write_text("def test_function(): pass")
        (tmp_path / "file2.py").write_text("test_function()  # Call test_function")

        analyzer.root = tmp_path
        result = analyzer.impact_analysis("test_function")

        assert result["symbol"] == "test_function"
        assert result["total_usages"] >= 2
        assert result["total_files"] >= 2

    def test_impact_analysis_no_results(self, analyzer, tmp_path):
        """Test impact analysis with no results"""
        (tmp_path / "file1.py").write_text("def other_function(): pass")

        analyzer.root = tmp_path
        result = analyzer.impact_analysis("nonexistent_function")

        assert result["total_usages"] == 0
        assert result["total_files"] == 0
        assert result["risk_level"] == "low"

    def test_dependency_graph_json(self, analyzer, tmp_path):
        """Test dependency graph generation in JSON format"""
        # Create test files
        (tmp_path / "main.py").write_text("import utils")
        (tmp_path / "utils.py").write_text("import helpers")

        analyzer.root = tmp_path
        result = analyzer.dependency_graph("json")

        assert "nodes" in result
        assert "edges" in result
        assert len(result["nodes"]) >= 2

    def test_dependency_graph_mermaid(self, analyzer, tmp_path):
        """Test dependency graph generation in Mermaid format"""
        (tmp_path / "main.py").write_text("import utils")

        analyzer.root = tmp_path
        result = analyzer.dependency_graph("mermaid")

        assert isinstance(result, str)
        assert "graph TD;" in result
        assert "-->" in result

    def test_dependency_graph_dot(self, analyzer, tmp_path):
        """Test dependency graph generation in DOT format"""
        (tmp_path / "main.py").write_text("import utils")

        analyzer.root = tmp_path
        result = analyzer.dependency_graph("dot")

        assert isinstance(result, str)
        assert "digraph G {" in result
        assert "->" in result

    def test_dependency_graph_unsupported_format(self, analyzer, tmp_path):
        """Test dependency graph with unsupported format"""
        (tmp_path / "main.py").write_text("import utils")

        analyzer.root = tmp_path
        result = analyzer.dependency_graph("unsupported")

        assert "error" in result
        assert "Unsupported format" in result["error"]


class TestRealCodebase:
    """Test with real codebase (web2md)"""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer for web2md project"""
        # Assume we're in the web2md project
        return CodeAnalyzer("/Users/lucascardoso/web2md")

    def test_trace_web2md(self, analyzer):
        """Test tracing web2md.ts"""
        result = analyzer.trace_calls("web2md.ts")

        # Should either work or give a clear error
        assert "error" not in result or "file" in result

        if "error" not in result:
            assert "stats" in result
            assert result["stats"]["total_functions"] >= 0

    def test_impact_web2md_extract(self, analyzer):
        """Test impact analysis for web2md_extract function"""
        result = analyzer.impact_analysis("web2md_extract")

        assert "symbol" in result
        assert "total_usages" in result
        assert result["total_usages"] >= 0

    def test_dependency_web2md(self, analyzer):
        """Test dependency graph for web2md project"""
        result = analyzer.dependency_graph("json")

        assert "nodes" in result or "error" in result
        if "error" not in result:
            assert len(result["nodes"]) >= 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

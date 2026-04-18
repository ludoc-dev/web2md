#!/usr/bin/env python3
"""
Code Graph Analyzer - Core analysis logic

Analyzes code structure, traces function calls, and builds dependency graphs.
Supports Python, TypeScript, and JavaScript.
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
import networkx as nx
from dataclasses import dataclass


@dataclass
class FunctionInfo:
    """Information about a function"""
    name: str
    line: int
    end_line: int
    calls: List[str]
    file_path: str


@dataclass
class UsageInfo:
    """Information about symbol usage"""
    file: str
    usages: int
    lines: List[int]


class CodeAnalyzer:
    """Analyze code structure and build graphs"""

    def __init__(self, root_dir: str = "."):
        self.root = Path(root_dir)
        self.graph = nx.DiGraph()
        self.language_map = {
            '.py': 'python',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.js': 'javascript',
            '.jsx': 'javascript',
        }

    def detect_language(self, file_path: str) -> Optional[str]:
        """Detect programming language from file extension"""
        path = Path(file_path)
        return self.language_map.get(path.suffix)

    def trace_calls(self, file_path: str, depth: int = 3) -> dict:
        """Trace function calls in a file

        Args:
            file_path: Path to file to analyze
            depth: How deep to trace calls (default: 3)

        Returns:
            Dictionary with call graph information
        """
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}

        language = self.detect_language(file_path)
        if not language:
            return {"error": f"Unsupported language: {path.suffix}"}

        if language == 'python':
            return self._trace_python_calls(file_path, depth)
        elif language in ('typescript', 'javascript'):
            return self._trace_js_calls(file_path, depth)
        else:
            return {"error": f"Language not implemented: {language}"}

    def _trace_python_calls(self, file_path: str, depth: int) -> dict:
        """Trace calls in Python file using AST"""
        try:
            with open(file_path, 'r') as f:
                source = f.read()

            tree = ast.parse(source)
            analyzer = PythonCallAnalyzer()
            analyzer.visit(tree)

            # Build graph
            local_graph = nx.DiGraph()
            for func in analyzer.functions:
                local_graph.add_node(func['name'], **func)
                for call in func['calls']:
                    local_graph.add_edge(func['name'], call)

            return {
                "file": file_path,
                "language": "python",
                "functions": analyzer.functions,
                "graph": {
                    "nodes": [{"id": n} for n in local_graph.nodes()],
                    "edges": [{"from": u, "to": v} for u, v in local_graph.edges()]
                },
                "stats": {
                    "total_functions": len(analyzer.functions),
                    "total_calls": sum(len(f['calls']) for f in analyzer.functions)
                }
            }
        except Exception as e:
            return {"error": f"Failed to analyze Python file: {str(e)}"}

    def _trace_js_calls(self, file_path: str, depth: int) -> dict:
        """Trace calls in TypeScript/JavaScript file using regex

        Note: This is a simplified implementation. For production,
        use a proper parser like TypeScript compiler API or Babel.
        """
        try:
            with open(file_path, 'r') as f:
                source = f.read()

            # Find function definitions
            func_pattern = r'(?:function\s+(\w+)|(\w+)\s*\([^)]*\)\s*[{=>]|(?:const|let|var)\s+(\w+)\s*=\s*(?:\([^)]*\)\s*=>|function))'
            functions = []

            for match in re.finditer(func_pattern, source):
                func_name = match.group(1) or match.group(2) or match.group(3)
                if not func_name:
                    continue

                # Find function calls (simplified)
                call_pattern = r'\b(\w+)\s*\('
                calls = list(set(re.findall(call_pattern, source)))

                functions.append({
                    "name": func_name,
                    "line": source[:match.start()].count('\n') + 1,
                    "calls": calls
                })

            # Build graph
            local_graph = nx.DiGraph()
            for func in functions:
                local_graph.add_node(func['name'], **func)
                for call in func['calls']:
                    if call != func['name']:  # Don't self-loop
                        local_graph.add_edge(func['name'], call)

            return {
                "file": file_path,
                "language": Path(file_path).suffix[1:],
                "functions": functions,
                "graph": {
                    "nodes": [{"id": n} for n in local_graph.nodes()],
                    "edges": [{"from": u, "to": v} for u, v in local_graph.edges()]
                },
                "stats": {
                    "total_functions": len(functions),
                    "total_calls": sum(len(f['calls']) for f in functions)
                }
            }
        except Exception as e:
            return {"error": f"Failed to analyze JS/TS file: {str(e)}"}

    def impact_analysis(self, symbol: str, symbol_type: str = "function") -> dict:
        """Find all usages of a symbol in the codebase

        Args:
            symbol: Symbol name to search for
            symbol_type: Type of symbol ("function", "class", "variable")

        Returns:
            Dictionary with impact information
        """
        if not self.root.exists():
            return {"error": f"Root directory not found: {self.root}"}

        # Search for symbol usage in all source files
        affected_files = []
        total_usages = 0

        for ext in self.language_map.keys():
            for file_path in self.root.rglob(f"*{ext}"):
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()

                    usages = []
                    for i, line in enumerate(lines, 1):
                        # Search for symbol usage
                        pattern = rf'\b{re.escape(symbol)}\b'
                        if re.search(pattern, line):
                            usages.append(i)

                    if usages:
                        affected_files.append(UsageInfo(
                            file=str(file_path),
                            usages=len(usages),
                            lines=usages
                        ))
                        total_usages += len(usages)

                except Exception:
                    continue

        # Calculate risk level
        if total_usages > 50:
            risk_level = "high"
        elif total_usages > 10:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "symbol": symbol,
            "type": symbol_type,
            "affected_files": [
                {
                    "file": info.file,
                    "usages": info.usages,
                    "lines": info.lines
                }
                for info in affected_files
            ],
            "total_usages": total_usages,
            "total_files": len(affected_files),
            "risk_level": risk_level
        }

    def dependency_graph(self, format_type: str = "json") -> dict:
        """Generate dependency graph for the codebase

        Args:
            format_type: Output format ("json", "mermaid", "dot")

        Returns:
            Dependency graph in specified format
        """
        if not self.root.exists():
            return {"error": f"Root directory not found: {self.root}"}

        # Build dependency graph
        dep_graph = nx.DiGraph()

        for ext in self.language_map.keys():
            for file_path in self.root.rglob(f"*{ext}"):
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()

                    # Find imports
                    if ext == '.py':
                        imports = self._find_python_imports(content)
                    else:
                        imports = self._find_js_imports(content, ext)

                    # Add nodes and edges
                    file_str = str(file_path)
                    dep_graph.add_node(file_str, type="source")

                    for imp in imports:
                        dep_graph.add_edge(file_str, imp, type="imports")

                except Exception:
                    continue

        # Convert to requested format
        if format_type == "json":
            return {
                "nodes": [
                    {"id": n, "type": dep_graph.nodes[n].get("type", "unknown")}
                    for n in dep_graph.nodes()
                ],
                "edges": [
                    {"from": u, "to": v, "type": dep_graph.edges[u, v].get("type", "unknown")}
                    for u, v in dep_graph.edges()
                ]
            }
        elif format_type == "mermaid":
            lines = ["graph TD;"]
            for u, v in dep_graph.edges():
                u_label = Path(u).name
                v_label = Path(v).name if '/' not in v else v
                lines.append(f'  "{u_label}" --> "{v_label}";')
            return "\n".join(lines)
        elif format_type == "dot":
            lines = ["digraph G {"]
            for u, v in dep_graph.edges():
                u_label = Path(u).name
                v_label = Path(v).name if '/' not in v else v
                lines.append(f'  "{u_label}" -> "{v_label}";')
            lines.append("}")
            return "\n".join(lines)
        else:
            return {"error": f"Unsupported format: {format_type}"}

    def _find_python_imports(self, content: str) -> List[str]:
        """Find imports in Python code"""
        try:
            tree = ast.parse(content)
            imports = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)

            return imports
        except Exception:
            return []

    def _find_js_imports(self, content: str, ext: str) -> List[str]:
        """Find imports in TypeScript/JavaScript code"""
        imports = []

        # ES6 imports
        import_patterns = [
            r'import\s+.*?\s+from\s+["\']([^"\']+)["\']',
            r'import\s+["\']([^"\']+)["\']',
            r'export\s+.*?\s+from\s+["\']([^"\']+)["\']',
        ]

        # CommonJS require
        require_patterns = [
            r'require\(["\']([^"\']+)["\']\)',
        ]

        all_patterns = import_patterns + require_patterns

        for pattern in all_patterns:
            matches = re.findall(pattern, content)
            imports.extend(matches)

        return list(set(imports))


class PythonCallAnalyzer(ast.NodeVisitor):
    """AST visitor for analyzing Python function calls"""

    def __init__(self):
        self.functions = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        """Visit function definition"""
        self.current_function = node.name
        calls = []

        # Find function calls within this function
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)

        self.functions.append({
            "name": node.name,
            "line": node.lineno,
            "end_line": node.end_lineno,
            "calls": list(set(calls))
        })

        self.current_function = None
        self.generic_visit(node)

#!/usr/bin/env python3
"""
Tests for Codebase Indexer
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.indexer import CodebaseIndexer


class TestCodebaseIndexer:
    """Test codebase indexer functionality"""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def indexer(self, temp_dir):
        """Create indexer instance"""
        db_path = Path(temp_dir) / "test_db"
        return CodebaseIndexer(persist_directory=str(db_path))

    def test_indexer_initialization(self, indexer):
        """Test indexer initializes correctly"""
        assert indexer.model is not None
        assert indexer.chroma is not None
        assert indexer.collection is not None

    def test_index_single_file(self, indexer, temp_dir):
        """Test indexing a single file"""
        # Create test file
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("""
def hello_world():
    print("Hello, World!")

def add_numbers(a, b):
    return a + b
""")

        # Index file
        result = indexer.index_file(str(test_file))

        assert "error" not in result
        assert result["status"] == "indexed"
        assert result["chunks_created"] > 0
        assert result["language"] == "python"

    def test_index_nonexistent_file(self, indexer):
        """Test indexing non-existent file"""
        result = indexer.index_file("/nonexistent/file.py")

        assert "error" in result
        assert "not found" in result["error"].lower()

    def test_index_directory(self, indexer, temp_dir):
        """Test indexing entire directory"""
        # Create test files
        (Path(temp_dir) / "file1.py").write_text("def func1(): pass")
        (Path(temp_dir) / "file2.ts").write_text("function func2() {}")
        (Path(temp_dir) / "README.md").write_text("# Test Project")

        # Index directory
        result = indexer.index_directory(temp_dir)

        assert "error" not in result
        assert result["indexed_files"] == 3
        assert result["total_chunks"] > 0
        assert "python" in result["languages"]
        assert "typescript" in result["languages"]

    def test_index_empty_directory(self, indexer, temp_dir):
        """Test indexing empty directory"""
        result = indexer.index_directory(temp_dir)

        assert "error" in result
        assert "no files found" in result["error"].lower()

    def test_force_reindex(self, indexer, temp_dir):
        """Test force reindex"""
        # Create test file
        test_file = Path(temp_dir) / "test.py"
        test_file.write_text("def test(): pass")

        # Index once
        result1 = indexer.index_directory(temp_dir, force_reindex=False)
        files_indexed_1 = result1["indexed_files"]

        # Index again (should skip)
        result2 = indexer.index_directory(temp_dir, force_reindex=False)
        files_indexed_2 = result2.get("indexed_files", 0)

        # Force reindex
        result3 = indexer.index_directory(temp_dir, force_reindex=True)
        files_indexed_3 = result3["indexed_files"]

        assert files_indexed_1 > 0
        assert files_indexed_2 == 0  # No new files
        assert files_indexed_3 > 0  # Reindexed

    def test_chunking(self, indexer):
        """Test content chunking"""
        content = "word " * 1000  # 2000 words
        chunks = indexer._chunk_content(content, chunk_size=500, chunk_overlap=50)

        assert len(chunks) > 1  # Should be multiple chunks
        assert all(len(chunk) > 0 for chunk in chunks)

    def test_language_detection(self, indexer):
        """Test programming language detection"""
        tests = [
            ("test.py", "python"),
            ("test.ts", "typescript"),
            ("test.js", "javascript"),
            ("test.md", "markdown"),
            ("test.txt", "text"),
        ]

        for filename, expected_lang in tests:
            detected = indexer._detect_language(Path(filename))
            assert detected == expected_lang

    def test_get_stats(self, indexer, temp_dir):
        """Test getting index statistics"""
        # Index some files
        (Path(temp_dir) / "test.py").write_text("def test(): pass")
        indexer.index_directory(temp_dir)

        # Get stats
        stats = indexer.get_stats()

        assert "error" not in stats
        assert stats["total_chunks"] > 0
        assert stats["total_files"] > 0
        assert "languages" in stats

    def test_clear_index(self, indexer, temp_dir):
        """Test clearing index"""
        # Index some files
        (Path(temp_dir) / "test.py").write_text("def test(): pass")
        indexer.index_directory(temp_dir)

        # Clear index
        result = indexer.clear_index()

        assert result["status"] == "cleared"

        # Verify empty
        stats = indexer.get_stats()
        assert stats["total_chunks"] == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
#!/usr/bin/env python3
"""
Codebase Indexer - Index code for semantic search

Handles file scanning, content extraction, chunking, and vector storage.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


class CodebaseIndexer:
    """Index codebase for semantic search"""

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        persist_directory: str = "./rag_db"
    ):
        """Initialize indexer

        Args:
            embedding_model: Model name from sentence-transformers
            persist_directory: Directory for ChromaDB persistence
        """
        print(f"📦 Loading embedding model: {embedding_model}")
        self.model = SentenceTransformer(embedding_model)
        self.embedding_dim = self.model.get_sentence_embedding_dimension()

        print(f"💾 Initializing ChromaDB: {persist_directory}")
        self.chroma = chromadb.PersistentClient(path=persist_directory)

        # Get or create collection
        self.collection = self.chroma.get_or_create_collection(
            name="codebase",
            metadata={"hnsw:space": "cosine"}
        )

        self.persist_directory = persist_directory

    def index_file(
        self,
        file_path: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> Dict:
        """Index a single file

        Args:
            file_path: Path to file
            chunk_size: Chunk size in tokens
            chunk_overlap: Overlap between chunks

        Returns:
            Indexing result
        """
        file_path = Path(file_path)

        if not file_path.exists():
            return {"error": f"File not found: {file_path}"}

        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Detect language
            language = self._detect_language(file_path)

            # Chunk content
            chunks = self._chunk_content(content, chunk_size, chunk_overlap)

            if not chunks:
                return {"error": "No content to index"}

            # Generate embeddings
            embeddings = self.model.encode(chunks, show_progress_bar=False)

            # Create metadata
            metadatas = []
            for i, chunk in enumerate(chunks):
                metadatas.append({
                    "file": str(file_path),
                    "chunk_id": i,
                    "language": language,
                    "type": self._get_file_type(file_path),
                    "size": len(chunk)
                })

            # Add to collection
            ids = [f"{file_path}#{i}" for i in range(len(chunks))]
            self.collection.add(
                documents=chunks,
                embeddings=embeddings.tolist(),
                metadatas=metadatas,
                ids=ids
            )

            return {
                "file": str(file_path),
                "chunks_created": len(chunks),
                "language": language,
                "status": "indexed"
            }

        except Exception as e:
            return {"error": f"Failed to index {file_path}: {str(e)}"}

    def index_directory(
        self,
        directory: str,
        file_patterns: Optional[List[str]] = None,
        force_reindex: bool = False,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> Dict:
        """Index entire directory

        Args:
            directory: Directory path
            file_patterns: File patterns to include (default: code files)
            force_reindex: Reindex even if already indexed
            chunk_size: Chunk size in tokens
            chunk_overlap: Overlap between chunks

        Returns:
            Indexing result
        """
        import time
        start_time = time.time()

        directory = Path(directory)

        if not directory.exists():
            return {"error": f"Directory not found: {directory}"}

        # Default file patterns
        if file_patterns is None:
            file_patterns = [
                "*.py", "*.ts", "*.tsx", "*.js", "*.jsx",
                "*.md", "*.rst", "*.txt",
                "*.json", "*.yaml", "*.yml"
            ]

        # Collect files
        files = []
        for pattern in file_patterns:
            files.extend(directory.rglob(pattern))

        # Remove duplicates
        files = list(set(files))

        if not files:
            return {"error": "No files found matching patterns"}

        print(f"📂 Found {len(files)} files to index")

        # If not force reindex, check what's already indexed
        if not force_reindex:
            indexed_files = set()
            try:
                # Get existing metadata
                existing = self.collection.get()
                for metadata in existing.get('metadatas', []):
                    indexed_files.add(metadata['file'])
            except:
                pass

            # Filter out already indexed files
            new_files = [f for f in files if str(f) not in indexed_files]

            if not new_files:
                return {
                    "message": "All files already indexed",
                    "indexed_files": 0,
                    "force_reindex": True
                }

            files = new_files
            print(f"📊 {len(files)} new files to index")

        # Index files
        results = {
            "indexed_files": 0,
            "total_chunks": 0,
            "errors": [],
            "languages": {}
        }

        for file_path in tqdm(files, desc="Indexing"):
            result = self.index_file(
                file_path,
                chunk_size,
                chunk_overlap
            )

            if "error" in result:
                results["errors"].append(result["error"])
            else:
                results["indexed_files"] += 1
                results["total_chunks"] += result["chunks_created"]

                # Track languages
                lang = result.get("language", "unknown")
                results["languages"][lang] = results["languages"].get(lang, 0) + 1

        elapsed_time = time.time() - start_time

        return {
            "indexed_files": results["indexed_files"],
            "total_chunks": results["total_chunks"],
            "errors": results["errors"],
            "languages": results["languages"],
            "indexing_time": round(elapsed_time, 2),
            "embedding_model": self.model.model_card_data["model_name"],
            "vector_db_size": self.collection.count(),
            "status": "completed"
        }

    def _detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension"""
        ext_map = {
            '.py': 'python',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.md': 'markdown',
            '.rst': 'restructuredtext',
            '.txt': 'text',
            '.json': 'json',
            '.yaml': 'yaml',
            '.yml': 'yaml',
        }
        return ext_map.get(file_path.suffix, 'unknown')

    def _get_file_type(self, file_path: Path) -> str:
        """Get file type category"""
        ext = file_path.suffix

        if ext in ['.py', '.ts', '.tsx', '.js', '.jsx']:
            return 'code'
        elif ext in ['.md', '.rst', '.txt']:
            return 'documentation'
        elif ext in ['.json', '.yaml', '.yml']:
            return 'config'
        else:
            return 'other'

    def _chunk_content(
        self,
        content: str,
        chunk_size: int,
        chunk_overlap: int
    ) -> List[str]:
        """Chunk content into overlapping pieces

        Args:
            content: Text content
            chunk_size: Target chunk size (tokens)
            chunk_overlap: Overlap between chunks

        Returns:
            List of chunks
        """
        # Simple token-based chunking
        tokens = content.split()
        chunks = []

        if len(tokens) <= chunk_size:
            return [content] if content.strip() else []

        start = 0
        while start < len(tokens):
            end = start + chunk_size
            chunk = ' '.join(tokens[start:end])

            if chunk.strip():
                chunks.append(chunk)

            start = end - chunk_overlap

        return chunks

    def get_stats(self) -> Dict:
        """Get index statistics

        Returns:
            Index statistics
        """
        try:
            count = self.collection.count()

            # Get sample metadata
            sample = self.collection.get(limit=100)
            languages = {}
            files = set()

            for metadata in sample.get('metadatas', []):
                lang = metadata.get('language', 'unknown')
                languages[lang] = languages.get(lang, 0) + 1
                files.add(metadata.get('file', ''))

            return {
                "total_chunks": count,
                "total_files": len(files),
                "languages": languages,
                "embedding_model": self.model.model_card_data["model_name"],
                "embedding_dim": self.embedding_dim,
                "persist_directory": self.persist_directory
            }

        except Exception as e:
            return {"error": f"Failed to get stats: {str(e)}"}

    def clear_index(self) -> Dict:
        """Clear all indexed data

        Returns:
            Status
        """
        try:
            # Delete and recreate collection
            self.chroma.delete_collection("codebase")
            self.collection = self.chroma.create_collection(
                name="codebase",
                metadata={"hnsw:space": "cosine"}
            )

            return {"status": "cleared", "message": "Index cleared successfully"}

        except Exception as e:
            return {"error": f"Failed to clear index: {str(e)}"}

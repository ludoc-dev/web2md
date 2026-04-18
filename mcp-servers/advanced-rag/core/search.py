#!/usr/bin/env python3
"""
Semantic Search - Search codebase using vector embeddings

Provides semantic search, hybrid search, and context retrieval.
"""

import time
from typing import List, Dict, Optional, Literal
from sentence_transformers import SentenceTransformer
import chromadb


class SemanticSearch:
    """Semantic search in codebase"""

    def __init__(self, indexer):
        """Initialize search

        Args:
            indexer: CodebaseIndexer instance
        """
        self.indexer = indexer
        self.model = indexer.model
        self.collection = indexer.collection

    def search(
        self,
        query: str,
        top_k: int = 5,
        filter: Optional[Dict] = None,
        search_type: Literal["dense", "sparse", "hybrid"] = "dense"
    ) -> Dict:
        """Semantic search

        Args:
            query: Search query
            top_k: Number of results
            filter: Metadata filter (e.g., {"language": "python"})
            search_type: "dense", "sparse", or "hybrid"

        Returns:
            Search results
        """
        start_time = time.time()

        try:
            # Generate query embedding
            query_embedding = self.model.encode(query, show_progress_bar=False)

            # Search in ChromaDB
            if search_type == "dense":
                results = self.collection.query(
                    query_embeddings=[query_embedding.tolist()],
                    n_results=top_k,
                    where=filter
                )
            else:
                # For sparse/hybrid, use where document contains query terms
                # This is a simplified implementation
                results = self.collection.query(
                    query_embeddings=[query_embedding.tolist()],
                    n_results=top_k,
                    where=filter
                )

            # Format results
            formatted_results = []
            if results and 'documents' in results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if 'metadatas' in results else {}
                    distances = results['distances'][0] if 'distances' in results else [0]

                    # Convert distance to similarity score
                    similarity = 1 - min(distances[i] if i < len(distances) else 0, 1.0)

                    formatted_results.append({
                        "content": doc,
                        "score": round(similarity, 3),
                        "metadata": metadata
                    })

            search_time = time.time() - start_time

            return {
                "query": query,
                "results": formatted_results,
                "total_results": len(formatted_results),
                "search_time": round(search_time, 3),
                "search_type": search_type
            }

        except Exception as e:
            return {
                "query": query,
                "error": f"Search failed: {str(e)}",
                "results": [],
                "total_results": 0,
                "search_time": time.time() - start_time
            }

    def hybrid_search(
        self,
        query: str,
        semantic_weight: float = 0.7,
        top_k: int = 5,
        filter: Optional[Dict] = None
    ) -> Dict:
        """Hybrid semantic + keyword search

        Args:
            query: Search query
            semantic_weight: Weight for semantic search (0-1)
            top_k: Number of results
            filter: Metadata filter

        Returns:
            Combined search results
        """
        start_time = time.time()

        try:
            # Semantic search
            semantic_results = self.search(
                query,
                top_k=top_k * 2,  # Get more for reranking
                filter=filter,
                search_type="dense"
            )

            # Keyword search (simplified - just check if query words in content)
            keyword_results = self._keyword_search(query, top_k * 2, filter)

            # Combine and rerank
            combined = self._combine_results(
                semantic_results.get("results", []),
                keyword_results,
                semantic_weight
            )

            # Take top_k
            combined = combined[:top_k]

            search_time = time.time() - start_time

            return {
                "query": query,
                "results": combined,
                "total_results": len(combined),
                "search_time": round(search_time, 3),
                "search_type": "hybrid",
                "semantic_weight": semantic_weight
            }

        except Exception as e:
            return {
                "query": query,
                "error": f"Hybrid search failed: {str(e)}",
                "results": [],
                "search_time": time.time() - start_time
            }

    def context_retrieve(
        self,
        query: str,
        max_tokens: int = 4000,
        min_relevance: float = 0.7,
        diversify: bool = True
    ) -> Dict:
        """Retrieve context for LLM

        Args:
            query: Query
            max_tokens: Maximum tokens in context
            min_relevance: Minimum relevance score
            diversify: Use MMR diversification

        Returns:
            Formatted context with sources
        """
        start_time = time.time()

        try:
            # Get more results than needed
            results = self.search(query, top_k=20)

            # Filter by relevance
            relevant = [
                r for r in results.get("results", [])
                if r.get("score", 0) >= min_relevance
            ]

            if not relevant:
                return {
                    "query": query,
                    "context": "",
                    "sources": [],
                    "total_tokens": 0,
                    "retrieval_time": time.time() - start_time,
                    "message": "No relevant results found"
                }

            # Diversify if requested (MMR - Maximal Marginal Relevance)
            if diversify and len(relevant) > 1:
                relevant = self._mmr_selection(relevant, lambda_param=0.5)

            # Pack into context window
            selected = self._pack_context(relevant, max_tokens)

            # Format with citations
            context = self._format_with_citations(selected)

            # Extract sources
            sources = list(set([
                r["metadata"].get("file", "unknown")
                for r in selected
            ]))

            retrieval_time = time.time() - start_time

            return {
                "query": query,
                "context": context,
                "sources": sources,
                "total_tokens": self._count_tokens(context),
                "retrieval_time": round(retrieval_time, 3),
                "metadata": {
                    "files_used": len(sources),
                    "chunks_used": len(selected),
                    "avg_score": round(sum(r["score"] for r in selected) / len(selected), 3)
                }
            }

        except Exception as e:
            return {
                "query": query,
                "error": f"Context retrieval failed: {str(e)}",
                "context": "",
                "sources": [],
                "total_tokens": 0,
                "retrieval_time": time.time() - start_time
            }

    def _keyword_search(
        self,
        query: str,
        top_k: int,
        filter: Optional[Dict]
    ) -> List[Dict]:
        """Simple keyword search (simplified)

        Args:
            query: Search query
            top_k: Number of results
            filter: Metadata filter

        Returns:
            Keyword search results
        """
        # Extract keywords from query
        keywords = query.lower().split()

        # Get all documents
        results = self.collection.get(
            where=filter,
            limit=1000  # Reasonable limit
        )

        # Score by keyword matches
        scored = []
        for i, doc in enumerate(results.get('documents', [])):
            metadata = results.get('metadatas', [{}])[i] if i < len(results.get('metadatas', [])) else {}

            doc_lower = doc.lower()
            keyword_score = sum(1 for kw in keywords if kw in doc_lower)

            if keyword_score > 0:
                # Normalize score
                normalized_score = keyword_score / len(keywords)
                scored.append({
                    "content": doc,
                    "score": normalized_score,
                    "metadata": metadata
                })

        # Sort by score and take top_k
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    def _combine_results(
        self,
        semantic_results: List[Dict],
        keyword_results: List[Dict],
        semantic_weight: float
    ) -> List[Dict]:
        """Combine semantic and keyword results

        Args:
            semantic_results: Semantic search results
            keyword_results: Keyword search results
            semantic_weight: Weight for semantic (0-1)

        Returns:
            Combined and reranked results
        """
        # Create mapping for keyword results
        keyword_map = {
            r["metadata"].get("file", ""): r["score"]
            for r in keyword_results
        }

        # Combine scores
        combined = []
        for r in semantic_results:
            file_path = r["metadata"].get("file", "")
            semantic_score = r["score"]
            keyword_score = keyword_map.get(file_path, 0.0)

            # Weighted combination
            combined_score = (
                semantic_weight * semantic_score +
                (1 - semantic_weight) * keyword_score
            )

            combined.append({
                "content": r["content"],
                "semantic_score": round(semantic_score, 3),
                "keyword_score": round(keyword_score, 3),
                "combined_score": round(combined_score, 3),
                "metadata": r["metadata"]
            })

        # Sort by combined score
        combined.sort(key=lambda x: x["combined_score"], reverse=True)
        return combined

    def _mmr_selection(
        self,
        results: List[Dict],
        lambda_param: float = 0.5
    ) -> List[Dict]:
        """Maximal Marginal Relevance selection

        Args:
            results: Search results
            lambda_param: Balance relevance vs diversity (0-1)

        Returns:
            Diversified results
        """
        if not results:
            return results

        selected = [results[0]]  # Start with highest scoring
        remaining = results[1:]

        while remaining and len(selected) < len(results):
            # Find result with maximal marginal relevance
            best_idx = 0
            best_mmr = -float('inf')

            for i, candidate in enumerate(remaining):
                # Relevance to query
                relevance = candidate["score"]

                # Diversity from selected (min similarity to any selected)
                diversity = 1 - max([
                    self._similarity(candidate, s)
                    for s in selected
                ])

                # MMR score
                mmr = lambda_param * relevance + (1 - lambda_param) * diversity

                if mmr > best_mmr:
                    best_mmr = mmr
                    best_idx = i

            # Add to selected
            selected.append(remaining.pop(best_idx))

        return selected

    def _similarity(self, doc1: Dict, doc2: Dict) -> float:
        """Calculate similarity between two documents

        Args:
            doc1: First document
            doc2: Second document

        Returns:
            Similarity score (0-1)
        """
        # Simple text overlap similarity
        words1 = set(doc1["content"].lower().split())
        words2 = set(doc2["content"].lower().split())

        if not words1 or not words2:
            return 0.0

        intersection = words1 & words2
        union = words1 | words2

        return len(intersection) / len(union) if union else 0.0

    def _pack_context(
        self,
        results: List[Dict],
        max_tokens: int
    ) -> List[Dict]:
        """Pack results into context window

        Args:
            results: Search results
            max_tokens: Maximum tokens

        Returns:
            Selected results
        """
        selected = []
        current_tokens = 0

        for result in results:
            tokens = self._count_tokens(result["content"])

            if current_tokens + tokens <= max_tokens:
                selected.append(result)
                current_tokens += tokens
            else:
                break

        return selected

    def _format_with_citations(self, results: List[Dict]) -> str:
        """Format results with citations

        Args:
            results: Search results

        Returns:
            Formatted context
        """
        formatted = []

        for i, result in enumerate(results, 1):
            file_path = result["metadata"].get("file", "unknown")
            chunk_id = result["metadata"].get("chunk_id", 0)

            formatted.append(
                f"[{i}] From {file_path} (chunk {chunk_id}):\n"
                f"{result['content']}\n"
            )

        return "\n".join(formatted)

    def _count_tokens(self, text: str) -> int:
        """Count tokens in text (simplified)

        Args:
            text: Text to count

        Returns:
            Token count
        """
        # Simple word-based approximation
        # For production, use tiktoken or similar
        return len(text.split()) * 1.3  # Rough estimate

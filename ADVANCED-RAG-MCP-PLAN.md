# 🎯 Advanced RAG MCP Server - Implementation Plan

## 📊 Executive Summary

**Implementar MCP server para RAG avançado com:**
- Semantic search usando vector embeddings
- Context retrieval otimizado para LLMs
- Integração com web2md para indexação
- Vector database ChromaDB (self-hosted)
- Embedding models: sentence-transformers

---

## 🏗️ Architecture Design

### **System Components**

```
┌─────────────────────────────────────────────────────────────┐
│                   Advanced RAG MCP Server                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │  Indexing    │    │   Search     │    │  Retrieval   │  │
│  │   Module     │    │   Module     │    │   Module     │  │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘  │
│         │                   │                   │           │
│  ┌──────▼───────────────────▼───────────────────▼───────┐  │
│  │              Vector Database (ChromaDB)              │  │
│  │  - 1536 dimensions (all-MiniLM-L6-v2)               │  │
│  │  - Persistent storage                               │  │
│  │  - Metadata filtering                               │  │
│  │  - Hybrid search (dense + sparse)                   │  │
│  └──────────────────────────┬────────────────────────────┘  │
│                             │                                │
│  ┌──────────────────────────▼────────────────────────────┐  │
│  │         Embedding Model (sentence-transformers)       │  │
│  │  - all-MiniLM-L6-v2 (fast, good quality)            │  │
│  │  - all-mpnet-base-v2 (slower, better quality)        │  │
│  │  - Multilingual support                             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌──────────────────────────────────────────────────────────┐│
│  │              Integration Layer                           ││
│  │  - web2md for document extraction                        ││
│  │  - Code Graph MCP for code indexing                     ││
│  │  - File watcher for auto-reindexing                     ││
│  └──────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Technology Stack

### **Vector Database: ChromaDB**

**Por que ChromaDB?**
- ✅ **Self-hosted** (no cloud dependency)
- ✅ **Python native** (fácil integração)
- ✅ **Persistent storage** (SQLite backend)
- ✅ **Metadata filtering** (filtros avançados)
- ✅ **Hybrid search** (dense + sparse vectors)
- ✅ **Zero configuration** (setup imediato)
- ✅ **Apache 2.0 licensed** (open source)

**Alternativas consideradas:**
- ❌ Qdrant: Mais complexo, requer Rust
- ❌ Milvus: Overhead pesado, requires Kubernetes
- ❌ Pinecone: Cloud-only, não self-hosted
- ❌ Weaviate: Setup complexo

### **Embedding Models**

**Modelo Primário: all-MiniLM-L6-v2**
- **Speed:** ⚡ Ultra rápido (400ms para 1000 docs)
- **Quality:** ⭐⭐⭐⭐ Bom para código
- **Size:** 80MB (leve)
- **Dimensions:** 384 (compacto)
- **Language:** Inglês (bom para código)

**Modelo Secundário: all-mpnet-base-v2**
- **Speed:** ⚡⚡ Mais lento (800ms para 1000 docs)
- **Quality:** ⭐⭐⭐⭐⭐ Excelente para código
- **Size:** 420MB (médio)
- **Dimensions:** 768 (preciso)
- **Language:** Inglês

**Modelo Multilingual: paraphrase-multilingual-MiniLM-L12-v2**
- **Speed:** ⚡⚡ Médio
- **Quality:** ⭐⭐⭐⭐ Bom para multilingual
- **Size:** 470MB
- **Dimensions:** 384
- **Language:** 50+ idiomas

---

## 📋 MCP Tools Specification

### **1. index_codebase**

**Propósito:** Indexar codebase para semantic search

**Input:**
```python
{
    "force_reindex": bool = False,  # Reindexar tudo?
    "file_patterns": list = [     # Quais arquivos?
        "*.py",
        "*.ts",
        "*.js",
        "*.md"
    ],
    "chunk_size": int = 500,      # Tamanho do chunk (tokens)
    "chunk_overlap": int = 50     # Overlap entre chunks
}
```

**Output:**
```python
{
    "indexed_files": int,         # Arquivos indexados
    "total_chunks": int,          # Chunks criados
    "indexing_time": float,       # Tempo total (segundos)
    "embedding_model": str,       # Modelo usado
    "vector_db_size": int         # Tamanho do DB (vectors)
}
```

**Algorithm:**
```python
def index_codebase(file_patterns, chunk_size, chunk_overlap):
    # 1. Scan directory for matching files
    files = scan_files(file_patterns)

    # 2. Extract content using web2md if needed
    for file in files:
        if is_web_file(file):
            content = web2md_extract(file)
        else:
            content = read_file(file)

        # 3. Chunk content with overlap
        chunks = chunk_content(content, chunk_size, chunk_overlap)

        # 4. Generate embeddings
        embeddings = model.encode(chunks)

        # 5. Store in ChromaDB with metadata
        chroma_db.add(
            documents=chunks,
            embeddings=embeddings,
            metadatas=[{
                "file": file,
                "chunk_id": i,
                "language": detect_language(file),
                "type": get_file_type(file)
            } for i in range(len(chunks))]
        )
```

---

### **2. semantic_search**

**Propósito:** Busca semântica no codebase

**Input:**
```python
{
    "query": str,                  # Query em linguagem natural
    "top_k": int = 5,              # Top K resultados
    "filter": dict = None,         # Filtro de metadados
    "search_type": str = "dense"   # "dense", "sparse", "hybrid"
}
```

**Output:**
```python
{
    "query": str,
    "results": [
        {
            "content": str,
            "score": float,         # Similarity score
            "metadata": {
                "file": str,
                "chunk_id": int,
                "language": str,
                "type": str
            }
        }
    ],
    "total_results": int,
    "search_time": float
}
```

**Algorithm:**
```python
def semantic_search(query, top_k, filter, search_type):
    # 1. Generate query embedding
    query_embedding = model.encode(query)

    # 2. Search in ChromaDB
    if search_type == "dense":
        results = chroma_db.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter  # metadata filter
        )
    elif search_type == "hybrid":
        # Combine dense + sparse (BM25)
        results = chroma_db.hybrid_search(
            query_text=query,
            query_embedding=query_embedding,
            n_results=top_k,
            where=filter
        )

    # 3. Format results
    return format_results(results)
```

---

### **3. context_retrieve**

**Propósito:** Recuperar contexto otimizado para LLM

**Input:**
```python
{
    "query": str,
    "max_tokens": int = 4000,      # Max tokens para contexto
    "min_relevance": float = 0.7,  # Score mínimo
    "diversify": bool = True       # Diversificar resultados?
}
```

**Output:**
```python
{
    "query": str,
    "context": str,                # Contexto formatado
    "sources": list,               # Fontes usadas
    "total_tokens": int,
    "retrieval_time": float,
    "metadata": {
        "files_used": int,
        "chunks_used": int,
        "avg_score": float
    }
}
```

**Algorithm:**
```python
def context_retrieve(query, max_tokens, min_relevance, diversify):
    # 1. Semantic search with more results
    results = semantic_search(query, top_k=20)

    # 2. Filter by relevance
    relevant = [r for r in results if r["score"] >= min_relevance]

    # 3. Diversify (MMR - Maximal Marginal Relevance)
    if diversify:
        selected = mmr_selection(relevant, lambda=0.5)
    else:
        selected = relevant

    # 4. Pack into context window (respect max_tokens)
    context = pack_context(selected, max_tokens)

    # 5. Format with citations
    formatted = format_with_citations(context)

    return {
        "context": formatted,
        "sources": [r["metadata"] for r in selected],
        "total_tokens": count_tokens(formatted)
    }
```

---

### **4. hybrid_search**

**Propósito:** Busca híbrida (semantic + keyword)

**Input:**
```python
{
    "query": str,
    "semantic_weight": float = 0.7,  # Peso semantic vs keyword
    "top_k": int = 5
}
```

**Output:**
```python
{
    "query": str,
    "results": [
        {
            "content": str,
            "semantic_score": float,
            "keyword_score": float,
            "combined_score": float,
            "metadata": dict
        }
    ]
}
```

---

## 🚀 Implementation Plan

### **Phase 1: Core RAG (Week 1)**

**Day 1-2: Setup & Infrastructure**
```bash
# Create project structure
mkdir -p mcp-servers/advanced-rag/{core,embeddings,integration,tests}

# Install dependencies
pip install chromadb sentence-transformers

# Create base ChromaDB setup
python -c "import chromadb; chromadb.Client()"
```

**Day 3-4: Indexing Module**
```python
# core/indexer.py
class CodebaseIndexer:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embedding_model)
        self.chroma = chromadb.PersistentClient("./rag_db")

    def index_file(self, file_path: str, chunk_size=500):
        # Extract, chunk, embed, store
        pass

    def index_directory(self, dir_path: str, patterns=None):
        # Batch index
        pass
```

**Day 5-6: Search Module**
```python
# core/search.py
class SemanticSearch:
    def __init__(self, indexer):
        self.indexer = indexer

    def search(self, query: str, top_k=5):
        # Semantic search
        pass

    def hybrid_search(self, query: str, semantic_weight=0.7):
        # Hybrid semantic + keyword
        pass
```

**Day 7: Integration Testing**
```bash
# Test with real codebase
python tests/test_integration.py
```

### **Phase 2: MCP Integration (Week 2)**

**Day 1-2: MCP Server**
```python
# server.py (FastMCP)
mcp = FastMCP("Advanced RAG")

@mcp.tool()
def index_codebase(force_reindex=False):
    return indexer.index_directory()

@mcp.tool()
def semantic_search(query, top_k=5):
    return search.search(query, top_k)
```

**Day 3-4: web2md Integration**
```python
# integration/web2md.py
def extract_and_index(url):
    # Use web2md to extract, then index
    content = web2md(url)
    indexer.index_content(content)
```

**Day 5-6: Performance Optimization**
```python
# core/cache.py
class EmbeddingCache:
    # Cache embeddings to avoid recomputation
    pass

# core/batch.py
class BatchIndexer:
    # Batch processing for performance
    pass
```

**Day 7: End-to-End Testing**
```bash
# Complete workflow test
python tests/test_e2e.py
```

### **Phase 3: Advanced Features (Week 3)**

**Day 1-2: Multi-Model Support**
```python
# embeddings/multi_model.py
class MultiModelEmbedder:
    def __init__(self):
        self.models = {
            "fast": SentenceTransformer("all-MiniLM-L6-v2"),
            "quality": SentenceTransformer("all-mpnet-base-v2"),
            "multilingual": SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        }

    def embed(self, text, model="fast"):
        return self.models[model].encode(text)
```

**Day 3-4: Query Expansion**
```python
# core/query_expansion.py
def expand_query(query):
    # Expand query with synonyms, related terms
    # Improve recall
    pass
```

**Day 5-6: Re-ranking**
```python
# core/rerank.py
def rerank_results(results, query):
    # Re-rank using cross-encoder
    # Improve precision
    pass
```

**Day 7: Performance Tuning**
```python
# Core optimization
- Batch embedding (100 docs at once)
- Parallel indexing (multi-threading)
- Vector quantization (reduce memory)
```

---

## 📊 Performance Targets

### **Indexing Performance**
- **Small codebase** (<100 files): <30s
- **Medium codebase** (100-1000 files): <2min
- **Large codebase** (1000-10000 files): <10min

### **Search Performance**
- **Semantic search**: <100ms (per query)
- **Hybrid search**: <200ms (per query)
- **Context retrieval**: <500ms (with packing)

### **Quality Metrics**
- **Recall** (relevant documents found): >85%
- **Precision** (found documents relevant): >90%
- **MRR** (Mean Reciprocal Rank): >0.75

---

## 🧪 Testing Strategy

### **Unit Tests**
```python
# tests/test_indexer.py
def test_index_single_file():
    indexer = CodebaseIndexer()
    result = indexer.index_file("test.py")
    assert result["chunks_created"] > 0

# tests/test_search.py
def test_semantic_search():
    search = SemanticSearch(indexer)
    result = search.search("web scraping")
    assert len(result["results"]) > 0
    assert result["results"][0]["score"] > 0.7
```

### **Integration Tests**
```python
# tests/test_integration.py
def test_full_workflow():
    # Index real codebase
    indexer.index_directory("/Users/lucascardoso/web2md")

    # Search
    result = search.search("web to markdown converter")

    # Verify
    assert "web2md" in str(result["results"]).lower()
```

### **Performance Tests**
```python
# tests/test_performance.py
def test_indexing_performance():
    start = time.time()
    indexer.index_directory(large_codebase)
    elapsed = time.time() - start
    assert elapsed < 600  # <10min

def test_search_performance():
    start = time.time()
    result = search.search("test query")
    elapsed = time.time() - start
    assert elapsed < 0.2  # <200ms
```

---

## 🔗 Integration with Existing Tools

### **web2md Integration**
```python
# Use web2md to extract web content, then index
from web2md import web2md_extract

def index_web_documentation(url):
    # Extract with web2md
    content = web2md_extract(url)

    # Index with RAG
    indexer.index_content(content, source=url)

    return {"indexed": True, "url": url}
```

### **Code Graph MCP Integration**
```python
# Use Code Graph to understand structure, enhance RAG
from code_graph import trace_calls

def enhanced_code_search(query):
    # Semantic search
    semantic_results = search.search(query)

    # Enhance with code graph
    for result in semantic_results:
        file = result["metadata"]["file"]
        calls = trace_calls(file)
        result["call_graph"] = calls

    return semantic_results
```

---

## 📈 Success Metrics

### **Functional Metrics**
- ✅ Index 1000 files in <2min
- ✅ Search latency <100ms
- ✅ Context retrieval <500ms
- ✅ Recall >85%
- ✅ Precision >90%

### **Integration Metrics**
- ✅ Works with web2md extracted content
- ✅ Works with Code Graph analysis
- ✅ Compatible with Claude Code MCP
- ✅ No dependency conflicts

### **User Experience Metrics**
- ✅ Simple CLI interface
- ✅ Clear error messages
- ✅ Progress indicators
- ✅ Cached results (speed)

---

## 🎯 Next Steps

### **Immediate (Week 1)**
1. ✅ Create project structure
2. ✅ Setup ChromaDB + sentence-transformers
3. ✅ Implement basic indexing
4. ✅ Implement semantic search

### **Short-term (Week 2)**
5. ✅ MCP server integration
6. ✅ web2md integration
7. ✅ Performance optimization
8. ✅ End-to-end testing

### **Medium-term (Week 3)**
9. ✅ Multi-model support
10. ✅ Query expansion
11. ✅ Re-ranking
12. ✅ Production deployment

---

## 📚 References

### **Documentation**
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Sentence-Transformers](https://www.sbert.net/)
- [RAG Best Practices](https://arxiv.org/abs/2312.10997)

### **Papers**
- "Retrieval-Augmented Generation for Large Language Models" (Lewis et al., 2020)
- "Dense Passage Retrieval for Open-Domain Question Answering" (Karpukhin et al., 2020)

### **Code Examples**
- [ChromaDB Examples](https://github.com/chroma-core/chroma/tree/main/examples)
- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering/)

---

**Status:** PLANO COMPLETO - PRONTO PARA IMPLEMENTAÇÃO

**Estimativa:** 3 semanas até produção

**Prioridade:** CRÍTICA (próximo MCP server após Code Graph)

# 🎯 Gap Fill Implementation Plan - Claude Code Harness

## 📊 Executive Summary

**6 features identified as missing** from Claude Code compared to competitors.

**Strategy:** Implement via MCP servers + Skills (maintain Rust performance)

**Timeline:** 3 phases (Critical → High → Medium priority)

---

## 🚀 Phase 1: Critical Gaps (Week 1-2)

### **1. Code Graph Analysis MCP Server** ⭐⭐⭐⭐⭐

**Priority:** CRITICAL
**Complexity:** Medium
**Dependencies:** None

**Purpose:**

- Trace function calls across codebase
- Impact analysis for changes
- Dependency visualization
- Refactor suggestions

**Architecture:**

```python
# mcp-servers/code-graph/server.py
import ast
import networkx as nx
from pathlib import Path

class CodeGraphAnalyzer:
    """Analyze Python codebase structure"""

    def __init__(self, root_dir: str):
        self.root = Path(root_dir)
        self.graph = nx.DiGraph()

    def trace_calls(self, file_path: str) -> dict:
        """Trace all function calls in a file"""
        # Parse AST
        # Build call graph
        # Return structured data
        pass

    def impact_analysis(self, symbol: str) -> list:
        """Find all usages of a symbol"""
        # Search codebase
        # Return affected files
        pass

    def dependency_graph(self) -> dict:
        """Generate module dependency graph"""
        # Analyze imports
        # Build graph
        # Return JSON
        pass
```

**MCP Tools:**

```json
{
  "tools": [
    {
      "name": "trace_calls",
      "description": "Trace function calls in a file",
      "inputSchema": {
        "type": "object",
        "properties": {
          "file_path": { "type": "string" }
        }
      }
    },
    {
      "name": "impact_analysis",
      "description": "Analyze impact of changing a symbol",
      "inputSchema": {
        "type": "object",
        "properties": {
          "symbol": { "type": "string" },
          "symbol_type": { "type": "string", "enum": ["function", "class", "variable"] }
        }
      }
    },
    {
      "name": "dependency_graph",
      "description": "Generate dependency graph",
      "inputSchema": {
        "type": "object",
        "properties": {
          "format": { "type": "string", "enum": ["json", "dot", "mermaid"] }
        }
      }
    }
  ]
}
```

**Dependencies:**

- `networkx` (graph algorithms)
- `ast` (Python AST parser)
- `astroid` (advanced AST)

**Testing:**

```bash
# Unit tests
pytest tests/mcp-servers/test-code-graph.py

# Integration test
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{
  "name":"trace_calls",
  "arguments":{"file_path":"web2md.ts"}
}}' | python mcp-servers/code-graph/server.py
```

**Integration:**

```json
// settings.json - Add to MCP servers
{
  "mcpServers": {
    "code-graph": {
      "command": "python",
      "args": ["mcp-servers/code-graph/server.py"]
    }
  }
}
```

**Use Case Examples:**

```bash
# Claude Code can now:
"I'm renaming web2md_extract() - what files will be affected?"
→ MCP: impact_analysis("web2md_extract")
→ Returns: 15 files affected

"Show me the call graph for web2md.ts"
→ MCP: trace_calls("web2md.ts")
→ Returns: visualization

"Generate dependency graph for this project"
→ MCP: dependency_graph()
→ Returns: Mermaid diagram
```

---

### **2. Advanced RAG MCP Server** ⭐⭐⭐⭐⭐

**Priority:** CRITICAL
**Complexity:** High
**Dependencies:** Vector database (ChromaDB/Qdrant)

**Purpose:**

- Semantic search in codebase
- Context retrieval for LLM
- Knowledge graph
- Vector embeddings

**Architecture:**

```python
# mcp-servers/advanced-rag/server.py
import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path

class AdvancedRAG:
    """Semantic search and context retrieval"""

    def __init__(self, root_dir: str):
        self.root = Path(root_dir)
        self.client = chromadb.PersistentClient("./rag_db")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection("codebase")

    def index_codebase(self) -> dict:
        """Index all code files"""
        # Walk directory
        # Chunk files
        # Generate embeddings
        # Store in vector DB
        pass

    def semantic_search(self, query: str, top_k: int = 5) -> list:
        """Semantic search in codebase"""
        # Embed query
        # Search vector DB
        # Return results
        pass

    def context_retrieve(self, query: str, max_tokens: int = 4000) -> str:
        """Retrieve relevant context for LLM"""
        # Semantic search
        # Format results
        # Return context string
        pass
```

**MCP Tools:**

```json
{
  "tools": [
    {
      "name": "index_codebase",
      "description": "Index codebase for semantic search",
      "inputSchema": {
        "type": "object",
        "properties": {
          "force_reindex": { "type": "boolean" }
        }
      }
    },
    {
      "name": "semantic_search",
      "description": "Search codebase semantically",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": { "type": "string" },
          "top_k": { "type": "integer", "default": 5 }
        }
      }
    },
    {
      "name": "context_retrieve",
      "description": "Retrieve context for LLM",
      "inputSchema": {
        "type": "object",
        "properties": {
          "query": { "type": "string" },
          "max_tokens": { "type": "integer", "default": 4000 }
        }
      }
    }
  ]
}
```

**Dependencies:**

- `chromadb` (vector database)
- `sentence-transformers` (embeddings)
- `tiktoken` (token counting)

**Testing:**

```bash
# Index codebase
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{
  "name":"index_codebase",
  "arguments":{"force_reindex":true}
}}' | python mcp-servers/advanced-rag/server.py

# Semantic search
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{
  "name":"semantic_search",
  "arguments":{"query":"web scraping", "top_k":3}
}}' | python mcp-servers/advanced-rag/server.py
```

**Integration with web2md:**

```bash
# Combine web2md + RAG
web2md https://docs.example.com | \
  jq '.text' | \
  # Pass to RAG for indexing
```

**Use Case Examples:**

```bash
# Claude Code can now:
"Find all functions related to web scraping"
→ MCP: semantic_search("web scraping")
→ Returns: 7 relevant functions

"Get context for refactoring the authentication module"
→ MCP: context_retrieve("authentication", max_tokens=8000)
→ Returns: Relevant code snippets

"Index this new documentation"
→ MCP: index_codebase(force_reindex=true)
→ Returns: Indexed 127 files
```

---

## 🚀 Phase 2: High Priority Gaps (Week 3-4)

### **3. GUI Automation MCP Server** ⭐⭐⭐⭐

**Priority:** HIGH
**Complexity:** High
**Dependencies:** Playwright/Selenium

**Purpose:**

- Record/replay GUI actions
- Browser automation
- Desktop automation
- Visual testing

**Architecture:**

```python
# mcp-servers/gui-automation/server.py
from playwright.async_api import async_playwright
import json

class GUIAutomation:
    """Record and replay GUI interactions"""

    def __init__(self):
        self.recordings = {}

    async def record_gui(self, name: str, url: str) -> dict:
        """Record GUI interactions"""
        # Launch browser
        # Record actions
        # Save script
        pass

    async def replay_gui(self, name: str) -> dict:
        """Replay recorded GUI script"""
        # Load script
        # Execute actions
        # Return results
        pass

    async def browser_automate(self, actions: list) -> dict:
        """Execute browser automation"""
        # Parse actions
        # Execute in browser
        # Return screenshots/results
        pass
```

**MCP Tools:**

```json
{
  "tools": [
    {
      "name": "record_gui",
      "description": "Record GUI interactions",
      "inputSchema": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "url": { "type": "string" }
        }
      }
    },
    {
      "name": "replay_gui",
      "description": "Replay recorded GUI script",
      "inputSchema": {
        "type": "object",
        "properties": {
          "name": { "type": "string" }
        }
      }
    },
    {
      "name": "browser_automate",
      "description": "Execute browser automation",
      "inputSchema": {
        "type": "object",
        "properties": {
          "actions": { "type": "array" }
        }
      }
    }
  ]
}
```

**Dependencies:**

- `playwright` (browser automation)
- `selenium` (alternative)
- `PIL` (screenshots)

**Testing:**

```bash
# Record
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{
  "name":"record_gui",
  "arguments":{"name":"login-test", "url":"https://example.com/login"}
}}' | python mcp-servers/gui-automation/server.py

# Replay
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{
  "name":"replay_gui",
  "arguments":{"name":"login-test"}
}}' | python mcp-servers/gui-automation/server.py
```

**Use Case Examples:**

```bash
# Claude Code can now:
"Record a test for the login flow"
→ MCP: record_gui("login-test", "https://example.com/login")
→ Returns: Recorded 5 actions

"Replay the login test"
→ MCP: replay_gui("login-test")
→ Returns: Test passed

"Automate filling this form"
→ MCP: browser_automate([actions])
→ Returns: Form submitted
```

---

### **4. Multi-Model Support Skill** ⭐⭐⭐⭐

**Priority:** HIGH
**Complexity:** Low
**Dependencies:** None (skill-based)

**Purpose:**

- Choose appropriate model for task
- Cost optimization
- Performance optimization
- Fallback strategies

**Architecture:**

```markdown
# skills/model-chooser/SKILL.md

---

name: model-chooser
description: Choose the best AI model for a given task based on complexity, speed, and cost requirements

---

# Model Chooser Skill

## Task Analysis

Before choosing a model, analyze the task:

### 1. Task Complexity

- **Simple**: Pattern matching, simple transformations, lookups
  → Use Haiku 4.5 (fastest, cheapest)
- **Medium**: Code generation, explanation, analysis
  → Use Sonnet 4.6 (balanced)
- **Complex**: Reasoning, multi-step logic, architecture
  → Use Opus 4.6 (smartest)

### 2. Speed Requirements

- **Real-time**: <1s response needed
  → Use Haiku 4.5
- **Interactive**: 1-5s response acceptable
  → Use Sonnet 4.6
- **Batch**: Speed not critical
  → Use Opus 4.6

### 3. Cost Constraints

- **High volume**: Many calls per hour
  → Use Haiku 4.5 ($0.25/M tokens)
- **Medium volume**: Regular usage
  → Use Sonnet 4.6 ($3/M tokens)
- **Low volume**: Occasional complex tasks
  → Use Opus 4.6 ($15/M tokens)

### 4. Specialized Requirements

- **Local processing**: No API calls
  → Use Ollama (local models)
- **Privacy**: Data cannot leave machine
  → Use LM Studio (local)
- **Specific capabilities**: Vision, audio, etc.
  → Use appropriate model

## Decision Matrix

| Task                | Complexity | Speed  | Cost   | Model      |
| ------------------- | ---------- | ------ | ------ | ---------- |
| Code completion     | Low        | Fast   | High   | Haiku 4.5  |
| Bug fix             | Medium     | Medium | Medium | Sonnet 4.6 |
| Architecture design | High       | Slow   | Low    | Opus 4.6   |
| Documentation       | Medium     | Medium | Medium | Sonnet 4.6 |
| Testing             | Low        | Fast   | High   | Haiku 4.5  |
| Refactoring         | Medium     | Medium | Medium | Sonnet 4.6 |
| Research            | High       | Slow   | Low    | Opus 4.6   |

## Examples

**Example 1: Quick Code Fix**
```

User: "Fix this syntax error"
Task: Simple (syntax fix)
Speed: Fast (interactive)
Cost: High (many calls)
→ Choose: Haiku 4.5

```

**Example 2: Feature Implementation**
```

User: "Implement user authentication"
Task: Medium (standard feature)
Speed: Medium (development)
Cost: Medium (normal usage)
→ Choose: Sonnet 4.6

```

**Example 3: System Architecture**
```

User: "Design microservices architecture for this system"
Task: High (complex reasoning)
Speed: Slow (one-time)
Cost: Low (single call)
→ Choose: Opus 4.6

````

## Fallback Strategy

If primary model fails:
1. **Timeout/Error**: Retry with same model (1x)
2. **Still failing**: Fall back to simpler model
   - Opus → Sonnet
   - Sonnet → Haiku
3. **All failing**: Use local model (Ollama)

## Cost Optimization

**For high-volume tasks:**
1. Start with Haiku 4.5
2. If quality insufficient, upgrade to Sonnet 4.6
3. Only use Opus 4.6 for complex reasoning

**Example workflow:**
```bash
# Step 1: Try Haiku (fast, cheap)
claude --model haiku "generate unit tests"

# Step 2: If quality low, try Sonnet
claude --model sonnet "generate unit tests with edge cases"

# Step 3: Only if needed, use Opus
claude --model opus "generate comprehensive test suite with mocks"
````

## Integration with Claude Code

When using this skill, Claude Code will:

1. Analyze task automatically
2. Choose appropriate model
3. Execute with chosen model
4. Fall back if needed
5. Report model choice and reasoning

````

**Testing:**
```bash
# Test skill
claude --skill model-chooser "What's the best model for generating unit tests?"
# Expected: Haiku 4.5 (simple, fast, high-volume)

claude --skill model-chooser "Design a payment processing system"
# Expected: Opus 4.6 (complex, slow, low-volume)
````

**Use Case Examples:**

```bash
# Claude Code will automatically:
"Generate unit tests for web2md.ts"
→ Skill: Choose Haiku 4.5 (simple, fast)

"Design architecture for multi-agent system"
→ Skill: Choose Opus 4.6 (complex reasoning)

"Fix this bug in production"
→ Skill: Choose Sonnet 4.6 (balanced)

"Index 1000 files"
→ Skill: Choose Haiku 4.5 (high-volume, fast)
```

---

## 🚀 Phase 3: Medium Priority Gaps (Week 5-6)

### **5. Real-time Collaboration MCP Server** ⭐⭐⭐

**Priority:** MEDIUM
**Complexity:** Medium
**Dependencies:** WebSocket server

**Purpose:**

- Multi-user sessions
- Shared context
- Live editing
- Team workflows

**Architecture:**

```python
# mcp-servers/collaboration/server.py
import asyncio
import websockets
import json

class CollaborationServer:
    """Real-time collaboration"""

    def __init__(self):
        self.sessions = {}
        self.connections = {}

    def share_session(self, session_id: str, users: list) -> dict:
        """Share session with multiple users"""
        # Create session
        # Invite users
        # Sync context
        pass

    def sync_context(self, session_id: str) -> dict:
        """Sync context across users"""
        # Get current context
        # Broadcast to all users
        # Confirm sync
        pass

    async def broadcast_update(self, session_id: str, update: dict):
        """Broadcast update to all users"""
        # Send to all connections
        pass
```

**MCP Tools:**

```json
{
  "tools": [
    {
      "name": "share_session",
      "description": "Share session with team",
      "inputSchema": {
        "type": "object",
        "properties": {
          "session_id": { "type": "string" },
          "users": { "type": "array", "items": { "type": "string" } }
        }
      }
    },
    {
      "name": "sync_context",
      "description": "Sync context across users",
      "inputSchema": {
        "type": "object",
        "properties": {
          "session_id": { "type": "string" }
        }
      }
    }
  ]
}
```

**Dependencies:**

- `websockets` (real-time communication)
- `redis` (session storage)

**Use Case Examples:**

```bash
# Claude Code can now:
"Share this session with the team"
→ MCP: share_session("session-123", ["user1", "user2"])
→ Returns: Session shared

"Sync context with all users"
→ MCP: sync_context("session-123")
→ Returns: Context synced
```

---

### **6. Distributed Agents Skill** ⭐⭐⭐⭐

**Priority:** MEDIUM
**Complexity:** High
**Dependencies:** Message queue (Redis/RabbitMQ)

**Purpose:**

- Orchestrate multiple agents
- Agent-to-agent communication
- Distributed task execution
- Fault tolerance

**Architecture:**

```markdown
# skills/distributed/SKILL.md

---

name: distributed
description: Orchestrate multiple autonomous agents for distributed task execution

---

# Distributed Agents Skill

## When to Use

**Use distributed agents when:**

- Task can be parallelized
- Multiple agents needed for complexity
- Fault tolerance required
- Scalability is important

**Don't use when:**

- Task is simple (single agent faster)
- Communication overhead too high
- Real-time coordination needed

## Agent Patterns

### 1. Map-Reduce Pattern
```

Master Agent
├─ Agent 1: Process chunk 1
├─ Agent 2: Process chunk 2
├─ Agent 3: Process chunk 3
└─ Reduce: Combine results

```

**Use case:** Process 100 files in parallel

### 2. Pipeline Pattern
```

Agent 1 (Fetch)
↓
Agent 2 (Process)
↓
Agent 3 (Store)

```

**Use case:** ETL workflow

### 3. Expert Pattern
```

Dispatcher Agent
├─ Code Expert Agent
├─ Design Expert Agent
├─ Security Expert Agent
└─ Integrator Agent

```

**Use case:** Code review with multiple experts

### 4. Voting Pattern
```

Task Agent
├─ Agent 1: Generate solution
├─ Agent 2: Generate solution
├─ Agent 3: Generate solution
└─ Voter Agent: Choose best

````

**Use case:** Generate multiple options, pick best

## Implementation

### Spawn Agent
```bash
# Spawn new agent via CLI
AGENT_OUTPUT=$(claude --print --output-format=json \
  --agent autonomous \
  "execute subtask: analyze file X" 2>/dev/null)

# Parse result
AGENT_ID=$(echo "$AGENT_OUTPUT" | jq -r '.agent_id')
STATUS=$(echo "$AGENT_OUTPUT" | jq -r '.status')
````

### Agent Communication

```bash
# Send message to agent
echo '{"message": "update context", "data": {...}}' | \
  redis-cli PUBLISH agent:$AGENT_ID

# Receive message from agent
redis-cli SUBSCRIBE agent:$AGENT_ID
```

### Fault Tolerance

```bash
# Monitor agent health
if ! ping_agent $AGENT_ID; then
  # Spawn replacement
  NEW_AGENT=$(spawn_agent "retry task")
  update_context "$NEW_AGENT"
fi
```

## Examples

**Example 1: Parallel File Processing**

```
Task: "Analyze 100 files"
→ Spawn 10 agents
→ Each processes 10 files
→ Combine results
```

**Example 2: Multi-Expert Review**

```
Task: "Review this PR"
→ Spawn Code Expert
→ Spawn Security Expert
→ Spawn Performance Expert
→ Combine reviews
```

**Example 3: Distributed Web Scraping**

```
Task: "Scrape 1000 URLs"
→ Spawn 20 agents
→ Each scrapes 50 URLs
→ Aggregate results
```

## Monitoring

```bash
# Check agent status
claude --agent status --agent-id $AGENT_ID

# List all agents
claude --agent list

# Kill agent
claude --agent kill --agent-id $AGENT_ID
```

## Best Practices

1. **Start small**: 2-3 agents max
2. **Monitor closely**: Watch for failures
3. **Set timeouts**: Don't let agents run forever
4. **Aggregate carefully**: Handle agent failures
5. **Test locally**: Before scaling up

````

**Dependencies:**
- `redis` (message queue)
- `celery` (task queue)

**Use Case Examples:**
```bash
# Claude Code can now:
"Analyze these 100 files in parallel"
→ Skill: Spawn 10 agents, 10 files each
→ Returns: Combined analysis

"Get security, performance, and code review"
→ Skill: Spawn 3 expert agents
→ Returns: Combined reviews

"Scrape these 1000 URLs"
→ Skill: Spawn 20 agents, 50 URLs each
→ Returns: Aggregated data
````

---

## 📋 Implementation Timeline

### **Week 1-2: Critical**

- [ ] Code Graph Analysis MCP
- [ ] Advanced RAG MCP

### **Week 3-4: High Priority**

- [ ] GUI Automation MCP
- [ ] Multi-Model Skill

### **Week 5-6: Medium Priority**

- [ ] Collaboration MCP
- [ ] Distributed Agents Skill

---

## 🧪 Testing Strategy

### **Unit Tests**

```bash
# Each MCP server
pytest tests/mcp-servers/test-{server}.py

# Each skill
claude --skill {skill} "test prompt"
```

### **Integration Tests**

```bash
# Test MCP integration
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  python mcp-servers/{server}/server.py

# Test skill integration
claude --skill {skill} "integration test"
```

### **End-to-End Tests**

```bash
# Complete workflow
claude "Analyze this codebase with code-graph"
claude "Search for authentication code with RAG"
claude "Record GUI test for login flow"
```

---

## 📊 Success Metrics

### **Code Graph**

- ✅ Trace calls in <5s for 100 files
- ✅ Impact analysis accurate 95%+
- ✅ Dependency graph generates in <10s

### **Advanced RAG**

- ✅ Index 1000 files in <5min
- ✅ Semantic search returns results in <1s
- ✅ Context retrieval relevant 90%+

### **GUI Automation**

- ✅ Record 10 actions in <30s
- ✅ Replay with 95%+ success rate
- ✅ Browser automation <5s per action

### **Multi-Model**

- ✅ Correct model choice 90%+
- ✅ Cost reduction 50%+ (vs always using Opus)
- ✅ Speed improvement 3x+ (vs always using Opus)

### **Collaboration**

- ✅ <100ms latency for updates
- ✅ Support 10+ concurrent users
- ✅ Context sync 99%+ reliable

### **Distributed Agents**

- ✅ Spawn agent in <2s
- ✅ 10 agents run in parallel
- ✅ 95%+ task completion rate

---

## 🎯 Final Architecture

```
Claude Code (Rust Native)
├─ Hooks (Event System)
│   ├─ Telemetry
│   ├─ Auto-documentation
│   └─ Guardrails
├─ Skills (Custom Behaviors)
│   ├─ model-chooser (NEW)
│   ├─ distributed (NEW)
│   └─ web2md
├─ MCP Servers (Extensibility)
│   ├─ code-graph (NEW)
│   ├─ advanced-rag (NEW)
│   ├─ gui-automation (NEW)
│   ├─ collaboration (NEW)
│   └─ notebooklm (existing)
└─ jq (JSON Processing)
```

**Result:** Claude Code com 100% das features dos competidores, mantendo performance Rust.

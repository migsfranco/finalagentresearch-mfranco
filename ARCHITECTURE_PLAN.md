# Scientific Paper Research Agent - Architecture Plan

## Summary of Current Implementation (Jupyter Notebook)

The notebook implements a **Scientific Paper Research Agent** with:

### Current Features:
1. **5 Research Tools:**
   - Google Scholar Search (via SerpAPI)
   - Tavily Search (general web search)
   - PubMed Search (medical/biomedical papers)
   - ArXiv Search (preprints)
   - DuckDuckGo Search (free fallback)

2. **RAG System for APA Citation Correction:**
   - PDF ingestion (APA 7th edition manual)
   - ChromaDB vector store
   - Citation correction tool
   - Multi-citation extraction and correction

3. **Agent Architecture:**
   - LangGraph ReAct agent
   - Memory persistence (MemorySaver)
   - OpenAI GPT-3.5-turbo as LLM

---

## Proposed Clean Architecture

```
agente-investigador/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config/
│   │   │   ├── __init__.py
│   │   │   └── settings.py            # Pydantic settings (env vars)
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── chat.py            # Chat/conversation endpoints
│   │   │   │   ├── tools.py           # Tool execution endpoints
│   │   │   │   └── health.py          # Health check endpoints
│   │   │   └── dependencies.py        # FastAPI dependencies
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── agent.py               # LangGraph agent factory
│   │   │   ├── memory.py              # Memory/checkpoint management
│   │   │   └── prompts.py             # System prompts
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── base.py                # Abstract tool interface
│   │   │   ├── google_scholar.py      # Google Scholar tool
│   │   │   ├── tavily_search.py       # Tavily search tool
│   │   │   ├── pubmed.py              # PubMed tool
│   │   │   ├── arxiv.py               # ArXiv tool
│   │   │   ├── duckduckgo.py          # DuckDuckGo tool
│   │   │   └── apa_corrector.py       # APA citation corrector
│   │   ├── rag/
│   │   │   ├── __init__.py
│   │   │   ├── document_loader.py     # PDF/document ingestion
│   │   │   ├── vector_store.py        # ChromaDB operations
│   │   │   ├── retriever.py           # Retrieval logic
│   │   │   └── chain.py               # RAG chain composition
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── chat.py                # Chat request/response schemas
│   │   │   ├── tools.py               # Tool schemas
│   │   │   └── rag.py                 # RAG schemas
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── chat_service.py        # Chat business logic
│   │       └── rag_service.py         # RAG business logic
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py                # Pytest fixtures
│   │   ├── unit/
│   │   │   ├── __init__.py
│   │   │   ├── test_tools.py
│   │   │   ├── test_rag.py
│   │   │   └── test_agent.py
│   │   ├── integration/
│   │   │   ├── __init__.py
│   │   │   ├── test_api.py
│   │   │   └── test_chat_flow.py
│   │   └── e2e/
│   │       └── test_full_conversation.py
│   ├── data/
│   │   └── documents/
│   │       └── APA_7ed.pdf            # APA manual for RAG
│   ├── pyproject.toml                 # uv/Python project config
│   ├── ruff.toml                      # Ruff linter config
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── main.tsx                   # App entry
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   │   ├── ChatContainer.tsx
│   │   │   │   ├── MessageList.tsx
│   │   │   │   ├── MessageBubble.tsx
│   │   │   │   └── ChatInput.tsx
│   │   │   ├── Tools/
│   │   │   │   ├── ToolSelector.tsx
│   │   │   │   └── ToolResult.tsx
│   │   │   └── Layout/
│   │   │       ├── Header.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       └── Footer.tsx
│   │   ├── hooks/
│   │   │   ├── useChat.ts
│   │   │   ├── useTools.ts
│   │   │   └── useWebSocket.ts
│   │   ├── services/
│   │   │   └── api.ts                 # API client
│   │   ├── types/
│   │   │   ├── chat.ts
│   │   │   └── tools.ts
│   │   ├── stores/
│   │   │   └── chatStore.ts           # Zustand/Redux store
│   │   ├── schemas/
│   │   │   └── validation.ts          # Zod schemas
│   │   └── utils/
│   │       └── formatters.ts
│   ├── public/
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── eslint.config.js
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## SOLID Principles Application

### 1. Single Responsibility Principle (SRP)
- Each tool in `tools/` handles ONE search source
- Separate services for chat and RAG operations
- Dedicated schemas for validation

### 2. Open/Closed Principle (OCP)
- `base.py` defines abstract `BaseTool` interface
- New tools extend base without modifying existing code
- Plugin-like architecture for adding new search sources

### 3. Liskov Substitution Principle (LSP)
- All tools implement same interface
- Can swap Google Scholar for Semantic Scholar seamlessly
- RAG components are interchangeable

### 4. Interface Segregation Principle (ISP)
- Small, focused interfaces per tool type
- Separate schemas for different API operations
- Frontend components are atomic and composable

### 5. Dependency Inversion Principle (DIP)
- High-level modules depend on abstractions
- Settings injected via Pydantic BaseSettings
- Tools injected into agent factory

---

## API Keys Required (.env file)

```env
# LLM Provider
OPENAI_API_KEY=sk-...                    # Required for GPT models

# Search Tools
TAVILY_API_KEY=tvly-...                  # Tavily search API
SERP_API_KEY=...                         # Google Scholar via SerpAPI

# Optional - LangSmith for tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__...
LANGCHAIN_PROJECT=agente-investigador

# Server Config
HOST=0.0.0.0
PORT=8000
ENVIRONMENT=development

# Vector Store
CHROMA_PERSIST_DIRECTORY=./data/chroma

# Frontend (if using Vercel)
VITE_API_URL=http://localhost:8000
```

### API Key Sources:
| Key | Source | Cost |
|-----|--------|------|
| OPENAI_API_KEY | https://platform.openai.com/api-keys | Pay-per-use |
| TAVILY_API_KEY | https://tavily.com/ | Free tier available |
| SERP_API_KEY | https://serpapi.com/ | Free tier (100 searches/month) |
| LANGCHAIN_API_KEY | https://smith.langchain.com/ | Free tier available |

---

## Deployment Options

### Option 1: Vercel (Frontend) + Backend as a Service

**Pros:**
- Easy deployment for React frontend
- Serverless functions for simple APIs
- Free tier generous for hobby projects

**Cons:**
- Vercel serverless has 10s timeout (problematic for LLM calls)
- Need separate backend host for Python

**Recommended Setup:**
```
Frontend: Vercel (React + Vite)
Backend: Railway / Render / Fly.io (FastAPI)
Vector DB: Pinecone or hosted ChromaDB
```

### Option 2: Google Cloud Platform (Full Stack)

**Architecture:**
```
┌─────────────────────────────────────────────────────────┐
│                    Google Cloud                          │
├─────────────────────────────────────────────────────────┤
│  Cloud Run (Backend)          │  Cloud Storage          │
│  - FastAPI container          │  - PDF documents        │
│  - Auto-scaling               │  - Static assets        │
│  - Pay-per-request            │                         │
├─────────────────────────────────────────────────────────┤
│  Firebase Hosting (Frontend)  │  Cloud SQL / Firestore  │
│  - React SPA                  │  - Session storage      │
│  - Global CDN                 │  - User data            │
├─────────────────────────────────────────────────────────┤
│  Secret Manager               │  Cloud Monitoring       │
│  - API keys                   │  - Logging & traces     │
└─────────────────────────────────────────────────────────┘
```

**GCP Services:**
- **Cloud Run**: Containerized FastAPI backend
- **Firebase Hosting**: Static React frontend
- **Secret Manager**: Secure API key storage
- **Cloud Storage**: PDF documents for RAG
- **Vertex AI** (optional): Replace OpenAI with Google models

**Estimated Cost (Low Traffic):**
- Cloud Run: ~$5-10/month
- Firebase Hosting: Free
- Storage: <$1/month
- Vertex AI: Pay-per-use

### Option 3: Local Development Setup

```bash
# Backend
cd backend
uv sync
uv run uvicorn src.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

---

## Test-Driven Development Strategy

### Unit Tests
```python
# tests/unit/test_tools.py
def test_arxiv_tool_parses_response():
    tool = ArxivTool()
    result = tool.run("2510.13422")
    assert "Title" in result
    assert "Authors" in result

def test_apa_corrector_fixes_et_al():
    corrector = APACorrectorTool()
    result = corrector.correct("(Gomez et al, 2023)")
    assert "et al." in result  # Note the period
```

### Integration Tests
```python
# tests/integration/test_api.py
async def test_chat_endpoint_returns_response(client):
    response = await client.post("/api/chat", json={
        "message": "Find 2 papers on AI",
        "thread_id": "test-123"
    })
    assert response.status_code == 200
    assert "papers" in response.json()["content"].lower()
```

### E2E Tests
```python
# tests/e2e/test_full_conversation.py
async def test_multi_turn_conversation():
    # Create session
    # Send message 1
    # Verify tool call
    # Send follow-up
    # Verify memory retention
```

---

## Next Steps (Implementation Order)

1. **Initialize Backend Project**
   - Set up `pyproject.toml` with uv
   - Configure ruff for linting
   - Create folder structure

2. **Implement Core Tools (TDD)**
   - Write tests first
   - Implement tool abstractions
   - Add each search tool

3. **Build RAG System**
   - Document loader
   - Vector store setup
   - Retrieval chain

4. **Create FastAPI Endpoints**
   - Chat endpoint with streaming
   - Health checks
   - Tool info endpoint

5. **Initialize Frontend**
   - Vite + React + TypeScript setup
   - Chat UI components
   - API integration

6. **Docker & Local Deployment**
   - Dockerfiles for both services
   - docker-compose for local dev

7. **Production Deployment**
   - Choose platform (GCP recommended)
   - CI/CD pipeline
   - Monitoring setup

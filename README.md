# Scientific Paper Research Agent

AI-powered research assistant for searching scientific papers across multiple databases and correcting APA citations.

## Features

- **Multi-Database Search**: Google Scholar, PubMed, ArXiv, Tavily, DuckDuckGo
- **APA Citation Correction**: RAG-based system using APA 7th edition guidelines
- **Conversational Interface**: LangGraph ReAct agent with memory
- **Modern Stack**: FastAPI backend + React/TypeScript frontend

## Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Node.js 18+
- [uv](https://docs.astral.sh/uv/) package manager

### 1. Clone the Repository

```bash
git clone https://github.com/beotavalo/agente-investigador.git
cd agente-investigador
```

### 2. Configure Environment Variables

```bash
cp .env.example backend/.env
```

Edit `backend/.env` with your API keys:

```env
# Required
OPENAI_API_KEY=sk-your-openai-key

# Optional (enhances search capabilities)
TAVILY_API_KEY=tvly-your-tavily-key
SERP_API_KEY=your-serpapi-key

# Optional (enables tracing)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls__your-langsmith-key
```

### 3. Start Backend

```bash
cd backend
uv sync
uv run uvicorn src.main:app --reload --port 8000
```

Backend runs at: http://localhost:8000

### 4. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: http://localhost:5173

---

## API Keys

| Key | Source | Required | Free Tier |
|-----|--------|----------|-----------|
| `OPENAI_API_KEY` | [OpenAI Platform](https://platform.openai.com/api-keys) | Yes | Pay-per-use |
| `TAVILY_API_KEY` | [Tavily](https://tavily.com/) | No | 1000 searches/month |
| `SERP_API_KEY` | [SerpAPI](https://serpapi.com/) | No | 100 searches/month |
| `LANGCHAIN_API_KEY` | [LangSmith](https://smith.langchain.com/) | No | Free tier available |

---

## Production Deployment

### Backend on Railway

#### Step 1: Create Railway Project

1. Go to [railway.app](https://railway.app) and login with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select `beotavalo/agente-investigador`

#### Step 2: Configure Service

1. In service settings, set **Root Directory**: `backend`
2. Railway auto-detects Dockerfile

#### Step 3: Set Environment Variables

Go to **Variables** tab and add:

| Variable | Value | Required |
|----------|-------|----------|
| `OPENAI_API_KEY` | `sk-...` | Yes |
| `ENVIRONMENT` | `production` | Yes |
| `TAVILY_API_KEY` | `tvly-...` | No |
| `SERP_API_KEY` | `...` | No |
| `LANGCHAIN_TRACING_V2` | `true` | No |
| `LANGCHAIN_API_KEY` | `ls__...` | No |
| `FRONTEND_URL` | `https://your-app.vercel.app` | Yes (after Vercel deploy) |

#### Step 4: Generate Domain

1. Go to **Settings** → **Networking** → **Generate Domain**
2. Copy your Railway URL (e.g., `https://agente-investigador-production.up.railway.app`)

---

### Frontend on Vercel

#### Step 1: Create Vercel Project

1. Go to [vercel.com](https://vercel.com) and login with GitHub
2. Click **"Add New..."** → **"Project"**
3. Import `beotavalo/agente-investigador`

#### Step 2: Configure Build

| Setting | Value |
|---------|-------|
| Root Directory | `frontend` |
| Framework Preset | Vite (auto-detected) |
| Build Command | `npm run build` |
| Output Directory | `dist` |

#### Step 3: Set Environment Variables

Go to **Settings** → **Environment Variables**:

| Variable | Value |
|----------|-------|
| `VITE_API_URL` | `https://YOUR-RAILWAY-URL.railway.app/api` |

Replace `YOUR-RAILWAY-URL` with your actual Railway domain.

#### Step 4: Deploy

Click **Deploy** and wait for completion.

---

### Post-Deployment: Update CORS

After Vercel deployment, go back to Railway and add:

| Variable | Value |
|----------|-------|
| `FRONTEND_URL` | `https://your-app.vercel.app` |

Railway will auto-redeploy with updated CORS settings.

---

## Security

| Secret | Location | Client Exposed |
|--------|----------|----------------|
| `OPENAI_API_KEY` | Railway | No |
| `TAVILY_API_KEY` | Railway | No |
| `SERP_API_KEY` | Railway | No |
| `LANGCHAIN_API_KEY` | Railway | No |
| `VITE_API_URL` | Vercel | Yes (public URL, safe) |

All sensitive API keys remain server-side and are never exposed to the frontend.

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/ready` | GET | Readiness check |
| `/api/chat` | POST | Send message to agent |
| `/api/chat/{thread_id}` | DELETE | Delete conversation |
| `/api/tools` | GET | List available tools |
| `/api/tools/{name}` | GET | Get tool details |

---

## Project Structure

```
agente-investigador/
├── backend/
│   ├── src/
│   │   ├── api/routes/      # FastAPI endpoints
│   │   ├── core/            # Agent, memory, prompts
│   │   ├── tools/           # Search tools
│   │   ├── rag/             # RAG system
│   │   └── schemas/         # Pydantic models
│   ├── tests/               # pytest tests
│   ├── pyproject.toml       # Python dependencies
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── stores/          # Zustand state
│   │   ├── services/        # API client
│   │   └── schemas/         # Zod validation
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml       # Local development
```

---

## Docker (Local)

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## Tech Stack

**Backend:**
- Python 3.11, FastAPI, uvicorn
- LangChain, LangGraph, LangSmith
- ChromaDB (vector store)
- uv (package manager)

**Frontend:**
- React 18, TypeScript, Vite
- Zustand (state management)
- Zod (validation)
- Tailwind CSS

---

## License

MIT

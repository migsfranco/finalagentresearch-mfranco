# Scientific Paper Research Agent - Backend

FastAPI backend for the Scientific Paper Research Agent.

## Setup

```bash
uv sync
uv run uvicorn src.main:app --reload
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/chat` - Send message to agent
- `GET /api/tools` - List available tools

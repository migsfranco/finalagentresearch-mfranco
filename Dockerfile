# Railway Dockerfile - builds from repository root
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy backend dependency files
COPY backend/pyproject.toml backend/README.md ./

# Install dependencies
RUN uv venv && uv pip install .

# Copy backend source code
COPY backend/src/ ./src/

# Create data directory
RUN mkdir -p data/chroma

# Expose port
EXPOSE 8000

# Run the application - Railway sets PORT env variable
CMD ["sh", "-c", ". .venv/bin/activate && uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

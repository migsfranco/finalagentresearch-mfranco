# Backend Dockerfile (for docker-compose / local builds)
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

# Copy dependency files
COPY pyproject.toml README.md ./

# Install dependencies
RUN uv venv && uv pip install .

# Copy source code
COPY src/ ./src/

# Create data directory
RUN mkdir -p data/chroma

# Expose port
EXPOSE 8000

# Run the application
CMD ["sh", "-c", ". .venv/bin/activate && uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

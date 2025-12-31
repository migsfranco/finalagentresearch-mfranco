"""FastAPI application entry point."""

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# Load .env file before importing settings
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

from .api.routes import chat, health, tools
from .config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    settings = get_settings()
    logger.info(f"Starting application in {settings.environment} mode")
    logger.info(f"LangSmith tracing: {'enabled' if settings.langchain_tracing_v2 else 'disabled'}")

    # Log available tools
    logger.info("Available search tools:")
    logger.info(f"  - Google Scholar: {'available' if settings.serp_api_key else 'unavailable (no SERP_API_KEY)'}")
    logger.info(f"  - Tavily: {'available' if settings.tavily_api_key else 'unavailable (no TAVILY_API_KEY)'}")
    logger.info("  - PubMed: available (no API key required)")
    logger.info("  - ArXiv: available (no API key required)")
    logger.info("  - DuckDuckGo: available (no API key required)")

    yield

    # Shutdown
    logger.info("Shutting down application")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI app instance.
    """
    settings = get_settings()

    app = FastAPI(
        title="Scientific Paper Research Agent API",
        description=(
            "AI agent for searching scientific papers across multiple databases "
            "(Google Scholar, PubMed, ArXiv) and correcting APA citations."
        ),
        version="0.1.0",
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS - allow all origins for API access
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["*"],
        expose_headers=["*"],
        max_age=86400,  # Cache preflight for 24 hours
    )

    # Register routers
    app.include_router(health.router, prefix="/api")
    app.include_router(chat.router, prefix="/api")
    app.include_router(tools.router, prefix="/api")

    # CORS headers for error responses
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "*",
        "Access-Control-Allow-Headers": "*",
    }

    # Handle validation errors (400)
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.warning(f"Validation error: {exc.errors()}")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors()},
            headers=cors_headers,
        )

    # Handle HTTP exceptions
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=cors_headers,
        )

    # Handle all other exceptions
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=500,
            content={"detail": str(exc)},
            headers=cors_headers,
        )

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        "src.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.is_development,
    )

"""Health check endpoints."""

from fastapi import APIRouter

from ...config import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Check if the API is healthy.

    Returns:
        Health status.
    """
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check() -> dict[str, str | bool]:
    """Check if the API is ready to serve requests.

    Returns:
        Readiness status with configuration info.
    """
    settings = get_settings()
    return {
        "status": "ready",
        "openai_configured": bool(settings.openai_api_key),
        "tavily_configured": bool(settings.tavily_api_key),
        "serp_configured": bool(settings.serp_api_key),
    }

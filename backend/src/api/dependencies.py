"""FastAPI dependencies."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from ..config import Settings, get_settings


# Type alias for settings dependency
SettingsDep = Annotated[Settings, Depends(get_settings)]


@lru_cache
def get_app_info() -> dict[str, str]:
    """Get application information.

    Returns:
        Application info dict.
    """
    return {
        "name": "Scientific Paper Research Agent",
        "version": "0.1.0",
        "description": "AI agent for searching scientific papers and correcting APA citations",
    }

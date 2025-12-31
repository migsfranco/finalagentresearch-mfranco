"""Tool-related schemas."""

from pydantic import BaseModel


class ToolInfo(BaseModel):
    """Information about an available tool."""

    name: str
    description: str
    requires_api_key: bool = False
    is_available: bool = True


class ToolsResponse(BaseModel):
    """Response schema for tools endpoint."""

    tools: list[ToolInfo]
    total: int

"""Tool information endpoints."""

from fastapi import APIRouter

from ...config import get_settings
from ...schemas import ToolInfo, ToolsResponse

router = APIRouter(prefix="/tools", tags=["tools"])


@router.get("", response_model=ToolsResponse)
async def list_tools() -> ToolsResponse:
    """List all available tools.

    Returns:
        List of tool information.
    """
    settings = get_settings()

    tools = [
        ToolInfo(
            name="google_scholar",
            description="Search Google Scholar for academic papers",
            requires_api_key=True,
            is_available=bool(settings.serp_api_key),
        ),
        ToolInfo(
            name="tavily_search",
            description="Search the web using Tavily",
            requires_api_key=True,
            is_available=bool(settings.tavily_api_key),
        ),
        ToolInfo(
            name="pubmed",
            description="Search PubMed for biomedical literature",
            requires_api_key=False,
            is_available=True,
        ),
        ToolInfo(
            name="arxiv",
            description="Search ArXiv for preprints",
            requires_api_key=False,
            is_available=True,
        ),
        ToolInfo(
            name="duckduckgo",
            description="Search the web using DuckDuckGo (free)",
            requires_api_key=False,
            is_available=True,
        ),
        ToolInfo(
            name="apa_citation_corrector",
            description="Correct APA citations using RAG",
            requires_api_key=False,
            is_available=True,
        ),
    ]

    return ToolsResponse(
        tools=tools,
        total=len(tools),
    )


@router.get("/{tool_name}", response_model=ToolInfo)
async def get_tool(tool_name: str) -> ToolInfo:
    """Get information about a specific tool.

    Args:
        tool_name: Name of the tool.

    Returns:
        Tool information.

    Raises:
        HTTPException: If tool not found.
    """
    from fastapi import HTTPException

    tools_response = await list_tools()

    for tool in tools_response.tools:
        if tool.name == tool_name:
            return tool

    raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

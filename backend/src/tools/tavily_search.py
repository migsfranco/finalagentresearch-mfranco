"""Tavily search tool for general web search."""

from langchain.tools import BaseTool as LangChainBaseTool
from langchain_tavily import TavilySearch

from .base import BaseTool


class TavilySearchTool(BaseTool):
    """Tavily search tool for general web search.

    Requires TAVILY_API_KEY environment variable.
    """

    def __init__(
        self,
        api_key: str | None = None,
        max_results: int = 5,
        topic: str = "general",
    ):
        """Initialize Tavily search tool.

        Args:
            api_key: Tavily API key. If None, reads from TAVILY_API_KEY env var.
            max_results: Maximum number of results to return.
            topic: Search topic ('general' or 'news').
        """
        self._api_key = api_key
        self._max_results = max_results
        self._topic = topic

    @property
    def name(self) -> str:
        return "tavily_search"

    @property
    def description(self) -> str:
        return (
            "Search the web for current information using Tavily. "
            "Useful for finding recent news, blog posts, and general web content. "
            "Input should be a search query string."
        )

    def create_tool(self) -> LangChainBaseTool:
        """Create Tavily search tool.

        Returns:
            TavilySearch: Configured Tavily search tool.
        """
        return TavilySearch(
            max_results=self._max_results,
            topic=self._topic,
            name=self.name,
            description=self.description,
        )

    def validate_config(self) -> bool:
        """Check if Tavily API key is available."""
        import os

        return bool(self._api_key or os.getenv("TAVILY_API_KEY"))

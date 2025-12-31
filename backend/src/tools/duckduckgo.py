"""DuckDuckGo search tool - free fallback search."""

from langchain.tools import BaseTool as LangChainBaseTool
from langchain_community.tools import DuckDuckGoSearchRun

from .base import BaseTool


class DuckDuckGoSearchTool(BaseTool):
    """DuckDuckGo search tool - free web search without API key.

    Useful as a fallback when other search APIs are unavailable.
    """

    @property
    def name(self) -> str:
        return "duckduckgo"

    @property
    def description(self) -> str:
        return (
            "Search the web using DuckDuckGo. "
            "A free search option for general web queries when other search tools "
            "are unavailable or rate-limited. "
            "Input should be a search query string."
        )

    def create_tool(self) -> LangChainBaseTool:
        """Create DuckDuckGo search tool.

        Returns:
            DuckDuckGoSearchRun: Configured DuckDuckGo search tool.
        """
        return DuckDuckGoSearchRun(
            name=self.name,
            description=self.description,
        )

    def validate_config(self) -> bool:
        """DuckDuckGo doesn't require API key."""
        return True

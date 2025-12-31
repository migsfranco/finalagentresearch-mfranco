"""Google Scholar search tool using SerpAPI."""

from langchain.tools import BaseTool as LangChainBaseTool
from langchain_community.tools.google_scholar import GoogleScholarQueryRun
from langchain_community.utilities.google_scholar import GoogleScholarAPIWrapper

from .base import BaseTool


class GoogleScholarTool(BaseTool):
    """Google Scholar search tool for academic papers.

    Requires SERP_API_KEY environment variable.
    """

    def __init__(self, api_key: str | None = None):
        """Initialize Google Scholar tool.

        Args:
            api_key: SerpAPI key. If None, reads from SERP_API_KEY env var.
        """
        self._api_key = api_key

    @property
    def name(self) -> str:
        return "google_scholar"

    @property
    def description(self) -> str:
        return (
            "Search for academic papers and articles on Google Scholar. "
            "Useful for finding peer-reviewed research, citations, and scholarly articles. "
            "Input should be a search query string."
        )

    def create_tool(self) -> LangChainBaseTool:
        """Create Google Scholar search tool.

        Returns:
            GoogleScholarQueryRun: Configured Google Scholar tool.
        """
        import os
        # Get API key from instance or environment
        api_key = self._api_key or os.getenv("SERP_API_KEY")
        wrapper = GoogleScholarAPIWrapper(serp_api_key=api_key)
        return GoogleScholarQueryRun(
            api_wrapper=wrapper,
            name=self.name,
            description=self.description,
        )

    def validate_config(self) -> bool:
        """Check if SerpAPI key is available."""
        import os

        return bool(self._api_key or os.getenv("SERP_API_KEY"))

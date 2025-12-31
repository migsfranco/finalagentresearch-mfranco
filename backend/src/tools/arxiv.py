"""ArXiv search tool for preprints and open-access papers."""

from langchain.tools import BaseTool as LangChainBaseTool
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_community.utilities.arxiv import ArxivAPIWrapper

from .base import BaseTool


class ArxivSearchTool(BaseTool):
    """ArXiv search tool for preprints and open-access papers.

    No API key required - uses ArXiv's free public API.
    """

    def __init__(
        self,
        top_k_results: int = 5,
        doc_content_chars_max: int = 4000,
    ):
        """Initialize ArXiv search tool.

        Args:
            top_k_results: Maximum number of results to return.
            doc_content_chars_max: Maximum characters per document summary.
        """
        self._top_k_results = top_k_results
        self._doc_content_chars_max = doc_content_chars_max

    @property
    def name(self) -> str:
        return "arxiv"

    @property
    def description(self) -> str:
        return (
            "Search ArXiv for preprints and open-access papers in physics, mathematics, "
            "computer science, biology, finance, and more. "
            "Input can be a search query or an ArXiv paper ID (e.g., '2510.13422')."
        )

    def create_tool(self) -> LangChainBaseTool:
        """Create ArXiv search tool.

        Returns:
            ArxivQueryRun: Configured ArXiv search tool.
        """
        wrapper = ArxivAPIWrapper(
            top_k_results=self._top_k_results,
            doc_content_chars_max=self._doc_content_chars_max,
        )
        return ArxivQueryRun(
            api_wrapper=wrapper,
            name=self.name,
            description=self.description,
        )

    def validate_config(self) -> bool:
        """ArXiv doesn't require API key."""
        return True

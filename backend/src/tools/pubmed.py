"""PubMed search tool for biomedical literature."""

from langchain.tools import BaseTool as LangChainBaseTool
from langchain_community.tools.pubmed.tool import PubmedQueryRun
from langchain_community.utilities.pubmed import PubMedAPIWrapper

from .base import BaseTool


class PubMedSearchTool(BaseTool):
    """PubMed search tool for biomedical and life sciences literature.

    No API key required - uses NCBI's free public API.
    """

    def __init__(
        self,
        top_k_results: int = 10,
        doc_content_chars_max: int = 2000,
    ):
        """Initialize PubMed search tool.

        Args:
            top_k_results: Maximum number of results to return.
            doc_content_chars_max: Maximum characters per document summary.
        """
        self._top_k_results = top_k_results
        self._doc_content_chars_max = doc_content_chars_max

    @property
    def name(self) -> str:
        return "pubmed"

    @property
    def description(self) -> str:
        return (
            "Search PubMed for biomedical and life sciences literature. "
            "Useful for finding medical research papers, clinical studies, "
            "and health-related scientific articles. "
            "Input should be a search query string."
        )

    def create_tool(self) -> LangChainBaseTool:
        """Create PubMed search tool.

        Returns:
            PubmedQueryRun: Configured PubMed search tool.
        """
        wrapper = PubMedAPIWrapper(
            top_k_results=self._top_k_results,
            doc_content_chars_max=self._doc_content_chars_max,
        )
        return PubmedQueryRun(
            api_wrapper=wrapper,
            name=self.name,
            description=self.description,
        )

    def validate_config(self) -> bool:
        """PubMed doesn't require API key."""
        return True

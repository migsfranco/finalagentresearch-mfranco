"""APA citation corrector tool using RAG."""

from typing import TYPE_CHECKING

from langchain.tools import BaseTool as LangChainBaseTool, tool

from .base import BaseTool

if TYPE_CHECKING:
    from ..rag.chain import APARagChain


class APACorrectorTool(BaseTool):
    """APA citation corrector tool using RAG with APA 7th edition manual.

    This tool validates and corrects citations according to APA 7th edition guidelines.
    """

    def __init__(self, rag_chain: "APARagChain | None" = None):
        """Initialize APA corrector tool.

        Args:
            rag_chain: Pre-configured RAG chain. If None, will be lazy-loaded.
        """
        self._rag_chain = rag_chain

    @property
    def name(self) -> str:
        return "apa_citation_corrector"

    @property
    def description(self) -> str:
        return (
            "Correct APA citations according to APA 7th edition guidelines. "
            "Input should be a citation that needs to be validated and corrected. "
            "Returns the corrected citation with explanation of changes."
        )

    def _get_rag_chain(self) -> "APARagChain":
        """Lazy-load the RAG chain if not provided."""
        if self._rag_chain is None:
            from ..rag.chain import APARagChain

            self._rag_chain = APARagChain()
        return self._rag_chain

    def create_tool(self) -> LangChainBaseTool:
        """Create APA citation corrector tool.

        Returns:
            LangChainBaseTool: Configured APA corrector tool.
        """
        rag_chain = self._get_rag_chain()
        tool_description = self.description

        @tool
        def apa_citation_corrector(citation: str) -> str:
            """Correct APA citations according to APA 7th edition guidelines.
            Input should be a citation that needs to be validated and corrected.
            Returns the corrected citation with explanation of changes.

            Args:
                citation: The citation to correct.

            Returns:
                The corrected citation with explanation.
            """
            try:
                return rag_chain.invoke(citation)
            except Exception as e:
                return f"Error processing citation: {e}"

        return apa_citation_corrector

    def validate_config(self) -> bool:
        """Check if RAG chain can be initialized."""
        try:
            self._get_rag_chain()
            return True
        except Exception:
            return False

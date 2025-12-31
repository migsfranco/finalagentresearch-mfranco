"""Base tool interface following Open/Closed Principle."""

from abc import ABC, abstractmethod
from typing import Any

from langchain.tools import BaseTool as LangChainBaseTool


class BaseTool(ABC):
    """Abstract base class for all research tools.

    This follows the Open/Closed Principle - new tools can be added
    by extending this class without modifying existing code.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the tool name."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Return the tool description for the LLM."""
        ...

    @abstractmethod
    def create_tool(self) -> LangChainBaseTool:
        """Create and return the LangChain tool instance.

        Returns:
            LangChainBaseTool: The configured LangChain tool.
        """
        ...

    def validate_config(self) -> bool:
        """Validate that the tool is properly configured.

        Returns:
            bool: True if configuration is valid.
        """
        return True

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name='{self.name}')>"

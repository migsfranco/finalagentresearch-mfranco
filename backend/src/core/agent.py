"""Agent factory for creating research agents."""

from typing import Any

from langchain.tools import BaseTool as LangChainBaseTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from ..config import get_settings
from ..tools import (
    ArxivSearchTool,
    DuckDuckGoSearchTool,
    GoogleScholarTool,
    PubMedSearchTool,
    TavilySearchTool,
    APACorrectorTool,
)
from ..tools.base import BaseTool
from .memory import MemoryManager
from .prompts import RESEARCH_AGENT_PROMPT


class AgentFactory:
    """Factory for creating research agents.

    Follows Factory Pattern and Dependency Inversion Principle.
    """

    def __init__(
        self,
        model_name: str | None = None,
        temperature: float | None = None,
    ):
        """Initialize agent factory.

        Args:
            model_name: OpenAI model name. Defaults to settings.
            temperature: LLM temperature. Defaults to settings.
        """
        settings = get_settings()
        self._model_name = model_name or settings.openai_model
        self._temperature = temperature if temperature is not None else settings.openai_temperature
        self._memory_manager = MemoryManager()

    def _create_llm(self) -> ChatOpenAI:
        """Create the LLM instance.

        Returns:
            Configured ChatOpenAI instance.
        """
        return ChatOpenAI(
            model=self._model_name,
            temperature=self._temperature,
        )

    def _get_default_tools(self) -> list[BaseTool]:
        """Get the default set of research tools.

        Returns:
            List of tool wrapper instances.
        """
        settings = get_settings()
        tools: list[BaseTool] = []

        # Add tools based on available API keys
        if settings.serp_api_key:
            tools.append(GoogleScholarTool())

        if settings.tavily_api_key:
            tools.append(TavilySearchTool())

        # These don't require API keys
        tools.extend([
            PubMedSearchTool(),
            ArxivSearchTool(),
            DuckDuckGoSearchTool(),
        ])

        return tools

    def _create_langchain_tools(
        self,
        tool_wrappers: list[BaseTool],
    ) -> list[LangChainBaseTool]:
        """Convert tool wrappers to LangChain tools.

        Args:
            tool_wrappers: List of tool wrapper instances.

        Returns:
            List of LangChain tool instances.
        """
        return [wrapper.create_tool() for wrapper in tool_wrappers]

    def create_agent(
        self,
        tools: list[BaseTool] | None = None,
        include_apa_corrector: bool = True,
    ) -> Any:
        """Create a research agent with specified tools.

        Args:
            tools: List of tools to include. Defaults to all available.
            include_apa_corrector: Whether to include APA citation corrector.

        Returns:
            Configured LangGraph agent.
        """
        # Use default tools if none provided
        if tools is None:
            tools = self._get_default_tools()

        # Add APA corrector if requested
        if include_apa_corrector:
            tools.append(APACorrectorTool())

        # Convert to LangChain tools
        langchain_tools = self._create_langchain_tools(tools)

        # Create LLM
        llm = self._create_llm()

        # Create agent using LangGraph
        agent = create_react_agent(
            llm,
            langchain_tools,
            checkpointer=self._memory_manager.checkpointer,
            prompt=RESEARCH_AGENT_PROMPT,
        )

        return agent

    @property
    def memory_manager(self) -> MemoryManager:
        """Get the memory manager.

        Returns:
            MemoryManager instance.
        """
        return self._memory_manager

    def get_thread_config(self, thread_id: str) -> dict[str, Any]:
        """Get configuration for a conversation thread.

        Args:
            thread_id: Thread identifier.

        Returns:
            Configuration dict for the agent.
        """
        return self._memory_manager.get_config(thread_id)

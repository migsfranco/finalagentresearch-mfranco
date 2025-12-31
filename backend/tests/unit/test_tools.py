"""Unit tests for research tools."""

import pytest

from src.tools import (
    ArxivSearchTool,
    DuckDuckGoSearchTool,
    GoogleScholarTool,
    PubMedSearchTool,
    TavilySearchTool,
)


class TestArxivTool:
    """Tests for ArXiv search tool."""

    def test_name(self) -> None:
        """Test tool name."""
        tool = ArxivSearchTool()
        assert tool.name == "arxiv"

    def test_description_contains_arxiv(self) -> None:
        """Test description mentions ArXiv."""
        tool = ArxivSearchTool()
        assert "arxiv" in tool.description.lower()

    def test_validate_config_returns_true(self) -> None:
        """Test that ArXiv doesn't require API key."""
        tool = ArxivSearchTool()
        assert tool.validate_config() is True

    def test_create_tool_returns_langchain_tool(self) -> None:
        """Test tool creation."""
        tool = ArxivSearchTool()
        langchain_tool = tool.create_tool()
        assert langchain_tool is not None
        assert hasattr(langchain_tool, "run")


class TestPubMedTool:
    """Tests for PubMed search tool."""

    def test_name(self) -> None:
        """Test tool name."""
        tool = PubMedSearchTool()
        assert tool.name == "pubmed"

    def test_description_contains_biomedical(self) -> None:
        """Test description mentions biomedical."""
        tool = PubMedSearchTool()
        assert "biomedical" in tool.description.lower()

    def test_validate_config_returns_true(self) -> None:
        """Test that PubMed doesn't require API key."""
        tool = PubMedSearchTool()
        assert tool.validate_config() is True


class TestDuckDuckGoTool:
    """Tests for DuckDuckGo search tool."""

    def test_name(self) -> None:
        """Test tool name."""
        tool = DuckDuckGoSearchTool()
        assert tool.name == "duckduckgo"

    def test_validate_config_returns_true(self) -> None:
        """Test that DuckDuckGo doesn't require API key."""
        tool = DuckDuckGoSearchTool()
        assert tool.validate_config() is True


class TestGoogleScholarTool:
    """Tests for Google Scholar tool."""

    def test_name(self) -> None:
        """Test tool name."""
        tool = GoogleScholarTool()
        assert tool.name == "google_scholar"

    def test_description_contains_academic(self) -> None:
        """Test description mentions academic."""
        tool = GoogleScholarTool()
        assert "academic" in tool.description.lower()

    def test_validate_config_without_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test validation fails without API key."""
        monkeypatch.delenv("SERP_API_KEY", raising=False)
        tool = GoogleScholarTool()
        assert tool.validate_config() is False

    def test_validate_config_with_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test validation passes with API key."""
        monkeypatch.setenv("SERP_API_KEY", "test-key")
        tool = GoogleScholarTool()
        assert tool.validate_config() is True


class TestTavilyTool:
    """Tests for Tavily search tool."""

    def test_name(self) -> None:
        """Test tool name."""
        tool = TavilySearchTool()
        assert tool.name == "tavily_search"

    def test_validate_config_without_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test validation fails without API key."""
        monkeypatch.delenv("TAVILY_API_KEY", raising=False)
        tool = TavilySearchTool()
        assert tool.validate_config() is False

    def test_validate_config_with_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test validation passes with API key."""
        monkeypatch.setenv("TAVILY_API_KEY", "test-key")
        tool = TavilySearchTool()
        assert tool.validate_config() is True

    def test_custom_max_results(self) -> None:
        """Test custom max_results parameter."""
        tool = TavilySearchTool(max_results=10)
        assert tool._max_results == 10

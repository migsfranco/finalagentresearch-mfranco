"""Pytest fixtures for tests."""

import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient

# Set test environment variables before importing app
os.environ["OPENAI_API_KEY"] = "test-key"
os.environ["ENVIRONMENT"] = "testing"


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Specify the async backend for pytest-asyncio."""
    return "asyncio"


@pytest.fixture
def test_client() -> Generator[TestClient, None, None]:
    """Create a test client for the FastAPI app.

    Yields:
        TestClient instance.
    """
    from src.main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture
def mock_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Set up mock environment variables.

    Args:
        monkeypatch: Pytest monkeypatch fixture.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("TAVILY_API_KEY", "test-tavily-key")
    monkeypatch.setenv("SERP_API_KEY", "test-serp-key")
    monkeypatch.setenv("ENVIRONMENT", "testing")


@pytest.fixture
def sample_citation() -> str:
    """Provide a sample citation for testing.

    Returns:
        Sample APA citation.
    """
    return "(Gomez et al, 2023, pag. 23)"


@pytest.fixture
def sample_thread_id() -> str:
    """Provide a sample thread ID.

    Returns:
        Sample thread ID.
    """
    return "test-thread-123"

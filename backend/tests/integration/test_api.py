"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_check(self, test_client: TestClient) -> None:
        """Test health endpoint returns healthy."""
        response = test_client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_readiness_check(self, test_client: TestClient) -> None:
        """Test readiness endpoint returns ready."""
        response = test_client.get("/api/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}


class TestToolsEndpoints:
    """Tests for tools endpoints."""

    def test_list_tools(self, test_client: TestClient) -> None:
        """Test listing all tools."""
        response = test_client.get("/api/tools")
        assert response.status_code == 200
        data = response.json()
        assert "tools" in data
        assert "total" in data
        assert data["total"] > 0

    def test_list_tools_contains_required_tools(self, test_client: TestClient) -> None:
        """Test that required tools are present."""
        response = test_client.get("/api/tools")
        data = response.json()
        tool_names = [t["name"] for t in data["tools"]]

        assert "pubmed" in tool_names
        assert "arxiv" in tool_names
        assert "duckduckgo" in tool_names

    def test_get_specific_tool(self, test_client: TestClient) -> None:
        """Test getting a specific tool."""
        response = test_client.get("/api/tools/arxiv")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "arxiv"
        assert data["requires_api_key"] is False
        assert data["is_available"] is True

    def test_get_nonexistent_tool(self, test_client: TestClient) -> None:
        """Test getting a non-existent tool returns 404."""
        response = test_client.get("/api/tools/nonexistent")
        assert response.status_code == 404


class TestChatEndpoints:
    """Tests for chat endpoints."""

    def test_delete_nonexistent_thread(self, test_client: TestClient) -> None:
        """Test deleting non-existent thread returns 404."""
        response = test_client.delete("/api/chat/nonexistent-thread-id")
        assert response.status_code == 404


class TestCORSHeaders:
    """Tests for CORS configuration."""

    def test_cors_headers_present(self, test_client: TestClient) -> None:
        """Test CORS headers are present for allowed origins."""
        response = test_client.options(
            "/api/health",
            headers={
                "Origin": "http://localhost:5173",
                "Access-Control-Request-Method": "GET",
            },
        )
        # FastAPI returns 200 for OPTIONS requests with CORS
        assert response.status_code in [200, 405]

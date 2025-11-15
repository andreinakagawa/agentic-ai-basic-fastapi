"""Smoke tests for system endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_root_endpoint(client: AsyncClient):
    """Test root endpoint returns API information."""
    response = await client.get("/")

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "Agentic AI FastAPI"
    assert data["version"] == "1.0.0"
    assert data["status"] == "running"
    assert data["environment"] == "local"


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    """Test health check endpoint."""
    response = await client.get("/health")

    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert data["environment"] == "local"

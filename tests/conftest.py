"""Pytest configuration and shared fixtures."""

import pytest
from httpx import ASGITransport, AsyncClient

from src.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Create an async test client.

    This fixture provides an async HTTP client for testing the FastAPI app.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

"""Tests for hello_agent."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "input_data,expected_message",
    [
        ({}, "hello agentic world!"),
        ({"name": "Alice"}, "hello Alice!"),
        ({"name": "Bob"}, "hello Bob!"),
    ],
)
async def test_hello_agent_greet(
    client: AsyncClient, input_data: dict, expected_message: str
):
    """Test hello agent greeting with various inputs."""
    response = await client.post("/hello/greet", json=input_data)

    assert response.status_code == 200
    data = response.json()

    assert data["message"] == expected_message
    assert data["agent_name"] == "hello_agent"
    assert "request_id" in data
    assert "execution_time" in data
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_hello_agent_metadata(client: AsyncClient):
    """Test getting hello agent metadata."""
    response = await client.get("/hello/metadata")

    assert response.status_code == 200
    data = response.json()

    assert data["name"] == "hello_agent"
    assert data["description"]
    assert data["version"] == "1.0.0"
    assert "capabilities" in data
    assert "greeting" in data["capabilities"]


@pytest.mark.asyncio
async def test_list_agents(client: AsyncClient):
    """Test listing all agents includes hello_agent."""
    response = await client.get("/agents")

    assert response.status_code == 200
    data = response.json()

    assert "count" in data
    assert "agents" in data
    assert data["count"] > 0

    # Verify hello_agent is in the list
    agent_names = [agent["name"] for agent in data["agents"]]
    assert "hello_agent" in agent_names

    # Verify hello_agent metadata is complete
    hello_agent = next(a for a in data["agents"] if a["name"] == "hello_agent")
    assert hello_agent["description"]
    assert hello_agent["version"] == "1.0.0"
    assert "greeting" in hello_agent["capabilities"]

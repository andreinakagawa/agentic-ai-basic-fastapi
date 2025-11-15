"""FastAPI router for hello_agent.

Defines the HTTP endpoints for the hello agent.
"""

from fastapi import APIRouter, status

from src.agents.hello_agent.agent import HelloAgent
from src.agents.hello_agent.schemas import HelloInput, HelloOutput

# Create router with prefix and tags
router = APIRouter(
    prefix="/hello",
    tags=["Hello Agent"],
)

# Instantiate agent
agent = HelloAgent()


@router.post(
    "/greet",
    response_model=HelloOutput,
    status_code=status.HTTP_200_OK,
    summary="Greet the world",
    description="Returns a simple greeting message. This is a mock agent for demonstration.",
)
async def greet(input_data: HelloInput) -> HelloOutput:
    """Execute the hello agent to get a greeting.

    Args:
        input_data: HelloInput with optional name

    Returns:
        HelloOutput with greeting message
    """
    return await agent.execute(input_data)


@router.get(
    "/metadata",
    summary="Get agent metadata",
    description="Returns metadata about the hello agent",
)
async def get_metadata():
    """Get hello agent metadata."""
    return agent.metadata.model_dump()

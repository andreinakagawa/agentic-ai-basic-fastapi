"""Pydantic schemas for hello_agent.

Defines the input and output contracts for the hello agent.
"""

from pydantic import Field

from src.agents.base import BaseAgentInput, BaseAgentOutput


class HelloInput(BaseAgentInput):
    """Input schema for hello agent.

    Simple agent that doesn't need any specific input fields beyond the base.
    All required data comes from BaseAgentInput.
    """

    name: str | None = Field(
        default=None,
        description="Optional name to greet (if not provided, uses 'agentic world')",
    )


class HelloOutput(BaseAgentOutput):
    """Output schema for hello agent."""

    message: str = Field(..., description="The greeting message")

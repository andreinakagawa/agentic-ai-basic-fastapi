"""Base agent abstraction and contracts.

This module defines the minimal interface that all agents must implement,
along with base Pydantic schemas for input/output validation.
"""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class AgentMetadata(BaseModel):
    """Metadata about an agent."""

    name: str = Field(..., description="Agent name")
    description: str = Field(..., description="What this agent does")
    version: str = Field(default="1.0.0", description="Agent version")
    capabilities: list[str] = Field(
        default_factory=list,
        description="List of capabilities this agent has",
    )


class BaseAgentInput(BaseModel):
    """Base input schema for all agents.

    All agent-specific input schemas should inherit from this.
    """

    request_id: UUID = Field(
        default_factory=uuid4,
        description="Unique request identifier",
    )
    user_id: str | None = Field(
        default=None,
        description="User identifier (for auth/tracking)",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata for this request",
    )
    config_override: dict[str, Any] | None = Field(
        default=None,
        description="Runtime configuration overrides",
    )


class BaseAgentOutput(BaseModel):
    """Base output schema for all agents.

    All agent-specific output schemas should inherit from this.

    Note: Success/failure is indicated by HTTP status codes:
    - 200: Success
    - 4xx: Client error (invalid input, etc.)
    - 5xx: Server/agent error (LLM failure, etc.)
    """

    request_id: UUID = Field(..., description="Request identifier from input")
    agent_name: str = Field(..., description="Name of the agent that processed this")
    execution_time: float = Field(..., description="Execution time in seconds")
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="When this response was generated",
    )


class StreamChunk(BaseModel):
    """A chunk of streamed data from an agent.

    For agents that support streaming execution.
    """

    request_id: UUID = Field(..., description="Request identifier")
    chunk_type: str = Field(..., description="Type of chunk (text, tool_call, etc)")
    content: Any = Field(..., description="Chunk content")
    is_final: bool = Field(default=False, description="Whether this is the final chunk")


class BaseAgent(ABC):
    """Base class for all agents.

    All agents must:
    1. Inherit from this class
    2. Implement the execute() method
    3. Provide metadata via the metadata property

    Agents optionally can:
    - Implement stream_execute() for streaming support
    - Override validate_config() for custom validation
    """

    @property
    @abstractmethod
    def metadata(self) -> AgentMetadata:
        """Return agent metadata.

        This should be a property that returns an AgentMetadata instance
        describing the agent's name, description, version, and capabilities.
        """
        pass

    @abstractmethod
    async def execute(self, input_data: BaseAgentInput) -> BaseAgentOutput:
        """Execute the agent with the given input.

        Args:
            input_data: Validated input data conforming to self.input_schema

        Returns:
            Output data conforming to self.output_schema

        Raises:
            Exception: If execution fails
        """
        pass

    async def stream_execute(
        self, input_data: BaseAgentInput
    ) -> AsyncIterator[StreamChunk]:
        """Execute the agent with streaming output.

        This is optional. Agents that support streaming should implement this method.

        Args:
            input_data: Validated input data conforming to self.input_schema

        Yields:
            StreamChunk: Chunks of output data

        Raises:
            NotImplementedError: If streaming is not supported by this agent
        """
        raise NotImplementedError(
            f"{self.metadata.name} does not support streaming execution"
        )

    def validate_config(self) -> bool:
        """Validate agent configuration.

        Override this method to perform custom configuration validation
        at agent initialization time.

        Returns:
            bool: True if configuration is valid

        Raises:
            ConfigurationError: If configuration is invalid
        """
        return True

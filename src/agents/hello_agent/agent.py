"""Hello Agent implementation.

A simple mock agent that returns a greeting message.
Demonstrates the minimal agent implementation.
"""

import time

from fastapi import HTTPException, status

from src.agents.base import AgentMetadata, BaseAgent
from src.agents.hello_agent.schemas import HelloInput, HelloOutput


class HelloAgent(BaseAgent):
    """A simple greeting agent.

    This agent demonstrates the minimal implementation of BaseAgent.
    It doesn't use any LLM or external service - just returns a greeting.
    """

    @property
    def metadata(self) -> AgentMetadata:
        """Return agent metadata."""
        return AgentMetadata(
            name="hello_agent",
            description="A simple greeting agent that returns 'hello agentic world!'",
            version="1.0.0",
            capabilities=["greeting", "mock"],
        )

    async def execute(self, input_data: HelloInput) -> HelloOutput:
        """Execute the hello agent.

        Args:
            input_data: Validated HelloInput

        Returns:
            HelloOutput with greeting message

        Raises:
            HTTPException: If execution fails
        """
        start_time = time.time()

        try:
            # Determine who to greet
            greeting_target = input_data.name if input_data.name else "agentic world"

            # Generate the message
            message = f"hello {greeting_target}!"

            # Calculate execution time
            execution_time = time.time() - start_time

            # Return output
            return HelloOutput(
                request_id=input_data.request_id,
                agent_name=self.metadata.name,
                execution_time=execution_time,
                message=message,
            )

        except Exception as e:
            # Raise HTTP exception for errors
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Agent execution failed: {str(e)}",
            ) from e

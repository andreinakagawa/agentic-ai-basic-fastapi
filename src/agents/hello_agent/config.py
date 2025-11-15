"""Configuration for hello_agent.

This agent doesn't require any special configuration,
but this file is here to demonstrate the pattern.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class HelloAgentConfig(BaseSettings):
    """Configuration for hello agent."""

    model_config = SettingsConfigDict(
        env_prefix="HELLO_AGENT_",  # Environment variables like HELLO_AGENT_DEFAULT_NAME
        env_file=".env",
        case_sensitive=True,
    )

    # Example configuration
    DEFAULT_NAME: str = "agentic world"
    ENABLE_LOGGING: bool = True


# Agent config instance
hello_config = HelloAgentConfig()

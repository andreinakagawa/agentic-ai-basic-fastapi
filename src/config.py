"""Global application configuration."""

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    """Global application configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Environment
    ENVIRONMENT: str = "local"

    # Database
    DATABASE_URL: PostgresDsn

    # API Configuration
    API_TITLE: str = "Agentic AI FastAPI"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "A minimal, plugin-based agentic AI system"

    # Security
    SECRET_KEY: str
    API_KEY: str | None = None

    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Logging
    LOG_LEVEL: str = "INFO"

    # Optional: LLM Provider API Keys (agents can access these if needed)
    OPENAI_API_KEY: str | None = None
    ANTHROPIC_API_KEY: str | None = None


# Global settings instance
settings = Config()

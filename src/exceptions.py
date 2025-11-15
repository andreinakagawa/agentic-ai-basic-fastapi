"""Global exception classes."""

from fastapi import HTTPException, status


class AgenticAIException(Exception):
    """Base exception for all custom exceptions."""

    def __init__(
        self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    ):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ConfigurationError(AgenticAIException):
    """Raised when there's a configuration error."""

    def __init__(self, message: str = "Configuration error"):
        super().__init__(message, status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthenticationError(AgenticAIException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED)


class AuthorizationError(AgenticAIException):
    """Raised when authorization fails."""

    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, status.HTTP_403_FORBIDDEN)


class NotFoundError(AgenticAIException):
    """Raised when a resource is not found."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status.HTTP_404_NOT_FOUND)


class ValidationError(AgenticAIException):
    """Raised when validation fails."""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY)


def agentic_exception_handler(exc: AgenticAIException) -> HTTPException:
    """Convert custom exceptions to HTTPException for FastAPI."""
    return HTTPException(
        status_code=exc.status_code,
        detail=exc.message,
    )

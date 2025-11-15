"""Global dependencies for FastAPI routes."""

from fastapi import Header, HTTPException, status

from src.config import settings


async def verify_api_key(x_api_key: str = Header(None)) -> str:
    """
    Verify API key from request header.

    This is a simple example. In production, you might want to:
    - Store API keys in database
    - Use JWT tokens
    - Implement rate limiting per key

    Usage:
        @router.get("/endpoint", dependencies=[Depends(verify_api_key)])
        async def protected_endpoint():
            ...
    """
    if not settings.API_KEY:
        # If no API key is configured, skip validation
        return "no-key-configured"

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required",
        )

    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return x_api_key


# Add more global dependencies here as needed
# Examples:
# - async def get_current_user()
# - async def rate_limit()
# - async def validate_tenant()

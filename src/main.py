"""FastAPI application initialization.

This is the entry point for the Agentic AI FastAPI application.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.agents import discover_agents, get_agent_metadata
from src.config import settings
from src.database import engine
from src.exceptions import AgenticAIException

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting Agentic AI FastAPI application...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")

    # Test database connection
    try:
        async with engine.begin():
            logger.info("Database connection successful")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")

    yield

    # Shutdown
    logger.info("Shutting down Agentic AI FastAPI application...")
    await engine.dispose()


# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler for custom exceptions
@app.exception_handler(AgenticAIException)
async def custom_exception_handler(request, exc: AgenticAIException):
    """Handle custom AgenticAI exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message, "type": exc.__class__.__name__},
    )


# Root endpoint
@app.get(
    "/",
    tags=["System"],
    summary="Root endpoint",
    description="Returns basic API information",
)
async def root():
    """Root endpoint."""
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
    }


# Health check endpoint
@app.get(
    "/health",
    tags=["System"],
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the API is healthy",
)
async def health():
    """Health check endpoint."""
    # Could add more health checks here (database, redis, etc.)
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
    }


# Agent discovery endpoint
@app.get(
    "/agents",
    tags=["System"],
    summary="List available agents",
    description="Returns metadata for all discovered agents",
)
async def list_agents():
    """List all available agents and their metadata."""
    agents_metadata = get_agent_metadata()
    return {
        "count": len(agents_metadata),
        "agents": agents_metadata,
    }


# Auto-discover and register all agent routers
logger.info("Discovering agents...")
agent_routers = discover_agents()
for router in agent_routers:
    app.include_router(router)
    logger.info(f"Registered router: {router.prefix}")

logger.info(f"Application initialized with {len(agent_routers)} agent(s)")

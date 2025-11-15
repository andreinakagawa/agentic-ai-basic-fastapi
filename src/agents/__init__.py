"""Agent auto-discovery and registration.

This module automatically discovers all agents in the agents/ directory
and makes their routers available for registration with the FastAPI app.
"""

import importlib
import logging
from pathlib import Path

from fastapi import APIRouter

logger = logging.getLogger(__name__)


def discover_agents() -> list[APIRouter]:
    """Discover and load all agent routers.

    This function:
    1. Scans the agents/ directory for subdirectories
    2. Tries to import router.py from each subdirectory
    3. Collects all routers and returns them

    Returns:
        list[APIRouter]: List of agent routers to be included in the main app

    Example:
        # In main.py
        from src.agents import discover_agents

        app = FastAPI()
        for router in discover_agents():
            app.include_router(router)
    """
    routers = []
    agents_dir = Path(__file__).parent

    # Iterate through all subdirectories in agents/
    for agent_path in agents_dir.iterdir():
        # Skip special files and the base module
        if not agent_path.is_dir() or agent_path.name.startswith("_"):
            continue

        agent_name = agent_path.name

        try:
            # Try to import the router module from this agent
            router_module = importlib.import_module(f"src.agents.{agent_name}.router")

            # Check if the module has a 'router' attribute
            if hasattr(router_module, "router"):
                router = router_module.router
                routers.append(router)
                logger.info(f"Discovered agent: {agent_name}")
            else:
                logger.warning(
                    f"Agent '{agent_name}' has no 'router' attribute in router.py"
                )

        except ImportError as e:
            logger.warning(f"Could not import router for agent '{agent_name}': {e}")
        except Exception as e:
            logger.error(f"Error loading agent '{agent_name}': {e}")

    logger.info(f"Discovered {len(routers)} agent(s)")
    return routers


def get_agent_metadata() -> list[dict]:
    """Get metadata for all discovered agents.

    This can be used to build an agent registry or discovery endpoint.

    Returns:
        list[dict]: List of agent metadata dictionaries
    """
    metadata_list = []
    agents_dir = Path(__file__).parent

    for agent_path in agents_dir.iterdir():
        if not agent_path.is_dir() or agent_path.name.startswith("_"):
            continue

        agent_name = agent_path.name

        try:
            # Try to import the router module to get the agent instance
            router_module = importlib.import_module(f"src.agents.{agent_name}.router")

            # Look for an agent instance in the router module
            if hasattr(router_module, "agent"):
                agent_instance = router_module.agent
                if hasattr(agent_instance, "metadata"):
                    metadata = agent_instance.metadata
                    if hasattr(metadata, "model_dump"):
                        metadata_list.append(metadata.model_dump())
                    elif isinstance(metadata, dict):
                        metadata_list.append(metadata)

        except Exception as e:
            logger.debug(f"Could not extract metadata from agent '{agent_name}': {e}")

    return metadata_list

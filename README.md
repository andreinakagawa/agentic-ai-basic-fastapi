# Agentic AI FastAPI Template

A minimal, plugin-based template for building agentic AI systems with FastAPI. This template provides the structure and foundational patterns while giving you complete freedom to choose your own LLM providers, agent frameworks, and implementation approaches.

## Features

- **Plugin Architecture** - Agents auto-discover and register themselves
- **Contract-Based** - Pydantic schemas ensure type safety and validation
- **Database-First** - Built-in SQLAlchemy + Alembic for persistence
- **Developer Freedom** - Use any LLM provider, framework (LangChain, LangGraph, Agno, etc.), or pattern
- **FastAPI Native** - Async-first, auto-generated docs, built-in validation
- **Minimal & Extensible** - Start simple, add complexity only when needed

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL
- [uv](https://github.com/astral-sh/uv) - Fast Python package manager

### 1. Install uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd agentic-ai-basic-fastapi

# uv automatically creates and manages virtual environment
# Install dependencies
uv sync
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
# - Set DATABASE_URL to your PostgreSQL connection string
# - Set SECRET_KEY to a secure random string
# - Add any LLM API keys your agents will use
```

### 4. Setup Database

```bash
# Create database (if needed)
createdb agentic_ai

# Run migrations with uv
uv run alembic upgrade head
```

### 5. Run the Application

```bash
# Development mode with auto-reload
uv run uvicorn src.main:app --reload

# Production mode
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### 5. Test the API

```bash
# Open interactive docs
open http://localhost:8000/docs

# Test the hello agent
curl -X POST http://localhost:8000/hello/greet \
  -H "Content-Type: application/json" \
  -d '{"name": "world"}'

# List available agents
curl http://localhost:8000/agents
```

## Project Structure

```
agentic-ai-basic-fastapi/
├── src/
│   ├── agents/              # Agent plugins
│   │   ├── base.py         # Base agent abstraction
│   │   ├── __init__.py     # Auto-discovery logic
│   │   └── hello_agent/    # Example agent
│   ├── config.py           # Global configuration
│   ├── database.py         # Database setup
│   ├── exceptions.py       # Global exceptions
│   ├── dependencies.py     # Global dependencies
│   └── main.py            # FastAPI app
├── tests/                  # Test suite
├── alembic/               # Database migrations
├── docs/                  # Documentation
└── .env                   # Environment configuration
```

## Creating Your First Agent

### 1. Create Agent Structure

```bash
mkdir -p src/agents/my_agent
cd src/agents/my_agent
touch __init__.py schemas.py agent.py router.py config.py
```

### 2. Define Input/Output Schemas

```python
# schemas.py
from pydantic import Field
from src.agents.base import BaseAgentInput, BaseAgentOutput

class MyAgentInput(BaseAgentInput):
    query: str = Field(..., description="User query")

class MyAgentOutput(BaseAgentOutput):
    answer: str = Field(..., description="Agent's answer")
```

### 3. Implement the Agent

```python
# agent.py
from src.agents.base import BaseAgent, AgentMetadata
from .schemas import MyAgentInput, MyAgentOutput

class MyAgent(BaseAgent):
    input_schema = MyAgentInput
    output_schema = MyAgentOutput

    @property
    def metadata(self) -> AgentMetadata:
        return AgentMetadata(
            name="my_agent",
            description="My custom agent",
            version="1.0.0",
        )

    async def execute(self, input_data: MyAgentInput) -> MyAgentOutput:
        # Your agent logic here
        # Use any LLM provider, framework, or approach you want!
        answer = f"Processed: {input_data.query}"

        return MyAgentOutput(
            request_id=input_data.request_id,
            agent_name=self.metadata.name,
            execution_time=0.1,
            success=True,
            answer=answer,
        )

my_agent = MyAgent()
```

### 4. Create Router

```python
# router.py
from fastapi import APIRouter
from .agent import my_agent
from .schemas import MyAgentInput, MyAgentOutput

router = APIRouter(prefix="/my-agent", tags=["My Agent"])

@router.post("/execute", response_model=MyAgentOutput)
async def execute(input_data: MyAgentInput) -> MyAgentOutput:
    return await my_agent.execute(input_data)
```

### 5. Restart and Test

The agent will auto-discover on restart. No manual registration needed!

```bash
# Restart the app
# Your new agent is now available at /my-agent/execute
```

## Using LLM Providers and Frameworks

This template doesn't impose any framework choices. You're free to use:

### Native SDKs
```python
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

# Use directly in your agent.py
client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
```

### Agent Frameworks
```python
# LangChain
from langchain.agents import AgentExecutor

# LangGraph
from langgraph.graph import StateGraph

# Agno
import agno

# Use any framework within your agent implementation
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test
uv run pytest tests/agents/hello_agent/test_hello_agent.py
```

## Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "description"

# Apply migrations
uv run alembic upgrade head

# Rollback one migration
uv run alembic downgrade -1
```

## Documentation

- [Architecture](docs/architecture.md) - Detailed system architecture and design decisions
- [API Docs](http://localhost:8000/docs) - Interactive API documentation (when running)

## Development

```bash
# Format code with ruff
uv run ruff format src

# Lint code
uv run ruff check src

# Fix linting issues
uv run ruff check --fix src

# Add a new dependency
uv add <package-name>

# Add a dev dependency
uv add --dev <package-name>
```

## Architecture Highlights

- **No LLM Abstractions** - Template provides structure, not implementation constraints
- **Heterogeneous by Design** - Each agent can use different tools and frameworks
- **Contract-Based Integration** - Agents communicate through Pydantic schemas
- **Auto-Discovery** - Agents register automatically via filesystem scanning
- **Database-First** - Built-in persistence for agent state and results

## License

MIT

## Contributing

Contributions welcome! Please read the contributing guidelines first.

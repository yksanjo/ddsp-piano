# Getting Started

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd agentic-automation-platform

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

## Quick Start

### 1. Create an Agent

```python
from agentic_automation import Agent, Orchestrator
from agentic_automation.core.models import AgentDefinition, LLMBackend
from agentic_automation.llm.openai_backend import OpenAIBackend

# Create agent definition
definition = AgentDefinition(
    id="assistant",
    name="Assistant",
    description="Helpful assistant",
    llm_backend=LLMBackend.OPENAI,
    model="gpt-4",
    system_prompt="You are a helpful assistant.",
)

# Create LLM backend
llm = OpenAIBackend(api_key="your-api-key")

# Create agent
agent = Agent(definition=definition, llm_backend=llm)

# Execute agent
result = await agent.execute("What is the capital of France?")
print(result["result"])
```

### 2. Create a Workflow

Create a workflow YAML file:

```yaml
id: my_workflow
name: My Workflow
version: 1.0.0

tasks:
  - id: task1
    name: Process Request
    type: agent
    agent_id: assistant
    inputs:
      task: "Process: $input.request"

dependencies: {}
```

Run the workflow:

```bash
agentic run workflow.yaml --inputs '{"request": "Hello"}'
```

### 3. Start the API Server

```bash
agentic serve --port 8000
```

Access the web UI at `http://localhost:8000`

## Next Steps

- Read the [Architecture Guide](ARCHITECTURE.md)
- Check out [Examples](../examples/)
- See the [API Documentation](API.md)


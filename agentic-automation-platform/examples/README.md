# Examples

This directory contains example configurations and workflows for the Agentic AI Automation Platform.

## Agent Definitions

- `agent_definition.yaml` - Example agent definition in YAML format

## Workflows

- `simple_workflow.yaml` - Basic single-agent workflow
- `multi_agent_workflow.yaml` - Multi-agent workflow with dependencies

## Usage

### Running a Workflow

```bash
# Run a simple workflow
agentic run examples/simple_workflow.yaml --inputs '{"request": "Hello"}'

# Run a multi-agent workflow
agentic run examples/multi_agent_workflow.yaml --inputs '{"topic": "AI trends 2026"}'
```

### Loading an Agent Definition

```python
from agentic_automation.core.agent_parser import AgentParser
from agentic_automation.llm.openai_backend import OpenAIBackend
from agentic_automation.core.agent import Agent

# Parse agent definition
with open("examples/agent_definition.yaml") as f:
    definition = AgentParser.parse_yaml(f.read())

# Create agent
llm = OpenAIBackend(api_key="your-key")
agent = Agent(definition=definition, llm_backend=llm)

# Use agent
result = await agent.execute("What is machine learning?")
```


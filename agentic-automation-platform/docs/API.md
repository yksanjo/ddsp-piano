# API Documentation

## REST API

### Base URL

```
http://localhost:8000/api/v1
```

### Endpoints

#### Health Check

```http
GET /health
```

Returns the health status of the platform.

#### Execute Agent

```http
POST /api/v1/agents/execute
Content-Type: application/json

{
  "agent_id": "assistant",
  "task": "What is the capital of France?",
  "context": {}
}
```

#### Execute Workflow

```http
POST /api/v1/workflows/execute
Content-Type: application/json

{
  "workflow_id": "my_workflow",
  "inputs": {
    "request": "Hello"
  }
}
```

#### Get Metrics

```http
GET /api/v1/metrics
```

Returns platform metrics.

## Python SDK

### Agent

```python
from agentic_automation import Agent

agent = Agent(definition=agent_definition, llm_backend=llm_backend)
result = await agent.execute("task description")
```

### Workflow

```python
from agentic_automation import Workflow

workflow = Workflow(definition=workflow_definition, orchestrator=orchestrator)
result = await workflow.execute(inputs={"key": "value"})
```

### Orchestrator

```python
from agentic_automation import Orchestrator

orchestrator = Orchestrator(agent_pool, state_store, event_bus)
result = await orchestrator.execute_agent("agent_id", "task")
```


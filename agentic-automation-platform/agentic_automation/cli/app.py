"""Main CLI application."""

import asyncio
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from agentic_automation.core.agent_pool import AgentPool
from agentic_automation.core.event_bus import InMemoryEventBus
from agentic_automation.core.state_store import RedisStateStore
from agentic_automation.core.workflow import Workflow
from agentic_automation.orchestrator import Orchestrator
from agentic_automation.workflow_builder.parser import WorkflowParser

app = typer.Typer(help="Agentic AI Automation Platform CLI")
console = Console()

# Global state
orchestrator: Optional[Orchestrator] = None


@app.command()
def serve(
    host: str = typer.Option("0.0.0.0", help="Host to bind to"),
    port: int = typer.Option(8000, help="Port to bind to"),
):
    """Start the API server."""
    import uvicorn

    console.print(f"[green]Starting server on {host}:{port}[/green]")
    uvicorn.run("agentic_automation.api.server:app", host=host, port=port)


@app.command()
def run(
    workflow_file: Path = typer.Argument(..., help="Workflow YAML file"),
    inputs: Optional[str] = typer.Option(None, help="Input JSON string"),
):
    """Run a workflow from a YAML file."""
    console.print(f"[green]Loading workflow from {workflow_file}[/green]")

    # Parse workflow
    with open(workflow_file, "r") as f:
        workflow_def = WorkflowParser.parse_yaml(f.read())

    # Initialize orchestrator (simplified - would need proper setup)
    agent_pool = AgentPool()
    state_store = RedisStateStore(None)  # Would need Redis client
    event_bus = InMemoryEventBus()
    orch = Orchestrator(agent_pool, state_store, event_bus)

    # Create workflow
    workflow = Workflow(workflow_def, orch)

    # Parse inputs
    import json

    workflow_inputs = json.loads(inputs) if inputs else {}

    # Execute
    console.print("[green]Executing workflow...[/green]")
    result = asyncio.run(workflow.execute(workflow_inputs))

    if result.state.value == "completed":
        console.print(f"[green]Workflow completed: {result.result}[/green]")
    else:
        console.print(f"[red]Workflow failed: {result.error}[/red]")


@app.command()
def list_agents():
    """List all registered agents."""
    # This would connect to the actual system
    console.print("[yellow]Agent listing not yet implemented[/yellow]")


@app.command()
def create_agent(
    name: str = typer.Option(..., help="Agent name"),
    system_prompt: str = typer.Option(..., help="System prompt"),
    model: str = typer.Option("gpt-4", help="LLM model"),
):
    """Create a new agent."""
    console.print(f"[green]Creating agent: {name}[/green]")
    console.print("[yellow]Agent creation not yet fully implemented[/yellow]")


if __name__ == "__main__":
    app()


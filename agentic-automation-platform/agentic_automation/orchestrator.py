"""Orchestration engine for multi-agent systems."""

import asyncio
import uuid
from typing import Any, Dict, List, Optional

from agentic_automation.core.agent_pool import AgentPool
from agentic_automation.core.event_bus import Event, EventBus
from agentic_automation.core.models import ExecutionState, ExecutionResult
from agentic_automation.core.state_store import StateStore


class Orchestrator:
    """Orchestrates multi-agent systems."""

    def __init__(
        self,
        agent_pool: AgentPool,
        state_store: StateStore,
        event_bus: EventBus,
    ):
        """Initialize the orchestrator.

        Args:
            agent_pool: Pool of available agents
            state_store: State storage backend
            event_bus: Event bus for communication
        """
        self.agent_pool = agent_pool
        self.state_store = state_store
        self.event_bus = event_bus
        self._active_executions: Dict[str, Any] = {}

    async def execute_agent(
        self,
        agent_id: str,
        task: str,
        context: Optional[Dict[str, Any]] = None,
        execution_id: Optional[str] = None,
    ) -> ExecutionResult:
        """Execute a single agent.

        Args:
            agent_id: Agent identifier
            task: Task description
            context: Additional context
            execution_id: Optional execution ID

        Returns:
            Execution result
        """
        execution_id = execution_id or str(uuid.uuid4())
        context = context or {}

        # Get agent
        agent = self.agent_pool.get_agent(agent_id)
        if not agent:
            return ExecutionResult(
                execution_id=execution_id,
                state=ExecutionState.FAILED,
                error=f"Agent {agent_id} not found",
            )

        # Store execution state
        await self.state_store.set(
            f"execution:{execution_id}",
            {
                "state": ExecutionState.RUNNING.value,
                "agent_id": agent_id,
                "task": task,
            },
        )

        # Publish start event
        await self.event_bus.publish(
            Event(
                event_type="execution.started",
                source="orchestrator",
                payload={
                    "execution_id": execution_id,
                    "agent_id": agent_id,
                    "task": task,
                },
                timestamp=asyncio.get_event_loop().time(),
                correlation_id=execution_id,
            )
        )

        try:
            # Execute agent
            result = await agent.execute(task, context)

            # Store result
            await self.state_store.set(
                f"execution:{execution_id}:result",
                result,
            )

            # Publish completion event
            await self.event_bus.publish(
                Event(
                    event_type="execution.completed",
                    source="orchestrator",
                    payload={
                        "execution_id": execution_id,
                        "result": result,
                    },
                    timestamp=asyncio.get_event_loop().time(),
                    correlation_id=execution_id,
                )
            )

            return ExecutionResult(
                execution_id=execution_id,
                state=result["state"],
                result=result.get("result"),
                error=result.get("error"),
                metrics=result.get("metrics", {}),
            )

        except Exception as e:
            # Store error
            await self.state_store.set(
                f"execution:{execution_id}:error",
                str(e),
            )

            # Publish error event
            await self.event_bus.publish(
                Event(
                    event_type="execution.failed",
                    source="orchestrator",
                    payload={
                        "execution_id": execution_id,
                        "error": str(e),
                    },
                    timestamp=asyncio.get_event_loop().time(),
                    correlation_id=execution_id,
                )
            )

            return ExecutionResult(
                execution_id=execution_id,
                state=ExecutionState.FAILED,
                error=str(e),
            )

    async def coordinate_agents(
        self,
        agent_ids: List[str],
        task: str,
        coordination_pattern: str = "parallel",  # "parallel", "sequential", "hierarchical"
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, ExecutionResult]:
        """Coordinate multiple agents.

        Args:
            agent_ids: List of agent identifiers
            task: Task description
            coordination_pattern: How to coordinate agents
            context: Additional context

        Returns:
            Dictionary mapping agent_id to execution result
        """
        context = context or {}
        results: Dict[str, ExecutionResult] = {}

        if coordination_pattern == "parallel":
            # Execute all agents in parallel
            tasks = [
                self.execute_agent(agent_id, task, context)
                for agent_id in agent_ids
            ]
            execution_results = await asyncio.gather(*tasks, return_exceptions=True)

            for agent_id, result in zip(agent_ids, execution_results):
                if isinstance(result, Exception):
                    results[agent_id] = ExecutionResult(
                        execution_id=str(uuid.uuid4()),
                        state=ExecutionState.FAILED,
                        error=str(result),
                    )
                else:
                    results[agent_id] = result

        elif coordination_pattern == "sequential":
            # Execute agents sequentially
            for agent_id in agent_ids:
                result = await self.execute_agent(agent_id, task, context)
                results[agent_id] = result
                # Pass result as context to next agent
                if result.result:
                    context[f"previous_result_{agent_id}"] = result.result

        elif coordination_pattern == "hierarchical":
            # First agent coordinates, others execute subtasks
            if agent_ids:
                coordinator_id = agent_ids[0]
                worker_ids = agent_ids[1:]

                # Coordinator decides how to use workers
                coordinator_result = await self.execute_agent(
                    coordinator_id,
                    f"{task}\n\nAvailable workers: {worker_ids}",
                    context,
                )

                # If coordinator succeeded, execute workers
                if coordinator_result.state == ExecutionState.COMPLETED:
                    worker_tasks = [
                        self.execute_agent(worker_id, task, context)
                        for worker_id in worker_ids
                    ]
                    worker_results = await asyncio.gather(
                        *worker_tasks, return_exceptions=True
                    )

                    results[coordinator_id] = coordinator_result
                    for worker_id, result in zip(worker_ids, worker_results):
                        if isinstance(result, Exception):
                            results[worker_id] = ExecutionResult(
                                execution_id=str(uuid.uuid4()),
                                state=ExecutionState.FAILED,
                                error=str(result),
                            )
                        else:
                            results[worker_id] = result
                else:
                    results[coordinator_id] = coordinator_result

        return results

    async def get_execution_state(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get the state of an execution.

        Args:
            execution_id: Execution identifier

        Returns:
            Execution state or None if not found
        """
        return await self.state_store.get(f"execution:{execution_id}")

    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a running execution.

        Args:
            execution_id: Execution identifier

        Returns:
            True if cancelled, False if not found
        """
        state = await self.get_execution_state(execution_id)
        if not state:
            return False

        # Update state
        state["state"] = ExecutionState.CANCELLED.value
        await self.state_store.set(f"execution:{execution_id}", state)

        # Publish cancellation event
        await self.event_bus.publish(
            Event(
                event_type="execution.cancelled",
                source="orchestrator",
                payload={"execution_id": execution_id},
                timestamp=asyncio.get_event_loop().time(),
                correlation_id=execution_id,
            )
        )

        return True


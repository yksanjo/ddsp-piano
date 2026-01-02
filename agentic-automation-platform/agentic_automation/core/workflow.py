"""Workflow execution engine."""

import asyncio
import uuid
from typing import Any, Dict, List, Optional

from agentic_automation.core.models import (
    ExecutionState,
    ExecutionResult,
    TaskDefinition,
    TaskType,
    WorkflowDefinition,
)


class DependencyGraph:
    """Represents task dependencies in a workflow."""

    def __init__(self, tasks: List[TaskDefinition], dependencies: Dict[str, List[str]]):
        """Initialize dependency graph.

        Args:
            tasks: List of tasks
            dependencies: Task dependencies mapping
        """
        self.tasks = {task.id: task for task in tasks}
        self.dependencies = dependencies
        self._reverse_deps: Dict[str, List[str]] = {}
        self._build_reverse_deps()

    def _build_reverse_deps(self) -> None:
        """Build reverse dependency mapping."""
        for task_id, deps in self.dependencies.items():
            for dep_id in deps:
                if dep_id not in self._reverse_deps:
                    self._reverse_deps[dep_id] = []
                self._reverse_deps[dep_id].append(task_id)

    def get_ready_tasks(self, completed_tasks: set[str]) -> List[str]:
        """Get tasks that are ready to execute (all dependencies completed).

        Args:
            completed_tasks: Set of completed task IDs

        Returns:
            List of ready task IDs
        """
        ready = []
        for task_id, task in self.tasks.items():
            if task_id in completed_tasks:
                continue

            deps = self.dependencies.get(task_id, [])
            if all(dep_id in completed_tasks for dep_id in deps):
                ready.append(task_id)

        return ready

    def get_dependencies(self, task_id: str) -> List[str]:
        """Get dependencies for a task.

        Args:
            task_id: Task identifier

        Returns:
            List of dependency task IDs
        """
        return self.dependencies.get(task_id, [])


class Workflow:
    """Workflow execution engine."""

    def __init__(
        self,
        definition: WorkflowDefinition,
        orchestrator: Any,  # Orchestrator
        tool_registry: Optional[Dict[str, Any]] = None,  # Dict[str, Tool]
    ):
        """Initialize workflow.

        Args:
            definition: Workflow definition
            orchestrator: Orchestrator instance
            tool_registry: Registry of available tools
        """
        self.definition = definition
        self.orchestrator = orchestrator
        self.tool_registry = tool_registry or {}
        self.dependency_graph = DependencyGraph(
            definition.tasks, definition.dependencies
        )

    async def execute(
        self, inputs: Optional[Dict[str, Any]] = None, execution_id: Optional[str] = None
    ) -> ExecutionResult:
        """Execute the workflow.

        Args:
            inputs: Input values for the workflow
            execution_id: Optional execution ID

        Returns:
            Execution result
        """
        execution_id = execution_id or str(uuid.uuid4())
        inputs = inputs or {}
        completed_tasks: set[str] = {}
        task_results: Dict[str, Any] = {}
        failed_tasks: set[str] = set()

        try:
            # Execute tasks in dependency order
            while len(completed_tasks) + len(failed_tasks) < len(self.definition.tasks):
                ready_tasks = self.dependency_graph.get_ready_tasks(completed_tasks)

                if not ready_tasks:
                    # Check if we're stuck
                    if not failed_tasks:
                        return ExecutionResult(
                            execution_id=execution_id,
                            state=ExecutionState.FAILED,
                            error="Workflow stuck: circular dependencies or missing tasks",
                        )
                    break

                # Execute ready tasks in parallel
                task_executions = [
                    self._execute_task(task_id, inputs, task_results)
                    for task_id in ready_tasks
                ]
                results = await asyncio.gather(*task_executions, return_exceptions=True)

                for task_id, result in zip(ready_tasks, results):
                    if isinstance(result, Exception):
                        failed_tasks.add(task_id)
                        task_results[task_id] = {"error": str(result)}
                    else:
                        completed_tasks.add(task_id)
                        task_results[task_id] = result

            # Determine final state
            if failed_tasks:
                state = ExecutionState.FAILED
                error = f"Tasks failed: {failed_tasks}"
            else:
                state = ExecutionState.COMPLETED
                error = None

            # Get final output (from last task or specified output task)
            final_result = self._get_final_result(task_results)

            return ExecutionResult(
                execution_id=execution_id,
                state=state,
                result=final_result,
                error=error,
                metrics={"tasks_completed": len(completed_tasks), "tasks_failed": len(failed_tasks)},
            )

        except Exception as e:
            return ExecutionResult(
                execution_id=execution_id,
                state=ExecutionState.FAILED,
                error=str(e),
            )

    async def _execute_task(
        self, task_id: str, inputs: Dict[str, Any], task_results: Dict[str, Any]
    ) -> Any:
        """Execute a single task.

        Args:
            task_id: Task identifier
            inputs: Workflow inputs
            task_results: Results from previous tasks

        Returns:
            Task result
        """
        task = self.dependency_graph.tasks[task_id]

        # Resolve task inputs
        task_inputs = self._resolve_inputs(task, inputs, task_results)

        # Execute based on task type
        if task.type == TaskType.AGENT:
            if not task.agent_id:
                raise ValueError(f"Task {task_id} requires agent_id")
            result = await self.orchestrator.execute_agent(
                task.agent_id, str(task_inputs.get("task", "")), task_inputs
            )
            return result.result

        elif task.type == TaskType.TOOL:
            if not task.tool_id:
                raise ValueError(f"Task {task_id} requires tool_id")
            tool = self.tool_registry.get(task.tool_id)
            if not tool:
                raise ValueError(f"Tool {task.tool_id} not found")
            return await tool.execute(**task_inputs)

        elif task.type == TaskType.CONDITION:
            # Evaluate condition
            condition = task.condition
            if condition:
                # Simple condition evaluation (can be extended)
                result = eval(condition, {"inputs": task_inputs, "results": task_results})
                return {"condition_result": result}

        elif task.type == TaskType.LOOP:
            # Execute loop
            loop_config = task.loop_config or {}
            items = loop_config.get("items", [])
            results = []
            for item in items:
                # Execute task for each item
                loop_inputs = {**task_inputs, "item": item, "index": items.index(item)}
                # Recursively execute (simplified)
                results.append(loop_inputs)
            return results

        else:
            raise ValueError(f"Unknown task type: {task.type}")

    def _resolve_inputs(
        self, task: TaskDefinition, inputs: Dict[str, Any], task_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Resolve task inputs from workflow inputs and previous task results.

        Args:
            task: Task definition
            inputs: Workflow inputs
            task_results: Previous task results

        Returns:
            Resolved inputs
        """
        resolved = {}

        for key, value in task.inputs.items():
            if isinstance(value, str) and value.startswith("$"):
                # Reference to another task output
                ref = value[1:]  # Remove $
                if "." in ref:
                    task_id, output_key = ref.split(".", 1)
                    if task_id in task_results:
                        resolved[key] = task_results[task_id].get(output_key)
                else:
                    # Reference to workflow input
                    resolved[key] = inputs.get(ref)
            else:
                resolved[key] = value

        return resolved

    def _get_final_result(self, task_results: Dict[str, Any]) -> Any:
        """Get the final result from workflow execution.

        Args:
            task_results: All task results

        Returns:
            Final result
        """
        # Return results from last task or combine all results
        if task_results:
            # Get the last task (simplified - could be more sophisticated)
            last_task_id = list(task_results.keys())[-1]
            return task_results[last_task_id]
        return None


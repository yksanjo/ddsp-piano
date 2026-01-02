"""Agent implementation."""

import time
from typing import Any, Dict, List, Optional

from agentic_automation.core.models import (
    AgentDefinition,
    ExecutionState,
    LLMBackend,
    MemoryConfig,
)


class Agent:
    """An agent that can execute tasks using LLM backends."""

    def __init__(
        self,
        definition: AgentDefinition,
        llm_backend: Any,  # LLMBackendInterface
        memory_manager: Optional[Any] = None,  # MemoryManager
        tools: Optional[List[Any]] = None,  # List[Tool]
    ):
        """Initialize an agent.

        Args:
            definition: Agent definition
            llm_backend: LLM backend implementation
            memory_manager: Memory manager for context
            tools: List of available tools
        """
        self.definition = definition
        self.llm_backend = llm_backend
        self.memory_manager = memory_manager
        self.tools = tools or []
        self._tool_registry: Dict[str, Any] = {tool.id: tool for tool in self.tools}

    async def execute(
        self, task: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a task.

        Args:
            task: Task description or prompt
            context: Additional context for the task

        Returns:
            Execution result
        """
        context = context or {}
        state = ExecutionState.RUNNING

        # Build messages with memory context
        messages = await self._build_messages(task, context)

        # Execute agent loop
        result = None
        error = None

        try:
            for iteration in range(self.definition.max_iterations):
                # Call LLM
                response = await self.llm_backend.generate(
                    messages=messages,
                    model=self.definition.model,
                    temperature=self.definition.temperature,
                    tools=self._get_tool_schemas(),
                )

                # Process response
                if response.tool_calls:
                    # Execute tool calls
                    tool_results = await self._execute_tools(response.tool_calls)
                    messages.append({
                        "role": response.message.role,
                        "content": response.message.content,
                    })
                    messages.extend(tool_results)
                else:
                    # Final answer
                    result = response.content
                    state = ExecutionState.COMPLETED
                    break

            if state != ExecutionState.COMPLETED:
                state = ExecutionState.FAILED
                error = "Max iterations reached"

        except Exception as e:
            state = ExecutionState.FAILED
            error = str(e)

        # Update memory
        if self.memory_manager:
            await self.memory_manager.store_interaction(
                task=task,
                response=result,
                context=context,
            )

        return {
            "state": state,
            "result": result,
            "error": error,
            "iterations": iteration + 1 if "iteration" in locals() else 0,
        }

    async def _build_messages(
        self, task: str, context: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Build messages for LLM with memory context."""
        messages = []

        # System prompt
        messages.append({"role": "system", "content": self.definition.system_prompt})

        # Memory context
        if self.memory_manager:
            memory_context = await self.memory_manager.retrieve_relevant(task, context)
            if memory_context:
                messages.append(
                    {
                        "role": "system",
                        "content": f"Relevant context from memory:\n{memory_context}",
                    }
                )

        # User task
        task_with_context = task
        if context:
            context_str = "\n".join(f"{k}: {v}" for k, v in context.items())
            task_with_context = f"{task}\n\nContext:\n{context_str}"

        messages.append({"role": "user", "content": task_with_context})

        return messages

    def _get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get tool schemas for LLM."""
        return [tool.get_schema() for tool in self.tools]

    async def _execute_tools(
        self, tool_calls: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Execute tool calls."""
        results = []
        for tool_call in tool_calls:
            tool_id = tool_call.get("id")
            tool_name = tool_call.get("function", {}).get("name")
            arguments = tool_call.get("function", {}).get("arguments", {})

            if tool_name in self._tool_registry:
                tool = self._tool_registry[tool_name]
                try:
                    result = await tool.execute(**arguments)
                    results.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_id,
                            "content": str(result),
                        }
                    )
                except Exception as e:
                    results.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_id,
                            "content": f"Error: {str(e)}",
                        }
                    )
            else:
                results.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "content": f"Tool {tool_name} not found",
                    }
                )

        return results


"""Parser for workflow definitions."""

import yaml
from typing import Any, Dict

from agentic_automation.core.models import (
    TaskDefinition,
    TaskType,
    WorkflowDefinition,
    RetryConfig,
    ErrorHandlingConfig,
)


class WorkflowParser:
    """Parser for YAML/JSON workflow definitions."""

    @staticmethod
    def parse_yaml(yaml_content: str) -> WorkflowDefinition:
        """Parse a YAML workflow definition.

        Args:
            yaml_content: YAML content

        Returns:
            Workflow definition
        """
        data = yaml.safe_load(yaml_content)
        return WorkflowParser._parse_dict(data)

    @staticmethod
    def parse_dict(data: Dict[str, Any]) -> WorkflowDefinition:
        """Parse a dictionary workflow definition.

        Args:
            data: Dictionary data

        Returns:
            Workflow definition
        """
        return WorkflowParser._parse_dict(data)

    @staticmethod
    def _parse_dict(data: Dict[str, Any]) -> WorkflowDefinition:
        """Parse dictionary into workflow definition."""
        # Parse tasks
        tasks = []
        for task_data in data.get("tasks", []):
            task = WorkflowParser._parse_task(task_data)
            tasks.append(task)

        # Parse dependencies
        dependencies = data.get("dependencies", {})

        # Parse retry config
        retry_config = RetryConfig()
        if "retry" in data:
            retry_config = WorkflowParser._parse_retry_config(data["retry"])

        # Parse error handling
        error_handling = ErrorHandlingConfig()
        if "error_handling" in data:
            error_handling = WorkflowParser._parse_error_handling(data["error_handling"])

        return WorkflowDefinition(
            id=data.get("id", "workflow"),
            name=data.get("name", "Workflow"),
            version=data.get("version", "1.0.0"),
            description=data.get("description", ""),
            tasks=tasks,
            dependencies=dependencies,
            retry_config=retry_config,
            error_handling=error_handling,
            metadata=data.get("metadata", {}),
        )

    @staticmethod
    def _parse_task(data: Dict[str, Any]) -> TaskDefinition:
        """Parse a task definition."""
        task_type = TaskType(data.get("type", "agent"))

        # Parse retry config
        retry_config = RetryConfig()
        if "retry" in data:
            retry_config = WorkflowParser._parse_retry_config(data["retry"])

        # Parse error handling
        error_handling = ErrorHandlingConfig()
        if "error_handling" in data:
            error_handling = WorkflowParser._parse_error_handling(data["error_handling"])

        return TaskDefinition(
            id=data.get("id", ""),
            name=data.get("name", ""),
            type=task_type,
            agent_id=data.get("agent_id"),
            tool_id=data.get("tool_id"),
            inputs=data.get("inputs", {}),
            outputs=data.get("outputs", {}),
            condition=data.get("condition"),
            loop_config=data.get("loop"),
            retry_config=retry_config,
            error_handling=error_handling,
            metadata=data.get("metadata", {}),
        )

    @staticmethod
    def _parse_retry_config(data: Dict[str, Any]) -> RetryConfig:
        """Parse retry configuration."""
        return RetryConfig(
            max_retries=data.get("max_retries", 3),
            initial_delay=data.get("initial_delay", 1.0),
            max_delay=data.get("max_delay", 60.0),
            exponential_base=data.get("exponential_base", 2.0),
            jitter=data.get("jitter", True),
        )

    @staticmethod
    def _parse_error_handling(data: Dict[str, Any]) -> ErrorHandlingConfig:
        """Parse error handling configuration."""
        return ErrorHandlingConfig(
            on_error=data.get("on_error", "fail"),
            error_notification=data.get("error_notification"),
            fallback_task=data.get("fallback_task"),
        )


class WorkflowCodeGenerator:
    """Generate Python code from workflow definitions."""

    @staticmethod
    def generate(workflow: WorkflowDefinition) -> str:
        """Generate Python code for a workflow.

        Args:
            workflow: Workflow definition

        Returns:
            Python code
        """
        lines = [
            "from agentic_automation import Workflow, Orchestrator",
            "",
            f"# Workflow: {workflow.name}",
            f"# Version: {workflow.version}",
            "",
            "async def execute_workflow(orchestrator: Orchestrator, inputs: dict):",
            '    """Execute workflow."""',
        ]

        # Generate task execution code
        for task in workflow.tasks:
            if task.type == TaskType.AGENT:
                lines.append(f"    # Task: {task.name}")
                lines.append(f"    result_{task.id} = await orchestrator.execute_agent(")
                lines.append(f'        "{task.agent_id}",')
                lines.append(f'        "{task.inputs.get("task", "")}",')
                lines.append("    )")

        lines.append("    return result")

        return "\n".join(lines)


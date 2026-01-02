"""Parser for declarative agent definitions (YAML/JSON)."""

import json
from typing import Any, Dict

import yaml

from agentic_automation.core.models import AgentDefinition, LLMBackend, MemoryConfig


class AgentParser:
    """Parser for YAML/JSON agent definitions."""

    @staticmethod
    def parse_yaml(yaml_content: str) -> AgentDefinition:
        """Parse a YAML agent definition.

        Args:
            yaml_content: YAML content

        Returns:
            Agent definition
        """
        data = yaml.safe_load(yaml_content)
        return AgentParser._parse_dict(data)

    @staticmethod
    def parse_json(json_content: str) -> AgentDefinition:
        """Parse a JSON agent definition.

        Args:
            json_content: JSON content

        Returns:
            Agent definition
        """
        data = json.loads(json_content)
        return AgentParser._parse_dict(data)

    @staticmethod
    def parse_dict(data: Dict[str, Any]) -> AgentDefinition:
        """Parse a dictionary agent definition.

        Args:
            data: Dictionary data

        Returns:
            Agent definition
        """
        return AgentParser._parse_dict(data)

    @staticmethod
    def _parse_dict(data: Dict[str, Any]) -> AgentDefinition:
        """Parse dictionary into agent definition."""
        # Parse memory config
        memory_config = MemoryConfig()
        if "memory" in data:
            memory_data = data["memory"]
            memory_config = MemoryConfig(
                short_term_enabled=memory_data.get("short_term_enabled", True),
                long_term_enabled=memory_data.get("long_term_enabled", False),
                max_context_tokens=memory_data.get("max_context_tokens", 8000),
                summarization_threshold=memory_data.get("summarization_threshold", 6000),
                vector_db_provider=memory_data.get("vector_db_provider"),
            )

        return AgentDefinition(
            id=data.get("id", ""),
            name=data.get("name", "Agent"),
            description=data.get("description", ""),
            llm_backend=LLMBackend(data.get("llm_backend", "openai")),
            model=data.get("model", "gpt-4"),
            system_prompt=data.get("system_prompt", "You are a helpful assistant."),
            tools=data.get("tools", []),
            memory_config=memory_config,
            max_iterations=data.get("max_iterations", 10),
            temperature=data.get("temperature", 0.7),
            metadata=data.get("metadata", {}),
        )

    @staticmethod
    def to_yaml(definition: AgentDefinition) -> str:
        """Convert agent definition to YAML.

        Args:
            definition: Agent definition

        Returns:
            YAML string
        """
        data = {
            "id": definition.id,
            "name": definition.name,
            "description": definition.description,
            "llm_backend": definition.llm_backend.value,
            "model": definition.model,
            "system_prompt": definition.system_prompt,
            "tools": definition.tools,
            "memory": {
                "short_term_enabled": definition.memory_config.short_term_enabled,
                "long_term_enabled": definition.memory_config.long_term_enabled,
                "max_context_tokens": definition.memory_config.max_context_tokens,
                "summarization_threshold": definition.memory_config.summarization_threshold,
                "vector_db_provider": definition.memory_config.vector_db_provider,
            },
            "max_iterations": definition.max_iterations,
            "temperature": definition.temperature,
            "metadata": definition.metadata,
        }
        return yaml.dump(data, default_flow_style=False)


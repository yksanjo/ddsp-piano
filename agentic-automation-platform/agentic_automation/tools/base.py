"""Base tool interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict


class Tool(ABC):
    """Base tool class."""

    def __init__(self, tool_id: str, name: str, description: str):
        """Initialize tool.

        Args:
            tool_id: Unique tool identifier
            name: Tool name
            description: Tool description
        """
        self.id = tool_id
        self.name = name
        self.description = description

    @abstractmethod
    async def execute(self, **kwargs: Any) -> Any:
        """Execute the tool.

        Args:
            **kwargs: Tool arguments

        Returns:
            Tool result
        """
        pass

    def get_schema(self) -> Dict[str, Any]:
        """Get JSON schema for the tool (for function calling).

        Returns:
            JSON schema
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self._get_parameters_schema(),
            },
        }

    @abstractmethod
    def _get_parameters_schema(self) -> Dict[str, Any]:
        """Get parameters schema for the tool.

        Returns:
            JSON schema for parameters
        """
        pass


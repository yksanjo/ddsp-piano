"""Built-in tools for agents."""

import json
from typing import Any, Dict

from agentic_automation.tools.base import Tool


class CalculatorTool(Tool):
    """Simple calculator tool."""

    def __init__(self):
        """Initialize calculator tool."""
        super().__init__(
            tool_id="calculator",
            name="calculator",
            description="Perform basic arithmetic operations",
        )

    async def execute(self, expression: str) -> float:
        """Evaluate a mathematical expression.

        Args:
            expression: Mathematical expression (e.g., "2 + 2")

        Returns:
            Calculation result
        """
        try:
            # Simple evaluation (in production, use a safer evaluator)
            result = eval(expression, {"__builtins__": {}}, {})
            return float(result)
        except Exception as e:
            raise ValueError(f"Invalid expression: {e}")

    def _get_parameters_schema(self) -> Dict[str, Any]:
        """Get parameters schema."""
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate",
                }
            },
            "required": ["expression"],
        }


class WebSearchTool(Tool):
    """Web search tool (placeholder)."""

    def __init__(self):
        """Initialize web search tool."""
        super().__init__(
            tool_id="web_search",
            name="web_search",
            description="Search the web for information",
        )

    async def execute(self, query: str) -> str:
        """Search the web.

        Args:
            query: Search query

        Returns:
            Search results (placeholder)
        """
        # Placeholder - in production, integrate with search API
        return f"Search results for: {query} (placeholder)"

    def _get_parameters_schema(self) -> Dict[str, Any]:
        """Get parameters schema."""
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query",
                }
            },
            "required": ["query"],
        }


class FileReadTool(Tool):
    """File reading tool."""

    def __init__(self):
        """Initialize file read tool."""
        super().__init__(
            tool_id="file_read",
            name="file_read",
            description="Read contents of a file",
        )

    async def execute(self, file_path: str) -> str:
        """Read a file.

        Args:
            file_path: Path to the file

        Returns:
            File contents
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")

    def _get_parameters_schema(self) -> Dict[str, Any]:
        """Get parameters schema."""
        return {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read",
                }
            },
            "required": ["file_path"],
        }


class JSONParseTool(Tool):
    """JSON parsing tool."""

    def __init__(self):
        """Initialize JSON parse tool."""
        super().__init__(
            tool_id="json_parse",
            name="json_parse",
            description="Parse JSON string into Python object",
        )

    async def execute(self, json_string: str) -> Dict[str, Any]:
        """Parse JSON string.

        Args:
            json_string: JSON string to parse

        Returns:
            Parsed JSON object
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {e}")

    def _get_parameters_schema(self) -> Dict[str, Any]:
        """Get parameters schema."""
        return {
            "type": "object",
            "properties": {
                "json_string": {
                    "type": "string",
                    "description": "JSON string to parse",
                }
            },
            "required": ["json_string"],
        }


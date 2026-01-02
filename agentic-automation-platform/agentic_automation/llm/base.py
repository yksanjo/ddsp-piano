"""Base LLM backend interface."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class LLMMessage(BaseModel):
    """LLM message model."""

    role: str  # "system", "user", "assistant", "tool"
    content: str
    tool_call_id: Optional[str] = None
    name: Optional[str] = None  # For tool messages


class ToolCall(BaseModel):
    """Tool call model."""

    id: str
    function: Dict[str, Any]  # name, arguments


class LLMResponse(BaseModel):
    """LLM response model."""

    content: str
    tool_calls: List[ToolCall] = []
    message: LLMMessage
    usage: Optional[Dict[str, int]] = None  # tokens used


class LLMBackend(ABC):
    """Abstract LLM backend interface."""

    @abstractmethod
    async def generate(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        temperature: float = 0.7,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        """Generate a response from the LLM.

        Args:
            messages: List of messages
            model: Model name
            temperature: Sampling temperature
            tools: Available tools (function calling)

        Returns:
            LLM response
        """
        pass

    @abstractmethod
    async def stream(
        self,
        messages: List[Dict[str, Any]],
        model: str,
        temperature: float = 0.7,
    ):
        """Stream responses from the LLM.

        Args:
            messages: List of messages
            model: Model name
            temperature: Sampling temperature

        Yields:
            Response chunks
        """
        pass


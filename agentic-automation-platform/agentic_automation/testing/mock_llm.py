"""Mock LLM backend for testing."""

from typing import Any, Dict, List, Optional

from agentic_automation.llm.base import LLMBackend, LLMResponse, ToolCall


class MockLLMBackend(LLMBackend):
    """Mock LLM backend for deterministic testing."""

    def __init__(self, responses: Optional[Dict[str, str]] = None):
        """Initialize mock LLM backend.

        Args:
            responses: Dictionary mapping prompts to responses
        """
        self.responses = responses or {}
        self.call_history: List[Dict[str, Any]] = []

    async def generate(
        self,
        messages: List[Dict[str, Any]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        """Generate a mock response."""
        # Record call
        self.call_history.append({
            "messages": messages,
            "model": model,
            "temperature": temperature,
            "tools": tools,
        })

        # Get last user message
        user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        # Look up response or use default
        if user_message and user_message in self.responses:
            content = self.responses[user_message]
        else:
            content = f"Mock response to: {user_message}"

        return LLMResponse(
            content=content,
            tool_calls=[],
            message={
                "role": "assistant",
                "content": content,
            },
            usage={
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30,
            },
        )

    async def stream(
        self,
        messages: List[Dict[str, Any]],
        model: str = "gpt-4",
        temperature: float = 0.7,
    ):
        """Stream mock responses."""
        response = await self.generate(messages, model, temperature)
        # Yield response in chunks
        words = response.content.split()
        for word in words:
            yield word + " "

    def set_response(self, prompt: str, response: str) -> None:
        """Set a response for a specific prompt.

        Args:
            prompt: Input prompt
            response: Mock response
        """
        self.responses[prompt] = response

    def clear_history(self) -> None:
        """Clear call history."""
        self.call_history.clear()

    def get_call_count(self) -> int:
        """Get number of LLM calls made.

        Returns:
            Number of calls
        """
        return len(self.call_history)


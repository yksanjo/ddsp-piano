"""OpenAI LLM backend."""

from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI

from agentic_automation.llm.base import LLMBackend, LLMResponse, ToolCall


class OpenAIBackend(LLMBackend):
    """OpenAI LLM backend implementation."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        """Initialize OpenAI backend.

        Args:
            api_key: OpenAI API key
            base_url: Custom base URL (for OpenAI-compatible APIs)
        """
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url)

    async def generate(
        self,
        messages: List[Dict[str, Any]],
        model: str = "gpt-4",
        temperature: float = 0.7,
        tools: Optional[List[Dict[str, Any]]] = None,
    ) -> LLMResponse:
        """Generate a response using OpenAI API."""
        # Convert messages format
        openai_messages = []
        for msg in messages:
            openai_msg = {"role": msg["role"], "content": msg["content"]}
            if "tool_call_id" in msg:
                openai_msg["tool_call_id"] = msg["tool_call_id"]
            if "name" in msg:
                openai_msg["name"] = msg["name"]
            openai_messages.append(openai_msg)

        # Prepare request
        kwargs = {
            "model": model,
            "messages": openai_messages,
            "temperature": temperature,
        }

        if tools:
            kwargs["tools"] = tools

        # Call API
        response = await self.client.chat.completions.create(**kwargs)

        # Extract response
        choice = response.choices[0]
        message = choice.message

        # Parse tool calls
        tool_calls = []
        if message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append(
                    ToolCall(
                        id=tc.id,
                        function={
                            "name": tc.function.name,
                            "arguments": tc.function.arguments,
                        },
                    )
                )

        from agentic_automation.llm.base import LLMMessage

        return LLMResponse(
            content=message.content or "",
            tool_calls=tool_calls,
            message=LLMMessage(
                role=message.role,
                content=message.content or "",
            ),
            usage={
                "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                "total_tokens": response.usage.total_tokens if response.usage else 0,
            },
        )

    async def stream(
        self,
        messages: List[Dict[str, Any]],
        model: str = "gpt-4",
        temperature: float = 0.7,
    ):
        """Stream responses from OpenAI API."""
        openai_messages = [
            {"role": msg["role"], "content": msg["content"]} for msg in messages
        ]

        stream = await self.client.chat.completions.create(
            model=model,
            messages=openai_messages,
            temperature=temperature,
            stream=True,
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


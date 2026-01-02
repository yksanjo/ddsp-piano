"""Tests for Agent class."""

import pytest

from agentic_automation.core.agent import Agent
from agentic_automation.core.models import AgentDefinition, LLMBackend
from agentic_automation.testing.mock_llm import MockLLMBackend


@pytest.mark.asyncio
async def test_agent_execution():
    """Test basic agent execution."""
    definition = AgentDefinition(
        id="test_agent",
        name="Test Agent",
        description="Test agent",
        llm_backend=LLMBackend.MOCK,
        model="mock",
        system_prompt="You are a helpful assistant.",
    )

    mock_llm = MockLLMBackend(responses={"Hello": "Hi there!"})
    agent = Agent(definition=definition, llm_backend=mock_llm)

    result = await agent.execute("Hello")

    assert result["state"].value == "completed"
    assert "Hi there!" in result.get("result", "")


@pytest.mark.asyncio
async def test_agent_with_tools():
    """Test agent with tools."""
    from agentic_automation.tools.builtin import CalculatorTool

    definition = AgentDefinition(
        id="test_agent",
        name="Test Agent",
        description="Test agent",
        llm_backend=LLMBackend.MOCK,
        model="mock",
        system_prompt="You are a helpful assistant.",
    )

    mock_llm = MockLLMBackend()
    calculator = CalculatorTool()
    agent = Agent(definition=definition, llm_backend=mock_llm, tools=[calculator])

    # Agent should have access to calculator tool
    assert len(agent.tools) == 1
    assert agent.tools[0].id == "calculator"


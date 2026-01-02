"""Test fixtures for common agent scenarios."""

from typing import Any, Dict, List

from agentic_automation.core.agent import Agent
from agentic_automation.core.agent_pool import AgentPool
from agentic_automation.core.models import AgentDefinition, LLMBackend
from agentic_automation.testing.mock_llm import MockLLMBackend


def create_test_agent(
    agent_id: str = "test_agent",
    system_prompt: str = "You are a helpful assistant.",
    responses: Dict[str, str] = None,
) -> Agent:
    """Create a test agent with mock LLM.

    Args:
        agent_id: Agent identifier
        system_prompt: System prompt
        responses: Mock responses mapping

    Returns:
        Test agent instance
    """
    definition = AgentDefinition(
        id=agent_id,
        name="Test Agent",
        description="Test agent for unit testing",
        llm_backend=LLMBackend.MOCK,
        model="mock",
        system_prompt=system_prompt,
    )

    mock_llm = MockLLMBackend(responses=responses or {})
    return Agent(definition=definition, llm_backend=mock_llm)


def create_test_agent_pool(agents: List[Agent]) -> AgentPool:
    """Create a test agent pool.

    Args:
        agents: List of agents to add to pool

    Returns:
        Agent pool instance
    """
    pool = AgentPool()
    for agent in agents:
        pool.register_agent(agent.definition, agent)
    return pool


class AgentTestCase:
    """Base test case for agent tests."""

    def __init__(self):
        """Initialize test case."""
        self.agent_pool = AgentPool()

    def setup_agent(
        self,
        agent_id: str,
        system_prompt: str,
        responses: Dict[str, str] = None,
    ) -> Agent:
        """Set up a test agent.

        Args:
            agent_id: Agent identifier
            system_prompt: System prompt
            responses: Mock responses

        Returns:
            Agent instance
        """
        agent = create_test_agent(agent_id, system_prompt, responses)
        self.agent_pool.register_agent(agent.definition, agent)
        return agent

    def assert_agent_response_contains(
        self, agent: Agent, task: str, expected_text: str
    ) -> None:
        """Assert that agent response contains expected text.

        Args:
            agent: Agent instance
            task: Task to execute
            expected_text: Expected text in response
        """
        import asyncio

        result = asyncio.run(agent.execute(task))
        assert expected_text.lower() in result.get("result", "").lower(), (
            f"Expected '{expected_text}' in response: {result.get('result')}"
        )

    def assert_agent_succeeds(self, agent: Agent, task: str) -> None:
        """Assert that agent execution succeeds.

        Args:
            agent: Agent instance
            task: Task to execute
        """
        import asyncio

        result = asyncio.run(agent.execute(task))
        assert result["state"].value == "completed", (
            f"Agent execution failed: {result.get('error')}"
        )


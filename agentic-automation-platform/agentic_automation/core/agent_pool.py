"""Agent pool for managing agent instances."""

from typing import Dict, Optional

from agentic_automation.core.agent import Agent
from agentic_automation.core.models import AgentDefinition


class AgentPool:
    """Manages a pool of agent instances."""

    def __init__(self):
        """Initialize the agent pool."""
        self._agents: Dict[str, Agent] = {}
        self._definitions: Dict[str, AgentDefinition] = {}

    def register_agent(self, definition: AgentDefinition, agent: Agent) -> None:
        """Register an agent in the pool.

        Args:
            definition: Agent definition
            agent: Agent instance
        """
        self._definitions[definition.id] = definition
        self._agents[definition.id] = agent

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        """Get an agent by ID.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent instance or None if not found
        """
        return self._agents.get(agent_id)

    def get_definition(self, agent_id: str) -> Optional[AgentDefinition]:
        """Get an agent definition by ID.

        Args:
            agent_id: Agent identifier

        Returns:
            Agent definition or None if not found
        """
        return self._definitions.get(agent_id)

    def list_agents(self) -> list[str]:
        """List all registered agent IDs.

        Returns:
            List of agent IDs
        """
        return list(self._agents.keys())

    def remove_agent(self, agent_id: str) -> bool:
        """Remove an agent from the pool.

        Args:
            agent_id: Agent identifier

        Returns:
            True if removed, False if not found
        """
        if agent_id in self._agents:
            del self._agents[agent_id]
            del self._definitions[agent_id]
            return True
        return False

    def clear(self) -> None:
        """Clear all agents from the pool."""
        self._agents.clear()
        self._definitions.clear()


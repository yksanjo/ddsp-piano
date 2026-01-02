"""Rate limiting for agent executions."""

import time
from collections import defaultdict
from typing import Dict, Optional


class RateLimiter:
    """Rate limiter for controlling execution frequency."""

    def __init__(self, max_calls: int = 10, time_window: float = 60.0):
        """Initialize rate limiter.

        Args:
            max_calls: Maximum number of calls allowed
            time_window: Time window in seconds
        """
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls: Dict[str, list[float]] = defaultdict(list)

    async def acquire(self, key: str) -> bool:
        """Acquire a rate limit slot.

        Args:
            key: Rate limit key (e.g., agent_id, user_id)

        Returns:
            True if allowed, False if rate limited
        """
        now = time.time()
        calls = self.calls[key]

        # Remove old calls outside the time window
        calls[:] = [call_time for call_time in calls if now - call_time < self.time_window]

        if len(calls) >= self.max_calls:
            return False

        calls.append(now)
        return True

    async def wait_if_needed(self, key: str) -> None:
        """Wait if rate limited.

        Args:
            key: Rate limit key

        Raises:
            Exception: If rate limited
        """
        if not await self.acquire(key):
            raise Exception(f"Rate limit exceeded for {key}")

    def get_remaining(self, key: str) -> int:
        """Get remaining calls in current window.

        Args:
            key: Rate limit key

        Returns:
            Number of remaining calls
        """
        now = time.time()
        calls = [c for c in self.calls[key] if now - c < self.time_window]
        return max(0, self.max_calls - len(calls))

    def reset(self, key: Optional[str] = None) -> None:
        """Reset rate limiter for a key or all keys.

        Args:
            key: Rate limit key, or None to reset all
        """
        if key:
            self.calls.pop(key, None)
        else:
            self.calls.clear()


class CostTracker:
    """Track costs for LLM usage."""

    def __init__(self):
        """Initialize cost tracker."""
        self.costs: Dict[str, float] = defaultdict(float)
        # Cost per 1M tokens (approximate)
        self.model_costs = {
            "gpt-4": {"prompt": 30.0, "completion": 60.0},
            "gpt-4-turbo": {"prompt": 10.0, "completion": 30.0},
            "gpt-3.5-turbo": {"prompt": 0.5, "completion": 1.5},
            "claude-3-opus": {"prompt": 15.0, "completion": 75.0},
            "claude-3-sonnet": {"prompt": 3.0, "completion": 15.0},
        }

    def record_usage(
        self,
        agent_id: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
    ) -> float:
        """Record token usage and calculate cost.

        Args:
            agent_id: Agent identifier
            model: Model name
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens

        Returns:
            Cost in USD
        """
        if model not in self.model_costs:
            return 0.0

        costs = self.model_costs[model]
        prompt_cost = (prompt_tokens / 1_000_000) * costs["prompt"]
        completion_cost = (completion_tokens / 1_000_000) * costs["completion"]
        total_cost = prompt_cost + completion_cost

        self.costs[agent_id] += total_cost
        return total_cost

    def get_total_cost(self, agent_id: Optional[str] = None) -> float:
        """Get total cost for an agent or all agents.

        Args:
            agent_id: Agent identifier, or None for all

        Returns:
            Total cost in USD
        """
        if agent_id:
            return self.costs.get(agent_id, 0.0)
        return sum(self.costs.values())

    def reset(self, agent_id: Optional[str] = None) -> None:
        """Reset costs for an agent or all agents.

        Args:
            agent_id: Agent identifier, or None for all
        """
        if agent_id:
            self.costs.pop(agent_id, None)
        else:
            self.costs.clear()


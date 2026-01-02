"""State storage abstraction for the orchestration layer."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from redis import Redis


class StateStore(ABC):
    """Abstract interface for state storage."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get a value from the store."""
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in the store."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a value from the store."""
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Check if a key exists."""
        pass

    @abstractmethod
    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter."""
        pass


class RedisStateStore(StateStore):
    """Redis-based state store."""

    def __init__(self, redis_client: Redis):
        """Initialize with a Redis client."""
        self.redis = redis_client

    async def get(self, key: str) -> Optional[Any]:
        """Get a value from Redis."""
        import json

        value = self.redis.get(key)
        if value is None:
            return None
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value.decode("utf-8")

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set a value in Redis."""
        import json

        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        elif not isinstance(value, (str, bytes)):
            value = str(value)

        if ttl:
            self.redis.setex(key, ttl, value)
        else:
            self.redis.set(key, value)

    async def delete(self, key: str) -> None:
        """Delete a value from Redis."""
        self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if a key exists in Redis."""
        return bool(self.redis.exists(key))

    async def increment(self, key: str, amount: int = 1) -> int:
        """Increment a counter in Redis."""
        return self.redis.incrby(key, amount)


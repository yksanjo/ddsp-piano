"""Base integration adapter."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Adapter(ABC):
    """Base adapter for external service integration."""

    def __init__(self, adapter_id: str, name: str, config: Dict[str, Any]):
        """Initialize adapter.

        Args:
            adapter_id: Unique adapter identifier
            name: Adapter name
            config: Configuration (API keys, endpoints, etc.)
        """
        self.id = adapter_id
        self.name = name
        self.config = config

    @abstractmethod
    async def call(self, method: str, endpoint: str, **kwargs: Any) -> Any:
        """Make an API call.

        Args:
            method: HTTP method
            endpoint: API endpoint
            **kwargs: Additional parameters

        Returns:
            API response
        """
        pass

    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the service.

        Returns:
            True if authentication successful
        """
        pass


class AdapterRegistry:
    """Registry for managing adapters."""

    def __init__(self):
        """Initialize adapter registry."""
        self._adapters: Dict[str, Adapter] = {}

    def register(self, adapter: Adapter) -> None:
        """Register an adapter.

        Args:
            adapter: Adapter instance
        """
        self._adapters[adapter.id] = adapter

    def get(self, adapter_id: str) -> Optional[Adapter]:
        """Get an adapter by ID.

        Args:
            adapter_id: Adapter identifier

        Returns:
            Adapter instance or None
        """
        return self._adapters.get(adapter_id)

    def list(self) -> list[str]:
        """List all registered adapter IDs.

        Returns:
            List of adapter IDs
        """
        return list(self._adapters.keys())


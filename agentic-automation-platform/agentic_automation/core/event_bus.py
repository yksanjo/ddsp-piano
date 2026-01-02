"""Event bus for agent communication."""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, Optional

from pydantic import BaseModel


class Event(BaseModel):
    """Event model."""

    event_type: str
    source: str
    target: Optional[str] = None
    payload: Dict[str, Any]
    timestamp: float
    correlation_id: Optional[str] = None


class EventBus(ABC):
    """Abstract event bus interface."""

    @abstractmethod
    async def publish(self, event: Event) -> None:
        """Publish an event."""
        pass

    @abstractmethod
    async def subscribe(
        self, event_type: str, handler: Callable[[Event], None]
    ) -> str:
        """Subscribe to events of a specific type. Returns subscription ID."""
        pass

    @abstractmethod
    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from events."""
        pass


class InMemoryEventBus(EventBus):
    """In-memory event bus implementation (for testing/development)."""

    def __init__(self):
        """Initialize the in-memory event bus."""
        self._subscribers: Dict[str, Dict[str, Callable[[Event], None]]] = {}
        self._subscription_counter = 0

    async def publish(self, event: Event) -> None:
        """Publish an event to all subscribers."""
        subscribers = self._subscribers.get(event.event_type, {})
        for handler in subscribers.values():
            try:
                await handler(event) if hasattr(handler, "__await__") else handler(event)
            except Exception as e:
                # Log error but don't fail
                print(f"Error in event handler: {e}")

    async def subscribe(
        self, event_type: str, handler: Callable[[Event], None]
    ) -> str:
        """Subscribe to events of a specific type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = {}
        subscription_id = f"sub_{self._subscription_counter}"
        self._subscription_counter += 1
        self._subscribers[event_type][subscription_id] = handler
        return subscription_id

    async def unsubscribe(self, subscription_id: str) -> None:
        """Unsubscribe from events."""
        for event_type, subscribers in self._subscribers.items():
            if subscription_id in subscribers:
                del subscribers[subscription_id]
                break


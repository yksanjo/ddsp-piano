"""Memory manager for agents."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class MemoryManager(ABC):
    """Abstract memory manager interface."""

    @abstractmethod
    async def store_interaction(
        self,
        task: str,
        response: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store an interaction in memory.

        Args:
            task: Task or prompt
            response: Agent response
            context: Additional context
        """
        pass

    @abstractmethod
    async def retrieve_relevant(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        limit: int = 5,
    ) -> Optional[str]:
        """Retrieve relevant memories for a query.

        Args:
            query: Search query
            context: Additional context
            limit: Maximum number of memories to retrieve

        Returns:
            Relevant memory context or None
        """
        pass

    @abstractmethod
    async def clear(self) -> None:
        """Clear all memories."""
        pass


class ShortTermMemory(MemoryManager):
    """In-memory short-term memory (session-based)."""

    def __init__(self, max_size: int = 100):
        """Initialize short-term memory.

        Args:
            max_size: Maximum number of interactions to store
        """
        self.max_size = max_size
        self.interactions: List[Dict[str, Any]] = []

    async def store_interaction(
        self,
        task: str,
        response: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store interaction in short-term memory."""
        interaction = {
            "task": task,
            "response": str(response),
            "context": context or {},
        }
        self.interactions.append(interaction)

        # Limit size
        if len(self.interactions) > self.max_size:
            self.interactions = self.interactions[-self.max_size :]

    async def retrieve_relevant(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        limit: int = 5,
    ) -> Optional[str]:
        """Retrieve recent interactions (simple implementation)."""
        if not self.interactions:
            return None

        # Return most recent interactions
        recent = self.interactions[-limit:]
        context_str = "\n".join(
            f"Q: {i['task']}\nA: {i['response']}" for i in recent
        )
        return context_str

    async def clear(self) -> None:
        """Clear all interactions."""
        self.interactions.clear()


class LongTermMemory(MemoryManager):
    """Vector-based long-term memory."""

    def __init__(self, vector_db: Any = None):  # Vector DB client
        """Initialize long-term memory.

        Args:
            vector_db: Vector database client (Weaviate, Qdrant, etc.)
        """
        self.vector_db = vector_db
        self.collection_name = "agent_memories"

    async def store_interaction(
        self,
        task: str,
        response: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store interaction in vector database."""
        if not self.vector_db:
            return  # No vector DB configured

        # Create embedding-friendly text
        text = f"Task: {task}\nResponse: {response}"
        if context:
            context_str = " ".join(f"{k}: {v}" for k, v in context.items())
            text += f"\nContext: {context_str}"

        # Store in vector DB (implementation depends on vector DB)
        # This is a placeholder - actual implementation would use vector DB SDK
        pass

    async def retrieve_relevant(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        limit: int = 5,
    ) -> Optional[str]:
        """Retrieve relevant memories using semantic search."""
        if not self.vector_db:
            return None

        # Semantic search in vector DB (placeholder)
        # Actual implementation would:
        # 1. Generate embedding for query
        # 2. Search similar vectors
        # 3. Return top results
        return None

    async def clear(self) -> None:
        """Clear all memories from vector database."""
        if self.vector_db:
            # Clear collection (implementation depends on vector DB)
            pass


class HybridMemoryManager(MemoryManager):
    """Combines short-term and long-term memory."""

    def __init__(
        self,
        short_term: Optional[ShortTermMemory] = None,
        long_term: Optional[LongTermMemory] = None,
    ):
        """Initialize hybrid memory manager.

        Args:
            short_term: Short-term memory instance
            long_term: Long-term memory instance
        """
        self.short_term = short_term or ShortTermMemory()
        self.long_term = long_term

    async def store_interaction(
        self,
        task: str,
        response: Any,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Store in both short-term and long-term memory."""
        await self.short_term.store_interaction(task, response, context)
        if self.long_term:
            await self.long_term.store_interaction(task, response, context)

    async def retrieve_relevant(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        limit: int = 5,
    ) -> Optional[str]:
        """Retrieve from both short-term and long-term memory."""
        short_term_context = await self.short_term.retrieve_relevant(query, context, limit)
        long_term_context = None

        if self.long_term:
            long_term_context = await self.long_term.retrieve_relevant(query, context, limit)

        # Combine contexts
        contexts = []
        if short_term_context:
            contexts.append(f"Recent context:\n{short_term_context}")
        if long_term_context:
            contexts.append(f"Relevant history:\n{long_term_context}")

        return "\n\n".join(contexts) if contexts else None

    async def clear(self) -> None:
        """Clear both memories."""
        await self.short_term.clear()
        if self.long_term:
            await self.long_term.clear()


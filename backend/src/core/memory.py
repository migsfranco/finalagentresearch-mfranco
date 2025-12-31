"""Memory management for agent conversations."""

from typing import Any

from langgraph.checkpoint.memory import MemorySaver


class MemoryManager:
    """Manage conversation memory for the agent.

    Wraps LangGraph's MemorySaver with additional functionality.
    """

    def __init__(self):
        """Initialize memory manager."""
        self._memory_saver = MemorySaver()
        self._active_threads: dict[str, Any] = {}

    @property
    def checkpointer(self) -> MemorySaver:
        """Get the underlying checkpointer.

        Returns:
            MemorySaver instance for use with LangGraph agent.
        """
        return self._memory_saver

    def get_config(self, thread_id: str) -> dict[str, Any]:
        """Get configuration for a conversation thread.

        Args:
            thread_id: Unique identifier for the conversation.

        Returns:
            Configuration dict for the agent.
        """
        if thread_id not in self._active_threads:
            self._active_threads[thread_id] = {"created": True}

        return {"configurable": {"thread_id": thread_id}}

    def list_threads(self) -> list[str]:
        """List all active thread IDs.

        Returns:
            List of thread IDs.
        """
        return list(self._active_threads.keys())

    def thread_exists(self, thread_id: str) -> bool:
        """Check if a thread exists.

        Args:
            thread_id: Thread ID to check.

        Returns:
            True if thread exists.
        """
        return thread_id in self._active_threads

    def create_thread(self, thread_id: str) -> dict[str, Any]:
        """Create a new conversation thread.

        Args:
            thread_id: Unique identifier for the new thread.

        Returns:
            Configuration for the new thread.
        """
        self._active_threads[thread_id] = {"created": True}
        return self.get_config(thread_id)

    def delete_thread(self, thread_id: str) -> bool:
        """Delete a conversation thread.

        Args:
            thread_id: Thread ID to delete.

        Returns:
            True if thread was deleted, False if not found.
        """
        if thread_id in self._active_threads:
            del self._active_threads[thread_id]
            return True
        return False

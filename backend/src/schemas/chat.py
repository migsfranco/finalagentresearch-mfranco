"""Chat request/response schemas."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MessageRole(str, Enum):
    """Message role enum."""

    USER = "user"
    HUMAN = "human"  # LangChain uses 'human' for user messages
    ASSISTANT = "assistant"
    AI = "ai"  # LangChain uses 'ai' for assistant messages
    SYSTEM = "system"
    TOOL = "tool"


class Message(BaseModel):
    """A single message in the conversation."""

    role: MessageRole
    content: str
    tool_calls: list[dict[str, Any]] | None = None
    tool_call_id: str | None = None

    class Config:
        use_enum_values = True


class ChatRequest(BaseModel):
    """Request schema for chat endpoint."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="The user's message",
    )
    thread_id: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Unique identifier for the conversation thread",
    )


class ChatResponse(BaseModel):
    """Response schema for chat endpoint."""

    thread_id: str
    messages: list[Message]
    final_response: str


class StreamChunk(BaseModel):
    """Schema for streaming response chunks."""

    type: str = Field(
        ...,
        description="Type of chunk: 'message', 'tool_call', 'tool_result', 'done'",
    )
    content: str | None = None
    tool_name: str | None = None
    tool_input: dict[str, Any] | None = None
    tool_output: str | None = None


class ConversationHistory(BaseModel):
    """Schema for conversation history."""

    thread_id: str
    messages: list[Message]
    created_at: str | None = None
    updated_at: str | None = None

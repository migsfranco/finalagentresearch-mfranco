"""Chat endpoints for the research agent."""

import logging
from typing import Any, AsyncGenerator

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from langchain_core.messages import HumanMessage

from ...config import get_settings
from ...core import AgentFactory
from ...schemas import ChatRequest, ChatResponse, Message, MessageRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["chat"])

# Global agent factory (initialized once)
_agent_factory: AgentFactory | None = None
_agent: Any = None


def _check_api_key() -> None:
    """Check if OpenAI API key is configured."""
    settings = get_settings()
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=503,
            detail="OpenAI API key not configured. Set OPENAI_API_KEY environment variable.",
        )


def get_agent_factory() -> AgentFactory:
    """Get or create the agent factory singleton.

    Returns:
        AgentFactory instance.
    """
    global _agent_factory
    if _agent_factory is None:
        _agent_factory = AgentFactory()
    return _agent_factory


def get_agent() -> Any:
    """Get or create the agent singleton.

    Returns:
        Configured agent instance.
    """
    global _agent
    if _agent is None:
        factory = get_agent_factory()
        _agent = factory.create_agent()
    return _agent


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Send a message to the research agent.

    Args:
        request: Chat request with message and thread_id.

    Returns:
        Chat response with agent's reply.
    """
    _check_api_key()
    try:
        agent = get_agent()
        factory = get_agent_factory()
        config = factory.get_thread_config(request.thread_id)

        # Create human message
        human_message = HumanMessage(content=request.message)

        # Run agent
        messages_list: list[Message] = []
        final_response = ""

        for step in agent.stream(
            {"messages": [human_message]},
            config,
            stream_mode="values",
        ):
            last_message = step["messages"][-1]

            # Convert to our schema
            if hasattr(last_message, "type"):
                role = MessageRole(last_message.type)
            else:
                role = MessageRole.ASSISTANT

            message = Message(
                role=role,
                content=last_message.content if hasattr(last_message, "content") else str(last_message),
            )
            messages_list.append(message)
            final_response = message.content

        return ChatResponse(
            thread_id=request.thread_id,
            messages=messages_list,
            final_response=final_response,
        )

    except Exception as e:
        logger.exception("Error processing chat request")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {e}",
        )


@router.post("/stream")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    """Stream responses from the research agent.

    Args:
        request: Chat request with message and thread_id.

    Returns:
        Streaming response with agent's reply.
    """
    _check_api_key()

    async def generate() -> AsyncGenerator[str, None]:
        try:
            agent = get_agent()
            factory = get_agent_factory()
            config = factory.get_thread_config(request.thread_id)

            human_message = HumanMessage(content=request.message)

            for step in agent.stream(
                {"messages": [human_message]},
                config,
                stream_mode="values",
            ):
                last_message = step["messages"][-1]
                content = last_message.content if hasattr(last_message, "content") else str(last_message)

                # Yield as Server-Sent Events format
                yield f"data: {content}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.exception("Error in streaming chat")
            yield f"data: Error: {e}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
    )


@router.delete("/{thread_id}")
async def delete_thread(thread_id: str) -> dict[str, str]:
    """Delete a conversation thread.

    Args:
        thread_id: Thread ID to delete.

    Returns:
        Deletion status.
    """
    factory = get_agent_factory()
    deleted = factory.memory_manager.delete_thread(thread_id)

    if deleted:
        return {"status": "deleted", "thread_id": thread_id}
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Thread '{thread_id}' not found",
        )

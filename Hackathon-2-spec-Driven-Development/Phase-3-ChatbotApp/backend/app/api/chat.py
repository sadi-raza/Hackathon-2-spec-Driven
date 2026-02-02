"""
Chat API Router for Phase III Chatbot.

Provides the POST /{user_id}/chat endpoint for chat interactions.
All requests require JWT authentication.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.chat import ChatRequest, ChatResponse, ToolCallResult
from ..services.chat_service import ChatService
from ..database import get_db
from ..middleware.jwt import CurrentUser


router = APIRouter(tags=["chat"])


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: int,
    request: ChatRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Process a chat message and return the AI response.

    The user_id in the path must match the authenticated user's ID.
    This enforces user isolation and prevents unauthorized access.

    Args:
        user_id: User ID from path (must match authenticated user)
        request: Chat request with message and optional conversation_id
        current_user: Authenticated user from JWT
        db: Database session

    Returns:
        ChatResponse with conversation_id, response, and tool_calls

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 500: If chat processing fails
    """
    # Enforce user isolation - path user_id must match authenticated user
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own chat"
        )

    # Validate message
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    try:
        # Process through ChatService
        chat_service = ChatService(db, current_user.id)
        result = await chat_service.process_message(
            message=request.message.strip(),
            conversation_id=request.conversation_id
        )

        # Convert tool calls to response format
        tool_calls = [
            ToolCallResult(
                tool=tc.get("tool", ""),
                success=tc.get("success", False),
                result=tc.get("result")
            )
            for tc in result.get("tool_calls", [])
        ]

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=tool_calls
        )

    except Exception as e:
        # Log the error for debugging (in production, use proper logging)
        import logging
        logging.error(f"Chat processing error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Failed to process chat message"
        )

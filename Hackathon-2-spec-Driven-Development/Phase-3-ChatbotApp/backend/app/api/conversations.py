"""
Conversations API Router for Phase III Chatbot.

Provides endpoints for retrieving conversation history.
All requests require JWT authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from ..schemas.conversation import (
    ConversationSummary,
    ConversationDetail,
    ConversationListResponse,
    MessageSchema
)
from ..services.conversation_service import ConversationService
from ..database import get_db
from ..middleware.jwt import CurrentUser


router = APIRouter(tags=["conversations"])


@router.get("/{user_id}/conversations", response_model=ConversationListResponse)
async def list_conversations(
    user_id: int,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    limit: int = Query(20, ge=1, le=100, description="Max conversations to return"),
    offset: int = Query(0, ge=0, description="Number of conversations to skip")
):
    """
    List all conversations for a user.

    Args:
        user_id: User ID from path (must match authenticated user)
        current_user: Authenticated user from JWT
        db: Database session
        limit: Maximum conversations to return (default 20, max 100)
        offset: Number of conversations to skip for pagination

    Returns:
        ConversationListResponse with list of conversations and total count

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
    """
    # Enforce user isolation
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own conversations"
        )

    conversation_service = ConversationService(db)
    conversations, total = await conversation_service.get_conversations(
        user_id=current_user.id,
        limit=limit,
        offset=offset
    )

    return ConversationListResponse(
        conversations=[
            ConversationSummary(
                id=conv.id,
                title=conv.title,
                created_at=conv.created_at,
                updated_at=conv.updated_at
            )
            for conv in conversations
        ],
        total=total
    )


@router.get("/{user_id}/conversations/{conversation_id}", response_model=ConversationDetail)
async def get_conversation(
    user_id: int,
    conversation_id: int,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific conversation with its messages.

    Args:
        user_id: User ID from path (must match authenticated user)
        conversation_id: Conversation ID
        current_user: Authenticated user from JWT
        db: Database session

    Returns:
        ConversationDetail with conversation info and messages

    Raises:
        HTTPException 403: If user_id doesn't match authenticated user
        HTTPException 404: If conversation not found
    """
    # Enforce user isolation
    if user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own conversations"
        )

    conversation_service = ConversationService(db)

    # Get conversation
    conversation = await conversation_service.get_conversation(
        conversation_id=conversation_id,
        user_id=current_user.id
    )

    if not conversation:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    # Get messages
    messages = await conversation_service.get_messages(
        conversation_id=conversation_id,
        user_id=current_user.id
    )

    # Convert tool_calls from JSON to list format for response
    def format_tool_calls(tool_calls_json):
        if not tool_calls_json:
            return None
        calls = tool_calls_json.get("calls", [])
        return calls if calls else None

    return ConversationDetail(
        conversation=ConversationSummary(
            id=conversation.id,
            title=conversation.title,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at
        ),
        messages=[
            MessageSchema(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                tool_calls=format_tool_calls(msg.tool_calls),
                created_at=msg.created_at
            )
            for msg in messages
        ]
    )

"""
Conversation Service for Phase III Chatbot.

Handles all conversation and message CRUD operations with user isolation.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import Optional
from datetime import datetime

from ..models.conversation import Conversation
from ..models.message import Message, MessageRole


class ConversationService:
    """
    Service for managing conversations and messages.

    All operations enforce user isolation via user_id filtering.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_conversation(
        self,
        user_id: int,
        title: Optional[str] = None
    ) -> Conversation:
        """
        Create a new conversation for a user.

        Args:
            user_id: The user's ID
            title: Optional conversation title

        Returns:
            The created Conversation
        """
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        self.db.add(conversation)
        await self.db.flush()
        await self.db.refresh(conversation)
        return conversation

    async def get_conversation(
        self,
        conversation_id: int,
        user_id: int
    ) -> Optional[Conversation]:
        """
        Get a conversation by ID, filtered by user_id for isolation.

        Args:
            conversation_id: The conversation's ID
            user_id: The user's ID (for isolation)

        Returns:
            The Conversation if found and owned by user, None otherwise
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await self.db.execute(statement)
        return result.scalar_one_or_none()

    async def get_conversations(
        self,
        user_id: int,
        limit: int = 20,
        offset: int = 0
    ) -> tuple[list[Conversation], int]:
        """
        Get a user's conversations, ordered by most recent.

        Args:
            user_id: The user's ID
            limit: Maximum conversations to return
            offset: Number of conversations to skip

        Returns:
            Tuple of (conversations list, total count)
        """
        # Count total
        count_statement = select(Conversation).where(
            Conversation.user_id == user_id
        )
        count_result = await self.db.execute(count_statement)
        total = len(count_result.scalars().all())

        # Get paginated
        statement = (
            select(Conversation)
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await self.db.execute(statement)
        conversations = list(result.scalars().all())

        return conversations, total

    async def add_message(
        self,
        conversation_id: int,
        user_id: int,
        role: str,
        content: str,
        tool_calls: Optional[dict] = None
    ) -> Message:
        """
        Add a message to a conversation.

        Args:
            conversation_id: The conversation's ID
            user_id: The user's ID
            role: Message role (user/assistant)
            content: Message content
            tool_calls: Optional tool calls data

        Returns:
            The created Message
        """
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        self.db.add(message)

        # Update conversation timestamp
        conversation = await self.get_conversation(conversation_id, user_id)
        if conversation:
            conversation.updated_at = datetime.utcnow()

        await self.db.flush()
        await self.db.refresh(message)
        return message

    async def get_messages(
        self,
        conversation_id: int,
        user_id: int
    ) -> list[Message]:
        """
        Get all messages in a conversation, ordered chronologically.

        Args:
            conversation_id: The conversation's ID
            user_id: The user's ID (for isolation)

        Returns:
            List of messages in chronological order
        """
        statement = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.user_id == user_id
            )
            .order_by(Message.created_at.asc())
        )
        result = await self.db.execute(statement)
        return list(result.scalars().all())

    async def get_or_create_conversation(
        self,
        user_id: int,
        conversation_id: Optional[int] = None,
        title: Optional[str] = None
    ) -> Conversation:
        """
        Get an existing conversation or create a new one.

        Args:
            user_id: The user's ID
            conversation_id: Optional existing conversation ID
            title: Optional title for new conversation

        Returns:
            Existing or newly created Conversation
        """
        if conversation_id:
            conversation = await self.get_conversation(conversation_id, user_id)
            if conversation:
                return conversation

        # Create new conversation
        return await self.create_conversation(user_id, title)

    async def update_conversation_title(
        self,
        conversation_id: int,
        user_id: int,
        title: str
    ) -> Optional[Conversation]:
        """
        Update a conversation's title.

        Args:
            conversation_id: The conversation's ID
            user_id: The user's ID
            title: New title

        Returns:
            Updated Conversation or None if not found
        """
        conversation = await self.get_conversation(conversation_id, user_id)
        if not conversation:
            return None

        conversation.title = title[:100] if title else None
        conversation.updated_at = datetime.utcnow()
        await self.db.flush()
        await self.db.refresh(conversation)
        return conversation

"""
Chat Service for Phase III Chatbot.

Orchestrates the chat flow:
1. Get or create conversation
2. Save user message
3. Process through TodoAgent
4. Save assistant response
5. Return response with tool calls
"""

from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession

from .conversation_service import ConversationService
from ..agent.todo_agent import TodoAgent
from ..utils.urdu import detect_urdu


class ChatService:
    """
    Service for orchestrating chat interactions.

    Stateless design - all state is persisted in the database.
    """

    def __init__(self, db: AsyncSession, user_id: int):
        """
        Initialize the ChatService.

        Args:
            db: Database session
            user_id: User ID for ownership
        """
        self.db = db
        self.user_id = user_id
        self.conversation_service = ConversationService(db)
        self.agent = TodoAgent(db, user_id)

    async def process_message(
        self,
        message: str,
        conversation_id: Optional[int] = None
    ) -> dict[str, Any]:
        """
        Process a chat message and return the response.

        Args:
            message: User's message
            conversation_id: Optional existing conversation ID

        Returns:
            Dictionary with conversation_id, response, and tool_calls
        """
        # Get or create conversation
        conversation = await self.conversation_service.get_or_create_conversation(
            user_id=self.user_id,
            conversation_id=conversation_id,
            title=self._generate_title(message)
        )

        # Save user message
        await self.conversation_service.add_message(
            conversation_id=conversation.id,
            user_id=self.user_id,
            role="user",
            content=message
        )

        # Load conversation history for context
        history = await self._build_conversation_history(conversation.id)

        # Process through agent
        try:
            result = await self.agent.process_message(
                message=message,
                conversation_history=history[:-1]  # Exclude the message we just added
            )
        except Exception as e:
            # Handle agent errors gracefully
            result = {
                "response": self._get_error_response(message, str(e)),
                "tool_calls": [],
                "is_urdu": detect_urdu(message)
            }

        # Save assistant response
        await self.conversation_service.add_message(
            conversation_id=conversation.id,
            user_id=self.user_id,
            role="assistant",
            content=result["response"],
            tool_calls={"calls": result.get("tool_calls", [])} if result.get("tool_calls") else None
        )

        # Commit all changes
        await self.db.commit()

        # Format tool calls for response
        formatted_tool_calls = [
            {
                "tool": tc.get("tool", ""),
                "success": tc.get("success", False),
                "result": tc.get("result", "")
            }
            for tc in result.get("tool_calls", [])
        ]

        return {
            "conversation_id": conversation.id,
            "response": result["response"],
            "tool_calls": formatted_tool_calls
        }

    async def _build_conversation_history(
        self,
        conversation_id: int
    ) -> list[dict[str, str]]:
        """
        Build conversation history for agent context.

        Args:
            conversation_id: Conversation ID

        Returns:
            List of message dictionaries for the agent
        """
        messages = await self.conversation_service.get_messages(
            conversation_id=conversation_id,
            user_id=self.user_id
        )

        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

    def _generate_title(self, first_message: str) -> str:
        """
        Generate a conversation title from the first message.

        Args:
            first_message: User's first message

        Returns:
            Generated title (truncated to 50 chars)
        """
        # Take first 50 characters of the message
        title = first_message[:50]
        if len(first_message) > 50:
            title += "..."
        return title

    def _get_error_response(self, message: str, error: str) -> str:
        """
        Generate a user-friendly error response.

        Args:
            message: Original user message
            error: Error message

        Returns:
            User-friendly error response
        """
        is_urdu = detect_urdu(message)

        if is_urdu:
            return "کچھ غلط ہو گیا۔ براہ کرم دوبارہ کوشش کریں۔"

        return "I'm having trouble processing that request. Please try again in a moment."

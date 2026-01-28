"""
Todo Agent for Phase III Chatbot.

Uses Cohere API for LLM reasoning and MCP tools for task operations.
All LLM calls go through the Cohere API as mandated by the constitution.
"""

from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession

from .cohere_model import CohereModel
from ..mcp.tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
    TOOL_DEFINITIONS
)
from ..utils.urdu import detect_urdu, get_urdu_confirmation


# System prompt for the Todo Agent
SYSTEM_PROMPT = """You are a helpful todo assistant. You help users manage their tasks through natural language.

Available actions:
- Add tasks: "Add buy milk", "Create a task to call mom"
- List tasks: "Show my tasks", "What's on my list?"
- Complete tasks: "Complete task X", "Mark task X as done"
- Delete tasks: "Delete task X", "Remove task X"
- Update tasks: "Update task X title to Y", "Change task X description"

When the user wants to perform an action, use the appropriate tool.
Always be helpful and confirm actions clearly.

For task IDs, users may refer to tasks by their position in the list (1, 2, 3...) or by title.
If the user says "complete task 1", you should use the first task's ID.

Keep responses concise and friendly."""

URDU_SYSTEM_PROMPT = """آپ ایک مددگار ٹوڈو اسسٹنٹ ہیں۔ آپ صارفین کو قدرتی زبان کے ذریعے ان کے کاموں کا انتظام کرنے میں مدد کرتے ہیں۔

دستیاب اعمال:
- کام شامل کریں: "دودھ خریدنا شامل کریں"
- کام دکھائیں: "میرے کام دکھائیں"
- کام مکمل کریں: "کام X مکمل کریں"
- کام حذف کریں: "کام X حذف کریں"

جب صارف کوئی عمل کرنا چاہتا ہے تو مناسب ٹول استعمال کریں۔
ہمیشہ مددگار رہیں اور اعمال کی واضح تصدیق کریں۔"""


class TodoAgent:
    """
    Agent for processing natural language todo requests.

    Uses Cohere for reasoning and understanding user intent,
    then executes the appropriate MCP tool.
    """

    def __init__(self, db: AsyncSession, user_id: int):
        """
        Initialize the TodoAgent.

        Args:
            db: Database session for tool execution
            user_id: User ID for ownership enforcement
        """
        self.db = db
        self.user_id = user_id
        self.model = CohereModel()
        self._task_cache: Optional[list] = None

    async def process_message(
        self,
        message: str,
        conversation_history: Optional[list[dict]] = None
    ) -> dict[str, Any]:
        """
        Process a user message and execute the appropriate action.

        Args:
            message: User's natural language message
            conversation_history: Previous messages for context

        Returns:
            Dictionary with response content and any tool calls made
        """
        # Detect if message is in Urdu
        is_urdu = detect_urdu(message)
        system_prompt = URDU_SYSTEM_PROMPT if is_urdu else SYSTEM_PROMPT

        # Build messages for the model
        messages = []
        if conversation_history:
            messages.extend(conversation_history)
        messages.append({"role": "user", "content": message})

        # Call Cohere for reasoning
        response = await self.model.chat(
            messages=messages,
            tools=TOOL_DEFINITIONS,
            system_prompt=system_prompt
        )

        tool_calls_results = []

        # Execute any tool calls
        if response.get("tool_calls"):
            for tool_call in response["tool_calls"]:
                result = await self._execute_tool(
                    tool_call["name"],
                    tool_call.get("arguments", {}),
                    is_urdu
                )
                tool_calls_results.append(result)

        # Build final response
        final_response = response.get("content", "")

        # If we have tool results, incorporate them into the response
        if tool_calls_results:
            # Use the tool result message if no LLM content
            if not final_response:
                final_response = self._format_tool_response(
                    tool_calls_results,
                    is_urdu
                )

        return {
            "response": final_response,
            "tool_calls": tool_calls_results,
            "is_urdu": is_urdu
        }

    async def _execute_tool(
        self,
        tool_name: str,
        arguments: dict,
        is_urdu: bool = False
    ) -> dict[str, Any]:
        """
        Execute a tool and return the result.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments
            is_urdu: Whether to use Urdu confirmations

        Returns:
            Tool execution result
        """
        try:
            if tool_name == "add_task":
                result = await add_task(
                    db=self.db,
                    user_id=self.user_id,
                    title=arguments.get("title", ""),
                    description=arguments.get("description")
                )
            elif tool_name == "list_tasks":
                result = await list_tasks(
                    db=self.db,
                    user_id=self.user_id,
                    completed=arguments.get("completed")
                )
                # Cache tasks for reference by position
                self._task_cache = result.get("tasks", [])
            elif tool_name == "complete_task":
                task_id = await self._resolve_task_id(
                    arguments.get("task_id", "")
                )
                result = await complete_task(
                    db=self.db,
                    user_id=self.user_id,
                    task_id=task_id
                )
            elif tool_name == "delete_task":
                task_id = await self._resolve_task_id(
                    arguments.get("task_id", "")
                )
                result = await delete_task(
                    db=self.db,
                    user_id=self.user_id,
                    task_id=task_id
                )
            elif tool_name == "update_task":
                task_id = await self._resolve_task_id(
                    arguments.get("task_id", "")
                )
                result = await update_task(
                    db=self.db,
                    user_id=self.user_id,
                    task_id=task_id,
                    title=arguments.get("title"),
                    description=arguments.get("description")
                )
            else:
                result = {
                    "success": False,
                    "error": f"Unknown tool: {tool_name}"
                }

            # Add Urdu confirmation if needed
            if is_urdu and result.get("success"):
                urdu_key = self._get_urdu_key(tool_name)
                if urdu_key:
                    result["urdu_message"] = get_urdu_confirmation(
                        urdu_key,
                        title=result.get("title", "")
                    )

            return {
                "tool": tool_name,
                "success": result.get("success", False),
                "result": result.get("message", ""),
                "data": result
            }

        except Exception as e:
            return {
                "tool": tool_name,
                "success": False,
                "result": str(e),
                "error": str(e)
            }

    async def _resolve_task_id(self, task_ref: str | int) -> int:
        """
        Resolve a task reference to an actual task ID.

        Handles numeric references (1, 2, 3) by looking up the task
        at that position in the user's task list.

        Args:
            task_ref: Task reference (ID or position number)

        Returns:
            Resolved task ID as integer
        """
        # If already an int, return as-is
        if isinstance(task_ref, int):
            return task_ref

        # Try to parse as a number (could be position or actual ID)
        try:
            task_id = int(task_ref)

            # If small number, might be position reference
            if task_id <= 100:
                # Fetch tasks if not cached
                if self._task_cache is None:
                    result = await list_tasks(
                        db=self.db,
                        user_id=self.user_id
                    )
                    self._task_cache = result.get("tasks", [])

                # Get task at position (1-indexed)
                if 0 < task_id <= len(self._task_cache):
                    return self._task_cache[task_id - 1]["id"]

            # Otherwise, assume it's the actual task ID
            return task_id

        except (ValueError, IndexError):
            pass

        # Default to 0 if we can't resolve (will fail gracefully)
        return 0

    def _get_urdu_key(self, tool_name: str) -> Optional[str]:
        """Map tool name to Urdu confirmation key."""
        mapping = {
            "add_task": "task_added",
            "complete_task": "task_completed",
            "delete_task": "task_deleted",
            "update_task": "task_updated",
        }
        return mapping.get(tool_name)

    def _format_tool_response(
        self,
        tool_results: list[dict],
        is_urdu: bool
    ) -> str:
        """
        Format tool results into a human-readable response.

        Args:
            tool_results: List of tool execution results
            is_urdu: Whether to use Urdu formatting

        Returns:
            Formatted response string
        """
        responses = []
        for result in tool_results:
            if result.get("success"):
                # Use Urdu message if available and requested
                if is_urdu and result.get("data", {}).get("urdu_message"):
                    responses.append(result["data"]["urdu_message"])
                else:
                    responses.append(result.get("result", "Done!"))
            else:
                error = result.get("error", result.get("result", "An error occurred"))
                responses.append(f"Error: {error}")

        return "\n".join(responses)


def create_todo_agent(db: AsyncSession, user_id: int) -> TodoAgent:
    """
    Factory function to create a TodoAgent instance.

    Args:
        db: Database session
        user_id: User ID for ownership

    Returns:
        Configured TodoAgent instance
    """
    return TodoAgent(db=db, user_id=user_id)

"""
Cohere Model Wrapper for Phase III Chatbot.

Provides a wrapper around Cohere's API for use with the OpenAI Agents SDK.
All LLM reasoning uses the Cohere API key as mandated by the constitution.
"""

from typing import Any, Optional
import cohere

from ..config import settings


class CohereModel:
    """
    Wrapper for Cohere's Chat API.

    This class provides a simple interface for chat completions
    using Cohere's Command A model (command-a-03-2025).
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Cohere model.

        Args:
            api_key: Cohere API key. If not provided, reads from COHERE_API_KEY env var.
        """
        self.api_key = api_key or settings.COHERE_API_KEY
        if not self.api_key:
            raise ValueError("COHERE_API_KEY environment variable is required")

        self.client = cohere.ClientV2(api_key=self.api_key)
        self.model = "command-a-03-2025"

    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: Optional[list[dict[str, Any]]] = None,
        system_prompt: Optional[str] = None
    ) -> dict[str, Any]:
        """
        Send a chat request to Cohere.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            tools: Optional list of tool definitions
            system_prompt: Optional system prompt to prepend

        Returns:
            Response dictionary with 'content' and optionally 'tool_calls'
        """
        # Convert messages to Cohere format
        cohere_messages = self._convert_messages(messages)

        # Add system prompt if provided
        if system_prompt:
            cohere_messages.insert(0, {
                "role": "system",
                "content": system_prompt
            })

        try:
            # Make the API call
            response = self.client.chat(
                model=self.model,
                messages=cohere_messages,
                tools=self._convert_tools(tools) if tools else None
            )

            return self._convert_response(response)

        except cohere.errors.CohereAPIError as e:
            return {
                "content": "I'm having trouble connecting right now. Please try again in a moment.",
                "error": str(e),
                "tool_calls": []
            }

    def _convert_messages(
        self,
        messages: list[dict[str, Any]]
    ) -> list[dict[str, str]]:
        """Convert messages to Cohere format."""
        cohere_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")

            # Map roles to Cohere format
            if role == "assistant":
                cohere_role = "assistant"
            elif role == "system":
                cohere_role = "system"
            else:
                cohere_role = "user"

            cohere_messages.append({
                "role": cohere_role,
                "content": content
            })

        return cohere_messages

    def _convert_tools(
        self,
        tools: Optional[list[dict[str, Any]]]
    ) -> Optional[list[dict[str, Any]]]:
        """Convert tools to Cohere format."""
        if not tools:
            return None

        cohere_tools = []
        for tool in tools:
            cohere_tool = {
                "type": "function",
                "function": {
                    "name": tool.get("name", ""),
                    "description": tool.get("description", ""),
                    "parameters": tool.get("parameters", {})
                }
            }
            cohere_tools.append(cohere_tool)

        return cohere_tools

    def _convert_response(self, response: Any) -> dict[str, Any]:
        """Convert Cohere response to standard format."""
        import json

        result = {
            "content": "",
            "tool_calls": []
        }

        # Extract text content
        if hasattr(response, "message") and response.message:
            if hasattr(response.message, "content") and response.message.content:
                for content_block in response.message.content:
                    if hasattr(content_block, "text"):
                        result["content"] += content_block.text

        # Extract tool calls if present
        # Cohere V2 API returns tool_calls with nested function object
        if hasattr(response, "message") and response.message:
            if hasattr(response.message, "tool_calls") and response.message.tool_calls:
                for tool_call in response.message.tool_calls:
                    # Cohere V2 uses function.name and function.arguments
                    if hasattr(tool_call, "function") and tool_call.function:
                        func = tool_call.function
                        # Arguments come as JSON string, need to parse
                        arguments = getattr(func, "arguments", "{}")
                        if isinstance(arguments, str):
                            try:
                                arguments = json.loads(arguments)
                            except json.JSONDecodeError:
                                arguments = {}

                        result["tool_calls"].append({
                            "id": getattr(tool_call, "id", ""),
                            "name": getattr(func, "name", ""),
                            "arguments": arguments
                        })
                    else:
                        # Fallback for older format
                        result["tool_calls"].append({
                            "id": getattr(tool_call, "id", ""),
                            "name": getattr(tool_call, "name", ""),
                            "arguments": getattr(tool_call, "parameters", {})
                        })

        return result


def create_cohere_model(api_key: Optional[str] = None) -> CohereModel:
    """
    Factory function to create a CohereModel instance.

    Args:
        api_key: Optional Cohere API key

    Returns:
        Configured CohereModel instance
    """
    return CohereModel(api_key=api_key)

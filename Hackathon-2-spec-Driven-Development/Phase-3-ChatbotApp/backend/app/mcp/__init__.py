"""
MCP (Model Context Protocol) Server Module for Phase III Chatbot.

This module provides stateless MCP tools for task management operations.
All tools enforce user isolation via user_id filtering.
"""

from .tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
    get_mcp_tools,
)

__all__ = [
    "add_task",
    "list_tasks",
    "complete_task",
    "delete_task",
    "update_task",
    "get_mcp_tools",
]

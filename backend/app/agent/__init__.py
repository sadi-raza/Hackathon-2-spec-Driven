"""
AI Agent Module for Phase III Chatbot.

This module provides the AI agent logic using OpenAI Agents SDK
with Cohere as the LLM backend for all reasoning.
"""

from .cohere_model import CohereModel
from .todo_agent import TodoAgent, create_todo_agent

__all__ = [
    "CohereModel",
    "TodoAgent",
    "create_todo_agent",
]

"""
Utility Functions for Phase III Chatbot.

This module provides helper utilities including Urdu language detection.
"""

from .urdu import detect_urdu, is_urdu_text

__all__ = [
    "detect_urdu",
    "is_urdu_text",
]

"""
Urdu Language Detection Utility for Phase III Chatbot.

Provides functions to detect Urdu/Arabic script in text for
multi-language support (+100 bonus points).
"""

import re
from typing import Tuple

# Unicode range for Arabic script (used by Urdu)
# U+0600 to U+06FF covers Arabic, Persian, and Urdu characters
URDU_PATTERN = re.compile(r'[\u0600-\u06FF]')

# Extended pattern including Arabic presentation forms
URDU_EXTENDED_PATTERN = re.compile(r'[\u0600-\u06FF\uFB50-\uFDFF\uFE70-\uFEFF]')


def detect_urdu(text: str) -> bool:
    """
    Detect if text contains Urdu/Arabic script characters.

    Args:
        text: Input text to check

    Returns:
        True if Urdu/Arabic characters detected, False otherwise
    """
    if not text:
        return False
    return bool(URDU_PATTERN.search(text))


def is_urdu_text(text: str, threshold: float = 0.3) -> bool:
    """
    Determine if text is primarily Urdu based on character ratio.

    Args:
        text: Input text to analyze
        threshold: Minimum ratio of Urdu characters (default 0.3 = 30%)

    Returns:
        True if text is primarily Urdu, False otherwise
    """
    if not text:
        return False

    # Count Urdu characters
    urdu_chars = len(URDU_EXTENDED_PATTERN.findall(text))

    # Count total non-whitespace characters
    total_chars = len([c for c in text if not c.isspace()])

    if total_chars == 0:
        return False

    ratio = urdu_chars / total_chars
    return ratio >= threshold


def get_language_info(text: str) -> Tuple[str, float]:
    """
    Get language information for text.

    Args:
        text: Input text to analyze

    Returns:
        Tuple of (language_code, confidence)
        - language_code: 'ur' for Urdu, 'en' for English/other
        - confidence: float between 0 and 1
    """
    if not text:
        return ("en", 0.0)

    urdu_chars = len(URDU_EXTENDED_PATTERN.findall(text))
    total_chars = len([c for c in text if not c.isspace()])

    if total_chars == 0:
        return ("en", 0.0)

    urdu_ratio = urdu_chars / total_chars

    if urdu_ratio >= 0.5:
        return ("ur", urdu_ratio)
    elif urdu_ratio >= 0.1:
        return ("ur", urdu_ratio)  # Mixed, but likely Urdu intent
    else:
        return ("en", 1.0 - urdu_ratio)


# Urdu response templates for confirmations
URDU_CONFIRMATIONS = {
    "task_added": "کام '{title}' شامل کر دیا گیا!",
    "task_completed": "کام '{title}' مکمل ہو گیا!",
    "task_deleted": "کام '{title}' حذف کر دیا گیا!",
    "task_updated": "کام '{title}' اپڈیٹ کر دیا گیا!",
    "no_tasks": "آپ کے پاس ابھی کوئی کام نہیں ہے۔",
    "task_not_found": "یہ کام نہیں ملا۔",
    "error": "کچھ غلط ہو گیا۔ براہ کرم دوبارہ کوشش کریں۔",
    "list_header": "آپ کے کام:",
}


def get_urdu_confirmation(key: str, **kwargs) -> str:
    """
    Get an Urdu confirmation message.

    Args:
        key: Confirmation type (task_added, task_completed, etc.)
        **kwargs: Format arguments (e.g., title="Buy milk")

    Returns:
        Formatted Urdu confirmation message
    """
    template = URDU_CONFIRMATIONS.get(key, URDU_CONFIRMATIONS["error"])
    try:
        return template.format(**kwargs)
    except KeyError:
        return template

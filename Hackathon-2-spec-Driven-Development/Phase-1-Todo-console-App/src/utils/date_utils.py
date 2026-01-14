"""
Date and time utilities for the Todo application.

Contains functions for parsing various date formats, calculating recurrence dates,
and formatting dates for display.
"""
from datetime import datetime, timedelta
from typing import Optional
import re
from dateutil import parser


def parse_date_string(date_str: str) -> datetime:
    """
    Parse various date formats including absolute dates and relative dates.

    Supports formats like:
    - Absolute: "2025-12-31", "2025-12-31 14:30", "Dec 31, 2025"
    - Relative: "today", "tomorrow", "in 3 days", "next week", "next monday"
    - Natural: "next friday at 3pm", "in 2 days at 10am"

    Args:
        date_str: String representation of the date

    Returns:
        Parsed datetime object

    Raises:
        ValueError: If the date string cannot be parsed
    """
    if not date_str or not date_str.strip():
        raise ValueError("Date string cannot be empty")

    original_date_str = date_str  # Keep original for error messages
    date_str = date_str.strip().lower()
    now = datetime.now()

    # Handle time in natural language (e.g., "at 3pm", "at 10am") - extract first
    time_match = re.search(r'at\s+(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', date_str)
    has_time = time_match is not None

    # Extract the date part by removing time specification
    if has_time:
        date_part = re.sub(r'\s+at\s+\d{1,2}(?::\d{2})?\s*(am|pm)?', '', date_str).strip()
    else:
        date_part = date_str

    # Handle relative dates
    if date_part == "today":
        base_date = datetime.combine(now.date(), datetime.min.time())
    elif date_part == "tomorrow":
        base_date = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
    elif date_part == "yesterday":
        base_date = datetime.combine(now.date() - timedelta(days=1), datetime.min.time())
    else:
        base_date = None

    # If we found a relative date, apply time if present
    if base_date is not None:
        if has_time:
            try:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                am_pm = time_match.group(3)

                # Validate hour and minute ranges
                if hour < 0 or hour > 12:
                    raise ValueError(f"Invalid hour: {hour}")
                if minute < 0 or minute > 59:
                    raise ValueError(f"Invalid minute: {minute}")

                # Handle 12-hour format
                if am_pm:
                    if am_pm.lower() == 'pm' and hour != 12:
                        hour += 12
                    elif am_pm.lower() == 'am' and hour == 12:
                        hour = 0

                base_date = base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            except (ValueError, IndexError) as e:
                raise ValueError(f"Error parsing time component in: {original_date_str}. {str(e)}")
        return base_date

    # Handle "in N days" format
    match = re.match(r"in\s+(\d+)\s+days?", date_str)
    if match:
        try:
            days = int(match.group(1))
            return now + timedelta(days=days)
        except (ValueError, IndexError):
            raise ValueError(f"Invalid 'in N days' format: {original_date_str}")

    # Handle "in N weeks" format
    match = re.match(r"in\s+(\d+)\s+weeks?", date_str)
    if match:
        try:
            weeks = int(match.group(1))
            return now + timedelta(weeks=weeks)
        except (ValueError, IndexError):
            raise ValueError(f"Invalid 'in N weeks' format: {original_date_str}")

    # Handle "next [day]" format
    days_map = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }

    for day_name, day_num in days_map.items():
        if f"next {day_name}" in date_str:
            try:
                # Find next occurrence of the day
                current_day = now.weekday()
                days_ahead = day_num - current_day
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                return now + timedelta(days=days_ahead)
            except Exception:
                raise ValueError(f"Error calculating 'next {day_name}' date: {original_date_str}")

    # Try to parse the date part with dateutil
    try:
        parsed_date = parser.parse(date_part, default=now)

        # If we have time information, update the time
        if has_time:
            try:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2)) if time_match.group(2) else 0
                am_pm = time_match.group(3)

                # Validate hour and minute ranges
                if hour < 0 or hour > 12:
                    raise ValueError(f"Invalid hour: {hour}")
                if minute < 0 or minute > 59:
                    raise ValueError(f"Invalid minute: {minute}")

                # Handle 12-hour format
                if am_pm:
                    if am_pm.lower() == 'pm' and hour != 12:
                        hour += 12
                    elif am_pm.lower() == 'am' and hour == 12:
                        hour = 0
                    # For 12-hour format, 12 AM is 00:xx in 24-hour format

                parsed_date = parsed_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
            except (ValueError, IndexError) as e:
                raise ValueError(f"Error parsing time component in: {original_date_str}. {str(e)}")

        return parsed_date
    except parser.ParserError:
        raise ValueError(f"Unable to parse date string with dateutil: {original_date_str}")
    except ValueError as e:
        raise ValueError(f"Unable to parse date string: {original_date_str}. {str(e)}")
    except Exception as e:
        raise ValueError(f"Unexpected error parsing date string: {original_date_str}. {str(e)}")


def calculate_next_date(current_date: datetime, recurrence_pattern: str) -> datetime:
    """
    Calculate the next occurrence date based on the recurrence pattern.

    Args:
        current_date: The current date of the task
        recurrence_pattern: The recurrence pattern ("daily", "weekly", "monthly", etc.)

    Returns:
        Next occurrence date based on the pattern
    """
    if recurrence_pattern == "daily":
        return current_date + timedelta(days=1)
    elif recurrence_pattern == "weekly":
        return current_date + timedelta(weeks=1)
    elif recurrence_pattern == "monthly":
        # Add one month - handle month boundaries
        year = current_date.year
        month = current_date.month + 1
        day = current_date.day

        # Handle year overflow
        if month > 12:
            year += 1
            month = 1

        # Handle day overflow (e.g., Jan 31 -> Feb 31 doesn't exist)
        import calendar
        max_day = calendar.monthrange(year, month)[1]
        if day > max_day:
            day = max_day

        return current_date.replace(year=year, month=month, day=day)
    elif recurrence_pattern == "yearly":
        # Add one year - handle leap year edge cases
        year = current_date.year + 1
        month = current_date.month
        day = current_date.day

        # Handle Feb 29 edge case
        import calendar
        max_day = calendar.monthrange(year, month)[1]
        if day > max_day:
            day = max_day

        return current_date.replace(year=year, month=month, day=day)
    elif recurrence_pattern == "every_monday":
        # Find next Monday
        days_ahead = 0 - current_date.weekday()  # Monday is 0
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return current_date + timedelta(days=days_ahead)
    elif recurrence_pattern == "every_tuesday":
        # Find next Tuesday
        days_ahead = 1 - current_date.weekday()  # Tuesday is 1
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return current_date + timedelta(days=days_ahead)
    elif recurrence_pattern == "every_wednesday":
        # Find next Wednesday
        days_ahead = 2 - current_date.weekday()  # Wednesday is 2
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return current_date + timedelta(days=days_ahead)
    elif recurrence_pattern == "every_thursday":
        # Find next Thursday
        days_ahead = 3 - current_date.weekday()  # Thursday is 3
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return current_date + timedelta(days=days_ahead)
    elif recurrence_pattern == "every_friday":
        # Find next Friday
        days_ahead = 4 - current_date.weekday()  # Friday is 4
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return current_date + timedelta(days=days_ahead)
    elif recurrence_pattern == "every_saturday":
        # Find next Saturday
        days_ahead = 5 - current_date.weekday()  # Saturday is 5
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return current_date + timedelta(days=days_ahead)
    elif recurrence_pattern == "every_sunday":
        # Find next Sunday
        days_ahead = 6 - current_date.weekday()  # Sunday is 6
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        return current_date + timedelta(days=days_ahead)
    else:
        raise ValueError(f"Unsupported recurrence pattern: {recurrence_pattern}")


def format_datetime_for_display(dt: datetime) -> str:
    """
    Format datetime for display in the UI.

    Args:
        dt: The datetime to format

    Returns:
        Formatted string representation of the datetime
    """
    return dt.strftime("%Y-%m-%d %H:%M")
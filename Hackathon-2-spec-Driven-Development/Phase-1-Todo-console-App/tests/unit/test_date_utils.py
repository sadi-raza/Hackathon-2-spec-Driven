"""
Unit tests for date utilities module.

Tests date parsing, recurrence calculations, and datetime formatting.
"""
import unittest
from datetime import datetime, timedelta
from src.utils.date_utils import parse_date_string, calculate_next_date, format_datetime_for_display


class TestDateUtils(unittest.TestCase):
    """Test cases for date utility functions."""

    def test_parse_absolute_date_iso(self):
        """Test parsing ISO format dates."""
        result = parse_date_string("2025-12-31")
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 31)

    def test_parse_absolute_datetime(self):
        """Test parsing datetime with time component."""
        result = parse_date_string("2025-12-31 14:30")
        self.assertEqual(result.year, 2025)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 31)
        self.assertEqual(result.hour, 14)
        self.assertEqual(result.minute, 30)

    def test_parse_relative_today(self):
        """Test parsing 'today'."""
        result = parse_date_string("today")
        today = datetime.now().date()
        self.assertEqual(result.date(), today)

    def test_parse_relative_tomorrow(self):
        """Test parsing 'tomorrow'."""
        result = parse_date_string("tomorrow")
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        self.assertEqual(result.date(), tomorrow)

    def test_parse_in_n_days(self):
        """Test parsing 'in N days' format."""
        result = parse_date_string("in 3 days")
        expected = datetime.now() + timedelta(days=3)
        self.assertEqual(result.date(), expected.date())

    def test_parse_in_n_weeks(self):
        """Test parsing 'in N weeks' format."""
        result = parse_date_string("in 2 weeks")
        expected = datetime.now() + timedelta(weeks=2)
        self.assertEqual(result.date(), expected.date())

    def test_parse_next_monday(self):
        """Test parsing 'next monday' format."""
        result = parse_date_string("next monday")
        # Verify it's a Monday (0)
        self.assertEqual(result.weekday(), 0)
        # Verify it's in the future
        self.assertGreater(result, datetime.now())

    def test_parse_natural_with_time(self):
        """Test parsing natural language with time."""
        result = parse_date_string("tomorrow at 3pm")
        tomorrow = (datetime.now() + timedelta(days=1)).date()
        self.assertEqual(result.date(), tomorrow)
        self.assertEqual(result.hour, 15)  # 3 PM = 15:00

    def test_parse_empty_string_raises_error(self):
        """Test that empty string raises ValueError."""
        with self.assertRaises(ValueError):
            parse_date_string("")

    def test_parse_invalid_format_raises_error(self):
        """Test that invalid format raises ValueError."""
        with self.assertRaises(ValueError):
            parse_date_string("not a valid date")

    def test_calculate_next_date_daily(self):
        """Test calculating next date for daily recurrence."""
        current = datetime(2025, 12, 31, 10, 0)
        result = calculate_next_date(current, "daily")
        self.assertEqual(result, datetime(2026, 1, 1, 10, 0))

    def test_calculate_next_date_weekly(self):
        """Test calculating next date for weekly recurrence."""
        current = datetime(2025, 12, 31, 10, 0)
        result = calculate_next_date(current, "weekly")
        self.assertEqual(result, datetime(2026, 1, 7, 10, 0))

    def test_calculate_next_date_monthly(self):
        """Test calculating next date for monthly recurrence."""
        current = datetime(2025, 12, 15, 10, 0)
        result = calculate_next_date(current, "monthly")
        self.assertEqual(result, datetime(2026, 1, 15, 10, 0))

    def test_calculate_next_date_monthly_end_of_month(self):
        """Test calculating next date for monthly recurrence at end of month."""
        # Jan 31 -> Feb 28 (non-leap year)
        current = datetime(2025, 1, 31, 10, 0)
        result = calculate_next_date(current, "monthly")
        self.assertEqual(result.month, 2)
        self.assertEqual(result.day, 28)  # Feb has only 28 days in 2025

    def test_calculate_next_date_yearly(self):
        """Test calculating next date for yearly recurrence."""
        current = datetime(2025, 12, 31, 10, 0)
        result = calculate_next_date(current, "yearly")
        self.assertEqual(result, datetime(2026, 12, 31, 10, 0))

    def test_calculate_next_date_every_monday(self):
        """Test calculating next date for 'every monday' recurrence."""
        # Start from a Monday
        monday = datetime(2025, 12, 29, 10, 0)  # This is a Monday
        result = calculate_next_date(monday, "every_monday")
        # Next Monday should be 7 days later
        self.assertEqual(result.weekday(), 0)
        self.assertEqual(result, monday + timedelta(days=7))

    def test_calculate_next_date_invalid_pattern(self):
        """Test that invalid recurrence pattern raises ValueError."""
        current = datetime(2025, 12, 31, 10, 0)
        with self.assertRaises(ValueError):
            calculate_next_date(current, "invalid_pattern")

    def test_format_datetime_for_display(self):
        """Test datetime formatting for display."""
        dt = datetime(2025, 12, 31, 14, 30)
        result = format_datetime_for_display(dt)
        self.assertEqual(result, "2025-12-31 14:30")


if __name__ == "__main__":
    unittest.main()

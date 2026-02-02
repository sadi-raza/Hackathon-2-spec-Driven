"""
Unit tests for recurring task functionality.

Tests recurring task creation, instance generation, and completion handling.
"""
import unittest
from datetime import datetime, timedelta
from src.services.todo_manager import TodoManager
from src.models.task import Task


class TestRecurringTasks(unittest.TestCase):
    """Test cases for recurring task functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = TodoManager()

    def test_create_recurring_task(self):
        """Test creating a recurring task."""
        task = self.manager.add_task(
            title="Daily Standup",
            description="Morning meeting",
            priority="high",
            due_date=datetime.now() + timedelta(hours=1),
            recurrence="daily"
        )

        self.assertTrue(task.is_recurring_template)
        self.assertEqual(task.recurrence, "daily")
        self.assertIsNone(task.recurrence_parent_id)

    def test_generate_next_occurrence(self):
        """Test generating next occurrence of a recurring task."""
        template = self.manager.add_task(
            title="Weekly Meeting",
            description="Team sync",
            priority="medium",
            due_date=datetime.now() + timedelta(days=1),
            recurrence="weekly"
        )

        next_task = self.manager.generate_next_occurrence(template)

        self.assertEqual(next_task.title, template.title)
        self.assertEqual(next_task.priority, template.priority)
        self.assertEqual(next_task.recurrence, template.recurrence)
        self.assertFalse(next_task.is_recurring_template)
        self.assertEqual(next_task.recurrence_parent_id, template.id)
        self.assertEqual(next_task.status, "pending")

    def test_generate_next_occurrence_updates_due_date(self):
        """Test that next occurrence has updated due date."""
        due_date = datetime(2025, 12, 31, 10, 0)
        template = self.manager.add_task(
            title="Daily Task",
            priority="low",
            due_date=due_date,
            recurrence="daily"
        )

        next_task = self.manager.generate_next_occurrence(template)

        expected_due = datetime(2026, 1, 1, 10, 0)
        self.assertEqual(next_task.due_date, expected_due)

    def test_generate_next_occurrence_non_recurring_raises_error(self):
        """Test that generating next occurrence for non-recurring task raises error."""
        task = self.manager.add_task(
            title="One-time Task",
            priority="medium"
        )

        with self.assertRaises(ValueError):
            self.manager.generate_next_occurrence(task)

    def test_get_recurring_tasks(self):
        """Test getting all recurring task templates."""
        # Create some tasks
        recurring1 = self.manager.add_task(
            title="Recurring 1",
            recurrence="daily"
        )
        non_recurring = self.manager.add_task(
            title="Non-recurring"
        )
        recurring2 = self.manager.add_task(
            title="Recurring 2",
            recurrence="weekly"
        )

        recurring_tasks = self.manager.get_recurring_tasks()

        self.assertEqual(len(recurring_tasks), 2)
        self.assertIn(recurring1, recurring_tasks)
        self.assertIn(recurring2, recurring_tasks)
        self.assertNotIn(non_recurring, recurring_tasks)

    def test_get_task_instances(self):
        """Test getting all instances of a recurring task."""
        template = self.manager.add_task(
            title="Template Task",
            recurrence="daily",
            due_date=datetime.now()
        )

        # Generate instances
        instance1 = self.manager.generate_next_occurrence(template)
        self.manager.tasks.append(instance1)
        instance2 = self.manager.generate_next_occurrence(template)
        self.manager.tasks.append(instance2)

        instances = self.manager.get_task_instances(template.id)

        self.assertEqual(len(instances), 2)
        self.assertIn(instance1, instances)
        self.assertIn(instance2, instances)

    def test_mark_recurring_task_complete_generates_next(self):
        """Test that marking recurring task complete generates next occurrence."""
        template = self.manager.add_task(
            title="Recurring Task",
            recurrence="daily",
            due_date=datetime.now() + timedelta(hours=1)
        )

        # Generate first instance
        instance = self.manager.generate_next_occurrence(template)
        self.manager.tasks.append(instance)

        initial_count = len(self.manager.tasks)

        # Mark instance complete
        completed = self.manager.mark_task_complete(instance.id)

        self.assertEqual(completed.status, "completed")
        # Should have generated a new instance
        self.assertEqual(len(self.manager.tasks), initial_count + 1)

    def test_recurring_task_validation(self):
        """Test validation of recurring task fields."""
        # Invalid recurrence pattern
        with self.assertRaises(ValueError):
            self.manager.add_task(
                title="Invalid Task",
                recurrence="invalid_pattern"
            )

    def test_recurring_template_and_instance_mutually_exclusive(self):
        """Test that a task cannot be both template and instance."""
        with self.assertRaises(ValueError):
            Task(
                id=1,
                title="Invalid",
                is_recurring_template=True,
                recurrence_parent_id=1,
                recurrence="daily"
            )


class TestDueDateReminders(unittest.TestCase):
    """Test cases for due date and reminder functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = TodoManager()

    def test_is_due_soon(self):
        """Test is_due_soon detection."""
        # Task due in 10 minutes
        task = self.manager.add_task(
            title="Due Soon",
            due_date=datetime.now() + timedelta(minutes=10)
        )

        self.assertTrue(self.manager.is_due_soon(task))

    def test_is_not_due_soon(self):
        """Test that task far in future is not due soon."""
        task = self.manager.add_task(
            title="Not Due Soon",
            due_date=datetime.now() + timedelta(hours=2)
        )

        self.assertFalse(self.manager.is_due_soon(task))

    def test_is_overdue(self):
        """Test is_overdue detection."""
        task = self.manager.add_task(
            title="Overdue",
            due_date=datetime.now() - timedelta(hours=1)
        )

        self.assertTrue(self.manager.is_overdue(task))

    def test_is_not_overdue(self):
        """Test that future task is not overdue."""
        task = self.manager.add_task(
            title="Not Overdue",
            due_date=datetime.now() + timedelta(hours=1)
        )

        self.assertFalse(self.manager.is_overdue(task))

    def test_check_reminders(self):
        """Test check_reminders returns due soon and overdue tasks."""
        # Create various tasks
        overdue = self.manager.add_task(
            title="Overdue",
            due_date=datetime.now() - timedelta(hours=1)
        )
        due_soon = self.manager.add_task(
            title="Due Soon",
            due_date=datetime.now() + timedelta(minutes=10)
        )
        future = self.manager.add_task(
            title="Future",
            due_date=datetime.now() + timedelta(days=1)
        )

        reminders = self.manager.check_reminders()

        self.assertEqual(len(reminders), 2)
        self.assertIn(overdue, reminders)
        self.assertIn(due_soon, reminders)
        self.assertNotIn(future, reminders)

    def test_completed_task_not_in_reminders(self):
        """Test that completed tasks don't appear in reminders."""
        task = self.manager.add_task(
            title="Completed Overdue",
            due_date=datetime.now() - timedelta(hours=1)
        )

        # Mark as complete
        self.manager.update_task(task.id, status="completed")

        reminders = self.manager.check_reminders()
        self.assertEqual(len(reminders), 0)

    def test_filter_tasks_by_due_date_overdue(self):
        """Test filtering overdue tasks."""
        overdue = self.manager.add_task(
            title="Overdue",
            due_date=datetime.now() - timedelta(hours=1)
        )
        future = self.manager.add_task(
            title="Future",
            due_date=datetime.now() + timedelta(days=1)
        )

        filtered = self.manager.filter_tasks_by_due_date(overdue=True)

        self.assertEqual(len(filtered), 1)
        self.assertIn(overdue, filtered)

    def test_filter_tasks_by_due_date_due_soon(self):
        """Test filtering due soon tasks."""
        due_soon = self.manager.add_task(
            title="Due Soon",
            due_date=datetime.now() + timedelta(minutes=10)
        )
        future = self.manager.add_task(
            title="Future",
            due_date=datetime.now() + timedelta(days=1)
        )

        filtered = self.manager.filter_tasks_by_due_date(due_soon=True)

        self.assertEqual(len(filtered), 1)
        self.assertIn(due_soon, filtered)

    def test_parse_and_format_due_date(self):
        """Test parsing and formatting due dates."""
        # Parse a date string
        parsed = self.manager.parse_due_date("tomorrow")

        # Format it back
        formatted = self.manager.format_due_date(parsed)

        # Verify format
        self.assertIsInstance(formatted, str)
        self.assertIn("-", formatted)  # Should contain date separators


if __name__ == "__main__":
    unittest.main()

"""
Integration tests for complete workflow scenarios.

Tests the interaction between all features working together:
- Recurring tasks with due dates
- Reminders for recurring tasks
- Completing recurring tasks and generating next occurrences
- Filtering and searching recurring tasks with due dates
"""
import unittest
from datetime import datetime, timedelta
from src.services.todo_manager import TodoManager


class TestCompleteWorkflow(unittest.TestCase):
    """Integration tests for complete feature workflows."""

    def setUp(self):
        """Set up test fixtures."""
        self.manager = TodoManager()

    def test_create_recurring_task_with_due_date_and_complete(self):
        """Test creating a recurring task with due date and completing it."""
        # Create a recurring task with due date
        task = self.manager.add_task(
            title="Daily Report",
            description="Send daily status report",
            priority="high",
            tags=["work", "daily"],
            due_date=datetime.now() + timedelta(hours=2),
            recurrence="daily"
        )

        # Verify task was created correctly
        self.assertEqual(task.title, "Daily Report")
        self.assertTrue(task.is_recurring_template)
        self.assertEqual(task.recurrence, "daily")
        self.assertIsNotNone(task.due_date)
        self.assertEqual(len(task.tags), 2)

        # Generate first instance
        instance1 = self.manager.generate_next_occurrence(task)
        self.manager.tasks.append(instance1)

        # Verify instance
        self.assertFalse(instance1.is_recurring_template)
        self.assertEqual(instance1.recurrence_parent_id, task.id)
        self.assertEqual(instance1.status, "pending")

        # Complete the instance
        initial_count = len(self.manager.tasks)
        completed = self.manager.mark_task_complete(instance1.id)

        # Verify completion and next instance generation
        self.assertEqual(completed.status, "completed")
        self.assertEqual(len(self.manager.tasks), initial_count + 1)

        # Find the new instance
        new_instances = [t for t in self.manager.tasks
                        if t.recurrence_parent_id == task.id and t.status == "pending"]
        self.assertEqual(len(new_instances), 1)

    def test_reminder_system_with_recurring_tasks(self):
        """Test reminder system working with recurring tasks."""
        # Create overdue task (not recurring to keep it overdue)
        overdue_task = self.manager.add_task(
            title="Overdue Task",
            due_date=datetime.now() - timedelta(hours=1)
        )

        # Create due soon task
        due_soon_task = self.manager.add_task(
            title="Due Soon Task",
            due_date=datetime.now() + timedelta(minutes=10)
        )

        # Create recurring task template
        recurring_task = self.manager.add_task(
            title="Recurring Meeting",
            due_date=datetime.now() + timedelta(minutes=12),
            recurrence="daily"
        )

        # Check reminders
        reminders = self.manager.check_reminders()

        # Should include overdue and due soon tasks
        self.assertGreaterEqual(len(reminders), 2)

        # Verify overdue detection
        self.assertTrue(self.manager.is_overdue(overdue_task))

        # Verify due soon detection
        self.assertTrue(self.manager.is_due_soon(due_soon_task))

        # Verify recurring template is also due soon
        self.assertTrue(self.manager.is_due_soon(recurring_task))

    def test_search_and_filter_recurring_tasks(self):
        """Test searching and filtering recurring tasks."""
        # Create various recurring tasks
        task1 = self.manager.add_task(
            title="Daily Standup",
            description="Team standup meeting",
            priority="high",
            tags=["meeting", "team"],
            due_date=datetime.now() + timedelta(days=1),
            recurrence="daily"
        )

        task2 = self.manager.add_task(
            title="Weekly Report",
            description="Send weekly report",
            priority="medium",
            tags=["report"],
            due_date=datetime.now() + timedelta(days=7),
            recurrence="weekly"
        )

        task3 = self.manager.add_task(
            title="Monthly Review",
            description="Review metrics",
            priority="low",
            tags=["review", "metrics"],
            due_date=datetime.now() + timedelta(days=30),
            recurrence="monthly"
        )

        # Search for recurring tasks
        search_results = self.manager.search_tasks("report")
        self.assertEqual(len(search_results), 1)
        self.assertIn(task2, search_results)

        # Filter by priority
        high_priority = self.manager.filter_tasks(priority="high")
        self.assertIn(task1, high_priority)

        # Filter by tag
        meeting_tasks = self.manager.filter_tasks(tag="meeting")
        self.assertIn(task1, meeting_tasks)

        # Get all recurring templates
        recurring = self.manager.get_recurring_tasks()
        self.assertEqual(len(recurring), 3)

    def test_update_recurring_task_with_due_date(self):
        """Test updating a recurring task's due date."""
        # Create recurring task
        task = self.manager.add_task(
            title="Weekly Backup",
            due_date=datetime.now() + timedelta(days=7),
            recurrence="weekly"
        )

        # Update due date
        new_due_date = datetime.now() + timedelta(days=14)
        updated = self.manager.update_task(
            task.id,
            due_date=new_due_date,
            title="Updated Weekly Backup"
        )

        # Verify updates
        self.assertEqual(updated.title, "Updated Weekly Backup")
        self.assertEqual(updated.due_date, new_due_date)
        self.assertTrue(updated.is_recurring_template)
        self.assertEqual(updated.recurrence, "weekly")

    def test_sort_tasks_with_due_dates(self):
        """Test sorting tasks by creation date with recurring tasks."""
        # Create tasks at different times
        task1 = self.manager.add_task(
            title="First Task",
            due_date=datetime.now() + timedelta(days=3),
            recurrence="daily"
        )

        task2 = self.manager.add_task(
            title="Second Task",
            due_date=datetime.now() + timedelta(days=1),
            recurrence="weekly"
        )

        task3 = self.manager.add_task(
            title="Third Task",
            due_date=datetime.now() + timedelta(days=2),
            recurrence="monthly"
        )

        # Sort by creation date (most recent first)
        sorted_tasks = self.manager.sort_tasks(field="created_at", direction="desc")

        # Verify order
        self.assertEqual(sorted_tasks[0].id, task3.id)
        self.assertEqual(sorted_tasks[1].id, task2.id)
        self.assertEqual(sorted_tasks[2].id, task1.id)

        # Sort by priority
        task1_high = self.manager.update_task(task1.id, priority="high")
        task2_med = self.manager.update_task(task2.id, priority="medium")
        task3_low = self.manager.update_task(task3.id, priority="low")

        sorted_by_priority = self.manager.sort_tasks(field="priority", direction="asc")
        self.assertEqual(sorted_by_priority[0].priority, "high")
        self.assertEqual(sorted_by_priority[-1].priority, "low")

    def test_delete_recurring_template_orphans_instances(self):
        """Test that deleting a recurring template orphans its instances."""
        # Create template with instances
        template = self.manager.add_task(
            title="Template Task",
            recurrence="daily",
            due_date=datetime.now() + timedelta(days=1)
        )

        # Generate instances
        instance1 = self.manager.generate_next_occurrence(template)
        self.manager.tasks.append(instance1)
        instance2 = self.manager.generate_next_occurrence(template)
        self.manager.tasks.append(instance2)

        # Delete template
        self.manager.delete_task(template.id)

        # Instances should still exist but are orphaned
        remaining = [t for t in self.manager.tasks if t.recurrence_parent_id == template.id]
        self.assertEqual(len(remaining), 2)

        # Completing orphaned instance should not generate new instance
        initial_count = len(self.manager.tasks)
        self.manager.mark_task_complete(instance1.id)

        # Count should not increase (no new instance generated)
        self.assertEqual(len(self.manager.tasks), initial_count)

    def test_multiple_recurrence_patterns(self):
        """Test various recurrence patterns working together."""
        # Create tasks with different recurrence patterns
        daily = self.manager.add_task(
            title="Daily Task",
            due_date=datetime(2025, 12, 31, 9, 0),
            recurrence="daily"
        )

        weekly = self.manager.add_task(
            title="Weekly Task",
            due_date=datetime(2025, 12, 31, 10, 0),
            recurrence="weekly"
        )

        monthly = self.manager.add_task(
            title="Monthly Task",
            due_date=datetime(2025, 12, 31, 11, 0),
            recurrence="monthly"
        )

        every_monday = self.manager.add_task(
            title="Every Monday Task",
            due_date=datetime(2025, 12, 29, 9, 0),  # A Monday
            recurrence="every_monday"
        )

        # Generate next occurrences
        daily_next = self.manager.generate_next_occurrence(daily)
        weekly_next = self.manager.generate_next_occurrence(weekly)
        monthly_next = self.manager.generate_next_occurrence(monthly)
        monday_next = self.manager.generate_next_occurrence(every_monday)

        # Verify due dates are calculated correctly
        self.assertEqual(daily_next.due_date, datetime(2026, 1, 1, 9, 0))
        self.assertEqual(weekly_next.due_date, datetime(2026, 1, 7, 10, 0))
        self.assertEqual(monthly_next.due_date, datetime(2026, 1, 31, 11, 0))

        # Monday next should be 7 days later
        self.assertEqual(monday_next.due_date.weekday(), 0)  # Monday
        self.assertGreater(monday_next.due_date, every_monday.due_date)


if __name__ == "__main__":
    unittest.main()

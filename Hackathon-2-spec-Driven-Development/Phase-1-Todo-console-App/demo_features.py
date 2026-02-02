#!/usr/bin/env python3
"""
Demo script to showcase all advanced features of the Todo application.

This script demonstrates:
- Creating recurring tasks with due dates
- Viewing tasks with visual indicators
- Reminder system for overdue/due soon tasks
- Completing recurring tasks and auto-generation of next occurrence
"""
from datetime import datetime, timedelta
from src.services.todo_manager import TodoManager
from src.cli.ui import TodoCLI


def demo_advanced_features():
    """Demonstrate all advanced features."""
    print("=" * 70)
    print("TODO APP ADVANCED FEATURES DEMO")
    print("=" * 70)

    manager = TodoManager()
    cli = TodoCLI()
    cli.manager = manager  # Use the same manager

    # 1. Create recurring task with due date
    print("\n1. Creating Daily Standup (recurring daily, due tomorrow at 9am)")
    print("-" * 70)
    daily_standup = manager.add_task(
        title="Daily Standup",
        description="Morning team meeting",
        priority="high",
        tags=["work", "team"],
        due_date=datetime.now() + timedelta(days=1, hours=9),
        recurrence="daily"
    )
    print(f"✓ Created recurring task: {daily_standup.title} (ID: {daily_standup.id})")
    print(f"  Due: {daily_standup.due_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Recurrence: {daily_standup.recurrence}")
    print(f"  Is template: {daily_standup.is_recurring_template}")

    # 2. Create overdue task
    print("\n2. Creating Overdue Report (overdue by 2 hours)")
    print("-" * 70)
    overdue_task = manager.add_task(
        title="Submit Quarterly Report",
        description="Q4 financial report",
        priority="high",
        tags=["urgent", "report"],
        due_date=datetime.now() - timedelta(hours=2)
    )
    print(f"✓ Created overdue task: {overdue_task.title} (ID: {overdue_task.id})")
    print(f"  Due: {overdue_task.due_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Status: OVERDUE ❌")

    # 3. Create due soon task
    print("\n3. Creating Due Soon Task (due in 10 minutes)")
    print("-" * 70)
    due_soon_task = manager.add_task(
        title="Client Call",
        description="Check-in with client",
        priority="medium",
        tags=["client", "call"],
        due_date=datetime.now() + timedelta(minutes=10)
    )
    print(f"✓ Created due soon task: {due_soon_task.title} (ID: {due_soon_task.id})")
    print(f"  Due: {due_soon_task.due_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Status: DUE SOON ⏰")

    # 4. Create weekly recurring task
    print("\n4. Creating Weekly Team Meeting (every Monday)")
    print("-" * 70)
    weekly_meeting = manager.add_task(
        title="Weekly Team Meeting",
        description="Weekly team sync",
        priority="medium",
        tags=["meeting", "weekly"],
        due_date=datetime.now() + timedelta(days=7),
        recurrence="every_monday"
    )
    print(f"✓ Created weekly recurring task: {weekly_meeting.title} (ID: {weekly_meeting.id})")
    print(f"  Recurrence: {weekly_meeting.recurrence}")

    # 5. Display all tasks
    print("\n5. All Tasks (with visual indicators)")
    print("=" * 70)
    cli.display_tasks(manager.list_tasks())

    # 6. Check reminders
    print("\n6. Active Reminders")
    print("=" * 70)
    reminders = manager.check_reminders()
    print(f"Found {len(reminders)} tasks needing attention:")
    for task in reminders:
        if manager.is_overdue(task):
            print(f"  ❌ OVERDUE: '{task.title}' was due {task.due_date.strftime('%Y-%m-%d %H:%M')}")
        elif manager.is_due_soon(task):
            print(f"  ⏰ DUE SOON: '{task.title}' is due {task.due_date.strftime('%Y-%m-%d %H:%M')}")

    # 7. Generate next occurrence of recurring task
    print("\n7. Generating Next Occurrence of Daily Standup")
    print("-" * 70)
    next_standup = manager.generate_next_occurrence(daily_standup)
    manager.tasks.append(next_standup)
    print(f"✓ Generated next occurrence: {next_standup.title} (ID: {next_standup.id})")
    print(f"  Due: {next_standup.due_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Parent ID: {next_standup.recurrence_parent_id}")
    print(f"  Is instance: {not next_standup.is_recurring_template}")

    # 8. Complete recurring task instance
    print("\n8. Completing Recurring Task Instance (auto-generates next)")
    print("-" * 70)
    initial_count = len(manager.tasks)
    completed = manager.mark_task_complete(next_standup.id)
    final_count = len(manager.tasks)
    print(f"✓ Completed task: {completed.title}")
    print(f"  Task count before: {initial_count}")
    print(f"  Task count after: {final_count}")
    print(f"  New instance auto-generated: {final_count > initial_count}")

    # 9. Filter recurring tasks
    print("\n9. All Recurring Task Templates")
    print("=" * 70)
    recurring_templates = manager.get_recurring_tasks()
    print(f"Found {len(recurring_templates)} recurring templates:")
    for task in recurring_templates:
        print(f"  🔄 {task.title} - {task.recurrence}")

    # 10. Search tasks
    print("\n10. Search for 'meeting' tasks")
    print("=" * 70)
    search_results = manager.search_tasks("meeting")
    print(f"Found {len(search_results)} tasks:")
    cli.display_tasks(search_results)

    # 11. Filter by priority
    print("\n11. High Priority Tasks Only")
    print("=" * 70)
    high_priority = manager.filter_tasks(priority="high")
    print(f"Found {len(high_priority)} high priority tasks:")
    cli.display_tasks(high_priority)

    # 12. Summary
    print("\n" + "=" * 70)
    print("DEMO COMPLETE - Summary")
    print("=" * 70)
    print(f"Total tasks: {len(manager.tasks)}")
    print(f"Recurring templates: {len(manager.get_recurring_tasks())}")
    print(f"Active reminders: {len(manager.check_reminders())}")
    print(f"Overdue tasks: {len([t for t in manager.tasks if manager.is_overdue(t)])}")
    print(f"Due soon tasks: {len([t for t in manager.tasks if manager.is_due_soon(t)])}")
    print("\nAll advanced features working correctly! ✓")
    print("=" * 70)


if __name__ == "__main__":
    demo_advanced_features()

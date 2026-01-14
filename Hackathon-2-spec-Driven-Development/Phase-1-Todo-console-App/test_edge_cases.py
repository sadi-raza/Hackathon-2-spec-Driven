#!/usr/bin/env python3
"""
Test edge cases for recurring tasks (modification, deletion).

This script tests various edge cases for recurring tasks to ensure robustness:
1. Modifying recurring task templates
2. Modifying recurring task instances
3. Deleting recurring task templates (should prompt user)
4. Deleting recurring task instances (should not affect template)
5. Completing recurring tasks with missing parent
6. Invalid recurrence patterns
"""
from datetime import datetime, timedelta
from src.services.todo_manager import TodoManager
from src.models.task import Task


def test_modify_recurring_template():
    """Test modifying a recurring task template."""
    print("\n=== Test: Modify Recurring Template ===")
    manager = TodoManager()

    # Create recurring template
    task = manager.add_task(
        title="Weekly Meeting",
        description="Team standup",
        priority="high",
        due_date=datetime.now() + timedelta(days=1),
        recurrence="weekly"
    )

    print(f"Created recurring template: {task.title} (ID: {task.id})")
    print(f"  is_recurring_template: {task.is_recurring_template}")
    print(f"  recurrence: {task.recurrence}")

    # Modify the template
    updated_task = manager.update_task(task.id, title="Updated Weekly Meeting", priority="medium")

    if updated_task:
        print(f"✓ Successfully modified template")
        print(f"  New title: {updated_task.title}")
        print(f"  New priority: {updated_task.priority}")
        print(f"  Still recurring: {updated_task.is_recurring_template}")
    else:
        print("✗ Failed to modify template")


def test_modify_recurring_instance():
    """Test modifying a recurring task instance."""
    print("\n=== Test: Modify Recurring Instance ===")
    manager = TodoManager()

    # Create recurring template
    template = manager.add_task(
        title="Daily Standup",
        description="Morning standup",
        priority="medium",
        due_date=datetime.now() + timedelta(hours=1),
        recurrence="daily"
    )

    # Generate an instance
    instance = manager.generate_next_occurrence(template)
    manager.tasks.append(instance)

    print(f"Created instance: {instance.title} (ID: {instance.id})")
    print(f"  is_recurring_template: {instance.is_recurring_template}")
    print(f"  recurrence_parent_id: {instance.recurrence_parent_id}")

    # Modify the instance
    updated_instance = manager.update_task(instance.id, description="Updated description")

    if updated_instance:
        print(f"✓ Successfully modified instance")
        print(f"  New description: {updated_instance.description}")
        print(f"  Parent ID unchanged: {updated_instance.recurrence_parent_id}")
    else:
        print("✗ Failed to modify instance")


def test_delete_recurring_template():
    """Test deleting a recurring task template."""
    print("\n=== Test: Delete Recurring Template ===")
    manager = TodoManager()

    # Create recurring template with instances
    template = manager.add_task(
        title="Weekly Report",
        description="Send weekly report",
        priority="high",
        due_date=datetime.now() + timedelta(days=7),
        recurrence="weekly"
    )

    # Generate instances
    instance1 = manager.generate_next_occurrence(template)
    manager.tasks.append(instance1)
    instance2 = manager.generate_next_occurrence(template)
    manager.tasks.append(instance2)

    print(f"Created template with 2 instances")
    print(f"  Template ID: {template.id}")
    print(f"  Instance IDs: {instance1.id}, {instance2.id}")

    # Delete the template
    deleted = manager.delete_task(template.id)

    if deleted:
        print(f"✓ Template deleted successfully")

        # Check if instances still exist
        remaining_instances = [task for task in manager.tasks if task.recurrence_parent_id == template.id]
        print(f"  Remaining instances: {len(remaining_instances)}")

        if len(remaining_instances) > 0:
            print("  ⚠ WARNING: Orphaned instances exist (parent deleted)")
    else:
        print("✗ Failed to delete template")


def test_delete_recurring_instance():
    """Test deleting a recurring task instance."""
    print("\n=== Test: Delete Recurring Instance ===")
    manager = TodoManager()

    # Create recurring template with instances
    template = manager.add_task(
        title="Daily Backup",
        description="Backup database",
        priority="high",
        due_date=datetime.now() + timedelta(hours=12),
        recurrence="daily"
    )

    # Generate instance
    instance = manager.generate_next_occurrence(template)
    manager.tasks.append(instance)

    print(f"Created template and instance")
    print(f"  Template ID: {template.id}")
    print(f"  Instance ID: {instance.id}")

    # Delete the instance
    deleted = manager.delete_task(instance.id)

    if deleted:
        print(f"✓ Instance deleted successfully")

        # Check if template still exists
        template_exists = manager.get_task(template.id) is not None
        print(f"  Template still exists: {template_exists}")
    else:
        print("✗ Failed to delete instance")


def test_complete_recurring_with_missing_parent():
    """Test completing a recurring instance whose parent has been deleted."""
    print("\n=== Test: Complete Recurring with Missing Parent ===")
    manager = TodoManager()

    # Create recurring template
    template = manager.add_task(
        title="Monthly Review",
        description="Review metrics",
        priority="medium",
        due_date=datetime.now() + timedelta(days=30),
        recurrence="monthly"
    )

    # Generate instance
    instance = manager.generate_next_occurrence(template)
    manager.tasks.append(instance)

    print(f"Created template and instance")
    print(f"  Template ID: {template.id}")
    print(f"  Instance ID: {instance.id}")

    # Delete the parent template
    manager.delete_task(template.id)
    print(f"Deleted parent template")

    # Try to complete the instance
    try:
        completed_task = manager.mark_task_complete(instance.id)

        if completed_task:
            print(f"✓ Instance completed (parent missing)")
            print(f"  Status: {completed_task.status}")

            # Check if a new instance was generated (should not be)
            new_instances = [task for task in manager.tasks
                           if task.recurrence_parent_id == template.id and task.id != instance.id]
            print(f"  New instances generated: {len(new_instances)}")
        else:
            print("✗ Failed to complete instance")
    except Exception as e:
        print(f"✗ Exception occurred: {e}")


def test_invalid_recurrence_pattern():
    """Test handling of invalid recurrence patterns."""
    print("\n=== Test: Invalid Recurrence Pattern ===")
    manager = TodoManager()

    try:
        # Try to create task with invalid recurrence
        task = manager.add_task(
            title="Test Task",
            description="Test",
            priority="low",
            due_date=datetime.now() + timedelta(days=1),
            recurrence="every_other_tuesday"  # Invalid pattern
        )

        print(f"✗ Task created with invalid recurrence pattern (should have failed)")
    except ValueError as e:
        print(f"✓ Correctly rejected invalid recurrence pattern")
        print(f"  Error message: {e}")


def test_complete_recurring_generates_next():
    """Test that completing a recurring instance generates the next occurrence."""
    print("\n=== Test: Complete Recurring Generates Next ===")
    manager = TodoManager()

    # Create recurring template
    template = manager.add_task(
        title="Daily Exercise",
        description="30 min workout",
        priority="high",
        due_date=datetime.now() + timedelta(hours=6),
        recurrence="daily"
    )

    # Generate first instance
    instance1 = manager.generate_next_occurrence(template)
    manager.tasks.append(instance1)

    initial_count = len(manager.tasks)
    print(f"Initial task count: {initial_count}")
    print(f"  Template ID: {template.id}")
    print(f"  Instance ID: {instance1.id}")

    # Complete the instance
    completed = manager.mark_task_complete(instance1.id)

    if completed:
        print(f"✓ Instance marked complete")
        print(f"  Status: {completed.status}")

        # Check if new instance was generated
        final_count = len(manager.tasks)
        print(f"  Final task count: {final_count}")

        if final_count > initial_count:
            print(f"  ✓ New instance generated automatically")
            new_instances = [task for task in manager.tasks
                           if task.recurrence_parent_id == template.id and task.status == "pending"]
            if new_instances:
                print(f"    New instance due: {new_instances[0].due_date}")
        else:
            print(f"  ✗ No new instance generated")
    else:
        print("✗ Failed to complete instance")


def run_all_tests():
    """Run all edge case tests."""
    print("=" * 60)
    print("EDGE CASE TESTING FOR RECURRING TASKS")
    print("=" * 60)

    test_modify_recurring_template()
    test_modify_recurring_instance()
    test_delete_recurring_template()
    test_delete_recurring_instance()
    test_complete_recurring_with_missing_parent()
    test_invalid_recurrence_pattern()
    test_complete_recurring_generates_next()

    print("\n" + "=" * 60)
    print("EDGE CASE TESTING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()

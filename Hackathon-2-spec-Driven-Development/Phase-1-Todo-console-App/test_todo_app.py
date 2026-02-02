#!/usr/bin/env python3
"""
Simple test to verify the Todo Console Application is working correctly.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from src.services.todo_manager import TodoManager
from src.models.task import Task


def test_todo_manager():
    """Test the TodoManager functionality."""
    print("Testing TodoManager...")

    # Create a TodoManager instance
    tm = TodoManager()

    # Test adding a task with priority and tags
    task1 = tm.add_task("Test task 1", "This is a test task", "high", ["test", "important"])
    print(f"Added task: ID={task1.id}, Title='{task1.title}', Description='{task1.description}', Priority='{task1.priority}', Tags={task1.tags}, Status='{task1.status}'")

    # Test adding another task
    task2 = tm.add_task("Test task 2")
    print(f"Added task: ID={task2.id}, Title='{task2.title}', Description='{task2.description}', Priority='{task2.priority}', Tags={task2.tags}, Status='{task2.status}'")

    # Test getting all tasks
    all_tasks = tm.list_tasks()  # Changed from get_all_tasks to list_tasks
    print(f"Total tasks: {len(all_tasks)}")

    # Test getting a specific task
    retrieved_task = tm.get_task(task1.id)
    print(f"Retrieved task: ID={retrieved_task.id}, Title='{retrieved_task.title}', Status='{retrieved_task.status}'")

    # Test marking task as complete (using update_task to change status)
    success = tm.update_task(task1.id, status="completed")
    print(f"Marked task {task1.id} as complete: {success is not None}")
    updated_task = tm.get_task(task1.id)
    print(f"Task {task1.id} completed status: {updated_task.status}")

    # Test updating a task
    updated_task = tm.update_task(task1.id, title="Updated test task 1", description="Updated description", priority="medium")
    print(f"Updated task: ID={updated_task.id}, Title='{updated_task.title}', Priority='{updated_task.priority}'")

    # Test deleting a task
    delete_success = tm.delete_task(task2.id)
    print(f"Deleted task {task2.id}: {delete_success}")

    # Check remaining tasks
    remaining_tasks = tm.list_tasks()  # Changed from get_all_tasks to list_tasks
    print(f"Remaining tasks: {len(remaining_tasks)}")

    # Test search functionality
    search_results = tm.search_tasks("Updated")
    print(f"Search results for 'Updated': {len(search_results)} tasks")

    # Test filter functionality
    all_pending = tm.filter_tasks(status="pending")
    print(f"Pending tasks: {len(all_pending)}")

    all_completed = tm.filter_tasks(status="completed")
    print(f"Completed tasks: {len(all_completed)}")

    # Test sort functionality
    sorted_tasks = tm.sort_tasks(field="priority", direction="asc")
    print(f"Sorted tasks by priority (asc): {len(sorted_tasks)} tasks")

    print("All tests passed!")


if __name__ == "__main__":
    test_todo_manager()
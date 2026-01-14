from typing import List, Optional
from datetime import datetime
from src.services.todo_manager import TodoManager
from src.models.task import Task


class TodoCLI:
    """
    CLI interface with enhanced menu and display functionality.
    """
    def __init__(self):
        self.manager = TodoManager()

    def display_task(self, task: Task):
        """
        Display a single task with enhanced format including priority icons, tags, due dates,
        recurrence indicators, and visual indicators for due soon/overdue tasks.
        """
        # Priority icons
        priority_icons = {
            "high": "🔥",
            "medium": "🟡",
            "low": "🟢"
        }

        priority_icon = priority_icons.get(task.priority, "⚪")
        priority_display = f"{priority_icon} {task.priority.capitalize()}"

        # Format tags for display
        tags_display = self.format_tags_display(task.tags)

        # Status icons
        status_icons = {
            "pending": "⏳",
            "completed": "✅"
        }

        status_icon = status_icons.get(task.status, "❓")
        status_display = f"{status_icon} {task.status.capitalize()}"

        # Format due date for display and add visual indicators
        from src.utils.date_utils import format_datetime_for_display
        due_date_display = "No due date"
        due_indicator = ""

        if task.due_date:
            due_date_display = format_datetime_for_display(task.due_date)

            # Check if task is due soon or overdue
            from datetime import datetime, timedelta
            now = datetime.now()

            # Check if due soon (within 15 minutes)
            if task.status == "pending" and task.due_date <= now + timedelta(minutes=15) and task.due_date >= now:
                due_indicator = " ⏰"  # Due soon indicator
            # Check if overdue
            elif task.status == "pending" and task.due_date < now:
                due_indicator = " ❌"  # Overdue indicator

            due_date_display += due_indicator

        # Format recurrence for display
        recurrence_display = ""
        if task.recurrence:
            recurrence_display = f" {task.recurrence} 🔄"
            if task.is_recurring_template:
                recurrence_display = f" {task.recurrence} (Template) 🔄"

        print(f"{task.id:2} | {priority_display:12} | {task.title:20} | {due_date_display:20} | {tags_display:15} | {status_display:12} | {recurrence_display}")

    def format_priority_display(self, priority: str) -> str:
        """
        Add priority display formatting with icons.
        """
        priority_icons = {
            "high": "🔥",
            "medium": "🟡",
            "low": "🟢"
        }

        priority_icon = priority_icons.get(priority, "⚪")
        return f"{priority_icon} {priority.capitalize()}"

    def format_tags_display(self, tags: List[str]) -> str:
        """
        Add tag display formatting.
        """
        if not tags:
            return "No tags"
        return ", ".join(tags)

    def display_tasks(self, tasks: List[Task], show_header: bool = True):
        """
        Display a list of tasks in the enhanced table format.
        """
        if show_header:
            print("ID |   Priority   |        Title         |        Due         |            Tags            |     Status       | Recurrence")
            print("-- | ------------ | -------------------- | ------------------ | ---------------------------| -----------------| ----------")

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            self.display_task(task)

    def display_reminder_notifications(self):
        """
        Display reminder notifications for tasks that are due soon or overdue.
        """
        # Get tasks that need reminders
        reminder_tasks = self.manager.check_reminders()

        if not reminder_tasks:
            return  # No reminders to display

        print("\n🔔 REMINDERS:")
        print("-" * 50)

        for task in reminder_tasks:
            from datetime import datetime
            now = datetime.now()

            if self.manager.is_overdue(task):
                print(f"❌ OVERDUE: '{task.title}' was due {task.due_date.strftime('%Y-%m-%d %H:%M')}")
            elif self.manager.is_due_soon(task):
                print(f"⏰ DUE SOON: '{task.title}' is due {task.due_date.strftime('%Y-%m-%d %H:%M')}")

        # Add console beep for attention
        print("\a")  # Console beep

    def update_main_menu_structure(self):
        """
        Update main menu structure to include new options.
        """
        print("\n--- Todo Application ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Mark Complete")
        print("5. Delete Task")
        print("6. Search Tasks")
        print("7. Exit")
        print("------------------------")

    def create_view_tasks_submenu(self):
        """
        Create View Tasks submenu with Filter/Sort/Search options.
        """
        print("\nView Tasks Options:")
        print("1. Show All Tasks")
        print("2. Filter Tasks")
        print("3. Sort Tasks")
        print("4. Back to Main Menu")

    def add_search_tasks_option(self):
        """
        Add Search Tasks menu option (option 6).
        """
        print("\n--- Todo Application ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Mark Complete")
        print("5. Delete Task")
        print("6. Search Tasks")
        print("7. Exit")
        print("------------------------")

    def display_menu(self):
        """
        Update main menu structure to include new options and ensure backward compatibility with existing functionality.
        """
        # Get reminder count
        reminder_tasks = self.manager.check_reminders()
        reminder_count = len(reminder_tasks)

        print("\n--- Todo Application ---")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Mark Complete")
        print("5. Delete Task")
        print("6. Search Tasks")
        print("7. View Overdue/Due Soon Tasks")
        print("8. Exit")
        print(f"({reminder_count} reminders)")
        print("------------------------")

    def get_user_choice(self) -> str:
        """
        Get user choice from the menu.
        """
        return input("Enter your choice (1-7): ").strip()

    def prompt_for_priority(self) -> str:
        """
        Prompt user for priority level with validation.
        """
        while True:
            priority = input("Enter priority (high/medium/low) [default: medium]: ").strip().lower()
            if not priority:
                return "medium"
            if priority in ["high", "medium", "low"]:
                return priority
            print("Invalid priority. Please enter 'high', 'medium', or 'low'.")

    def prompt_for_tags(self) -> List[str]:
        """
        Update CLI to handle comma-separated tags input.
        """
        tags_input = input("Enter tags (comma-separated) [optional]: ").strip()
        if not tags_input:
            return []

        # Split tags and clean them
        tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
        return tags

    def prompt_for_due_date(self) -> Optional[datetime]:
        """
        Prompt user for due date with multiple format support.

        Returns:
            The parsed datetime or None if user chooses not to set a due date
        """
        from datetime import datetime
        from src.utils.date_utils import parse_date_string

        print("\nEnter due date (or press Enter for no due date)")
        print("Supported formats:")
        print("- Absolute: YYYY-MM-DD, YYYY-MM-DD HH:MM")
        print("- Relative: today, tomorrow, in N days/weeks, next [day]")
        print("- Natural: 'next friday at 3pm', 'in 2 days at 10am'")

        date_input = input("Enter due date (or press Enter): ").strip()

        if not date_input:
            return None

        try:
            parsed_date = parse_date_string(date_input)
            return parsed_date
        except ValueError as e:
            print(f"Error parsing date: {e}")
            print("No due date will be set.")
            return None

    def prompt_for_recurrence(self) -> Optional[str]:
        """
        Prompt user for recurrence pattern selection.

        Returns:
            The selected recurrence pattern or None if user chooses not to make it recurring
        """
        print("\nSelect recurrence pattern (or press Enter for no recurrence):")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")
        print("4. Yearly")
        print("5. Every Monday")
        print("6. Every Tuesday")
        print("7. Every Wednesday")
        print("8. Every Thursday")
        print("9. Every Friday")
        print("10. Every Saturday")
        print("11. Every Sunday")
        print("Press Enter for no recurrence")

        choice = input("Enter your choice (1-11) or press Enter: ").strip()

        recurrence_map = {
            "1": "daily",
            "2": "weekly",
            "3": "monthly",
            "4": "yearly",
            "5": "every_monday",
            "6": "every_tuesday",
            "7": "every_wednesday",
            "8": "every_thursday",
            "9": "every_friday",
            "10": "every_saturday",
            "11": "every_sunday"
        }

        if choice in recurrence_map:
            return recurrence_map[choice]
        elif choice == "":
            return None
        else:
            print("Invalid choice. No recurrence will be set.")
            return None

    def run(self):
        """
        Main application loop.
        """
        while True:
            self.display_menu()

            # Display reminder notifications if there are any
            self.display_reminder_notifications()

            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.mark_task_complete()
            elif choice == "5":
                self.delete_task()
            elif choice == "6":
                self.search_tasks()
            elif choice == "7":
                self.view_overdue_due_soon_tasks()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")

    def add_task(self):
        """
        Add a new task with priority, tags, due date, and recurrence.
        """
        title = input("Enter task title: ").strip()
        if not title:
            print("Task title cannot be empty.")
            return

        description = input("Enter task description [optional]: ").strip()
        priority = self.prompt_for_priority()
        tags = self.prompt_for_tags()

        # Prompt for due date
        due_date = self.prompt_for_due_date()

        # Prompt for recurrence
        recurrence = self.prompt_for_recurrence()

        try:
            task = self.manager.add_task(title, description, priority, tags, due_date, recurrence)
            print(f"Task '{task.title}' added successfully with ID {task.id}")
            if recurrence:
                print(f"Task set to recur: {recurrence}")
        except ValueError as e:
            print(f"Error adding task: {e}")

    def view_tasks(self):
        """
        Create View Tasks submenu with Filter/Sort/Search options and update display to show count and applied filters.
        """
        print("\nView Tasks Options:")
        print("1. Show All Tasks")
        print("2. Show Overdue Tasks")
        print("3. Show Due Soon Tasks")
        print("4. Show Recurring Tasks")
        print("5. Filter Tasks")
        print("6. Sort Tasks")
        print("7. Back to Main Menu")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            tasks = self.manager.list_tasks()
            print(f"\nAll Tasks ({len(tasks)} total):")
            self.display_tasks(tasks)
        elif choice == "2":
            tasks = self.manager.filter_tasks_by_due_date(overdue=True)
            print(f"\nOverdue Tasks ({len(tasks)} total):")
            self.display_tasks(tasks)
        elif choice == "3":
            tasks = self.manager.filter_tasks_by_due_date(due_soon=True)
            print(f"\nDue Soon Tasks ({len(tasks)} total):")
            self.display_tasks(tasks)
        elif choice == "4":
            tasks = self.manager.filter_tasks_by_due_date(recurring=True)
            print(f"\nRecurring Tasks ({len(tasks)} total):")
            self.display_tasks(tasks)
        elif choice == "5":
            self.filter_tasks_submenu()
        elif choice == "6":
            self.sort_tasks_submenu()
        elif choice == "7":
            return
        else:
            print("Invalid choice.")

    def filter_tasks_submenu(self):
        """
        Submenu for filtering tasks.
        """
        print("\nFilter Tasks by:")
        print("1. Status")
        print("2. Priority")
        print("3. Tag")
        print("4. Combined Filters")
        print("5. Back to View Tasks")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            status = input("Enter status (pending/completed/all): ").strip().lower()
            if status in ["pending", "completed", "all"]:
                tasks = self.manager.filter_tasks(status=status)
                self.display_tasks(tasks)
            else:
                print("Invalid status.")
        elif choice == "2":
            priority = input("Enter priority (high/medium/low/all): ").strip().lower()
            if priority in ["high", "medium", "low", "all"]:
                tasks = self.manager.filter_tasks(priority=priority)
                self.display_tasks(tasks)
            else:
                print("Invalid priority.")
        elif choice == "3":
            tag = input("Enter tag to filter by: ").strip()
            if tag:
                tasks = self.manager.filter_tasks(tag=tag)
                self.display_tasks(tasks)
            else:
                print("Tag cannot be empty.")
        elif choice == "4":
            self.combined_filters()
        elif choice == "5":
            return
        else:
            print("Invalid choice.")

    def create_filter_submenu(self):
        """
        Create filter submenu under View Tasks.
        """
        print("\nFilter Tasks by:")
        print("1. Status")
        print("2. Priority")
        print("3. Tag")
        print("4. Combined Filters")
        print("5. Back to View Tasks")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            status = input("Enter status (pending/completed/all): ").strip().lower()
            if status in ["pending", "completed", "all"]:
                tasks = self.manager.filter_tasks(status=status)
                self.display_tasks(tasks)
            else:
                print("Invalid status.")
        elif choice == "2":
            priority = input("Enter priority (high/medium/low/all): ").strip().lower()
            if priority in ["high", "medium", "low", "all"]:
                tasks = self.manager.filter_tasks(priority=priority)
                self.display_tasks(tasks)
            else:
                print("Invalid priority.")
        elif choice == "3":
            tag = input("Enter tag to filter by: ").strip()
            if tag:
                tasks = self.manager.filter_tasks(tag=tag)
                self.display_tasks(tasks)
            else:
                print("Tag cannot be empty.")
        elif choice == "4":
            self.combined_filters()
        elif choice == "5":
            return
        else:
            print("Invalid choice.")

    def combined_filters(self):
        """
        Add filter functionality to CLI interface and add filter display showing applied filters.
        """
        print("Enter filter values (press Enter to skip):")

        status_input = input("Status (pending/completed/all): ").strip().lower()
        status = status_input if status_input in ["pending", "completed", "all"] else None

        priority_input = input("Priority (high/medium/low/all): ").strip().lower()
        priority = priority_input if priority_input in ["high", "medium", "low", "all"] else None

        tag = input("Tag: ").strip() or None

        tasks = self.manager.filter_tasks(status=status, priority=priority, tag=tag)
        print(f"\nFiltered Tasks (Applied filters - Status: {status}, Priority: {priority}, Tag: {tag}):")
        self.display_tasks(tasks)

    def sort_tasks_submenu(self):
        """
        Add sort functionality to CLI interface and create sort submenu under View Tasks.
        """
        print("\nSort Tasks by:")
        print("1. Priority")
        print("2. Title")
        print("3. Creation Date")
        print("4. Back to View Tasks")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            direction = input("Sort direction (asc/desc) [default: asc]: ").strip().lower()
            if direction not in ["asc", "desc"]:
                direction = "asc"
            tasks = self.manager.sort_tasks(field="priority", direction=direction)
            print(f"\nTasks sorted by Priority ({direction}):")
            self.display_tasks(tasks)
        elif choice == "2":
            direction = input("Sort direction (asc/desc) [default: asc]: ").strip().lower()
            if direction not in ["asc", "desc"]:
                direction = "asc"
            tasks = self.manager.sort_tasks(field="title", direction=direction)
            print(f"\nTasks sorted by Title ({direction}):")
            self.display_tasks(tasks)
        elif choice == "3":
            direction = input("Sort direction (asc/desc) [default: desc]: ").strip().lower()
            if direction not in ["asc", "desc"]:
                direction = "desc"
            tasks = self.manager.sort_tasks(field="created_at", direction=direction)
            print(f"\nTasks sorted by Creation Date ({direction}):")
            self.display_tasks(tasks)
        elif choice == "4":
            return
        else:
            print("Invalid choice.")

    def update_task(self):
        """
        Update an existing task.
        """
        try:
            task_id = int(input("Enter task ID to update: ").strip())
        except ValueError:
            print("Invalid task ID.")
            return

        task = self.manager.get_task(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        print(f"Updating task: {task.title}")
        new_title = input(f"Enter new title [{task.title}]: ").strip()
        new_description = input(f"Enter new description [{task.description}]: ").strip()
        new_priority = input(f"Enter new priority (high/medium/low) [{task.priority}]: ").strip().lower()
        new_tags_input = input(f"Enter new tags (comma-separated) [{', '.join(task.tags)}]: ").strip()

        # Handle due date update
        current_due_date = "No due date"
        if task.due_date:
            from src.utils.date_utils import format_datetime_for_display
            current_due_date = format_datetime_for_display(task.due_date)
        due_date_input = input(f"Enter new due date [{current_due_date}] (or press Enter to keep current): ").strip()

        # Prepare update parameters
        update_params = {}
        if new_title:
            update_params['title'] = new_title
        if new_description:
            update_params['description'] = new_description
        if new_priority:
            if new_priority in ["high", "medium", "low"]:
                update_params['priority'] = new_priority
            else:
                print("Invalid priority. Keeping current priority.")
        if new_tags_input:
            new_tags = [tag.strip() for tag in new_tags_input.split(",") if tag.strip()]
            update_params['tags'] = new_tags
        if due_date_input:
            from src.utils.date_utils import parse_date_string
            try:
                parsed_due_date = parse_date_string(due_date_input)
                update_params['due_date'] = parsed_due_date
            except ValueError as e:
                print(f"Error parsing due date: {e}. Keeping current due date.")

        try:
            updated_task = self.manager.update_task(task_id, **update_params)
            if updated_task:
                print(f"Task {task_id} updated successfully.")
            else:
                print("Failed to update task.")
        except ValueError as e:
            print(f"Error updating task: {e}")

    def mark_task_complete(self):
        """
        Mark a task as complete.
        """
        try:
            task_id = int(input("Enter task ID to mark complete: ").strip())
        except ValueError:
            print("Invalid task ID.")
            return

        task = self.manager.get_task(task_id)
        if not task:
            print(f"Task with ID {task_id} not found.")
            return

        # Update the task status to completed
        try:
            updated_task = self.manager.update_task(task_id, status="completed")
            if updated_task:
                print(f"Task '{updated_task.title}' marked as completed.")
            else:
                print("Failed to update task.")
        except ValueError as e:
            print(f"Error updating task: {e}")

    def delete_task(self):
        """
        Delete a task.
        """
        try:
            task_id = int(input("Enter task ID to delete: ").strip())
        except ValueError:
            print("Invalid task ID.")
            return

        if self.manager.delete_task(task_id):
            print(f"Task with ID {task_id} deleted successfully.")
        else:
            print(f"Task with ID {task_id} not found.")

    def implement_graceful_edge_case_handling(self):
        """
        Implement graceful handling of edge cases (empty lists, invalid inputs).
        """
        # This is handled through the existing methods with proper validation and error handling
        pass

    def view_overdue_due_soon_tasks(self):
        """
        View tasks that are overdue or due soon.
        """
        # Get tasks that are overdue or due soon
        overdue_tasks = [task for task in self.manager.list_tasks() if self.manager.is_overdue(task)]
        due_soon_tasks = [task for task in self.manager.list_tasks() if self.manager.is_due_soon(task)]

        print("\nOverdue Tasks:")
        print("-" * 20)
        if not overdue_tasks:
            print("No overdue tasks.")
        else:
            self.display_tasks(overdue_tasks)

        print("\nDue Soon Tasks:")
        print("-" * 20)
        if not due_soon_tasks:
            print("No tasks due soon.")
        else:
            self.display_tasks(due_soon_tasks)

        # Show reminder notifications
        self.display_reminder_notifications()

    def search_tasks(self):
        """
        Add search functionality to CLI interface and handle no results case.
        """
        query = input("Enter search keyword: ").strip()
        if not query:
            print("Search query cannot be empty.")
            return

        tasks = self.manager.search_tasks(query)
        print(f"\nSearch results for '{query}' (found {len(tasks)} tasks):")

        if not tasks:
            print("No tasks found.")
        else:
            self.display_tasks(tasks)
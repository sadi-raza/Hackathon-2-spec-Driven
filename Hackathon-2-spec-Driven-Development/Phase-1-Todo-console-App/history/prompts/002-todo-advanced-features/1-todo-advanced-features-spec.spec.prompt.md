---
id: 1
title: todo-advanced-features-spec
stage: spec
date: 2025-12-30
surface: agent
model: Claude Sonnet 4.5
feature: todo-advanced-features
branch: 002-todo-advanced-features
user: ai-developer
command: /sp.specify
labels: [specification, todo-app, recurring-tasks, due-dates, reminders]
links:
  spec: specs/002-todo-advanced-features/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/002-todo-advanced-features/spec.md
 - specs/002-todo-advanced-features/checklists/requirements.md
tests:
 - specs/002-todo-advanced-features/spec.md validated against quality checklist
---

## Prompt

# Project Specification Extension: Phase I Advanced Level - Intelligent Features

## Extension Objective
Further enhance the existing Phase I in-memory console Todo application by adding Advanced Level intelligent features: Recurring Tasks and Due Dates with Time Reminders.

This extension continues to use 100% Spec-Driven Development with Claude Code and Spec-Kit Plus. No manual coding allowed. The goal is to make the console app demonstrate intelligent behavior while preparing logic for future AI chatbot and cloud phases.

## New User Stories (Advanced Level)

As a user, I can:

1. **Create Recurring Tasks**
   - When adding a task, specify recurrence pattern: daily, weekly, monthly, yearly
   - Example: "Weekly team meeting every Monday at 10 AM"
   - After marking a recurring task as complete, the app automatically creates the next occurrence with updated due date
   - Recurrence stored as pattern (e.g., "weekly", "every_monday")
   - Parent recurring task remains as template, instances generated on completion

2. **Set Due Dates & Times**
   - Assign due date and optional time to any task (including recurring)
   - Input format: natural or "YYYY-MM-DD" or "YYYY-MM-DD HH:MM"
   - Support relative: "tomorrow", "next week", "in 3 days"

3. **Receive Time Reminders**
   - When app is running, periodically check for tasks due soon (within next 15 minutes) or overdue
   - Display prominent reminder notification in console:
     • Beep sound (if supported)
     • Bold/red flashing message
     • "REMINDER: 'Buy groceries' is due now!"
   - Reminder shown every time "View Tasks" is selected if any task is due/overdue
   - Clear visual indicator in task list (⏰ Due soon, ❌ Overdue)

## Updated Task Model Requirements

Extend existing Task model with:

- due_date: Optional[datetime] = None
- recurrence: Optional[str] = None  # "daily", "weekly", "monthly", "yearly", "every_monday", etc.
- recurrence_parent_id: Optional[int] = None  # For generated instances
- is_recurring_template: bool = False

## Core Implementation Logic

1. **Recurring Tasks Flow**
   - When adding task, ask: "Is this recurring? (y/n)"
   - If yes, ask pattern (offer menu: daily/weekly/monthly/custom)
   - Mark as is_recurring_template = True
   - When user marks a recurring instance complete:
     • Generate next instance with updated due_date based on pattern
     • Add new task automatically
     • Show: "Next occurrence created for [date]"

2. **Due Date Parsing**
   - Support inputs:
     • "2025-12-31"
     • "2025-12-31 14:30"
     • "today", "tomorrow", "in 2 days", "next friday"
   - Use dateutil or manual parser for relative dates

3. **Reminder System**
   - Background checker (in main loop):
     • Every 60 seconds, scan tasks
     • If due_date <= now + 15min or overdue → trigger reminder
   - In View Tasks: highlight due/overdue tasks with symbols and colors
   - Console beep: print("\a") for alert sound

## CLI Enhancements

- Add Task / Update Task prompts now include:
  • Due date/time?
  • Recurring? (y/n) → pattern selection

- View Tasks display:
  ID | Priority | Title              | Due                | Tags         | Status     | Recur
  1  | 🔥 High   | Weekly meeting     | 2025-12-30 10:00   | work, team   | ⏳ Pending  | Weekly 🔄

- Main menu add:
  • View Overdue / Due Soon tasks

## Non-Functional Requirements

- All logic in-memory (no persistence yet)
- Reminder checker non-blocking (use time checks in loop)
- Graceful handling of timezones (assume local time)
- Clean separation: reminder logic in separate method
- Prepare recurrence logic for future event-driven (Kafka/Dapr) phase

## Acceptance Criteria (Advanced Level)

- User can create recurring task and see next instance auto-generated on completion
- Due dates accepted in multiple formats including relative
- Console shows clear reminders for due/overdue tasks
- Task list visually indicates due dates and recurrence
- Beep/alert triggers for imminent tasks
- All previous Basic + Intermediate features remain fully functional
- Code remains clean, modular, and well-documented

## Out of Scope (Phase I)

- Browser notifications (will come in web phase)
- Email/SMS reminders
- Complex recurrence (e.g., "every 2nd Tuesday")
- Timezone support
- Persistence of recurring instances

## Deliverables Update

- Update README.md with new Advanced features and demo examples
- Include recurrence and reminder demo in future submission videos
- /specs folder must contain this advanced specification
- Show reusable intelligence potential (e.g., recurrence logic as future subagent skill)

This specification extends Phase I to include Advanced Level intelligent features. Implementation must fully adhere to constitution and previous specifications. Design with reusability for upcoming AI and cloud phases.

## Response snapshot

I have successfully created a comprehensive specification for the advanced todo app features, including recurring tasks, due dates, and time reminders. The specification includes:

1. Detailed user stories with priorities (P1-P2) covering recurring tasks, due dates, and reminders
2. Functional requirements (FR-001 through FR-010) that define the system's behavior
3. Key entities (Task, Recurrence Pattern, Reminder) that will be involved
4. Measurable success criteria (SC-001 through SC-005) that define how the feature will be evaluated
5. Edge cases that address potential boundary conditions and error scenarios

The specification has been validated against a quality checklist and all items have passed. The specification is now ready for the next phase of development using the Spec-Driven Development approach.

## Outcome

- ✅ Impact: Created comprehensive spec for advanced todo features with recurring tasks, due dates, and reminders
- 🧪 Tests: Specification validated against quality checklist with all items passing
- 📁 Files: Created spec.md and requirements checklist in specs/002-todo-advanced-features/
- 🔁 Next prompts: Ready for /sp.plan to create implementation plan
- 🧠 Reflection: Specification follows SDD principles and is ready for planning phase

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All validation items passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed with planning phase
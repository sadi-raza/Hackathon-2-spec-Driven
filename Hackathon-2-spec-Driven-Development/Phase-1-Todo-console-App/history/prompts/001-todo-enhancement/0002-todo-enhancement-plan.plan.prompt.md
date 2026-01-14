---
id: 0002
title: todo-enhancement-plan
stage: plan
date: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-enhancement
branch: 001-todo-enhancement
user: user
command: /sp.plan
labels: ["planning", "todo", "enhancement", "architecture", "data-model"]
links:
  spec: ../specs/001-todo-enhancement/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-todo-enhancement/plan.md
 - specs/001-todo-enhancement/research.md
 - specs/001-todo-enhancement/data-model.md
 - specs/001-todo-enhancement/quickstart.md
 - specs/001-todo-enhancement/contracts/task-api-contract.md
tests:
 - null
---

## Prompt

Read speckit.constitution and speckit.specify-intermediate carefully.

Now generate a complete speckit.plan for extending the existing Phase I in-memory console Todo app with Intermediate Level features (Priorities, Tags/Categories, Search, Filter, Sort).

Key constraints from constitution:
- 100% Claude Code generated (no manual coding)
- Reuse existing structure and code where possible
- Clean architecture, separation of concerns
- Prepare for future phases (reusable models/logic)

Plan Structure Requirements:
1. High-level Architecture Overview
   - How existing components (models.py, todo_manager.py, main.py) will be extended

2. Updated Data Model
   - Extend Task model with priority, tags:list[str], created_at:datetime
   - Use dataclass with proper type hints and defaults

3. Component Breakdown
   - models.py: Updated Task class
   - todo_manager.py: New methods for filter, search, sort
   - ui/cli.py or main.py: Enhanced menu system and display logic
   - Optional: utils.py for formatting helpers

4. Key Implementation Strategies
   - Priority: enum or string constants (HIGH="high", MEDIUM="medium", LOW="low")
   - Tags: store as list[str], input as comma-separated
   - Search: case-insensitive contains in title or description
   - Filter: support multiple criteria (status, priority, tag)
   - Sort: flexible sorting with key functions (priority order, title alpha, created_at)

5. CLI Flow Enhancements
   - Main menu with sub-options for View (Filter/Sort/Search)
   - Input prompts for priority and tags during add/update
   - Pretty table display with priority icons and tags

6. Reusability Considerations
   - Design Task model and manager methods to be reusable in future web/API phases
   - Validation logic that can become reusable skill later

7. Potential Risks & Mitigations
   - Performance with large lists (acceptable for in-memory demo)
   - Input validation for priority/tags

8. Testing Approach
   - Manual demo flow for all new features
   - Edge cases: empty list, no matches, invalid priority

Generate the plan in clean Markdown format with clear sections. Ensure every part traces back to requirements in speckit.specify-intermediate.

After plan, suggest next step: generate speckit.tasks for implementation.

## Response snapshot

Successfully created the implementation plan for the Todo Application Enhancement feature with all required artifacts:

1. Implementation Plan (plan.md) - Complete architecture overview with technical context and constitution compliance
2. Research Document (research.md) - Detailed research on implementation strategies for each feature
3. Data Model (data-model.md) - Comprehensive data model with Task, FilterCriteria, SortCriteria, and TaskSearchResult entities
4. Quickstart Guide (quickstart.md) - Step-by-step implementation guide
5. API Contract (contracts/task-api-contract.md) - Detailed contract for all methods and interfaces
6. Agent Context Updated - Technology stack added to Claude context

The plan addresses all requirements from the specification including:
- Enhanced Task model with priority, tags, and created_at fields
- New filtering, searching, and sorting capabilities
- Updated CLI interface with submenu options
- Proper validation and error handling
- Backward compatibility with existing functionality

## Outcome

- ✅ Impact: Complete implementation plan created with all required artifacts for todo enhancement
- 🧪 Tests: Contract defines validation for all new functionality
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contract files
- 🔁 Next prompts: Ready to generate tasks using /sp.tasks for implementation
- 🧠 Reflection: Plan addresses all architectural requirements and maintains Phase I constraints

## Evaluation notes (flywheel)

- Failure modes observed: Directory naming conflict with multiple "001" prefixes
- Graders run and results (PASS/FAIL): Not applicable at this stage
- Prompt variant (if applicable): Standard planning workflow
- Next experiment (smallest change to try): Generate tasks from this plan

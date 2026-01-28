# ADR 001: Multi-Phase Task Organization for Spec-Driven Development

## Status
Proposed

## Date
2026-01-09

## Context
When implementing complex features through spec-driven development, there's a need to organize implementation tasks in a way that:
- Enables independent development of user stories
- Maintains clear dependencies between foundational and feature-specific work
- Supports both solo and team-based development approaches
- Facilitates incremental delivery and validation of functionality
- Allows for parallel execution where possible to accelerate development

Traditional linear task lists often create bottlenecks and don't reflect the interconnected nature of software development where some work must precede others while other work can proceed in parallel.

## Decision
We will organize implementation tasks using a multi-phase approach with the following structure:

### Phase 1: Setup
- Project initialization and basic structure
- Can start immediately with no dependencies
- Often includes parallelizable foundational setup tasks

### Phase 2: Foundational
- Core infrastructure that blocks all subsequent user story work
- Must be completed before any user story implementation begins
- Includes authentication, database setup, error handling, etc.

### Phase 3+: User Stories
- Each user story gets its own phase organized by priority (P1, P2, P3, etc.)
- All user stories depend on foundational phase completion
- User stories can proceed in parallel after foundation is complete
- Each user story should be independently testable and deliverable

### Final Phase: Polish & Cross-Cutting
- Improvements that affect multiple user stories
- Depends on desired user stories being complete

### Task Format
Each task follows the format: `[ ] T### [P] [US#] Description with file path`
- T###: Sequential task ID
- [P]: Indicates task can run in parallel (different files, no dependencies)
- [US#]: Maps to specific user story for traceability
- Includes exact file paths in descriptions

## Alternatives Considered

### Linear Task List
- Pros: Simple to understand and follow
- Cons: Creates artificial dependencies, no parallelization opportunities, harder to track progress by user story

### Pure Parallel Approach
- Pros: Maximum parallelization
- Cons: Difficult to manage dependencies, risk of incomplete foundations, harder to ensure coherent architecture

### Agile Sprint-Based
- Pros: Familiar to teams, allows for reprioritization
- Cons: Doesn't align with spec-driven approach, harder to track against specific user stories in spec

## Consequences

### Positive
- Enables independent validation of each user story
- Supports both solo and team-based development
- Facilitates MVP-first delivery approach
- Makes dependencies explicit and manageable
- Allows for parallel work after foundational phase
- Maintains traceability from spec user stories to implementation tasks
- Enables incremental delivery and testing

### Negative
- More complex than simple linear task list
- Requires upfront planning to identify dependencies correctly
- May require adjustments if dependencies are discovered later
- Could lead to over-engineering if not managed carefully

## Implementation
The approach is implemented through the `/sp.tasks` command which:
1. Reads user stories from spec.md with their priorities
2. Identifies foundational requirements from plan.md
3. Generates tasks organized by phase
4. Marks parallelizable tasks with [P] indicator
5. Links tasks to specific user stories with [US#] labels
6. Includes exact file paths for clarity

## Examples
In the FastAPI Todo API implementation, this resulted in:
- Phase 1: Project structure and dependency setup
- Phase 2: Database, JWT auth, error handling foundations
- Phase 3: User Story 1 (Create Task) - P1 priority
- Phase 4: User Story 2 (View Tasks) - P1 priority
- Phase 5: User Story 3 (Update Task) - P2 priority
- And so on...

## Related Decisions
- User Story Prioritization (defined in spec.md)
- MVP-First Delivery Strategy (implemented in tasks.md)
- Parallel Development Enablement (reflected in [P] markings)

## References
- Feature Spec: `specs/001-fastapi-todo-api/spec.md`
- Implementation Plan: `specs/001-fastapi-todo-api/plan.md`
- Generated Tasks: `specs/001-fastapi-todo-api/tasks.md`
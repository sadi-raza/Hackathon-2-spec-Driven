# Quickstart Guide: Phase I - Todo In-Memory Python Console App

**Date**: 2025-12-30
**Feature**: Phase I - Todo In-Memory Python Console App
**Branch**: 001-phase1-todo-console

## Overview
This guide provides instructions to quickly set up and run the Phase I Todo console application.

## Prerequisites
- Python 3.13+ installed
- UV package manager installed

## Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd /path/to/hackathon-todo
   ```

2. **Create virtual environment**
   ```bash
   uv venv
   ```

3. **Activate virtual environment**
   ```bash
   source .venv/bin/activate  # On Linux/macOS
   # or
   .venv\Scripts\activate    # On Windows
   ```

4. **Run the application**
   ```bash
   uv run src/main.py
   ```

## Basic Usage

Once the application is running, you'll see the command prompt. Here are the available commands:

- **Add a task**: `add "Task title" "Optional description"`
- **List all tasks**: `list` or `ls`
- **Update a task**: `update <task_id> "New title" "New description"` (use empty quotes to keep existing)
- **Mark complete**: `complete <task_id>`
- **Mark incomplete**: `incomplete <task_id>`
- **Delete a task**: `delete <task_id>` (with confirmation)
- **Exit application**: `exit` or `quit`

## Example Session

```
> add "Buy groceries" "Milk, bread, eggs"
Task #1 added: Buy groceries
> add "Finish report"
Task #2 added: Finish report
> list
ID  | Title          | Description      | Status
--- | -------------- | ---------------- | --------
1   | Buy groceries  | Milk, bread, eggs| ⏳ Pending
2   | Finish report  | (no description) | ⏳ Pending
> complete 1
Task #1 marked as complete: Buy groceries
> list
ID  | Title          | Description      | Status
--- | -------------- | ---------------- | --------
1   | Buy groceries  | Milk, bread, eggs| ✅ Completed
2   | Finish report  | (no description) | ⏳ Pending
> exit
Goodbye!
```

## Troubleshooting

- If you get a "command not found" error, ensure your virtual environment is activated
- If the application fails to start, check that Python 3.13+ is installed
- For any other issues, ensure all source files exist in the `src/` directory as specified in the project structure
# Quickstart Guide: Phase I Console App

**Date**: 2026-01-14
**Feature**: Task CRUD Operations
**Plan**: specs/2-plan/phase-1-console.md

## Overview

This guide provides instructions for setting up, running, and using the Phase I Console App for task management. The application implements a layered architecture with clean separation of concerns, making it easy to extend in future phases.

## Prerequisites

- Python 3.13 or higher
- UV package manager
- Operating system: Linux, macOS, or Windows

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd evolution-of-todo-list-01
```

### 2. Install Dependencies

Using UV package manager:

```bash
uv sync
```

This will install all required dependencies including:
- Pydantic (for data models)
- Pytest (for testing)

### 3. Verify Installation

Run the tests to ensure everything is set up correctly:

```bash
uv run pytest
```

## Running the Application

### 1. Execute the Application

```bash
uv run python src/main.py
```

Or if you have the project installed in development mode:

```bash
python src/main.py
```

### 2. Interactive Mode

The application runs in interactive mode. After starting, you can enter commands directly:

```text
> add "Buy groceries" "Milk, eggs, bread"
[SUCCESS] Task 1 "Buy groceries" created.

> add "Walk the dog"
[SUCCESS] Task 2 "Walk the dog" created.

> view
ID | Status | Title
1  | [ ]    | Buy groceries - Milk, eggs, bread
2  | [ ]    | Walk the dog

> complete 1
[SUCCESS] Task 1 marked as complete.

> view
ID | Status | Title
1  | [x]    | Buy groceries - Milk, eggs, bread
2  | [ ]    | Walk the dog

> exit
Goodbye!
```

## Available Commands

### Add Task
```bash
add "title" "optional description"
```
Creates a new task with the specified title and optional description.
- **Success**: Displays "Task X created" message
- **Errors**: Shows specific error messages for invalid input (empty title, title too long, etc.)

### View Tasks
```bash
view
```
Displays all tasks with their ID, status, and title.
- **Success**: Shows formatted list of all tasks
- **Errors**: Shows "No tasks in your list" if no tasks exist

### Update Task
```bash
update <id> "new title" "optional new description"
```
Updates the task with the specified ID with new title and description.
- **Success**: Displays "Task X updated" message
- **Errors**: Shows "Task ID not found" or validation errors

### Delete Task
```bash
delete <id>
```
Removes the task with the specified ID.
- **Success**: Displays "Task X deleted" message
- **Errors**: Shows "Task ID not found" if ID doesn't exist

### Mark Complete/Incomplete
```bash
complete <id>
```
Toggles the completion status of the task with the specified ID.
- **Success**: Displays "Task X marked as complete/incomplete" message
- **Errors**: Shows "Task ID not found" if ID doesn't exist

### Exit Application
```bash
exit
```
Terminates the application.

## Project Structure

The application follows a layered architecture:

```
src/
├── models/
│   └── task.py          # Task data model with validation
├── repositories/
│   └── task_repository.py # In-memory storage operations
├── services/
│   └── task_service.py  # Business logic and validation
├── cli/
│   └── interface.py     # Command parsing and execution
└── main.py             # Application entry point
```

## Development

### Running Tests

Execute all tests:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov=src
```

### Adding New Features

1. Update the specification in `specs/1-specify/features/`
2. Update the plan in `specs/2-plan/` if needed
3. Create tasks in `specs/3-tasks/`
4. Implement the feature following the layered architecture

### Architecture Principles

- **Models**: Handle data validation and structure
- **Repositories**: Manage data storage and retrieval
- **Services**: Implement business logic and validation
- **CLI**: Handle user input and output
- **Main**: Orchestrate the components

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Ensure you've run `uv sync` to install dependencies
2. **Permission Error**: Make sure you have write permissions to the project directory
3. **Invalid Command**: Check command syntax matches the available commands

### Performance Tips

- The application is designed for task lists up to 1000 items
- For larger datasets, consider implementing pagination in future phases
- Response times should be under 100ms for all operations

## Next Steps

This Phase I implementation provides a solid foundation for the Todo Evolution project. In Phase II, the architecture is designed to easily accommodate a web interface while reusing the service and repository layers.
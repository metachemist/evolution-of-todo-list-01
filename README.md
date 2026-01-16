# Todo Evolution - From CLI to Cloud-Native AI

This project demonstrates the evolution of a simple todo application from a command-line interface to a cloud-native AI-powered system. The progression occurs in phases, with each building upon the previous one to create a robust, scalable, and intelligent todo management platform.

## Phase I: Console Application

The first phase implements a console-based task management application with the following features:
- Add, Delete, Update, View, and Mark Complete operations
- In-memory session storage
- Console-based user interactions

## Setup

1. Clone the repository
2. Install dependencies with `uv sync`
3. Run the application with `python src/main.py` or `uv run python -m src.main`
4. Use the CLI commands to manage tasks

## How to Run

To run the application:

```bash
# Using uv (recommended)
uv run python -m src.main

# Or directly with Python
python src/main.py
```

## Supported Commands

- `add "title" "optional description"` - Add a new task
- `view` - Display all tasks
- `update <id> "title" "optional description"` - Update a task
- `delete <id>` - Delete a task
- `complete <id>` - Toggle completion status
- `exit` - Exit the application

### Command Examples

```bash
# Add a task with title only
add "Buy groceries"

# Add a task with title and description
add "Walk the dog" "Take the dog for a 30-minute walk"

# View all tasks
view

# Update a task
update 1 "Buy milk and bread" "Get whole milk and sourdough"

# Mark a task as complete/incomplete
complete 1

# Delete a task
delete 1

# Exit the application
exit
```

## Technologies Used

- Python 3.13+
- Pydantic for data validation
- Argparse for CLI parsing
- Pytest for testing
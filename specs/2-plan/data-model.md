# Data Model: Phase I Console App

**Date**: 2026-01-14
**Feature**: Task CRUD Operations
**Plan**: specs/2-plan/phase-1-console.md

## Overview

This document defines the data models for the Phase I Console App, focusing on the Task entity with validation rules and relationships as specified in the feature requirements.

## Core Entity: Task

### Entity Definition

The `Task` entity represents a single todo item with the following attributes:

- **id**: Unique identifier for the task (integer)
- **title**: Required string representing the task name (1-200 characters)
- **description**: Optional string providing additional details about the task (0-500 characters)
- **completed**: Boolean indicating whether the task is completed (true) or pending (false)
- **created_at**: Timestamp indicating when the task was created

### Pydantic Model

```python
from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from typing import Optional

class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = datetime.now(timezone.utc)

    @field_validator('title')
    def validate_title(cls, v):
        if len(v) < 1 or len(v) > 200:
            raise ValueError('Title must be between 1 and 200 characters')
        return v

    @field_validator('description')
    def validate_description(cls, v):
        if v and len(v) > 500:
            raise ValueError('Description must not exceed 500 characters')
        return v
```

### Custom Exception Classes

```python
class TaskNotFoundException(Exception):
    """Raised when a task with a specific ID is not found"""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")

class InvalidTaskDataException(Exception):
    """Raised when task data fails validation"""
    def __init__(self, message: str):
        super().__init__(message)

class ValidationError(Exception):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message)
```

### Validation Rules

1. **Title Validation**:
   - Minimum length: 1 character
   - Maximum length: 200 characters
   - Required: Yes

2. **Description Validation**:
   - Minimum length: 0 characters
   - Maximum length: 500 characters
   - Required: No (optional field)

3. **ID Validation**:
   - Type: Integer
   - Uniqueness: Must be unique within the task list
   - Generation: Auto-incremented from the last used ID

4. **Completed Status**:
   - Type: Boolean
   - Default: False
   - Values: True (completed) or False (pending)

### State Transitions

The `completed` field supports the following state transitions:

- **Pending to Completed**: When the user marks a task as complete
- **Completed to Pending**: When the user marks a completed task as incomplete

### Relationships

The Task entity exists as part of a collection managed by the `InMemoryTaskRepository`:

- **Collection Type**: `List[Task]`
- **Management**: Repository handles all CRUD operations
- **Access Pattern**: Sequential access for display, indexed access for updates/deletes

## Repository Interface

### InMemoryTaskRepository

The repository interface for managing Task entities:

```python
from typing import List, Optional

class InMemoryTaskRepository:
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1
    
    def create(self, task: Task) -> Task:
        """Add a new task to the repository with a unique ID"""
        task.id = self._next_id
        self._next_id += 1
        self._tasks.append(task)
        return task
    
    def find_all(self) -> List[Task]:
        """Retrieve all tasks from the repository"""
        return self._tasks.copy()
    
    def find_by_id(self, id: int) -> Optional[Task]:
        """Find a task by its ID"""
        for task in self._tasks:
            if task.id == id:
                return task
        return None
    
    def update(self, id: int, task: Task) -> Optional[Task]:
        """Update an existing task"""
        for i, existing_task in enumerate(self._tasks):
            if existing_task.id == id:
                task.id = id  # Preserve the original ID
                self._tasks[i] = task
                return task
        return None
    
    def delete(self, id: int) -> bool:
        """Delete a task by its ID"""
        for i, task in enumerate(self._tasks):
            if task.id == id:
                del self._tasks[i]
                return True
        return False
```

## Data Flow

### Creation Flow
1. User enters `add "title" "optional description"`
2. CLI parses the command
3. TaskService validates the input
4. TaskService creates a new Task instance
5. InMemoryTaskRepository assigns an ID and stores the task

### Retrieval Flow
1. User enters `view` command
2. CLI parses the command
3. TaskService requests all tasks
4. InMemoryTaskRepository returns all stored tasks
5. CLI formats and displays the tasks

### Update Flow
1. User enters `update <id> "title" "optional description"`
2. CLI parses the command
3. TaskService validates the input and finds the task by ID
4. TaskService updates the task with new data
5. InMemoryTaskRepository updates the stored task

### Deletion Flow
1. User enters `delete <id>`
2. CLI parses the command
3. TaskService requests deletion by ID
4. InMemoryTaskRepository removes the task from storage

### Completion Flow
1. User enters `complete <id>`
2. CLI parses the command
3. TaskService finds the task by ID and toggles completion status
4. InMemoryTaskRepository updates the stored task

## Constraints

### Storage Constraints
- **In-Memory Only**: Data persists only during the application session
- **Session Bound**: All data is lost when the application exits
- **Size Limitation**: Practical limit based on available memory

### Validation Constraints
- **Title Length**: 1-200 characters
- **Description Length**: 0-500 characters
- **ID Uniqueness**: Each task must have a unique ID
- **Required Fields**: Title is required, description is optional

### Performance Constraints
- **Response Time**: All operations should complete within 100ms
- **Memory Usage**: Should not exceed reasonable memory limits
- **Scalability**: Designed for single-user, moderate-sized task lists
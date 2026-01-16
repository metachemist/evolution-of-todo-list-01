# [Task]: T-002 | [From]: specs/2-plan/phase-1-console.md

from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from typing import Optional


class TaskException(Exception):
    """Base exception class for all task-related errors"""
    pass


class TaskNotFoundException(TaskException):
    """Raised when a requested task ID does not exist"""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class InvalidTaskDataException(TaskException):
    """Raised when task data fails validation"""
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


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
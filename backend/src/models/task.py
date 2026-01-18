# [Task]: T-002 | [From]: specs/2-plan/phase-2-fullstack.md

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from datetime import datetime, timezone
import uuid
from typing import Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .user import User  # Forward reference for type checking


class TaskBase(SQLModel):
    """
    Base class for Task model with common fields.
    """
    title: str = Field(
        sa_column=Column(String(200), nullable=False),
        description="Required title of the task (1-200 characters)"
    )
    description: Optional[str] = Field(
        sa_column=Column(String(1000)),
        description="Optional description of the task (max 1000 characters)"
    )
    completed: bool = Field(
        default=False,
        description="Boolean indicating if the task is completed"
    )


class Task(TaskBase, table=True):
    """
    Task model representing a todo item in the system.
    """
    __tablename__ = "tasks"

    id: int = Field(
        default=None,
        primary_key=True,
        description="Unique identifier for the task"
    )
    user_id: uuid.UUID = Field(
        foreign_key="users.id",
        ondelete="CASCADE",  # Critical: Ensure tasks are deleted when user is deleted
        description="Foreign key linking to the owning user"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        description="Timestamp when the task was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        description="Timestamp when the task was last updated"
    )

    # Relationship to user (many-to-one)
    # Using forward reference to prevent circular imports
    user: Optional["User"] = Relationship(
        back_populates="tasks"
    )


class TaskCreate(TaskBase):
    """
    Model for creating new tasks.
    Inherits all fields from TaskBase.
    """
    pass  # All fields inherited from TaskBase


class TaskUpdate(TaskBase):
    """
    Model for partial task updates.
    All fields are optional to allow partial updates.
    """
    title: Optional[str] = Field(
        default=None,
        sa_column=Column(String(200)),
        description="New title for the task (optional)"
    )
    description: Optional[str] = Field(
        default=None,
        sa_column=Column(String(1000)),
        description="New description for the task (optional)"
    )
    completed: Optional[bool] = Field(
        default=None,
        description="New completion status (optional)"
    )


class TaskPublic(TaskBase):
    """
    Model for task responses in API.
    Includes ID and timestamps but excludes user_id for security.
    """
    id: int
    created_at: datetime
    updated_at: datetime
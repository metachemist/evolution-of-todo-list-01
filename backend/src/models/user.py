# [Task]: T-002 | [From]: specs/2-plan/phase-2-fullstack.md

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String
from datetime import datetime, timezone
import uuid
from typing import List, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .task import Task, TaskPublic  # Forward reference for type checking


class UserBase(SQLModel):
    """
    Base class for User model with common fields.
    """
    email: str = Field(
        sa_column=Column(String(254), unique=True, nullable=False),
        description="User's email address (unique)"
    )
    name: str = Field(
        sa_column=Column(String(100), nullable=False),
        description="User's display name"
    )


class User(UserBase, table=True):
    """
    User model representing a registered user in the system.
    """
    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique identifier for the user"
    )
    password_hash: str = Field(
        sa_column=Column(String, nullable=False),
        description="Hashed password for authentication"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the user was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the user was last updated"
    )

    # Relationship to tasks (one-to-many)
    # Using forward reference to prevent circular imports
    tasks: List["Task"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class UserCreate(SQLModel):
    """
    Model for creating new users.
    Has a plain password field that gets hashed before storing.
    """
    email: str = Field(
        sa_column=Column(String(254), unique=True, nullable=False),
        description="User's email address (unique)"
    )
    name: str = Field(
        sa_column=Column(String(100), nullable=False),
        description="User's display name"
    )
    password: str = Field(
        min_length=8,
        max_length=70,
        description="Plain text password (will be hashed before storage, max 70 bytes)"
    )


class UserUpdate(SQLModel):
    """
    Model for partial user updates.
    All fields are optional to allow partial updates.
    """
    email: Optional[str] = Field(
        default=None,
        sa_column=Column(String(254), unique=True),
        description="New email for the user (optional)"
    )
    name: Optional[str] = Field(
        default=None,
        sa_column=Column(String(100)),
        description="New name for the user (optional)"
    )
    password_hash: Optional[str] = Field(
        default=None,
        sa_column=Column(String),
        description="New hashed password (optional)"
    )


class UserPublic(UserBase):
    """
    Model for user responses in API.
    Includes ID and timestamps but excludes password_hash for security.
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        """Convert from ORM object to Pydantic model."""
        return cls(
            id=obj.id,
            email=obj.email,
            name=obj.name,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )
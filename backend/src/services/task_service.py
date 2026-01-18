"""
Task service for the Todo Evolution backend.

This module provides business logic for task management operations.
"""

from typing import List, Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from src.models.user import User
from src.repositories.task_repository import TaskRepository
import uuid
import re


class TaskService:
    """
    Service class for handling task business logic with user isolation.
    """

    def __init__(self):
        self.task_repo = TaskRepository()

    def _validate_title(self, title: str) -> bool:
        """
        Validate task title.

        Args:
            title: Title to validate

        Returns:
            True if title meets requirements, False otherwise
        """
        # Title should be 1-200 characters
        return 1 <= len(title) <= 200

    def _validate_description(self, description: Optional[str]) -> bool:
        """
        Validate task description.

        Args:
            description: Description to validate

        Returns:
            True if description meets requirements, False otherwise
        """
        if description is None:
            return True
        # Description should be 0-1000 characters
        return len(description) <= 1000

    async def create_task(self, session: AsyncSession, user: User, task_create: TaskCreate) -> Optional[TaskPublic]:
        """
        Create a new task for the specified user.

        Args:
            session: Async database session
            user: User object who owns the task
            task_create: Task creation data

        Returns:
            Created TaskPublic object if successful

        Raises:
            ValueError: If input validation fails
        """
        # Validate inputs
        if not self._validate_title(task_create.title):
            raise ValueError("Title must be between 1 and 200 characters")

        if not self._validate_description(task_create.description):
            raise ValueError("Description must be between 0 and 1000 characters")

        # Create the task with the user's ID
        task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=user.id
        )

        created_task = await self.task_repo.create_task(session, task)

        # Convert to public representation
        return TaskPublic.from_orm(created_task)

    async def list_tasks(self, session: AsyncSession, user_id: uuid.UUID, offset: int = 0, limit: int = 20) -> Tuple[List[TaskPublic], int]:
        """
        List tasks for the specified user with pagination.

        Args:
            session: Async database session
            user_id: ID of the user whose tasks to retrieve
            offset: Offset for pagination
            limit: Limit for pagination

        Returns:
            Tuple of (List of TaskPublic objects, total count)
        """
        return await self.task_repo.get_tasks(session, user_id, offset, limit)

    async def get_task(self, session: AsyncSession, task_id: int, user_id: uuid.UUID) -> Optional[TaskPublic]:
        """
        Get a specific task by ID for the specified user.

        Args:
            session: Async database session
            task_id: ID of the task to retrieve
            user_id: ID of the user who owns the task

        Returns:
            TaskPublic object if found and owned by user, None otherwise
        """
        return await self.task_repo.get_task_by_id(session, task_id, user_id)

    async def update_task(self, session: AsyncSession, task_id: int, user_id: uuid.UUID, task_update: TaskUpdate) -> Optional[TaskPublic]:
        """
        Update a specific task by ID for the specified user.

        Args:
            session: Async database session
            task_id: ID of the task to update
            user_id: ID of the user who owns the task
            task_update: Task update data

        Returns:
            Updated TaskPublic object if successful, None if task not found or not owned by user

        Raises:
            ValueError: If input validation fails
        """
        # Validate inputs if they are provided
        if task_update.title is not None and not self._validate_title(task_update.title):
            raise ValueError("Title must be between 1 and 200 characters")

        if task_update.description is not None and not self._validate_description(task_update.description):
            raise ValueError("Description must be between 0 and 1000 characters")

        return await self.task_repo.update_task(session, task_id, user_id, task_update)

    async def delete_task(self, session: AsyncSession, task_id: int, user_id: uuid.UUID) -> bool:
        """
        Delete a specific task by ID for the specified user.

        Args:
            session: Async database session
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if task was successfully deleted, False otherwise
        """
        return await self.task_repo.delete_task(session, task_id, user_id)

    async def toggle_completion(self, session: AsyncSession, task_id: int, user_id: uuid.UUID) -> Optional[TaskPublic]:
        """
        Toggle the completion status of a specific task by ID for the specified user.

        Args:
            session: Async database session
            task_id: ID of the task to toggle
            user_id: ID of the user who owns the task

        Returns:
            Updated TaskPublic object if successful, None if task not found or not owned by user
        """
        updated_task = await self.task_repo.toggle_completion(session, task_id, user_id)
        if not updated_task:
            return None
            
        # Convert to public representation
        return TaskPublic.from_orm(updated_task)
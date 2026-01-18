# [Task]: T-003 | [From]: specs/2-plan/phase-2-fullstack.md

from typing import List, Optional, Tuple
from sqlmodel import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from ..models.user import User
import uuid


class TaskRepository:
    """
    Repository class for handling Task data operations with user isolation.
    """

    async def create_task(self, session: AsyncSession, task: Task) -> Task:
        """
        Create a new task.

        Args:
            session: Async database session
            task: Task object to create (with user_id already set)

        Returns:
            Created Task object with assigned ID
        """
        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task

    async def get_tasks(self, session: AsyncSession, user_id: uuid.UUID, offset: int = 0, limit: int = 20) -> Tuple[List[TaskPublic], int]:
        """
        Retrieve all tasks for a specific user with pagination.

        Args:
            session: Async database session
            user_id: ID of the user whose tasks to retrieve
            offset: Offset for pagination (default: 0)
            limit: Limit for pagination (default: 20, max: 100)

        Returns:
            Tuple of (List of public tasks, total count)
        """
        # Ensure limit is within bounds
        if limit > 100:
            limit = 100

        # Get the tasks for the user
        statement = select(Task).where(Task.user_id == user_id).offset(offset).limit(limit)
        result = await session.execute(statement)
        tasks = result.scalars().all()

        # Get the total count
        count_statement = select(func.count(Task.id)).where(Task.user_id == user_id)
        count_result = await session.execute(count_statement)
        total_count = count_result.scalar()

        # Convert to public representation
        task_list = [TaskPublic.from_orm(task) for task in tasks]

        return task_list, total_count

    async def get_task_by_id(self, session: AsyncSession, task_id: int, user_id: uuid.UUID) -> Optional[TaskPublic]:
        """
        Retrieve a specific task by ID for a specific user.

        Args:
            session: Async database session
            task_id: ID of the task to retrieve
            user_id: ID of the user who owns the task

        Returns:
            TaskPublic object if found and owned by user, None otherwise
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if task:
            # Convert to public representation
            return TaskPublic.from_orm(task)
        return None

    async def update_task(self, session: AsyncSession, task_id: int, user_id: uuid.UUID, update_data: TaskUpdate) -> Optional[TaskPublic]:
        """
        Update an existing task if it belongs to the specified user.

        Args:
            session: Async database session
            task_id: ID of the task to update
            user_id: ID of the user who owns the task
            update_data: TaskUpdate object with new values

        Returns:
            Updated TaskPublic object if successful, None if task not found or not owned by user
        """
        # Get the existing task
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Update the task with provided values
        if update_data.title is not None:
            task.title = update_data.title
        if update_data.description is not None:
            task.description = update_data.description
        if update_data.completed is not None:
            task.completed = update_data.completed

        # Update the updated_at timestamp
        from datetime import datetime, timezone
        task.updated_at = datetime.now(timezone.utc)

        session.add(task)
        await session.commit()
        await session.refresh(task)

        # Convert to public representation
        return TaskPublic.from_orm(task)

    async def delete_task(self, session: AsyncSession, task_id: int, user_id: uuid.UUID) -> bool:
        """
        Delete a task if it belongs to the specified user.

        Args:
            session: Async database session
            task_id: ID of the task to delete
            user_id: ID of the user who owns the task

        Returns:
            True if task was successfully deleted, False if not found or not owned by user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.first()

        if not task:
            return False

        task = task.Task
        await session.delete(task)
        await session.commit()
        return True

    async def toggle_completion(self, session: AsyncSession, task_id: int, user_id: uuid.UUID) -> Optional[Task]:
        """
        Toggle the completion status of a task if it belongs to the specified user.

        Args:
            session: Async database session
            task_id: ID of the task to toggle
            user_id: ID of the user who owns the task

        Returns:
            Updated Task object if successful, None if task not found or not owned by user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            return None

        # Toggle the completion status
        task.completed = not task.completed
        from datetime import datetime, timezone
        task.updated_at = datetime.now(timezone.utc)

        session.add(task)
        await session.commit()
        await session.refresh(task)
        return task
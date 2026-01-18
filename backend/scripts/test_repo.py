#!/usr/bin/env python3
# [Task]: T-003 | [From]: specs/2-plan/phase-2-fullstack.md

"""
Test script to verify repository functionality.
This script tests the basic CRUD operations for users and tasks.
"""

import asyncio
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from src.db.session import AsyncSessionLocal, engine
from src.models.user import User
from src.models.task import Task
from src.repositories.user_repository import UserRepository
from src.repositories.task_repository import TaskRepository
import uuid
from datetime import datetime, timezone


async def test_repository_functionality():
    """
    Test the repository functionality by creating a user, creating a task for that user,
    and then retrieving the task.
    """
    # Create repositories
    user_repo = UserRepository()
    task_repo = TaskRepository()

    import time

    # Create a dummy user with a unique email
    unique_email = f"test_{int(time.time())}@example.com"
    user = User(
        id=uuid.uuid4(),
        email=unique_email,
        name="Test User",
        password_hash="hashed_password_here",
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )

    # Create a task for that user
    task = Task(
        id=None,  # Will be auto-assigned by the database
        user_id=user.id,
        title="Test Task",
        description="This is a test task",
        completed=False,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )

    # Use a session to perform operations
    async with AsyncSessionLocal() as session:
        # Create the user
        created_user = await user_repo.create_user(session, user)
        print(f"Created user: {created_user.name} ({created_user.email})")

        # Extract the user ID immediately after creation
        user_id = created_user.id

        # Update the task to have the user_id before creating
        task.user_id = user_id

        # Create the task for the user
        created_task = await task_repo.create_task(session, task)
        print(f"Created task: {created_task.title}")

        # Try to fetch the task using the task repository
        retrieved_tasks, count = await task_repo.get_tasks(session, user_id)
        print(f"Fetched {len(retrieved_tasks)} tasks for user")

        if len(retrieved_tasks) > 0:
            print(f"First task: {retrieved_tasks[0].title}")
            print("SUCCESS")
        else:
            print("FAILURE - No tasks retrieved")

    # Close the engine
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_repository_functionality())
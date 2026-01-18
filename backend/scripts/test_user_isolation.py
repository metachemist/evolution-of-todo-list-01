#!/usr/bin/env python3
# [Task]: T-012 | [From]: specs/2-plan/phase-2-fullstack.md

"""
Test script to verify user isolation in the Todo Evolution backend.
This script verifies that users cannot access other users' data.
"""

import asyncio
import sys
import os

# Add the backend/src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.db.session import AsyncSessionLocal, engine
from src.models.user import User
from src.models.task import Task
from src.repositories.user_repository import UserRepository
from src.repositories.task_repository import TaskRepository
import uuid
from datetime import datetime, timezone


async def test_user_isolation():
    """
    Test that users can only access their own tasks and not other users' tasks.
    """
    print("🧪 Testing user isolation...")
    
    # Create repositories
    user_repo = UserRepository()
    task_repo = TaskRepository()

    # Create two different users
    user1_email = f"user1_{int(datetime.now(timezone.utc).timestamp())}@example.com"
    user2_email = f"user2_{int(datetime.now(timezone.utc).timestamp())}@example.com"
    
    user1 = User(
        id=uuid.uuid4(),
        email=user1_email,
        name="User 1",
        password_hash="hashed_password_here",
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )

    user2 = User(
        id=uuid.uuid4(),
        email=user2_email,
        name="User 2",
        password_hash="hashed_password_here",
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )

    # Create tasks for each user
    task1_for_user1 = Task(
        id=None,  # Will be auto-assigned by the database
        user_id=user1.id,
        title="Task 1 for User 1",
        description="This is a task for user 1",
        completed=False,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )

    task2_for_user1 = Task(
        id=None,  # Will be auto-assigned by the database
        user_id=user1.id,
        title="Task 2 for User 1",
        description="This is another task for user 1",
        completed=True,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )

    task1_for_user2 = Task(
        id=None,  # Will be auto-assigned by the database
        user_id=user2.id,
        title="Task 1 for User 2",
        description="This is a task for user 2",
        completed=False,
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None)
    )

    async with AsyncSessionLocal() as session:
        # Create the users
        created_user1 = await user_repo.create_user(session, user1)
        created_user2 = await user_repo.create_user(session, user2)
        print(f"   Created users: {created_user1.email}, {created_user2.email}")

        # Create tasks for each user
        created_task1_u1 = await task_repo.create_task(session, task1_for_user1)
        created_task2_u1 = await task_repo.create_task(session, task2_for_user1)
        created_task1_u2 = await task_repo.create_task(session, task1_for_user2)
        print(f"   Created tasks: {created_task1_u1.title}, {created_task2_u1.title}, {created_task1_u2.title}")

        # Test that user1 can only see their own tasks
        user1_tasks, user1_task_count = await task_repo.get_tasks(session, user1.id)
        print(f"   User 1 sees {len(user1_tasks)} tasks: {[t.title for t in user1_tasks]}")
        
        # Test that user2 can only see their own tasks
        user2_tasks, user2_task_count = await task_repo.get_tasks(session, user2.id)
        print(f"   User 2 sees {len(user2_tasks)} tasks: {[t.title for t in user2_tasks]}")

        # Verify user isolation
        assert len(user1_tasks) == 2, f"User 1 should have 2 tasks, but has {len(user1_tasks)}"
        assert len(user2_tasks) == 1, f"User 2 should have 1 task, but has {len(user2_tasks)}"
        
        # Verify that user1's tasks are only user1's tasks
        user1_task_titles = [task.title for task in user1_tasks]
        assert "Task 1 for User 1" in user1_task_titles
        assert "Task 2 for User 1" in user1_task_titles
        assert "Task 1 for User 2" not in user1_task_titles  # User 1 should not see user 2's task
        
        # Verify that user2's tasks are only user2's tasks
        user2_task_titles = [task.title for task in user2_tasks]
        assert "Task 1 for User 2" in user2_task_titles
        assert "Task 1 for User 1" not in user2_task_titles  # User 2 should not see user 1's tasks
        assert "Task 2 for User 1" not in user2_task_titles  # User 2 should not see user 1's tasks

        # Test individual task access
        # User 1 should be able to access their own tasks
        task1_from_user1 = await task_repo.get_task_by_id(session, created_task1_u1.id, user1.id)
        assert task1_from_user1 is not None, "User 1 should be able to access their own task"
        
        # User 1 should NOT be able to access user 2's task (even if they knew the ID)
        task1_from_user2_by_user1 = await task_repo.get_task_by_id(session, created_task1_u2.id, user1.id)
        assert task1_from_user2_by_user1 is None, "User 1 should NOT be able to access user 2's task"
        
        # User 2 should be able to access their own task
        task1_from_user2 = await task_repo.get_task_by_id(session, created_task1_u2.id, user2.id)
        assert task1_from_user2 is not None, "User 2 should be able to access their own task"
        
        # User 2 should NOT be able to access user 1's task (even if they knew the ID)
        task1_from_user1_by_user2 = await task_repo.get_task_by_id(session, created_task1_u1.id, user2.id)
        assert task1_from_user1_by_user2 is None, "User 2 should NOT be able to access user 1's task"

        print("   ✅ User isolation verified successfully!")
        print("   - Users can only see their own tasks")
        print("   - Users cannot access other users' tasks even with the ID")
        print("   - Task retrieval is properly filtered by user ID")

    # Close the engine
    await engine.dispose()
    return True


if __name__ == "__main__":
    success = asyncio.run(test_user_isolation())
    if success:
        print("\n✅ USER ISOLATION TEST: SUCCESS")
    else:
        print("\n❌ USER ISOLATION TEST: FAILURE")
        sys.exit(1)
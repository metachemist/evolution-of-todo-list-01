# [Task]: T-004 | [From]: specs/2-plan/phase-2-fullstack.md

import pytest
from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Add the backend/src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'backend', 'src'))

from repositories.task_repository import TaskRepository
from models.task import Task, TaskUpdate
import uuid


@pytest.mark.asyncio
async def test_create_task_assigns_id_and_stores():
    """Test that create assigns an ID and stores the task"""
    # Create a mock session
    mock_session = AsyncMock()

    # Create the repository
    repo = TaskRepository()

    # Create a task without an ID (the ID will be assigned by the repo)
    user_id = uuid.uuid4()
    new_task = Task(
        id=None,  # Will be assigned by the repository
        user_id=user_id,
        title="Test Task",
        description="Test Description",
        completed=False,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    # Mock the session methods
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Create the task in the repository
    created_task = await repo.create_task(mock_session, new_task, user_id)

    # Verify the task was assigned an ID
    assert created_task.id is not None
    assert created_task.title == "Test Task"
    assert created_task.description == "Test Description"
    assert created_task.user_id == user_id

    # Verify the session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_tasks_returns_user_tasks():
    """Test that get_tasks returns only tasks for the specified user"""
    # Create a mock session
    mock_session = AsyncMock()

    # Create the repository
    repo = TaskRepository()

    # Mock the query results
    user_id = uuid.uuid4()
    mock_task = MagicMock()
    mock_task.id = 1
    mock_task.user_id = user_id
    mock_task.title = "Test Task"
    mock_task.description = "Test Description"
    mock_task.completed = False
    mock_task.created_at = datetime.now(timezone.utc)
    mock_task.updated_at = datetime.now(timezone.utc)

    mock_query_result = MagicMock()
    mock_query_result.scalars.return_value.all.return_value = [mock_task]
    mock_count_result = MagicMock()
    mock_count_result.scalar.return_value = 1

    mock_session.execute.side_effect = [mock_query_result, mock_count_result]

    # Get tasks for the user
    tasks, count = await repo.get_tasks(mock_session, user_id)

    # Verify we got the task
    assert len(tasks) == 1
    assert count == 1
    assert tasks[0].id == 1
    assert tasks[0].user_id == user_id


@pytest.mark.asyncio
async def test_get_task_by_id_returns_correct_task():
    """Test that get_task_by_id returns the correct task"""
    # Create a mock session
    mock_session = AsyncMock()

    # Create the repository
    repo = TaskRepository()

    # Mock the query result
    user_id = uuid.uuid4()
    task_id = 1
    mock_task = MagicMock()
    mock_task.Task = MagicMock()
    mock_task.Task.id = task_id
    mock_task.Task.user_id = user_id
    mock_task.Task.title = "Test Task"
    mock_task.Task.description = "Test Description"
    mock_task.Task.completed = False
    mock_task.Task.created_at = datetime.now(timezone.utc)
    mock_task.Task.updated_at = datetime.now(timezone.utc)

    mock_query_result = MagicMock()
    mock_query_result.first.return_value = mock_task

    mock_session.execute.return_value = mock_query_result

    # Find the task by ID
    found_task = await repo.get_task_by_id(mock_session, task_id, user_id)

    # Verify it's the correct task
    assert found_task.id == task_id
    assert found_task.title == "Test Task"
    assert found_task.description == "Test Description"


@pytest.mark.asyncio
async def test_get_task_by_id_returns_none_for_missing_task():
    """Test that get_task_by_id returns None for missing task"""
    # Create a mock session
    mock_session = AsyncMock()

    # Create the repository
    repo = TaskRepository()

    # Mock the query result to return None
    mock_query_result = MagicMock()
    mock_query_result.first.return_value = None

    mock_session.execute.return_value = mock_query_result

    # Try to find a task that doesn't exist
    user_id = uuid.uuid4()
    result = await repo.get_task_by_id(mock_session, 999, user_id)

    # Should return None instead of raising an exception
    assert result is None


@pytest.mark.asyncio
async def test_update_modifies_existing_task():
    """Test that update modifies the existing task correctly"""
    # Create a mock session
    mock_session = AsyncMock()

    # Create the repository
    repo = TaskRepository()

    # Mock the existing task
    user_id = uuid.uuid4()
    task_id = 1
    existing_task = MagicMock()
    existing_task.Task = MagicMock()
    existing_task.Task.id = task_id
    existing_task.Task.user_id = user_id
    existing_task.Task.title = "Original Title"
    existing_task.Task.description = "Original Description"
    existing_task.Task.completed = False
    existing_task.Task.created_at = datetime.now(timezone.utc)
    existing_task.Task.updated_at = datetime.now(timezone.utc)

    mock_query_result = MagicMock()
    mock_query_result.first.return_value = existing_task

    mock_session.execute.return_value = mock_query_result
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Update the task
    from src.models.task import TaskUpdate
    update_data = TaskUpdate(
        title="Updated Title",
        description="Updated Description",
        completed=True
    )

    updated_task = await repo.update_task(mock_session, task_id, user_id, update_data)

    # Verify the task was updated
    assert updated_task.id == task_id
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Updated Description"
    assert updated_task.completed is True

    # Verify the session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_update_returns_none_for_missing_task():
    """Test that update returns None for missing task"""
    # Create a mock session
    mock_session = AsyncMock()

    # Create the repository
    repo = TaskRepository()

    # Mock the query result to return None
    mock_query_result = MagicMock()
    mock_query_result.first.return_value = None

    mock_session.execute.return_value = mock_query_result

    # Try to update a task that doesn't exist
    user_id = uuid.uuid4()
    update_data = TaskUpdate(
        title="Updated Title",
        description="Updated Description",
        completed=True
    )

    result = await repo.update_task(mock_session, 999, user_id, update_data)

    # Should return None instead of raising an exception
    assert result is None


@pytest.mark.asyncio
async def test_delete_removes_task():
    """Test that delete removes the task and returns True"""
    # Create a mock session
    mock_session = AsyncMock()

    # Create the repository
    repo = TaskRepository()

    # Mock the existing task
    user_id = uuid.uuid4()
    task_id = 1
    existing_task = MagicMock()
    existing_task.Task = MagicMock()
    existing_task.Task.id = task_id
    existing_task.Task.user_id = user_id
    existing_task.Task.title = "Task to Delete"
    existing_task.Task.description = "Description"
    existing_task.Task.completed = False
    existing_task.Task.created_at = datetime.now(timezone.utc)
    existing_task.Task.updated_at = datetime.now(timezone.utc)

    mock_query_result = MagicMock()
    mock_query_result.first.return_value = existing_task

    mock_session.execute.return_value = mock_query_result
    mock_session.delete.return_value = None
    mock_session.commit.return_value = None

    # Delete the task
    result = await repo.delete_task(mock_session, task_id, user_id)

    # Verify the task was deleted
    assert result is True

    # Verify the session methods were called
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()


@pytest.mark.asyncio
async def test_delete_returns_false_for_missing_task():
    """Test that delete returns False for missing task"""
    # Create a mock session
    mock_session = AsyncMock()

    # Create the repository
    repo = TaskRepository()

    # Mock the query result to return None
    mock_query_result = MagicMock()
    mock_query_result.first.return_value = None

    mock_session.execute.return_value = mock_query_result

    # Try to delete a task that doesn't exist
    user_id = uuid.uuid4()
    result = await repo.delete_task(mock_session, 999, user_id)

    # Should return False instead of raising an exception
    assert result is False


@pytest.mark.asyncio
async def test_toggle_completion_flips_status():
    """Test that toggle_completion flips the completion status"""
    # Create a mock session
    mock_session = AsyncMock()

    # Create the repository
    repo = TaskRepository()

    # Mock the existing task (currently pending)
    user_id = uuid.uuid4()
    task_id = 1
    existing_task = MagicMock()
    existing_task.Task = MagicMock()
    existing_task.Task.id = task_id
    existing_task.Task.user_id = user_id
    existing_task.Task.title = "Test Task"
    existing_task.Task.description = "Test Description"
    existing_task.Task.completed = False  # Initially not completed
    existing_task.Task.created_at = datetime.now(timezone.utc)
    existing_task.Task.updated_at = datetime.now(timezone.utc)

    mock_query_result = MagicMock()
    mock_query_result.first.return_value = existing_task

    mock_session.execute.return_value = mock_query_result
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    # Toggle the completion status
    updated_task = await repo.toggle_completion(mock_session, task_id, user_id)

    # Verify the status was flipped to True (completed)
    assert updated_task.completed is True

    # Verify the session methods were called
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
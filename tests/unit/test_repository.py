# [Task]: T-004 | [From]: specs/2-plan/phase-1-console.md

import pytest
from datetime import datetime, timezone
from src.repositories.task_repository import InMemoryTaskRepository
from src.models.task import Task, TaskNotFoundException


def test_create_task_assigns_id_and_stores():
    """Test that create assigns an ID and stores the task"""
    repo = InMemoryTaskRepository()
    
    # Create a task without an ID (the ID will be assigned by the repo)
    new_task = Task(
        id=0,  # Will be replaced by the repository
        title="Test Task",
        description="Test Description",
        completed=False,
        created_at=datetime.now(timezone.utc)
    )
    
    # Create the task in the repository
    created_task = repo.create(new_task)
    
    # Verify the task was assigned an ID
    assert created_task.id == 1
    assert created_task.title == "Test Task"
    assert created_task.description == "Test Description"
    
    # Verify the task is stored in the repository
    all_tasks = repo.find_all()
    assert len(all_tasks) == 1
    assert all_tasks[0].id == 1


def test_find_all_returns_copy_of_list():
    """Test that find_all returns a copy of the internal list"""
    repo = InMemoryTaskRepository()
    
    # Add some tasks
    task1 = Task(
        id=0,
        title="Task 1",
        description="Description 1",
        completed=False,
        created_at=datetime.now(timezone.utc)
    )
    task2 = Task(
        id=0,
        title="Task 2",
        description="Description 2",
        completed=True,
        created_at=datetime.now(timezone.utc)
    )
    
    repo.create(task1)
    repo.create(task2)
    
    # Get all tasks
    tasks = repo.find_all()
    
    # Verify we got both tasks
    assert len(tasks) == 2
    
    # Verify modifying the returned list doesn't affect the internal list
    original_len = len(repo.find_all())
    tasks.pop()  # Remove one from the returned list
    assert len(repo.find_all()) == original_len  # Internal list unchanged


def test_find_by_id_returns_correct_task():
    """Test that find_by_id returns the correct task"""
    repo = InMemoryTaskRepository()
    
    # Add some tasks
    task1 = Task(
        id=0,
        title="Task 1",
        description="Description 1",
        completed=False,
        created_at=datetime.now(timezone.utc)
    )
    task2 = Task(
        id=0,
        title="Task 2",
        description="Description 2",
        completed=True,
        created_at=datetime.now(timezone.utc)
    )
    
    created_task1 = repo.create(task1)
    created_task2 = repo.create(task2)
    
    # Find the first task by ID
    found_task = repo.find_by_id(created_task1.id)
    
    # Verify it's the correct task
    assert found_task.id == created_task1.id
    assert found_task.title == "Task 1"
    assert found_task.description == "Description 1"


def test_find_by_id_raises_exception_for_missing_task():
    """Test that find_by_id raises TaskNotFoundException for missing task"""
    repo = InMemoryTaskRepository()
    
    # Try to find a task that doesn't exist
    with pytest.raises(TaskNotFoundException) as exc_info:
        repo.find_by_id(999)
    
    # Verify the exception contains the correct ID
    assert exc_info.value.task_id == 999


def test_update_modifies_existing_task():
    """Test that update modifies the existing task correctly"""
    repo = InMemoryTaskRepository()
    
    # Add a task
    original_task = Task(
        id=0,
        title="Original Title",
        description="Original Description",
        completed=False,
        created_at=datetime.now(timezone.utc)
    )
    created_task = repo.create(original_task)
    
    # Update the task
    updated_data = Task(
        id=created_task.id,
        title="Updated Title",
        description="Updated Description",
        completed=True,
        created_at=created_task.created_at  # Keep original creation time
    )
    
    updated_task = repo.update(created_task.id, updated_data)
    
    # Verify the task was updated
    assert updated_task.id == created_task.id
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Updated Description"
    assert updated_task.completed is True
    
    # Verify the update is reflected when retrieving from the repo
    retrieved_task = repo.find_by_id(created_task.id)
    assert retrieved_task.title == "Updated Title"
    assert retrieved_task.description == "Updated Description"
    assert retrieved_task.completed is True


def test_update_raises_exception_for_missing_task():
    """Test that update raises TaskNotFoundException for missing task"""
    repo = InMemoryTaskRepository()
    
    # Try to update a task that doesn't exist
    task_to_update = Task(
        id=999,
        title="Updated Title",
        description="Updated Description",
        completed=True,
        created_at=datetime.now(timezone.utc)
    )
    
    with pytest.raises(TaskNotFoundException) as exc_info:
        repo.update(999, task_to_update)
    
    # Verify the exception contains the correct ID
    assert exc_info.value.task_id == 999


def test_delete_removes_task():
    """Test that delete removes the task and returns True"""
    repo = InMemoryTaskRepository()
    
    # Add a task
    task = Task(
        id=0,
        title="Task to Delete",
        description="Description",
        completed=False,
        created_at=datetime.now(timezone.utc)
    )
    created_task = repo.create(task)
    
    # Verify the task exists
    assert len(repo.find_all()) == 1
    
    # Delete the task
    result = repo.delete(created_task.id)
    
    # Verify the task was deleted
    assert result is True
    assert len(repo.find_all()) == 0


def test_delete_raises_exception_for_missing_task():
    """Test that delete raises TaskNotFoundException for missing task"""
    repo = InMemoryTaskRepository()
    
    # Try to delete a task that doesn't exist
    with pytest.raises(TaskNotFoundException) as exc_info:
        repo.delete(999)
    
    # Verify the exception contains the correct ID
    assert exc_info.value.task_id == 999


def test_auto_increment_id_generation():
    """Test that IDs are auto-incremented correctly"""
    repo = InMemoryTaskRepository()
    
    # Add multiple tasks
    task1 = Task(
        id=0,
        title="Task 1",
        description="Description 1",
        completed=False,
        created_at=datetime.now(timezone.utc)
    )
    task2 = Task(
        id=0,
        title="Task 2",
        description="Description 2",
        completed=False,
        created_at=datetime.now(timezone.utc)
    )
    task3 = Task(
        id=0,
        title="Task 3",
        description="Description 3",
        completed=False,
        created_at=datetime.now(timezone.utc)
    )
    
    created_task1 = repo.create(task1)
    created_task2 = repo.create(task2)
    created_task3 = repo.create(task3)
    
    # Verify IDs are assigned sequentially starting from 1
    assert created_task1.id == 1
    assert created_task2.id == 2
    assert created_task3.id == 3
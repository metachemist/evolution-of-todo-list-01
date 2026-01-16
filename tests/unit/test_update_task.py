# [Task]: T-011, T-012 | [From]: specs/2-plan/phase-1-console.md

import pytest
from src.services.task_service import TaskService
from src.repositories.task_repository import InMemoryTaskRepository
from src.models.task import Task, InvalidTaskDataException, TaskNotFoundException


def test_update_task_just_title():
    """Test updating just the title of a task"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    
    # Update just the title, keeping the description
    updated_task = service.update_task(original_id, title="New Title")
    
    # Verify the task was updated correctly
    assert updated_task.id == original_id
    assert updated_task.title == "New Title"
    assert updated_task.description == "Original Description"  # Should remain unchanged
    assert updated_task.completed is False  # Should remain unchanged


def test_update_task_just_description():
    """Test updating just the description of a task"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    
    # Update just the description, keeping the title
    updated_task = service.update_task(original_id, description="New Description")
    
    # Verify the task was updated correctly
    assert updated_task.id == original_id
    assert updated_task.title == "Original Title"  # Should remain unchanged
    assert updated_task.description == "New Description"
    assert updated_task.completed is False  # Should remain unchanged


def test_update_task_both_title_and_description():
    """Test updating both title and description of a task"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    
    # Update both title and description
    updated_task = service.update_task(original_id, "New Title", "New Description")
    
    # Verify the task was updated correctly
    assert updated_task.id == original_id
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"
    assert updated_task.completed is False  # Should remain unchanged


def test_update_non_existent_task():
    """Test updating a non-existent task raises TaskNotFoundException"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Try to update a task that doesn't exist
    with pytest.raises(TaskNotFoundException):
        service.update_task(999, "New Title")


def test_update_task_to_empty_title_fails():
    """Test updating a task to an empty title raises InvalidTaskDataException"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    
    # Try to update the title to an empty string
    with pytest.raises(InvalidTaskDataException) as exc_info:
        service.update_task(original_id, "")
    
    # Verify the exception message
    assert "Title cannot be empty" in str(exc_info.value)


def test_update_task_preserves_completion_status():
    """Test that updating a task preserves its completion status"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task and mark it as complete
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    completed_task = service.toggle_complete(original_id)
    
    # Update the task
    updated_task = service.update_task(original_id, "New Title", "New Description")
    
    # Verify the completion status is preserved
    assert updated_task.completed is True  # Should remain completed
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"


def test_update_task_preserves_created_timestamp():
    """Test that updating a task preserves its creation timestamp"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    original_created_at = original_task.created_at
    
    # Update the task
    updated_task = service.update_task(original_id, "New Title", "New Description")
    
    # Verify the creation timestamp is preserved
    assert updated_task.created_at == original_created_at
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"


def test_update_task_partial_update_with_none_values():
    """Test that passing None explicitly for title/description preserves original values"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    
    # Update with None values explicitly - this should preserve original values
    updated_task = service.update_task(original_id, title=None, description=None)
    
    # Verify original values are preserved when explicitly passing None
    assert updated_task.title == "Original Title"
    assert updated_task.description == "Original Description"
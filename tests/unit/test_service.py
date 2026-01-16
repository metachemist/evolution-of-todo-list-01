# [Task]: T-005 | [From]: specs/2-plan/phase-1-console.md

import pytest
from datetime import datetime, timezone
from src.services.task_service import TaskService
from src.repositories.task_repository import InMemoryTaskRepository
from src.models.task import Task, InvalidTaskDataException, TaskNotFoundException


def test_add_task_success():
    """Test add_task creates a task successfully"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task
    result = service.add_task("Test Task", "Test Description")
    
    # Verify the task was created
    assert result.title == "Test Task"
    assert result.description == "Test Description"
    assert result.completed is False
    assert isinstance(result.created_at, datetime)
    
    # Verify the task is in the repository
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 1
    assert all_tasks[0].title == "Test Task"


def test_add_task_without_description():
    """Test add_task works when description is not provided"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task without description
    result = service.add_task("Test Task")
    
    # Verify the task was created with None description
    assert result.title == "Test Task"
    assert result.description is None
    assert result.completed is False


def test_add_task_empty_title_fails():
    """Test add_task fails when title is empty"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Try to add a task with empty title
    with pytest.raises(InvalidTaskDataException) as exc_info:
        service.add_task("")
    
    # Verify the exception message
    assert "Title cannot be empty" in str(exc_info.value)


def test_get_all_tasks():
    """Test get_all_tasks returns all tasks"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add some tasks
    service.add_task("Task 1", "Description 1")
    service.add_task("Task 2", "Description 2")
    
    # Get all tasks
    tasks = service.get_all_tasks()
    
    # Verify we got both tasks
    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"


def test_update_task_preserves_old_values():
    """Test update_task preserves old description if only title is changed"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    
    # Update only the title
    updated_task = service.update_task(original_id, title="Updated Title")
    
    # Verify the title was updated but description preserved
    assert updated_task.title == "Updated Title"
    assert updated_task.description == "Original Description"  # Preserved
    assert updated_task.completed is False  # Preserved


def test_update_task_updates_both_fields():
    """Test update_task updates both title and description when provided"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    
    # Update both title and description
    updated_task = service.update_task(original_id, "New Title", "New Description")
    
    # Verify both were updated
    assert updated_task.title == "New Title"
    assert updated_task.description == "New Description"
    assert updated_task.completed is False  # Preserved


def test_update_task_empty_title_fails():
    """Test update_task fails when title is empty"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    
    # Try to update with empty title
    with pytest.raises(InvalidTaskDataException) as exc_info:
        service.update_task(original_id, "")
    
    # Verify the exception message
    assert "Title cannot be empty" in str(exc_info.value)


def test_toggle_complete_flips_status():
    """Test toggle_complete flips status True <-> False"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task (initially not completed)
    task = service.add_task("Test Task", "Test Description")
    original_id = task.id
    assert task.completed is False
    
    # Toggle the completion status
    updated_task = service.toggle_complete(original_id)
    
    # Verify the status was flipped to True
    assert updated_task.completed is True
    
    # Toggle again
    toggled_again_task = service.toggle_complete(original_id)
    
    # Verify the status was flipped back to False
    assert toggled_again_task.completed is False


def test_delete_task():
    """Test delete_task removes the task"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task
    task = service.add_task("Test Task", "Test Description")
    original_id = task.id
    
    # Verify the task exists
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 1
    
    # Delete the task
    result = service.delete_task(original_id)
    
    # Verify the task was deleted
    assert result is True
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 0


def test_update_task_nonexistent_fails():
    """Test update_task raises exception for nonexistent task"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Try to update a non-existent task
    with pytest.raises(TaskNotFoundException):
        service.update_task(999, "New Title")


def test_toggle_complete_nonexistent_fails():
    """Test toggle_complete raises exception for nonexistent task"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Try to toggle a non-existent task
    with pytest.raises(TaskNotFoundException):
        service.toggle_complete(999)


def test_delete_task_nonexistent_fails():
    """Test delete_task raises exception for nonexistent task"""
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Try to delete a non-existent task
    with pytest.raises(TaskNotFoundException):
        service.delete_task(999)
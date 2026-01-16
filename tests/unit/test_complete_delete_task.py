# [Task]: T-013, T-014 | [From]: specs/2-plan/phase-1-console.md

import pytest
from src.services.task_service import TaskService
from src.repositories.task_repository import InMemoryTaskRepository
from src.models.task import Task, TaskNotFoundException


def test_toggle_complete_false_to_true():
    """Test toggling status from False (pending) to True (complete)"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first (initially not completed)
    original_task = service.add_task("Test Task", "Test Description")
    original_id = original_task.id
    assert original_task.completed is False  # Verify it starts as pending
    
    # Toggle the completion status
    updated_task = service.toggle_complete(original_id)
    
    # Verify the status was flipped to True (complete)
    assert updated_task.id == original_id
    assert updated_task.completed is True
    assert updated_task.title == "Test Task"
    assert updated_task.description == "Test Description"


def test_toggle_complete_true_to_false():
    """Test toggling status from True (complete) back to False (pending)"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first
    original_task = service.add_task("Test Task", "Test Description")
    original_id = original_task.id
    
    # First, mark as complete
    completed_task = service.toggle_complete(original_id)
    assert completed_task.completed is True  # Verify it's now complete
    
    # Now toggle back to pending
    updated_task = service.toggle_complete(original_id)
    
    # Verify the status was flipped back to False (pending)
    assert updated_task.id == original_id
    assert updated_task.completed is False
    assert updated_task.title == "Test Task"
    assert updated_task.description == "Test Description"


def test_toggle_complete_sequence_false_true_false():
    """Test toggling status in sequence: False -> True -> False"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first (starts as pending)
    original_task = service.add_task("Test Task", "Test Description")
    original_id = original_task.id
    assert original_task.completed is False  # Verify it starts as pending
    
    # First toggle: False -> True
    task_after_first_toggle = service.toggle_complete(original_id)
    assert task_after_first_toggle.completed is True
    
    # Second toggle: True -> False
    task_after_second_toggle = service.toggle_complete(original_id)
    assert task_after_second_toggle.completed is False


def test_delete_task_removes_from_repo():
    """Test deleting a task removes it from the repository"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first
    original_task = service.add_task("Test Task", "Test Description")
    original_id = original_task.id
    
    # Verify the task exists initially
    all_tasks_before = service.get_all_tasks()
    assert len(all_tasks_before) == 1
    assert all_tasks_before[0].id == original_id
    
    # Delete the task
    result = service.delete_task(original_id)
    
    # Verify the task was deleted
    assert result is True  # delete_task should return True on success
    all_tasks_after = service.get_all_tasks()
    assert len(all_tasks_after) == 0


def test_delete_non_existent_task():
    """Test deleting a non-existent task raises TaskNotFoundException"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Try to delete a task that doesn't exist
    with pytest.raises(TaskNotFoundException):
        service.delete_task(999)


def test_toggle_complete_non_existent_task():
    """Test toggling completion status of a non-existent task raises TaskNotFoundException"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Try to toggle completion status of a task that doesn't exist
    with pytest.raises(TaskNotFoundException):
        service.toggle_complete(999)


def test_delete_task_then_cannot_access():
    """Test that after deleting a task, it cannot be accessed"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task first
    original_task = service.add_task("Test Task", "Test Description")
    original_id = original_task.id
    
    # Delete the task
    service.delete_task(original_id)
    
    # Verify the task cannot be accessed anymore
    with pytest.raises(TaskNotFoundException):
        service.toggle_complete(original_id)


def test_toggle_complete_preserves_other_attributes():
    """Test that toggling completion status preserves other task attributes"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task with specific attributes
    original_task = service.add_task("Original Title", "Original Description")
    original_id = original_task.id
    original_created_at = original_task.created_at
    
    # Toggle the completion status
    updated_task = service.toggle_complete(original_id)
    
    # Verify that only the completion status changed
    assert updated_task.id == original_id
    assert updated_task.title == "Original Title"
    assert updated_task.description == "Original Description"
    assert updated_task.created_at == original_created_at  # Timestamp should be preserved
    assert updated_task.completed is True  # Status should be flipped
    
    # Toggle back to verify it goes back to original state (except for completion)
    toggled_back_task = service.toggle_complete(original_id)
    assert toggled_back_task.id == original_id
    assert toggled_back_task.title == "Original Title"
    assert toggled_back_task.description == "Original Description"
    assert toggled_back_task.created_at == original_created_at  # Timestamp should be preserved
    assert toggled_back_task.completed is False  # Status should be flipped back
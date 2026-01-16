# [Task]: T-008 | [From]: specs/2-plan/phase-1-console.md

import pytest
from src.services.task_service import TaskService
from src.repositories.task_repository import InMemoryTaskRepository
from src.models.task import InvalidTaskDataException


def test_add_valid_task():
    """Test adding a valid task with just a title"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task
    result = service.add_task("Valid Task Title")
    
    # Verify the task was created with correct properties
    assert result.title == "Valid Task Title"
    assert result.description is None
    assert result.completed is False
    assert result.id == 1  # First task should get ID 1


def test_add_valid_task_with_description():
    """Test adding a valid task with title and description"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task with description
    result = service.add_task("Valid Task Title", "This is a valid description")
    
    # Verify the task was created with correct properties
    assert result.title == "Valid Task Title"
    assert result.description == "This is a valid description"
    assert result.completed is False
    assert result.id == 1  # First task should get ID 1


def test_add_empty_title():
    """Test that adding a task with empty title raises InvalidTaskDataException"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Try to add a task with empty title
    with pytest.raises(InvalidTaskDataException) as exc_info:
        service.add_task("")
    
    # Verify the exception message
    assert "Title cannot be empty" in str(exc_info.value)


def test_add_whitespace_only_title():
    """Test that adding a task with whitespace-only title raises InvalidTaskDataException"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Try to add a task with whitespace-only title
    with pytest.raises(InvalidTaskDataException) as exc_info:
        service.add_task("   ")  # Just spaces
    
    # Verify the exception message
    assert "Title cannot be empty" in str(exc_info.value)


def test_title_too_long():
    """Test that adding a task with title longer than 200 characters raises an error"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Create a title with 201 characters
    long_title = "x" * 201
    
    # Try to add a task with too long title
    with pytest.raises(Exception) as exc_info:
        service.add_task(long_title)
    
    # The error should come from the Pydantic validation in the Task model
    assert "Title must be between 1 and 200 characters" in str(exc_info.value)


def test_description_too_long():
    """Test that adding a task with description longer than 500 characters raises an error"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Create a description with 501 characters
    long_description = "x" * 501
    
    # Try to add a task with too long description
    with pytest.raises(Exception) as exc_info:
        service.add_task("Valid Title", long_description)
    
    # The error should come from the Pydantic validation in the Task model
    assert "Description must not exceed 500 characters" in str(exc_info.value)


def test_add_task_increments_ids():
    """Test that adding multiple tasks increments IDs correctly"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add multiple tasks
    task1 = service.add_task("First Task")
    task2 = service.add_task("Second Task")
    task3 = service.add_task("Third Task")
    
    # Verify IDs are incremented correctly
    assert task1.id == 1
    assert task2.id == 2
    assert task3.id == 3


def test_add_task_stores_in_repository():
    """Test that added tasks are stored in the repository"""
    # Set up the service
    repo = InMemoryTaskRepository()
    service = TaskService(repo)
    
    # Add a task
    added_task = service.add_task("Test Task", "Test Description")
    
    # Get all tasks from the repository
    all_tasks = service.get_all_tasks()
    
    # Verify the task is stored
    assert len(all_tasks) == 1
    assert all_tasks[0].id == added_task.id
    assert all_tasks[0].title == "Test Task"
    assert all_tasks[0].description == "Test Description"
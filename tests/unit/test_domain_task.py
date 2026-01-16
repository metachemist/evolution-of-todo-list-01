# [Task]: T-002 | [From]: specs/2-plan/phase-1-console.md

import pytest
from datetime import datetime, timezone
from src.models.task import Task, InvalidTaskDataException


def test_task_creation_valid():
    """Test happy path - valid task creation"""
    task = Task(
        id=1,
        title="Sample Task",
        description="This is a sample task description",
        completed=False,
        created_at=datetime.now(timezone.utc)
    )

    assert task.id == 1
    assert task.title == "Sample Task"
    assert task.description == "This is a sample task description"
    assert task.completed is False
    assert isinstance(task.created_at, datetime)


def test_task_creation_with_defaults():
    """Test task creation with default values"""
    task = Task(
        id=1,
        title="Sample Task"
    )
    
    assert task.id == 1
    assert task.title == "Sample Task"
    assert task.description is None
    assert task.completed is False
    assert isinstance(task.created_at, datetime)


def test_task_title_validation_empty():
    """Test validation error - empty title raises error"""
    with pytest.raises(ValueError) as exc_info:
        Task(
            id=1,
            title="",
            description="This is a sample task description"
        )
    
    assert "Title must be between 1 and 200 characters" in str(exc_info.value)


def test_task_title_validation_too_long():
    """Test validation error - title too long raises error"""
    long_title = "x" * 201  # 201 characters, exceeding the limit
    
    with pytest.raises(ValueError) as exc_info:
        Task(
            id=1,
            title=long_title,
            description="This is a sample task description"
        )
    
    assert "Title must be between 1 and 200 characters" in str(exc_info.value)


def test_task_description_validation_too_long():
    """Test validation error - description too long raises error"""
    long_description = "x" * 501  # 501 characters, exceeding the limit
    
    with pytest.raises(ValueError) as exc_info:
        Task(
            id=1,
            title="Valid Title",
            description=long_description
        )
    
    assert "Description must not exceed 500 characters" in str(exc_info.value)


def test_task_minimal_title_length():
    """Test that minimum title length (1 char) is accepted"""
    task = Task(
        id=1,
        title="x"  # 1 character, should be valid
    )
    
    assert task.title == "x"


def test_task_max_title_length():
    """Test that maximum title length (200 chars) is accepted"""
    title_200_chars = "x" * 200  # Exactly 200 characters
    
    task = Task(
        id=1,
        title=title_200_chars
    )
    
    assert task.title == title_200_chars


def test_task_max_description_length():
    """Test that maximum description length (500 chars) is accepted"""
    desc_500_chars = "x" * 500  # Exactly 500 characters
    
    task = Task(
        id=1,
        title="Valid Title",
        description=desc_500_chars
    )
    
    assert task.description == desc_500_chars
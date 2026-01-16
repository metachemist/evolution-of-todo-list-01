# [Task]: T-006 | [From]: specs/2-plan/phase-1-console.md

import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from unittest.mock import Mock, MagicMock, patch
import pytest
from src.cli.interface import CLI, ArgumentError
from src.services.task_service import TaskService
from src.models.task import Task, TaskNotFoundException, InvalidTaskDataException


def test_add_command_prints_success_message(capsys):
    """Test add command prints the success message"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_task = Task(
        id=1,
        title="Buy Milk",
        description=None,
        completed=False
    )
    mock_service.add_task.return_value = mock_task

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Simulate command execution
    args = Mock()
    args.command = 'add'
    args.title = "Buy Milk"
    args.description = None

    cli.execute_command(args)

    # Capture the output
    captured = capsys.readouterr()

    # Verify the success message was printed
    assert "[SUCCESS] Task 1 \"Buy Milk\" created." in captured.out


def test_invalid_id_prints_error_message(capsys):
    """Test invalid ID prints the error message"""
    # Create a mock task service that raises TaskNotFoundException
    mock_service = Mock(spec=TaskService)
    mock_service.update_task.side_effect = TaskNotFoundException(999)

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Simulate command execution
    args = Mock()
    args.command = 'update'
    args.id = 999
    args.title = "New Title"
    args.description = "New Description"

    cli.execute_command(args)

    # Capture the output
    captured = capsys.readouterr()

    # Verify the error message was printed (it includes a newline)
    assert "[ERROR] Task with ID 999 not found" in captured.out


def test_view_command_shows_tasks(capsys):
    """Test view command shows tasks in the correct format"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_tasks = [
        Task(id=1, title="Task 1", description=None, completed=False),
        Task(id=2, title="Task 2", description="With description", completed=True)
    ]
    mock_service.get_all_tasks.return_value = mock_tasks

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Simulate command execution
    args = Mock()
    args.command = 'view'

    cli.execute_command(args)

    # Capture the output
    captured = capsys.readouterr()

    # Verify the tasks are displayed in the correct format
    assert "ID | Status | Title" in captured.out
    assert "1  | [ ]    | Task 1" in captured.out
    assert "2  | [x]    | Task 2 - With description" in captured.out


def test_view_command_no_tasks(capsys):
    """Test view command shows 'No tasks' when there are no tasks"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_service.get_all_tasks.return_value = []

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Simulate command execution
    args = Mock()
    args.command = 'view'

    cli.execute_command(args)

    # Capture the output
    captured = capsys.readouterr()

    # Verify the no tasks message was printed
    assert "No tasks in your list" in captured.out


def test_complete_command_success(capsys):
    """Test complete command prints success message"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_task = Task(id=1, title="Task 1", description=None, completed=True)
    mock_service.toggle_complete.return_value = mock_task

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Simulate command execution
    args = Mock()
    args.command = 'complete'
    args.id = 1

    cli.execute_command(args)

    # Capture the output
    captured = capsys.readouterr()

    # Verify the success message was printed
    assert "[SUCCESS] Task 1 marked as complete." in captured.out


def test_delete_command_success(capsys):
    """Test delete command prints success message"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_service.delete_task.return_value = True  # Assuming delete returns True on success

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Simulate command execution
    args = Mock()
    args.command = 'delete'
    args.id = 1

    cli.execute_command(args)

    # Capture the output
    captured = capsys.readouterr()

    # Verify the success message was printed
    assert "[SUCCESS] Task 1 deleted." in captured.out


def test_update_command_success(capsys):
    """Test update command prints success message"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_task = Task(id=1, title="Updated Title", description="Updated Description", completed=False)
    mock_service.update_task.return_value = mock_task

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Simulate command execution
    args = Mock()
    args.command = 'update'
    args.id = 1
    args.title = "Updated Title"
    args.description = "Updated Description"

    cli.execute_command(args)

    # Capture the output
    captured = capsys.readouterr()

    # Verify the success message was printed
    assert "[SUCCESS] Task 1 updated." in captured.out


def test_handle_error_with_task_not_found_exception(capsys):
    """Test error handling for TaskNotFoundException"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_service.get_all_tasks.side_effect = TaskNotFoundException(999)

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Simulate command execution
    args = Mock()
    args.command = 'view'

    cli.execute_command(args)

    # Capture the output
    captured = capsys.readouterr()

    # Verify the error message was printed (it includes a newline)
    assert "[ERROR] Task with ID 999 not found" in captured.out


def test_handle_error_with_invalid_task_data_exception(capsys):
    """Test error handling for InvalidTaskDataException"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_service.add_task.side_effect = InvalidTaskDataException("Title cannot be empty")

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Simulate command execution
    args = Mock()
    args.command = 'add'
    args.title = ""
    args.description = None

    cli.execute_command(args)

    # Capture the output
    captured = capsys.readouterr()

    # Verify the error message was printed
    assert "[ERROR] Title cannot be empty" in captured.out


def test_help_command_returns_custom_string(capsys):
    """Test help command returns custom string (not error)"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    
    # Create CLI instance with the mock service
    cli = CLI(mock_service)
    
    # Call the help handler directly
    cli._handle_help()
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Verify the help message was printed
    assert "Available commands:" in captured.out
    assert "add" in captured.out
    assert "view" in captured.out
    assert "update" in captured.out
    assert "delete" in captured.out
    assert "complete" in captured.out
    assert "help" in captured.out
    assert "exit" in captured.out


def test_add_without_args_returns_clean_error():
    """Test add without args returns a clean error (not system usage)"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)

    # Create CLI instance with the mock service
    cli = CLI(mock_service)

    # Test that parsing an incomplete command raises ArgumentError
    with pytest.raises(ArgumentError):
        cli.parser.parse_args(['add'])


def test_quoted_strings_parsed_correctly():
    """Test that quoted strings are parsed correctly using shlex"""
    import shlex

    # Test the shlex parsing directly
    input_str = 'add "Call mom" "birthday"'
    parsed = shlex.split(input_str)

    assert parsed == ['add', 'Call mom', 'birthday']

    # Another test case
    input_str2 = 'add "Buy groceries" "Milk, bread, eggs"'
    parsed2 = shlex.split(input_str2)

    assert parsed2 == ['add', 'Buy groceries', 'Milk, bread, eggs']



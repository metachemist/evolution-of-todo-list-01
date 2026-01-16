# [Task]: T-009, T-010 | [From]: specs/2-plan/phase-1-console.md

import io
import sys
from contextlib import redirect_stdout
from unittest.mock import Mock
from src.cli.interface import CLI
from src.services.task_service import TaskService
from src.models.task import Task


def test_view_command_shows_tasks_formatted_properly(capsys):
    """Test view command shows tasks in the correct format"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_tasks = [
        Task(id=1, title="Buy Milk", description=None, completed=False),
        Task(id=2, title="Walk Dog", description=None, completed=True),
        Task(id=3, title="Code", description="Write Python", completed=False)
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
    output_lines = captured.out.strip().split('\n')
    
    # Check header
    assert output_lines[0] == "ID | Status | Title"
    
    # Check each task format
    assert "1  | [ ]    | Buy Milk" in output_lines[1]
    assert "2  | [x]    | Walk Dog" in output_lines[2]
    assert "3  | [ ]    | Code - Write Python" in output_lines[3]


def test_view_command_shows_no_tasks_message(capsys):
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


def test_view_command_formats_pending_tasks(capsys):
    """Test that pending tasks are formatted with [ ]"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_tasks = [
        Task(id=1, title="Pending Task", description=None, completed=False)
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

    # Verify the pending task is formatted with [ ]
    assert "1  | [ ]    | Pending Task" in captured.out


def test_view_command_formats_completed_tasks(capsys):
    """Test that completed tasks are formatted with [x]"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_tasks = [
        Task(id=1, title="Completed Task", description=None, completed=True)
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

    # Verify the completed task is formatted with [x]
    assert "1  | [x]    | Completed Task" in captured.out


def test_view_command_shows_tasks_with_descriptions(capsys):
    """Test that tasks with descriptions are formatted as 'Title - Description'"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_tasks = [
        Task(id=1, title="Task with Desc", description="This is a description", completed=False)
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

    # Verify the task with description is formatted correctly
    assert "1  | [ ]    | Task with Desc - This is a description" in captured.out


def test_view_command_shows_tasks_without_descriptions(capsys):
    """Test that tasks without descriptions show just the title"""
    # Create a mock task service
    mock_service = Mock(spec=TaskService)
    mock_tasks = [
        Task(id=1, title="Task without Desc", description=None, completed=False)
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

    # Verify the task without description shows just the title
    assert "1  | [ ]    | Task without Desc" in captured.out
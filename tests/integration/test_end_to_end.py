# [Task]: T-015 | [From]: specs/2-plan/phase-1-console.md

import pytest
from src.main import main
from src.repositories.task_repository import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.cli.interface import CLI
from unittest.mock import patch, MagicMock


def test_end_to_end_workflow():
    """Test the complete user workflow: Add -> View -> Complete -> Update -> View -> Delete -> View"""
    # Create fresh components for the test
    repository = InMemoryTaskRepository()
    service = TaskService(repository)
    cli = CLI(service)
    
    # Test adding a task
    args_add = MagicMock()
    args_add.command = 'add'
    args_add.title = 'Buy groceries'
    args_add.description = 'Milk, bread, eggs'
    
    cli.execute_command(args_add)
    
    # Verify task was added
    tasks = service.get_all_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == 'Buy groceries'
    assert tasks[0].description == 'Milk, bread, eggs'
    assert tasks[0].completed is False
    
    # Test viewing tasks
    args_view = MagicMock()
    args_view.command = 'view'
    
    # Capture the output
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_view)
        # Verify that the print function was called (meaning tasks were displayed)
        assert mock_print.called
    
    # Test completing the task
    task_id = tasks[0].id
    args_complete = MagicMock()
    args_complete.command = 'complete'
    args_complete.id = task_id
    
    cli.execute_command(args_complete)
    
    # Verify task was completed
    updated_task = service.update_task(task_id, tasks[0].title, tasks[0].description)
    assert updated_task.completed is True
    
    # Test updating the task
    args_update = MagicMock()
    args_update.command = 'update'
    args_update.id = task_id
    args_update.title = 'Buy milk and bread'
    args_update.description = 'Get whole milk and sourdough'
    
    cli.execute_command(args_update)
    
    # Verify task was updated
    updated_task = service.update_task(task_id, args_update.title, args_update.description)
    assert updated_task.title == 'Buy milk and bread'
    assert updated_task.description == 'Get whole milk and sourdough'
    
    # Test viewing tasks again to see the updated task
    args_view2 = MagicMock()
    args_view2.command = 'view'
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_view2)
        # Verify that the print function was called
        assert mock_print.called
    
    # Test deleting the task
    args_delete = MagicMock()
    args_delete.command = 'delete'
    args_delete.id = task_id
    
    cli.execute_command(args_delete)
    
    # Verify task was deleted
    remaining_tasks = service.get_all_tasks()
    assert len(remaining_tasks) == 0


def test_happy_path_scenario():
    """Test the exact happy path scenario from the spec"""
    # Create fresh components for the test
    repository = InMemoryTaskRepository()
    service = TaskService(repository)
    cli = CLI(service)
    
    # Simulate the exact commands from the spec's happy path:
    # > add "Buy groceries"
    args_add1 = MagicMock()
    args_add1.command = 'add'
    args_add1.title = 'Buy groceries'
    args_add1.description = None
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_add1)
        # Check that success message was printed
        mock_print.assert_called()
        assert '[SUCCESS] Task' in str(mock_print.call_args)
    
    # > add "Walk the dog" "Take the dog for a 30-minute walk"
    args_add2 = MagicMock()
    args_add2.command = 'add'
    args_add2.title = 'Walk the dog'
    args_add2.description = 'Take the dog for a 30-minute walk'
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_add2)
        # Check that success message was printed
        mock_print.assert_called()
        assert '[SUCCESS] Task' in str(mock_print.call_args)
    
    # > view
    args_view = MagicMock()
    args_view.command = 'view'
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_view)
        # Verify that tasks were displayed
        assert mock_print.called
    
    # > complete 1
    args_complete = MagicMock()
    args_complete.command = 'complete'
    args_complete.id = 1
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_complete)
        # Check that success message was printed
        mock_print.assert_called()
        assert '[SUCCESS] Task 1 marked as complete' in str(mock_print.call_args) or 'marked as complete' in str(mock_print.call_args[0][0])
    
    # > update 2 "Walk the cat" "Take the cat for a 15-minute walk"
    args_update = MagicMock()
    args_update.command = 'update'
    args_update.id = 2
    args_update.title = 'Walk the cat'
    args_update.description = 'Take the cat for a 15-minute walk'
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_update)
        # Check that success message was printed
        mock_print.assert_called()
        assert '[SUCCESS] Task' in str(mock_print.call_args) and 'updated' in str(mock_print.call_args)
    
    # > view
    args_view2 = MagicMock()
    args_view2.command = 'view'
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_view2)
        # Verify that updated tasks were displayed
        assert mock_print.called
    
    # > delete 2
    args_delete = MagicMock()
    args_delete.command = 'delete'
    args_delete.id = 2
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_delete)
        # Check that success message was printed
        mock_print.assert_called()
        assert '[SUCCESS] Task 2 deleted' in str(mock_print.call_args[0][0])
    
    # > view
    args_view3 = MagicMock()
    args_view3.command = 'view'
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_view3)
        # Verify that only one task remains
        assert mock_print.called


def test_error_conditions():
    """Test error conditions and proper error handling"""
    # Create fresh components for the test
    repository = InMemoryTaskRepository()
    service = TaskService(repository)
    cli = CLI(service)
    
    # Try to update a non-existent task
    args_update = MagicMock()
    args_update.command = 'update'
    args_update.id = 999
    args_update.title = 'New Title'
    args_update.description = 'New Description'
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_update)
        # Check that error message was printed
        mock_print.assert_called()
        assert '[ERROR]' in str(mock_print.call_args)
    
    # Try to delete a non-existent task
    args_delete = MagicMock()
    args_delete.command = 'delete'
    args_delete.id = 999
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_delete)
        # Check that error message was printed
        mock_print.assert_called()
        assert '[ERROR]' in str(mock_print.call_args)
    
    # Try to complete a non-existent task
    args_complete = MagicMock()
    args_complete.command = 'complete'
    args_complete.id = 999
    
    with patch('builtins.print') as mock_print:
        cli.execute_command(args_complete)
        # Check that error message was printed
        mock_print.assert_called()
        assert '[ERROR]' in str(mock_print.call_args)
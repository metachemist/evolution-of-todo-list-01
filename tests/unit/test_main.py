# [Task]: T-007 | [From]: specs/2-plan/phase-1-console.md

import sys
from unittest.mock import patch
import pytest
from src.main import main


def test_main_imports_do_not_cause_circular_dependency():
    """Simple smoke test to ensure main.py can import classes without circular dependency errors"""
    # This test verifies that importing the main function doesn't cause circular import issues
    # If there were circular dependencies, this test would fail during import
    assert callable(main)


def test_main_runs_without_immediate_errors():
    """Test that main function can be called without immediate errors"""
    # Patch the CLI's main_loop method to avoid the interactive loop during testing
    with patch('src.cli.interface.CLI.main_loop') as mock_main_loop:
        # Configure the mock to return immediately
        mock_main_loop.return_value = None
        
        # Call the main function
        main()
        
        # Verify that main_loop was called
        mock_main_loop.assert_called_once()


def test_main_handles_keyboard_interrupt():
    """Test that main handles keyboard interrupt gracefully"""
    # Patch the CLI's main_loop method to raise KeyboardInterrupt
    with patch('src.cli.interface.CLI.main_loop') as mock_main_loop:
        mock_main_loop.side_effect = KeyboardInterrupt()
        
        # Call the main function - it should handle the exception gracefully
        main()
        
        # Verify that main_loop was called
        mock_main_loop.assert_called_once()


def test_main_handles_general_exception():
    """Test that main handles general exceptions"""
    # Patch the CLI's main_loop method to raise a general exception
    with patch('src.cli.interface.CLI.main_loop') as mock_main_loop:
        mock_main_loop.side_effect = RuntimeError("Test error")
        
        # Call the main function - it should re-raise the exception
        with pytest.raises(RuntimeError, match="Test error"):
            main()
        
        # Verify that main_loop was called
        mock_main_loop.assert_called_once()
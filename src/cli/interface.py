# [Task]: T-006 | [From]: specs/2-plan/phase-1-console.md

import argparse
import shlex
import sys
from typing import List
from src.services.task_service import TaskService
from src.models.task import TaskException


class ArgumentError(Exception):
    """Custom exception for argument parsing errors"""
    pass


class FriendlyArgumentParser(argparse.ArgumentParser):
    """Custom ArgumentParser that raises exceptions instead of printing usage and exiting"""

    def error(self, message):
        """Override error method to raise an exception instead of printing usage and exiting"""
        raise ArgumentError(message)


class CLI:
    """
    Command Line Interface class for interacting with the task management system.
    """

    def __init__(self, task_service: TaskService):
        """
        Initialize the CLI with a task service instance.

        Args:
            task_service: An instance of TaskService
        """
        self.task_service = task_service
        self.parser = self._create_parser()

    def _create_parser(self) -> FriendlyArgumentParser:
        """
        Create and configure the argument parser.

        Returns:
            Configured FriendlyArgumentParser instance
        """
        parser = FriendlyArgumentParser(
            prog='todo-cli',
            description='Manage your tasks from the command line',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  add "Buy groceries" "Milk, bread, eggs"
  view
  update 1 "Buy milk and bread" "Get whole milk and sourdough"
  delete 1
  complete 1
  exit
            """
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Add command
        add_parser = subparsers.add_parser('add', help='Add a new task')
        add_parser.add_argument('title', type=str, help='Title of the task')
        add_parser.add_argument('description', nargs='?', default=None, type=str, help='Description of the task')

        # View command
        view_parser = subparsers.add_parser('view', help='View all tasks')

        # Update command
        update_parser = subparsers.add_parser('update', help='Update an existing task')
        update_parser.add_argument('id', type=int, help='ID of the task to update')
        update_parser.add_argument('title', type=str, help='New title of the task')
        update_parser.add_argument('description', nargs='?', default=None, type=str, help='New description of the task')

        # Delete command
        delete_parser = subparsers.add_parser('delete', help='Delete a task')
        delete_parser.add_argument('id', type=int, help='ID of the task to delete')

        # Complete command
        complete_parser = subparsers.add_parser('complete', help='Toggle completion status of a task')
        complete_parser.add_argument('id', type=int, help='ID of the task to toggle')

        # Exit command
        subparsers.add_parser('exit', help='Exit the application')

        return parser

    def execute_command(self, args) -> None:
        """
        Execute the appropriate command based on parsed arguments.

        Args:
            args: Parsed arguments from argparse
        """
        if args.command == 'add':
            self._handle_add(args.title, args.description)
        elif args.command == 'view':
            self._handle_view()
        elif args.command == 'update':
            self._handle_update(args.id, args.title, args.description)
        elif args.command == 'delete':
            self._handle_delete(args.id)
        elif args.command == 'complete':
            self._handle_complete(args.id)
        elif args.command == 'exit':
            self._handle_exit()
        else:
            print("[ERROR] Invalid command. Use 'help' for available commands.")

    def _handle_add(self, title: str, description: str = None) -> None:
        """
        Handle the add command.

        Args:
            title: Title of the task to add
            description: Description of the task to add
        """
        try:
            task = self.task_service.add_task(title, description)
            print(f"[SUCCESS] Task {task.id} \"{task.title}\" created.")
        except Exception as e:
            self._handle_error(e)

    def _handle_view(self) -> None:
        """
        Handle the view command.
        """
        try:
            tasks = self.task_service.get_all_tasks()

            if not tasks:
                print("No tasks in your list")
                return

            print("ID | Status | Title")
            for task in tasks:
                status = "[x]" if task.completed else "[ ]"
                if task.description:
                    title_display = f"{task.title} - {task.description}"
                else:
                    title_display = task.title
                print(f"{task.id}  | {status}    | {title_display}")
        except Exception as e:
            self._handle_error(e)

    def _handle_update(self, task_id: int, title: str, description: str = None) -> None:
        """
        Handle the update command.

        Args:
            task_id: ID of the task to update
            title: New title for the task
            description: New description for the task
        """
        try:
            task = self.task_service.update_task(task_id, title, description)
            print(f"[SUCCESS] Task {task.id} updated.")
        except Exception as e:
            self._handle_error(e)

    def _handle_delete(self, task_id: int) -> None:
        """
        Handle the delete command.

        Args:
            task_id: ID of the task to delete
        """
        try:
            self.task_service.delete_task(task_id)
            print(f"[SUCCESS] Task {task_id} deleted.")
        except Exception as e:
            self._handle_error(e)

    def _handle_complete(self, task_id: int) -> None:
        """
        Handle the complete command.

        Args:
            task_id: ID of the task to toggle completion status
        """
        try:
            task = self.task_service.toggle_complete(task_id)
            status = "complete" if task.completed else "pending"
            print(f"[SUCCESS] Task {task.id} marked as {status}.")
        except Exception as e:
            self._handle_error(e)

    def _handle_exit(self) -> None:
        """
        Handle the exit command.
        """
        print("Goodbye!")
        sys.exit(0)

    def _handle_help(self) -> None:
        """
        Handle the help command by displaying available commands.
        """
        help_text = """
Available commands:
  add "title" "optional description"    - Add a new task
  view                                - View all tasks
  update <id> "title" "description"   - Update an existing task
  delete <id>                         - Delete a task
  complete <id>                       - Toggle completion status
  help                                - Show this help message
  exit                                - Exit the application
        """
        print(help_text.strip())

    def _handle_error(self, exception: Exception) -> None:
        """
        Handle errors by printing appropriate error messages.

        Args:
            exception: The exception that occurred
        """
        if isinstance(exception, TaskException):
            print(f"[ERROR] {exception}")
        else:
            print(f"[ERROR] An unexpected error occurred: {exception}")

    def main_loop(self) -> None:
        """
        Main loop to continuously prompt for user input until exit command is issued.
        """
        print("Welcome to the Task Manager CLI!")
        print("Enter commands (type 'help' for available commands, 'exit' to quit)")

        while True:
            try:
                # Get user input
                user_input = input("> ").strip()

                if not user_input:
                    continue

                # Special handling for 'help' command
                if user_input.lower() == 'help':
                    self._handle_help()
                    continue

                # Special handling for 'exit' command
                if user_input.lower() == 'exit':
                    self._handle_exit()
                    break

                # Parse the input into arguments using shlex to handle quoted strings
                try:
                    args = self.parser.parse_args(shlex.split(user_input))

                    # Execute the command
                    self.execute_command(args)

                except ValueError as e:
                    # Handle malformed input (unclosed quotes)
                    print("[ERROR] Malformed input: Unclosed quote.")
                    print("Use 'help' for available commands")
                except ArgumentError as e:
                    # Handle argument parsing errors gracefully
                    print(f"[ERROR] {str(e)}")
                    print("Use 'help' for available commands")

            except SystemExit:
                # argparse calls sys.exit when help is shown or when there's a parsing error
                # We don't want to exit the entire program, just continue the loop
                continue
            except EOFError:
                # Handle Ctrl+D (EOF) gracefully
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"[ERROR] Failed to parse command: {e}")
                print("Use 'help' for available commands")
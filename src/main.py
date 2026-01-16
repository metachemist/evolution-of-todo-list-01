# [Task]: T-007 | [From]: specs/2-plan/phase-1-console.md

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.repositories.task_repository import InMemoryTaskRepository
from src.services.task_service import TaskService
from src.cli.interface import CLI


def main():
    """
    Main entry point for the task management application.
    """
    try:
        # Instantiate the repository
        repository = InMemoryTaskRepository()

        # Instantiate the service with the repository
        task_service = TaskService(repository)

        # Instantiate the CLI with the service
        cli = CLI(task_service)

        # Start the main loop
        cli.main_loop()

    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
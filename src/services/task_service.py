# [Task]: T-005 | [From]: specs/2-plan/phase-1-console.md

from typing import List
from src.models.task import Task, InvalidTaskDataException
from src.repositories.task_repository import InMemoryTaskRepository


class TaskService:
    """
    Service class for handling business logic for task operations.
    """
    
    def __init__(self, repository: InMemoryTaskRepository):
        """
        Initialize the TaskService with a repository instance.
        
        Args:
            repository: An instance of InMemoryTaskRepository
        """
        self.repository = repository
    
    def add_task(self, title: str, description: str = None) -> Task:
        """
        Create a new task with validation.
        
        Args:
            title: The title of the task (required)
            description: The description of the task (optional)
            
        Returns:
            The created task
        """
        # Validate inputs
        if not title or title.strip() == "":
            raise InvalidTaskDataException("Title cannot be empty")
        
        # Create a new Task instance
        task = Task(
            id=0,  # Will be assigned by the repository
            title=title,
            description=description,
            completed=False
        )
        
        # Save the task using the repository
        return self.repository.create(task)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.
        
        Returns:
            A list of all tasks
        """
        return self.repository.find_all()
    
    def update_task(self, task_id: int, title: str = None, description: str = None) -> Task:
        """
        Update an existing task with new data.
        
        Args:
            task_id: The ID of the task to update
            title: The new title (optional, keeps existing if None)
            description: The new description (optional, keeps existing if None)
            
        Returns:
            The updated task
        """
        # Get the existing task
        existing_task = self.repository.find_by_id(task_id)
        
        # Prepare updated data, keeping existing values if new ones are None
        updated_title = title if title is not None else existing_task.title
        updated_description = description if description is not None else existing_task.description
        
        # Validate inputs
        if not updated_title or updated_title.strip() == "":
            raise InvalidTaskDataException("Title cannot be empty")
        
        # Create a new Task instance with updated data
        updated_task = Task(
            id=task_id,
            title=updated_title,
            description=updated_description,
            completed=existing_task.completed,
            created_at=existing_task.created_at
        )
        
        # Update the task using the repository
        return self.repository.update(task_id, updated_task)
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was successfully deleted
        """
        return self.repository.delete(task_id)
    
    def toggle_complete(self, task_id: int) -> Task:
        """
        Toggle the completion status of a task.
        
        Args:
            task_id: The ID of the task to toggle
            
        Returns:
            The updated task with flipped completion status
        """
        # Get the existing task
        existing_task = self.repository.find_by_id(task_id)
        
        # Flip the completion status
        updated_task = Task(
            id=task_id,
            title=existing_task.title,
            description=existing_task.description,
            completed=not existing_task.completed,
            created_at=existing_task.created_at
        )
        
        # Update the task using the repository
        return self.repository.update(task_id, updated_task)
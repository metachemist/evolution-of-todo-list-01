# [Task]: T-004 | [From]: specs/2-plan/phase-1-console.md

from typing import List
from src.models.task import Task, TaskNotFoundException


class InMemoryTaskRepository:
    """
    Repository class for managing tasks in memory.
    """
    
    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id = 1  # Track the next available ID for auto-increment
    
    def create(self, task: Task) -> Task:
        """
        Add a new task to storage with an auto-assigned ID.
        
        Args:
            task: The task to create
            
        Returns:
            The created task with assigned ID
        """
        # Assign the next available ID to the task
        task.id = self._next_id
        self._next_id += 1
        
        # Add the task to the internal list
        self._tasks.append(task)
        
        # Return the task with the assigned ID
        return task
    
    def find_all(self) -> List[Task]:
        """
        Retrieve all tasks.
        
        Returns:
            A list of all tasks, or empty list if none exist
        """
        # Return a copy of the list to prevent external modification
        return self._tasks.copy()
    
    def find_by_id(self, task_id: int) -> Task:
        """
        Find a task by ID.
        
        Args:
            task_id: The ID of the task to find
            
        Returns:
            The task with the specified ID
            
        Raises:
            TaskNotFoundException: If no task with the given ID exists
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        
        # If we get here, no task with the given ID was found
        raise TaskNotFoundException(task_id)
    
    def update(self, task_id: int, updated_task: Task) -> Task:
        """
        Update an existing task.
        
        Args:
            task_id: The ID of the task to update
            updated_task: The updated task data
            
        Returns:
            The updated task
            
        Raises:
            TaskNotFoundException: If no task with the given ID exists
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                # Update the task in place, preserving the ID
                updated_task.id = task_id
                self._tasks[i] = updated_task
                return updated_task
        
        # If we get here, no task with the given ID was found
        raise TaskNotFoundException(task_id)
    
    def delete(self, task_id: int) -> bool:
        """
        Remove a task by ID.
        
        Args:
            task_id: The ID of the task to delete
            
        Returns:
            True if the task was successfully deleted
            
        Raises:
            TaskNotFoundException: If no task with the given ID exists
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        
        # If we get here, no task with the given ID was found
        raise TaskNotFoundException(task_id)
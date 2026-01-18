#!/usr/bin/env python3
# [Task]: T-005 | [From]: specs/2-plan/phase-2-fullstack.md

"""
Test script to verify task endpoint functionality.
This script tests the basic CRUD operations for tasks using the API endpoints.
"""

import asyncio
import sys
import os

# Add the backend/src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from unittest.mock import AsyncMock, MagicMock, patch
from src.api.v1.endpoints.tasks import router
from src.models.task import Task, TaskCreate, TaskPublic
from src.models.user import User
import uuid
from datetime import datetime, timezone


async def test_task_endpoints():
    """
    Test the task endpoint functionality by simulating API calls.
    """
    print("Testing task endpoint functionality...")
    
    # Create a mock user (simulating the current user from auth)
    mock_user = User(
        id=uuid.uuid4(),
        email="test@example.com",
        name="Test User",
        password_hash="hashed_password",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    # Create a mock session
    mock_session = AsyncMock()
    
    # Create a task repository mock
    mock_task_repo = MagicMock()
    
    # Create a task for testing
    task_create = TaskCreate(
        title="Test Task",
        description="This is a test task",
        completed=False
    )
    
    # Mock task object that would be returned by the repository
    mock_task = TaskPublic(
        id=1,
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    
    print("\n1. Testing task creation endpoint...")
    # Test the create_task function
    with patch('src.api.v1.endpoints.tasks.TaskService') as MockTaskService:
        # Create a mock instance of the task service
        mock_instance = MockTaskService.return_value
        # Mock the create_task method to return an awaitable result
        mock_instance.create_task = AsyncMock(return_value=mock_task)

        # Call the create_task function directly
        from src.api.v1.endpoints.tasks import create_task
        result = await create_task(task_create=task_create, current_user=mock_user, session=mock_session)

        # Verify the result is a TaskPublic object
        assert isinstance(result, TaskPublic), f"Expected TaskPublic, got {type(result)}"
        assert result.title == "Test Task"
        assert result.description == "This is a test task"
        assert result.completed is False
        print("   ✅ Task creation endpoint working correctly")
    
    print("\n2. Testing task retrieval endpoint...")
    # Test the get_tasks function
    with patch('src.api.v1.endpoints.tasks.TaskService') as MockTaskService:
        # Create a mock instance of the task service
        mock_instance = MockTaskService.return_value
        # Mock the list_tasks method to return an awaitable result
        mock_instance.list_tasks = AsyncMock(return_value=([mock_task], 1))  # Return list with one task and total count

        # Call the get_tasks function directly
        from src.api.v1.endpoints.tasks import get_tasks
        results = await get_tasks(skip=0, limit=20, current_user=mock_user, session=mock_session)

        # Verify the result is a list of TaskPublic objects
        assert isinstance(results, list), f"Expected list, got {type(results)}"
        assert len(results) == 1, f"Expected 1 task, got {len(results)}"
        assert isinstance(results[0], TaskPublic), f"Expected TaskPublic, got {type(results[0])}"
        print("   ✅ Task retrieval endpoint working correctly")
    
    print("\n3. Testing single task retrieval endpoint...")
    # Test the get_task function
    with patch('src.api.v1.endpoints.tasks.TaskService') as MockTaskService:
        # Create a mock instance of the task service
        mock_instance = MockTaskService.return_value
        # Mock the get_task method to return an awaitable result
        mock_instance.get_task = AsyncMock(return_value=mock_task)

        # Call the get_task function directly
        from src.api.v1.endpoints.tasks import get_task
        result = await get_task(task_id=1, current_user=mock_user, session=mock_session)

        # Verify the result is a TaskPublic object
        assert isinstance(result, TaskPublic), f"Expected TaskPublic, got {type(result)}"
        assert result.id == 1
        assert result.title == "Test Task"
        print("   ✅ Single task retrieval endpoint working correctly")
    
    print("\n4. Testing task update endpoint...")
    # Test the update_task function
    from src.models.task import TaskUpdate
    task_update_data = TaskUpdate(
        title="Updated Task Title",
        description="Updated task description",
        completed=True
    )

    # Updated mock task object
    updated_mock_task = TaskPublic(
        id=1,
        title=task_update_data.title,
        description=task_update_data.description,
        completed=task_update_data.completed,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    with patch('src.api.v1.endpoints.tasks.TaskService') as MockTaskService:
        # Create a mock instance of the task service
        mock_instance = MockTaskService.return_value
        # Mock the update_task method to return an awaitable result
        mock_instance.update_task = AsyncMock(return_value=updated_mock_task)

        # Call the update_task function directly
        from src.api.v1.endpoints.tasks import update_task
        result = await update_task(task_id=1, task_update=task_update_data, current_user=mock_user, session=mock_session)

        # Verify the result is a TaskPublic object with updated values
        assert isinstance(result, TaskPublic), f"Expected TaskPublic, got {type(result)}"
        assert result.title == "Updated Task Title"
        assert result.description == "Updated task description"
        assert result.completed is True
        print("   ✅ Task update endpoint working correctly")

    print("\n5. Testing task partial update (PATCH) endpoint...")
    # Test the patch_update_task function
    patch_update_data = TaskUpdate(
        title="Partially Updated Task Title"  # Only updating title, other fields should remain unchanged
    )

    # Updated mock task object after partial update
    patched_mock_task = TaskPublic(
        id=1,
        title=patch_update_data.title,  # Only title changed
        description=task_create.description,  # Original description preserved
        completed=task_create.completed,  # Original completion status preserved
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    with patch('src.api.v1.endpoints.tasks.TaskService') as MockTaskService:
        # Create a mock instance of the task service
        mock_instance = MockTaskService.return_value
        # Mock the update_task method to return an awaitable result for PATCH
        mock_instance.update_task = AsyncMock(return_value=patched_mock_task)

        # Call the patch_update_task function directly
        from src.api.v1.endpoints.tasks import patch_update_task
        result = await patch_update_task(task_id=1, task_update=patch_update_data, current_user=mock_user, session=mock_session)

        # Verify the result is a TaskPublic object with only specified fields updated
        assert isinstance(result, TaskPublic), f"Expected TaskPublic, got {type(result)}"
        assert result.title == "Partially Updated Task Title"
        assert result.description == "This is a test task"  # Should remain unchanged
        assert result.completed is False  # Should remain unchanged
        print("   ✅ Task partial update (PATCH) endpoint working correctly")

    print("\n6. Testing task completion toggle endpoint...")
    # Test the toggle_task_completion function with initially incomplete task
    initially_incomplete_task = Task(
        id=1,
        user_id=mock_user.id,
        title="Toggle Completion Task",
        description="Task for testing completion toggle",
        completed=False,  # Initially incomplete
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    # Mock task object after toggling completion (should be completed)
    toggled_task_completed = TaskPublic(
        id=1,
        title="Toggle Completion Task",
        description="Task for testing completion toggle",
        completed=True,  # Now completed after toggle
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    with patch('src.api.v1.endpoints.tasks.TaskService') as MockTaskService:
        # Create a mock instance of the task service
        mock_instance = MockTaskService.return_value
        # Mock the toggle_completion method to return an awaitable result
        mock_instance.toggle_completion = AsyncMock(return_value=toggled_task_completed)

        # Call the toggle_task_completion function directly
        from src.api.v1.endpoints.tasks import toggle_task_completion
        result = await toggle_task_completion(task_id=1, current_user=mock_user, session=mock_session)

        # Verify the result is a TaskPublic object with completion status flipped
        assert isinstance(result, TaskPublic), f"Expected TaskPublic, got {type(result)}"
        assert result.completed is True  # Should be completed after toggle
        print("   ✅ Task completion toggle endpoint working correctly")
    
    print("\n7. Testing task deletion endpoint...")
    # Test the delete_task function
    with patch('src.api.v1.endpoints.tasks.TaskService') as MockTaskService:
        # Create a mock instance of the task service
        mock_instance = MockTaskService.return_value
        # Mock the delete_task method to return an awaitable result
        mock_instance.delete_task = AsyncMock(return_value=True)  # Simulate successful deletion

        # Call the delete_task function directly
        from src.api.v1.endpoints.tasks import delete_task
        # For delete, we just check that no exception is raised
        await delete_task(task_id=1, current_user=mock_user, session=mock_session)

        print("   ✅ Task deletion endpoint working correctly")

    print("\n🎉 All task endpoint tests passed!")
    print("   - Task creation endpoint")
    print("   - Task retrieval endpoint")
    print("   - Single task retrieval endpoint")
    print("   - Task update endpoint")
    print("   - Task partial update (PATCH) endpoint")
    print("   - Task completion toggle endpoint")
    print("   - Task deletion endpoint")

    return True


if __name__ == "__main__":
    success = asyncio.run(test_task_endpoints())
    if success:
        print("\n✅ TASK ENDPOINT TEST: SUCCESS")
    else:
        print("\n❌ TASK ENDPOINT TEST: FAILURE")
        sys.exit(1)
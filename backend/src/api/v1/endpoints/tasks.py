# [Task]: T-005 | [From]: specs/2-plan/phase-2-fullstack.md

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from src.models.user import User
from src.db.session import get_session
from src.services.task_service import TaskService
from src.api.deps import get_current_user
import hashlib
import json

# Initialize rate limiter for task endpoints
limiter = Limiter(key_func=get_remote_address)


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", response_model=TaskPublic)
@limiter.limit("100/minute")
async def create_task(
    request: Request,
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new task for the current user.

    Args:
        request: HTTP request object for rate limiting
        task_create: Task creation data (title, description, etc.)
        current_user: The authenticated user creating the task (from dependency)
        session: Async database session

    Returns:
        TaskPublic: The created task data
    """
    # Check for idempotency key in headers
    idempotency_key = request.headers.get("Idempotency-Key")

    task_service = TaskService()

    if idempotency_key:
        # Create a hash of the request data combined with user ID for uniqueness
        request_data = {
            "user_id": str(current_user.id),
            "task_create": task_create.dict()
        }
        request_hash = hashlib.sha256(json.dumps(request_data, sort_keys=True).encode()).hexdigest()

        # Check if this exact request was made before with this idempotency key
        # In a real implementation, we'd store this in Redis or DB

    try:
        # Create the task using the service
        created_task = await task_service.create_task(session, current_user, task_create)

        if not created_task:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create task"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return created_task


@router.get("/", response_model=List[TaskPublic])
@limiter.limit("100/minute")
async def get_tasks(
    request: Request,
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get all tasks for the current user with pagination.

    Args:
        request: HTTP request object for rate limiting
        skip: Number of tasks to skip (for pagination)
        limit: Maximum number of tasks to return (max 100)
        current_user: The authenticated user (from dependency)
        session: Async database session

    Returns:
        List[TaskPublic]: List of tasks belonging to the current user
    """
    # Limit the maximum number of tasks returned
    if limit > 100:
        limit = 100

    task_service = TaskService()

    # Get tasks for the current user with pagination
    tasks, _ = await task_service.list_tasks(session, current_user.id, offset=skip, limit=limit)

    return tasks


@router.get("/{task_id}", response_model=TaskPublic)
@limiter.limit("100/minute")
async def get_task(
    request: Request,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific task by ID.

    Args:
        request: HTTP request object for rate limiting
        task_id: ID of the task to retrieve
        current_user: The authenticated user (from dependency)
        session: Async database session

    Returns:
        TaskPublic: The requested task data

    Raises:
        HTTPException: 404 if task doesn't exist or doesn't belong to the user
    """
    task_service = TaskService()

    # Get the task by ID and user ID to ensure ownership
    task = await task_service.get_task(session, task_id, current_user.id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=TaskPublic)
@limiter.limit("100/minute")
async def update_task(
    request: Request,
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a specific task by ID.

    Args:
        request: HTTP request object for rate limiting
        task_id: ID of the task to update
        task_update: Task update data
        current_user: The authenticated user (from dependency)
        session: Async database session

    Returns:
        TaskPublic: The updated task data

    Raises:
        HTTPException: 404 if task doesn't exist or doesn't belong to the user
    """
    task_service = TaskService()

    try:
        # Update the task if it belongs to the current user
        updated_task = await task_service.update_task(session, task_id, current_user.id, task_update)

        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return updated_task


@router.patch("/{task_id}", response_model=TaskPublic)
@limiter.limit("100/minute")
async def patch_update_task(
    request: Request,
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Partially update a specific task by ID.

    Args:
        request: HTTP request object for rate limiting
        task_id: ID of the task to update
        task_update: Task update data (only specified fields will be updated)
        current_user: The authenticated user (from dependency)
        session: Async database session

    Returns:
        TaskPublic: The updated task data

    Raises:
        HTTPException: 404 if task doesn't exist or doesn't belong to the user
    """
    task_service = TaskService()

    try:
        # Update the task if it belongs to the current user
        updated_task = await task_service.update_task(session, task_id, current_user.id, task_update)

        if not updated_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return updated_task


@router.patch("/{task_id}/complete", response_model=TaskPublic)
@limiter.limit("100/minute")
async def toggle_task_completion(
    request: Request,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Toggle the completion status of a specific task by ID.

    Args:
        request: HTTP request object for rate limiting
        task_id: ID of the task to toggle
        current_user: The authenticated user (from dependency)
        session: Async database session

    Returns:
        TaskPublic: The updated task data with flipped completion status

    Raises:
        HTTPException: 404 if task doesn't exist or doesn't belong to the user
    """
    task_service = TaskService()

    # Toggle the completion status of the task if it belongs to the current user
    updated_task = await task_service.toggle_completion(session, task_id, current_user.id)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return updated_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("100/minute")
async def delete_task(
    request: Request,
    task_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a specific task by ID.

    Args:
        request: HTTP request object for rate limiting
        task_id: ID of the task to delete
        current_user: The authenticated user (from dependency)
        session: Async database session

    Raises:
        HTTPException: 404 if task doesn't exist or doesn't belong to the user
    """
    task_service = TaskService()

    # Delete the task if it belongs to the current user
    success = await task_service.delete_task(session, task_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Return 204 No Content on successful deletion
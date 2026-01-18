"""
Authentication middleware for the Todo Evolution backend.

This module provides JWT token validation and user context injection.
"""

from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import SECRET_KEY, ALGORITHM
from src.db.session import get_session
from src.models.user import User
from src.repositories.user_repository import UserRepository
import uuid


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user based on JWT token.

    Args:
        credentials: HTTP authorization credentials containing the JWT token
        session: Async database session

    Returns:
        User object if token is valid and user exists

    Raises:
        HTTPException: 401 if token is invalid, expired, or user doesn't exist
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    # Convert user_id to UUID if needed
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        raise credentials_exception

    # Fetch the user from the database
    user_repo = UserRepository()
    user = await user_repo.get_user_by_id(session, user_uuid)

    if user is None:
        raise credentials_exception

    return user
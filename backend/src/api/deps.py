# [Task]: T-007 | [From]: specs/2-plan/phase-2-fullstack.md

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.security import oauth2_scheme, SECRET_KEY, ALGORITHM
from src.db.session import get_session
from src.models.user import User
from src.repositories.user_repository import UserRepository
from src.utils.jwt import verify_access_token
from jose import jwt
from jose.exceptions import JWTError
from typing import Optional
import uuid


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user based on JWT token.

    Args:
        token: JWT token from Authorization header (extracted via oauth2_scheme)
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

    # Verify the JWT token using the utility function
    user_id = verify_access_token(token)
    if user_id is None:
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
# [Task]: T-004 | [From]: specs/2-plan/phase-2-fullstack.md

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import UserPublic
from src.db.session import get_session
from src.api.deps import get_current_user


users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/me", response_model=UserPublic)
async def get_current_user_profile(
    current_user: UserPublic = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Get the profile of the currently authenticated user.
    
    Args:
        current_user: The authenticated user (from get_current_user dependency)
        session: Async database session (unused in this endpoint but kept for consistency)
        
    Returns:
        UserPublic: Public user data (email, name, id, timestamps)
    """
    # Return the current user's public data
    # The user is already fetched and validated by the get_current_user dependency
    return current_user
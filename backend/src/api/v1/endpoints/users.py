# [Task]: T-004 | [From]: specs/2-plan/phase-2-fullstack.md

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import UserPublic
from src.db.session import get_session
from src.api.deps import get_current_user


users_router = APIRouter(prefix="/users", tags=["users"])


# NOTE: The /me endpoint is handled in auth.py to avoid duplication
# See: /api/v1/auth/me in auth.py
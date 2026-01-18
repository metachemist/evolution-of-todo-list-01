# [Task]: T-003 | [From]: specs/2-plan/phase-2-fullstack.md

from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User, UserCreate, UserUpdate, UserPublic
import uuid


class UserRepository:
    """
    Repository class for handling User data operations.
    """
    
    async def create_user(self, session: AsyncSession, user: User) -> User:
        """
        Create a new user in the database.

        Args:
            session: Async database session
            user: User object with user data (already hashed)

        Returns:
            Created User object with assigned ID
        """
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def get_user_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        """
        Retrieve a user by their email address.

        Args:
            session: Async database session
            email: Email address to search for

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_id(self, session: AsyncSession, user_id: uuid.UUID) -> Optional[User]:
        """
        Retrieve a user by their ID.

        Args:
            session: Async database session
            user_id: UUID of the user to search for

        Returns:
            User object if found, None otherwise
        """
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()
        return user
    
    async def update_user(self, session: AsyncSession, user_id: uuid.UUID, update_data: UserUpdate) -> Optional[User]:
        """
        Update an existing user.

        Args:
            session: Async database session
            user_id: ID of the user to update
            update_data: UserUpdate object with new values

        Returns:
            Updated User object if successful, None if user not found
        """
        # Get the existing user
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            return None

        # Update the user with provided values
        if update_data.email is not None:
            user.email = update_data.email
        if update_data.name is not None:
            user.name = update_data.name
        if update_data.password_hash is not None:
            user.password_hash = update_data.password_hash

        # Update the updated_at timestamp
        from datetime import datetime, timezone
        user.updated_at = datetime.now(timezone.utc)

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def delete_user(self, session: AsyncSession, user_id: uuid.UUID) -> bool:
        """
        Delete a user by their ID.

        Args:
            session: Async database session
            user_id: ID of the user to delete

        Returns:
            True if user was successfully deleted, False if not found
        """
        statement = select(User).where(User.id == user_id)
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

        if not user:
            return False

        await session.delete(user)
        await session.commit()
        return True
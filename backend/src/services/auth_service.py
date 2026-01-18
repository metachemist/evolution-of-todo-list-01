"""
Authentication service for the Todo Evolution backend.

This module provides business logic for user authentication operations.
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.user import User, UserCreate, UserUpdate
from src.repositories.user_repository import UserRepository
from src.utils.password import get_password_hash, verify_password
from src.utils.jwt import create_access_token
from datetime import timedelta
import uuid
import re


class AuthService:
    """
    Service class for handling authentication business logic.
    """

    def __init__(self):
        self.user_repo = UserRepository()

    def _validate_email(self, email: str) -> bool:
        """
        Validate email format using regex.

        Args:
            email: Email address to validate

        Returns:
            True if email format is valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def _validate_password(self, password: str) -> bool:
        """
        Validate password strength.

        Args:
            password: Password to validate

        Returns:
            True if password meets requirements, False otherwise
        """
        # At least 8 characters, one uppercase, one lowercase, one digit
        if len(password) < 8:
            return False
        # Bcrypt has a 72-byte limit, so we enforce a reasonable limit
        if len(password.encode('utf-8')) > 70:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True

    def _validate_name(self, name: str) -> bool:
        """
        Validate user name.

        Args:
            name: Name to validate

        Returns:
            True if name meets requirements, False otherwise
        """
        # Name should be 1-100 characters
        return 1 <= len(name) <= 100

    async def register_user(self, session: AsyncSession, user_create: UserCreate) -> Optional[User]:
        """
        Register a new user with the provided details.

        Args:
            session: Async database session
            user_create: User creation data (email, name, password)

        Returns:
            Created User object if successful, None if email already exists

        Raises:
            ValueError: If input validation fails
        """
        # Validate inputs
        if not self._validate_email(user_create.email):
            raise ValueError("Invalid email format")

        if not self._validate_password(user_create.password):
            raise ValueError("Password does not meet requirements (at least 8 characters, max 70 bytes, one uppercase, one lowercase, one digit)")

        if not self._validate_name(user_create.name):
            raise ValueError("Name must be between 1 and 100 characters")

        # Check if user with this email already exists
        existing_user = await self.user_repo.get_user_by_email(session, user_create.email)
        if existing_user:
            return None

        # Hash the password
        password_hash = get_password_hash(user_create.password)

        # Create the user with the hashed password
        user = User(
            email=user_create.email,
            name=user_create.name,
            password_hash=password_hash
        )

        return await self.user_repo.create_user(session, user)

    async def authenticate_user(self, session: AsyncSession, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with the provided email and password.

        Args:
            session: Async database session
            email: User's email address
            password: User's plain text password

        Returns:
            User object if credentials are valid, None otherwise
        """
        # Validate email format
        if not self._validate_email(email):
            return None

        # Validate password isn't empty
        if not password:
            return None

        user = await self.user_repo.get_user_by_email(session, email)
        if not user or not verify_password(password, user.password_hash):
            return None

        return user

    async def update_user_profile(self, session: AsyncSession, user_id: uuid.UUID, user_update: UserUpdate) -> Optional[User]:
        """
        Update user profile information.

        Args:
            session: Async database session
            user_id: ID of the user to update
            user_update: User update data

        Returns:
            Updated User object if successful, None if user not found

        Raises:
            ValueError: If input validation fails
        """
        # Validate email if provided
        if user_update.email is not None and not self._validate_email(user_update.email):
            raise ValueError("Invalid email format")

        # Validate name if provided
        if user_update.name is not None and not self._validate_name(user_update.name):
            raise ValueError("Name must be between 1 and 100 characters")

        # Validate password hash if provided (check length only, since it should already be hashed)
        if user_update.password_hash is not None and len(user_update.password_hash.encode('utf-8')) > 255:
            raise ValueError("Password hash is too long")

        return await self.user_repo.update_user(session, user_id, user_update)

    async def generate_access_token(self, user_id: uuid.UUID) -> str:
        """
        Generate an access token for the given user.

        Args:
            user_id: ID of the user to generate token for

        Returns:
            JWT access token string
        """
        access_token_expires = timedelta(minutes=10080)  # 7 days
        access_token = create_access_token(
            subject=str(user_id), expires_delta=access_token_expires
        )
        return access_token
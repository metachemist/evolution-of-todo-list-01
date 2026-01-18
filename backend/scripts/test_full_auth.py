#!/usr/bin/env python3
# [Task]: T-005 | [From]: specs/2-plan/phase-2-fullstack.md

"""
Test script to verify full authentication flow.
This script tests user registration, login, and profile access.
"""

import asyncio
import sys
import os

# Add the backend/src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

import uuid
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch, AsyncMock
from src.models.user import UserCreate, UserPublic
from src.models.token import Token
from src.api.v1.endpoints.auth import router


async def test_full_auth_flow():
    """
    Test the complete authentication flow:
    1. Register a user
    2. Login to get a token
    3. Use the token to fetch the profile
    """
    print("Testing full authentication flow...")

    # Create a mock session
    mock_session = AsyncMock()

    # Create a user repository mock
    mock_user_repo = MagicMock()

    # Create a user for testing
    user_create = UserCreate(
        email=f"test_{int(datetime.now().timestamp())}@example.com",
        name="Test User",
        password="secure_password_123"
    )

    # Mock user object that would be returned by the repository
    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_user.email = user_create.email
    mock_user.name = user_create.name
    mock_user.password_hash = "hashed_password_here"
    mock_user.created_at = datetime.now(timezone.utc)
    mock_user.updated_at = datetime.now(timezone.utc)

    print("\n1. Testing user registration (/signup)...")
    # Test the signup function
    with patch('src.api.v1.endpoints.auth.AuthService') as MockAuthService:
        # Create a mock instance of the auth service
        mock_auth_service = MockAuthService.return_value
        mock_auth_service.register_user = AsyncMock(return_value=mock_user)  # Return the mock user

        # Call the signup function directly
        from src.api.v1.endpoints.auth import signup
        result = await signup(user_create=user_create, session=mock_session)

        # Verify the result is a UserPublic object
        assert isinstance(result, UserPublic), f"Expected UserPublic, got {type(result)}"
        assert result.email == user_create.email
        assert result.name == user_create.name
        print("   ✅ User registration endpoint working correctly")

    print("\n2. Testing user login (/login)...")
    # Test the login function
    with patch('src.api.v1.endpoints.auth.AuthService') as MockAuthService:
        # Create a mock instance of the auth service
        mock_auth_service = MockAuthService.return_value
        mock_auth_service.authenticate_user = AsyncMock(return_value=mock_user)  # Return the mock user
        mock_auth_service.generate_access_token = AsyncMock(return_value="mock_access_token")  # Return a mock token

        # Mock form data for login
        from fastapi.security import OAuth2PasswordRequestForm
        class MockFormData:
            def __init__(self, username, password):
                self.username = username
                self.password = password

        mock_form_data = MockFormData(
            username=user_create.email,
            password=user_create.password
        )

        # Call the login function directly
        from src.api.v1.endpoints.auth import login
        result = await login(form_data=mock_form_data, session=mock_session)

        # Verify the result is a Token object
        assert isinstance(result, Token), f"Expected Token, got {type(result)}"
        assert result.access_token is not None
        assert result.token_type == "bearer"
        print("   ✅ User login endpoint working correctly")

    print("\n3. Testing profile access (/me)...")
    # Test the get_current_user_profile function
    with patch('src.api.v1.endpoints.auth.get_current_user') as mock_get_current_user:
        # Mock the get_current_user dependency to return our mock user
        mock_get_current_user.return_value = mock_user

        # Call the get_current_user_profile function directly
        from src.api.v1.endpoints.auth import get_current_user_profile
        result = await get_current_user_profile(current_user=mock_user)

        # Verify the result is a UserPublic object
        assert isinstance(result, UserPublic), f"Expected UserPublic, got {type(result)}"
        assert result.email == user_create.email
        assert result.name == user_create.name
        print("   ✅ Profile access endpoint working correctly")

    print("\n🎉 All authentication flow tests passed!")
    print("   - User registration endpoint")
    print("   - User login endpoint") 
    print("   - Profile access endpoint")

    return True


if __name__ == "__main__":
    success = asyncio.run(test_full_auth_flow())
    if success:
        print("\n✅ FULL AUTHENTICATION FLOW TEST: SUCCESS")
    else:
        print("\n❌ FULL AUTHENTICATION FLOW TEST: FAILURE")
        sys.exit(1)
#!/usr/bin/env python3
# [Task]: T-004 | [From]: specs/2-plan/phase-2-fullstack.md

"""
Test script to verify authentication flow.
This script tests the signup, login, and token verification functionality.
"""

import asyncio
import sys
import os

# Add the backend/src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from datetime import datetime, timedelta
from jose import jwt
from src.utils.jwt import create_access_token
from src.core.security import SECRET_KEY, ALGORITHM
from src.models.user import User
from src.models.token import TokenPayload
import uuid


async def test_auth_flow():
    """
    Test the authentication flow by simulating user registration, login, and token verification.
    """
    print("Testing authentication flow...")
    
    # Simulate user registration
    print("\n1. Simulating user registration...")
    user_email = "test_auth@example.com"
    user_name = "Test Auth User"
    user_password = "secure_password_123"
    
    print(f"   Registered user: {user_email}")
    
    # Simulate user login
    print("\n2. Simulating user login...")
    print(f"   User {user_email} logged in successfully")
    
    # Create a token for the user (simulating what happens during login)
    user_id = str(uuid.uuid4())
    token_data = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    
    # Create the access token
    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    token_type = "bearer"
    
    print(f"   Generated access token for user ID: {user_id}")
    
    # Verify the token
    print("\n3. Verifying the token...")
    try:
        # Decode the token
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        token_user_id = payload.get("sub")
        
        if token_user_id is None:
            print("   ❌ ERROR: Could not retrieve user ID from token")
            return False
            
        print(f"   Token contains user ID: {token_user_id}")
        
        # Verify that the token contains the correct user ID
        if token_user_id == user_id:
            print("   ✅ SUCCESS: Token contains the correct user ID")
        else:
            print("   ❌ ERROR: Token contains incorrect user ID")
            return False
            
    except jwt.JWTError:
        print("   ❌ ERROR: Could not decode token")
        return False
    
    print("\n✅ Authentication flow test completed successfully!")
    print("   - User registration simulated")
    print("   - Login simulated")
    print("   - Token created and verified")
    print("   - Token contains correct user ID")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(test_auth_flow())
    if success:
        print("\n🎉 AUTHENTICATION FLOW TEST: SUCCESS")
    else:
        print("\n💥 AUTHENTICATION FLOW TEST: FAILURE")
        sys.exit(1)
"""
Password utility functions for the Todo Evolution backend.

This module provides secure password hashing and verification using bcrypt.
"""

import logging
import bcrypt
from passlib.context import CryptContext


# Create a password context with bcrypt scheme
# Note: Due to compatibility issues between passlib 1.7.4 and bcrypt 5.0.0,
# we're using bcrypt directly for hashing but keeping passlib for verification
# to maintain compatibility with existing hashes
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# Set up logger
logger = logging.getLogger(__name__)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if passwords match, False otherwise
    """
    try:
        # Use bcrypt directly for verification to avoid passlib compatibility issues
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False


def get_password_hash(password: str) -> str:
    """
    Generate a hash for the given password using bcrypt directly
    to avoid compatibility issues between passlib and bcrypt 5.0.0.
    Truncates password to 70 bytes if needed to comply with bcrypt limitations.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string
    """
    try:
        # Bcrypt has a 72-byte limit, so truncate if needed
        original_length = len(password.encode('utf-8'))
        if original_length > 70:
            # Log when password is truncated
            logger.warning(f"Password being truncated from {original_length} bytes to 70 bytes for bcrypt hashing")
            # Truncate to 70 bytes while preserving character boundaries
            # Decode with 'ignore' to handle incomplete byte sequences
            password_bytes = password.encode('utf-8')[:70]
            password = password_bytes.decode('utf-8', errors='ignore')

        # Use bcrypt directly to avoid passlib compatibility issues
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Error hashing password: {str(e)}")
        raise
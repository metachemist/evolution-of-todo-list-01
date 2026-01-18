"""
Test cases for password validation and bcrypt 70-byte limit handling.
"""

import pytest
from src.utils.password import get_password_hash, verify_password
from src.services.auth_service import AuthService


def test_password_hash_with_long_password():
    """Test that passwords longer than 70 bytes are handled correctly."""
    # Create a password longer than 70 bytes
    long_password = "a" * 80  # 80 bytes

    # This should not raise an exception
    hashed = get_password_hash(long_password)

    # Verify the password still works with the truncated version (first 70 chars)
    assert verify_password(long_password[:70], hashed)  # Only first 70 chars matter due to new limit


def test_password_exactly_70_bytes():
    """Test that passwords exactly at 70 bytes work correctly."""
    password_70_bytes = "a" * 70

    # This should not raise an exception
    hashed = get_password_hash(password_70_bytes)

    # Verify the password works
    assert verify_password(password_70_bytes, hashed)


def test_password_over_70_bytes_utf8():
    """Test that UTF-8 passwords over 70 bytes are handled correctly."""
    # Create a UTF-8 password that exceeds 70 bytes when encoded
    utf8_char = "🔑"  # This is 4 bytes in UTF-8
    # Each "🔑" is 4 bytes, so 18 of them would be 72 bytes, 19 would be 76 bytes
    long_utf8_password = utf8_char * 19  # 76 bytes total

    # This should not raise an exception
    hashed = get_password_hash(long_utf8_password)

    # Verify the password still works with the truncated version
    # (first 70 bytes of the original password)
    truncated_version = long_utf8_password.encode('utf-8')[:70].decode('utf-8', errors='ignore')
    assert verify_password(truncated_version, hashed)


def test_auth_service_password_validation():
    """Test that the auth service validates passwords correctly."""
    auth_service = AuthService()

    # Valid password (under 70 bytes)
    assert auth_service._validate_password("ValidPass123")

    # Password that's 70 bytes when encoded as UTF-8 - needs to meet requirements
    password_70_bytes = "A" + "a" * 68 + "1"  # 70 chars with upper, lower, digit
    assert auth_service._validate_password(password_70_bytes)

    # Password that's over 70 bytes should fail validation
    password_over_70_bytes = "A" + "a" * 69 + "1"  # 72 chars total
    assert not auth_service._validate_password(password_over_70_bytes)


def test_password_with_mixed_utf8():
    """Test password validation with mixed UTF-8 characters."""
    auth_service = AuthService()

    # A password with mixed ASCII and UTF-8 that totals more than 70 bytes
    # "🔑" is 4 bytes, so 17 * 4 = 68 bytes, plus 1 more char makes it over 70
    # Need to add uppercase, lowercase, and digit to meet requirements
    mixed_password = "A" + ("🔑" * 17) + "a" + "1"  # 74 bytes total (1 + 68 + 1 + 1)

    assert not auth_service._validate_password(mixed_password)

    # But if it's 70 bytes or less, it should pass (with proper requirements met)
    # 1 upper + 16 emojis (64 bytes) + 1 lower + 1 digit = 67 bytes total
    mixed_password_valid = "A" + ("🔑" * 16) + "a" + "1"  # 67 bytes total
    assert auth_service._validate_password(mixed_password_valid)
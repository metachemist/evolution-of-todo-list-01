"""
Rate limiting middleware for the Todo Evolution backend.

This module provides rate limiting functionality to protect the API from abuse.
"""

import time
from collections import defaultdict
from fastapi import Request, HTTPException, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


# Initialize the rate limiter
limiter = Limiter(key_func=get_remote_address)


def get_rate_limit_middleware():
    """
    Creates and returns a rate limiting middleware.

    Returns:
        A FastAPI middleware function that enforces rate limits.
    """
    # Dictionary to store request timestamps for each IP address
    request_times = defaultdict(list)

    async def rate_limit_middleware(request: Request, call_next):
        # Get the client's IP address
        client_ip = get_remote_address(request)

        # Current time
        current_time = time.time()

        # Clean old requests (older than 60 seconds)
        request_times[client_ip] = [
            req_time for req_time in request_times[client_ip]
            if current_time - req_time < 60
        ]

        # Check if the client has exceeded the rate limit (100 requests per minute)
        if len(request_times[client_ip]) >= 100:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded: 100 requests per minute"
            )

        # Add current request time
        request_times[client_ip].append(current_time)

        # Continue with the request
        response = await call_next(request)
        return response

    return rate_limit_middleware


# Define specific rate limits for different endpoints
auth_limits = "5/minute"  # 5 requests per minute for auth endpoints
task_limits = "100/minute"  # 100 requests per minute for task endpoints
"""
Database connection configuration for the Todo Evolution backend.

This module sets up connection pooling and resilience patterns for database connections.
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import QueuePool
import os


# Database connection settings
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")


def create_engine_with_pool() -> AsyncEngine:
    """
    Create an async SQLAlchemy engine with connection pooling configured.
    
    Returns:
        AsyncEngine configured with connection pooling parameters
    """
    engine = create_async_engine(
        DATABASE_URL,
        poolclass=QueuePool,
        pool_size=10,  # Minimum number of connections in the pool
        max_overflow=30,  # Maximum number of connections beyond pool_size
        pool_pre_ping=True,  # Verify connections before use
        pool_recycle=300,  # Recycle connections after 5 minutes
        echo=False  # Set to True for SQL query logging
    )
    return engine


# Create the engine with pooling
engine = create_engine_with_pool()
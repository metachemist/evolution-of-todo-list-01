# [Task]: T-002 | [From]: specs/2-plan/phase-2-fullstack.md

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Critical check: If DATABASE_URL is missing, raise a clear ValueError
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required but not set")

# Create the async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to True for SQL query logging in development
    pool_size=10,  # Connection pool size (10-20 as specified in plan)
    max_overflow=30,  # Max overflow connections (as specified in plan)
    pool_timeout=30,  # Connection timeout (as specified in plan)
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={
        "server_settings": {
            "application_name": "todo-evolution-app",
        }
    }
)

# Create async session maker
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession
)


async def get_session():
    """
    Generator function to provide database sessions.
    
    Yields:
        AsyncSession: Database session for use in operations
    """
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables():
    """
    Create all tables defined in the SQLModel metadata.
    This function should be called during application startup.
    """
    async with engine.begin() as conn:
        # Create all tables defined in SQLModel models
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_tables():
    """
    Drop all tables defined in the SQLModel metadata.
    This is mainly for testing purposes.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
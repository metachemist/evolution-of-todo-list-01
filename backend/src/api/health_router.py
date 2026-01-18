"""
Health check router for the Todo Evolution backend.

This module provides health check endpoints to monitor the application status.
"""

from fastapi import APIRouter
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine
from src.db.session import engine

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the application is running.
    Returns status information including database connectivity.
    """
    try:
        # Attempt to connect to the database
        from sqlalchemy import text

        async with engine.connect() as conn:
            # Execute a simple query to test database connectivity
            result = await conn.execute(text("SELECT 1"))
            db_status = "connected" if result.fetchone() else "disconnected"

        return {
            "status": "ok",
            "database": db_status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": str(e)
        }


@router.get("/api/health")
async def api_health_check():
    """
    Alternative health check endpoint at /api/health
    """
    try:
        # Attempt to connect to the database
        from sqlalchemy import text

        async with engine.connect() as conn:
            # Execute a simple query to test database connectivity
            result = await conn.execute(text("SELECT 1"))
            db_status = "connected" if result.fetchone() else "disconnected"

        return {
            "success": True,
            "data": {
                "status": "healthy" if db_status == "connected" else "unhealthy",
                "service": "todo-api",
                "database": db_status,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "code": "HEALTH_CHECK_FAILED",
                "message": f"Service is not healthy: {str(e)}"
            }
        }
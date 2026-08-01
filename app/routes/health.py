"""
Health Check Routes
-------------------
Provides endpoints to verify backend health and basic application information.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from app.config import settings

router = APIRouter(
    prefix="/api/v1",
    tags=["Health Check"]
)


@router.get(
    "/health",
    summary="Health Check",
    description="Returns the current health status of the backend."
)
def health_check():
    """
    Verify backend availability.
    """

    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.APP_ENV,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
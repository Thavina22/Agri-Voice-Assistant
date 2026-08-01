from datetime import datetime, timezone
from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/api/v1", tags=["Health Check"])


@router.get("/health")
def health_check():
    """Health check endpoint to verify backend operational status."""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.APP_ENV,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

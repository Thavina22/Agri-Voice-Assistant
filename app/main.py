from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.health import router as health_router
from app.routes.voice import router as voice_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="Production-grade API for AI Voice Agriculture Assistant MVP",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS Configuration
    # During development "*" is acceptable.
    # Before production, replace "*" with your frontend URL.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get(
        "/",
        tags=["Root"],
        summary="Root",
    )
    def root():
        """API root endpoint."""
        return {
            "message": "Welcome to AI Voice Agriculture Assistant API",
            "documentation": "/docs",
            "health_check": "/api/v1/health",
            "voice_webhook": "/api/v1/voice/incoming",
        }

    # Register Routers
    app.include_router(
        health_router,
        tags=["Health Check"],
    )

    app.include_router(
        voice_router,
        tags=["Twilio Voice Webhook"],
    )

    return app


app = create_app()
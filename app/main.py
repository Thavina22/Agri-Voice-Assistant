from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes.health import router as health_router
from app.routes.voice import router as voice_router
from app.routes.dashboard import router as dashboard_router
from app.routes.demo import router as demo_router


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="Production-grade API for AI Voice Agriculture Assistant MVP",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    def root():
        return {
            "message": "Welcome to AI Voice Agriculture Assistant API",
            "documentation": "/docs",
            "health_check": "/api/v1/health",
            "voice_webhook": "/api/v1/voice/incoming",
        }

    app.include_router(health_router)
    app.include_router(voice_router)
    app.include_router(dashboard_router)
    app.include_router(demo_router)

    return app


app = create_app()
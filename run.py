"""
Application Entry Point
-----------------------
Starts the AI Voice Agriculture Assistant backend using Uvicorn.
"""

import uvicorn

from app.config import settings


def main() -> None:
    """Run the FastAPI application."""
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        reload_dirs=["app"],
    )


if __name__ == "__main__":
    main()
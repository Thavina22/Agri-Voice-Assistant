"""
Application Configuration
-------------------------
Loads all application settings from environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized application settings."""

    # --------------------------------------------------
    # Application
    # --------------------------------------------------
    APP_NAME: str = "AI Voice Agriculture Assistant"
    VERSION: str = "1.0.0"
    APP_ENV: str = "development"

    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000

    # --------------------------------------------------
    # Twilio
    # --------------------------------------------------
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""

    # --------------------------------------------------
    # AI Services
    # --------------------------------------------------
    GROQ_API_KEY: str = ""
    GEMINI_API_KEY: str = ""
    CLAUDE_API_KEY: str = ""


    # --------------------------------------------------
    # Speech-to-Text
    # --------------------------------------------------
    MAX_RECORDING_DURATION: int = 30

    # --------------------------------------------------
    # Environment
    # --------------------------------------------------
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
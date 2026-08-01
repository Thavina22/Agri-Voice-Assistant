from enum import Enum
from typing import Optional
from datetime import datetime, timezone

from pydantic import BaseModel, Field


class CallStage(str, Enum):
    """Represents each stage of the AI Voice Agriculture Assistant pipeline."""

    WELCOME = "Welcome"
    LANGUAGE_SELECTED = "Language Selected"
    RECORDING_STARTED = "Recording Started"
    RECORDING_COMPLETED = "Recording Completed"

    TRANSCRIBING = "Transcribing"

    ROOT_CAUSE_ANALYSIS = "Root Cause Analysis"

    AI_RESPONSE = "AI Response"

    VOICE_RESPONSE = "Voice Response"

    CALL_COMPLETED = "Call Completed"


class CallSession(BaseModel):
    """Stores all information related to one farmer call."""

    # -----------------------------
    # Call Information
    # -----------------------------
    call_sid: str
    caller_number: str = "Unknown"

    # -----------------------------
    # Language
    # -----------------------------
    selected_language: str = "English"
    language_code: str = "en-IN"

    # -----------------------------
    # Pipeline Status
    # -----------------------------
    current_stage: CallStage = CallStage.WELCOME

    # -----------------------------
    # Recording
    # -----------------------------
    recording_sid: Optional[str] = None
    recording_url: Optional[str] = None
    recording_duration: Optional[int] = None

    # -----------------------------
    # Speech-to-Text
    # -----------------------------
    transcript: Optional[str] = None

    # -----------------------------
    # Knowledge Retrieval (Phase 6)
    # -----------------------------
    detected_crop: Optional[str] = None
    detected_disease: Optional[str] = None
    confidence_score: Optional[float] = None

    # -----------------------------
    # AI Response (Phase 7)
    # -----------------------------
    ai_response: Optional[str] = None

    # -----------------------------
    # Metadata
    # -----------------------------
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).strftime(
            "%Y-%m-%d %H:%M:%S UTC"
        )
    )
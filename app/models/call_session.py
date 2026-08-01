from enum import Enum
from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class CallStage(str, Enum):
    """Call lifecycle stages in the processing pipeline."""
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
    """Lightweight session model tracking call lifecycle by Twilio CallSid."""
    call_sid: str
    caller_number: str = "Unknown"
    selected_language: str = "English"
    language_code: str = "en-IN"
    current_stage: CallStage = CallStage.WELCOME
    recording_sid: Optional[str] = None
    recording_url: Optional[str] = None
    recording_duration: Optional[int] = None
    transcript: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))

from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from app.utils.constants import CallStage


class CallSession(BaseModel):
    """Call Session model tracking lifecycle state by Twilio CallSid."""
    call_sid: str
    caller_number: str = "Unknown"
    selected_language: str = "English"
    language_code: str = "en-IN"
    current_stage: str = CallStage.WELCOME
    recording_sid: Optional[str] = None
    recording_url: Optional[str] = None
    recording_duration: Optional[int] = None
    transcript: Optional[str] = None
    ai_response: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
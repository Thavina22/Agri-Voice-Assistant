from typing import Dict, Optional
from app.models.call_session import CallSession
from app.utils.constants import CallStage


class CallSessionService:
    """In-memory session manager tracking call lifecycle state by Twilio CallSid."""

    _sessions: Dict[str, CallSession] = {}

    @classmethod
    def get_or_create_session(cls, call_sid: str, caller_number: str = "Unknown") -> CallSession:
        """Fetch existing call session or initialize a new session if not present."""
        sid = call_sid or "anonymous_session"

        if sid not in cls._sessions:
            cls._sessions[sid] = CallSession(
                call_sid=sid,
                caller_number=caller_number or "Unknown",
                current_stage=CallStage.WELCOME
            )
        return cls._sessions[sid]

    @classmethod
    def update_language(cls, call_sid: str, language_name: str, language_code: str) -> Optional[CallSession]:
        """Update session language selection and advance call stage."""
        session = cls.get_or_create_session(call_sid)
        session.selected_language = language_name
        session.language_code = language_code
        session.current_stage = CallStage.LANGUAGE_SELECTED
        return session

    @classmethod
    def update_recording(
        cls,
        call_sid: str,
        recording_sid: str,
        recording_url: str,
        recording_duration: int
    ) -> Optional[CallSession]:
        """Attach voice recording metadata to session and update call stage."""
        session = cls.get_or_create_session(call_sid)
        session.recording_sid = recording_sid
        session.recording_url = recording_url
        session.recording_duration = recording_duration
        session.current_stage = CallStage.RECORDING_COMPLETED
        return session

    @classmethod
    def update_transcript(cls, call_sid: str, transcript: str) -> Optional[CallSession]:
        """Attach transcribed speech text to session and update call stage to TRANSCRIBING."""
        session = cls.get_or_create_session(call_sid)
        session.transcript = transcript
        session.current_stage = CallStage.TRANSCRIBING
        return session

    @classmethod
    def clear_all(cls) -> None:
        """Reset session memory (useful for unit testing)."""
        cls._sessions.clear()
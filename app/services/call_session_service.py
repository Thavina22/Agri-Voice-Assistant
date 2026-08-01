from typing import Dict, Optional

from app.models.call_session import CallSession, CallStage


class CallSessionService:
    """In-memory session manager for tracking Twilio call lifecycle."""

    _sessions: Dict[str, CallSession] = {}

    # --------------------------------------------------
    # Session Creation
    # --------------------------------------------------
    @classmethod
    def get_or_create_session(
        cls,
        call_sid: str,
        caller_number: str = "Unknown"
    ) -> CallSession:

        if not call_sid:
            call_sid = "anonymous_session"

        if call_sid not in cls._sessions:
            cls._sessions[call_sid] = CallSession(
                call_sid=call_sid,
                caller_number=caller_number,
                current_stage=CallStage.WELCOME
            )

        return cls._sessions[call_sid]

    # --------------------------------------------------
    # Language
    # --------------------------------------------------
    @classmethod
    def update_language(
        cls,
        call_sid: str,
        language_name: str,
        language_code: str
    ) -> CallSession:

        session = cls.get_or_create_session(call_sid)

        session.selected_language = language_name
        session.language_code = language_code
        session.current_stage = CallStage.LANGUAGE_SELECTED

        return session

    # --------------------------------------------------
    # Recording
    # --------------------------------------------------
    @classmethod
    def update_recording(
        cls,
        call_sid: str,
        recording_sid: str,
        recording_url: str,
        recording_duration: int
    ) -> CallSession:

        session = cls.get_or_create_session(call_sid)

        session.recording_sid = recording_sid
        session.recording_url = recording_url
        session.recording_duration = recording_duration
        session.current_stage = CallStage.RECORDING_COMPLETED

        return session

    # --------------------------------------------------
    # Speech-to-Text
    # --------------------------------------------------
    @classmethod
    def update_transcript(
        cls,
        call_sid: str,
        transcript: str
    ) -> CallSession:

        session = cls.get_or_create_session(call_sid)

        session.transcript = transcript
        session.current_stage = CallStage.TRANSCRIBING

        return session

    # --------------------------------------------------
    # Agriculture Knowledge
    # --------------------------------------------------
    @classmethod
    def update_diagnosis(
        cls,
        call_sid: str,
        crop: str,
        disease: str,
        confidence: float
    ) -> CallSession:

        session = cls.get_or_create_session(call_sid)

        session.detected_crop = crop
        session.detected_disease = disease
        session.confidence_score = confidence
        session.current_stage = CallStage.ROOT_CAUSE_ANALYSIS

        return session

    # --------------------------------------------------
    # AI Response
    # --------------------------------------------------
    @classmethod
    def update_ai_response(
        cls,
        call_sid: str,
        response: str
    ) -> CallSession:

        session = cls.get_or_create_session(call_sid)

        session.ai_response = response
        session.current_stage = CallStage.AI_RESPONSE

        return session

    # --------------------------------------------------
    # Voice Response Completed
    # --------------------------------------------------
    @classmethod
    def complete_call(
        cls,
        call_sid: str
    ) -> CallSession:

        session = cls.get_or_create_session(call_sid)

        session.current_stage = CallStage.CALL_COMPLETED

        return session

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------
    @classmethod
    def get_session(
        cls,
        call_sid: str
    ) -> Optional[CallSession]:

        return cls._sessions.get(call_sid)

    @classmethod
    def clear_all(cls) -> None:
        """Clear all active sessions."""
        cls._sessions.clear()
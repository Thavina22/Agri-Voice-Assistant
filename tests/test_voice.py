from fastapi.testclient import TestClient
from app.main import app
from app.services.call_session_service import CallSessionService
from app.models.call_session import CallStage

client = TestClient(app)


def setup_function():
    """Clear in-memory session store before each test run."""
    CallSessionService.clear_all()


def test_incoming_voice_ivr_menu():
    """Verify incoming call initializes session and returns IVR gather menu."""
    response = client.post(
        "/api/v1/voice/incoming",
        data={"CallSid": "CA111", "From": "+919876543210"}
    )
    assert response.status_code == 200
    assert "<Gather" in response.text

    session = CallSessionService.get_or_create_session("CA111")
    assert session.caller_number == "+919876543210"
    assert session.current_stage == CallStage.WELCOME


def test_language_selection_updates_session_and_returns_record():
    """Verify language selection updates session to LANGUAGE_SELECTED and returns <Record>."""
    # First create session
    client.post("/api/v1/voice/incoming", data={"CallSid": "CA222", "From": "+919876543210"})

    # Select Tamil (1)
    response = client.post("/api/v1/voice/language", data={"CallSid": "CA222", "Digits": "1"})
    assert response.status_code == 200
    assert "<Record" in response.text

    session = CallSessionService.get_or_create_session("CA222")
    assert session.selected_language == "Tamil"
    assert session.current_stage == CallStage.LANGUAGE_SELECTED


def test_recording_callback_updates_session():
    """Verify recording callback updates session state to RECORDING_COMPLETED."""
    # Initialize call session
    client.post("/api/v1/voice/incoming", data={"CallSid": "CA333", "From": "+919876543210"})
    client.post("/api/v1/voice/language", data={"CallSid": "CA333", "Digits": "2"})

    # Trigger recording callback
    response = client.post(
        "/api/v1/voice/recording?lang=en-IN",
        data={
            "CallSid": "CA333",
            "RecordingSid": "RE999",
            "RecordingUrl": "https://api.twilio.com/2010-04-01/Accounts/AC1/Recordings/RE999.wav",
            "RecordingDuration": "18"
        }
    )
    assert response.status_code == 200
    assert "recording has been received" in response.text

    session = CallSessionService.get_or_create_session("CA333")
    assert session.current_stage == CallStage.TRANSCRIBING
    assert session.recording_sid == "RE999"
    assert session.recording_duration == 18
    assert session.transcript is not None


def test_openapi_only_exposes_canonical_voice_endpoints():
    """Legacy voice aliases should still work without appearing in the generated OpenAPI schema."""
    schema = app.openapi()
    paths = schema["paths"]

    assert "/api/v1/voice/incoming" in paths
    assert "/voice/incoming" not in paths
    assert "/api/v1/voice/language" in paths
    assert "/voice/language" not in paths
    assert "/api/v1/voice/recording" in paths
    assert "/api/v1/voice/record" not in paths


from app.services.speech_service import SpeechService
from app.services.call_session_service import CallSessionService
from app.utils.constants import CallStage


def setup_function():
    CallSessionService.clear_all()


def test_speech_service_validation():
    """Verify audio URL validation logic."""
    assert SpeechService.validate_recording("https://api.twilio.com/audio.wav") is True
    assert SpeechService.validate_recording("invalid_url") is False
    assert SpeechService.validate_recording(None) is False


def test_speech_service_transcribe_english():
    """Verify English STT transcription."""
    text = SpeechService.transcribe_audio("https://api.twilio.com/audio.wav", "en-IN")
    assert "tomato leaves" in text
    assert len(text) > 10


def test_speech_service_transcribe_tamil():
    """Verify Tamil STT transcription."""
    text = SpeechService.transcribe_audio("https://api.twilio.com/audio.wav", "ta-IN")
    assert "தக்காளி" in text


def test_speech_service_transcribe_telugu():
    """Verify Telugu STT transcription."""
    text = SpeechService.transcribe_audio("https://api.twilio.com/audio.wav", "te-IN")
    assert "టమోటా" in text


def test_call_session_transcript_update():
    """Verify CallSessionService update_transcript advances stage to TRANSCRIBING."""
    session = CallSessionService.get_or_create_session("STT_CALL_1")
    CallSessionService.update_transcript("STT_CALL_1", "Sample transcript")

    session = CallSessionService.get_or_create_session("STT_CALL_1")
    assert session.transcript == "Sample transcript"
    assert session.current_stage == CallStage.TRANSCRIBING

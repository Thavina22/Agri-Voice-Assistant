from typing import Optional

DEMO_TRANSCRIPTS = {
    "ta-IN": "என் தக்காளி இலையில் கருப்பு புள்ளிகள் மற்றும் மஞ்சள் நிற வளையங்கள் உள்ளன.",
    "en-IN": "My tomato leaves have dark brown spots with yellow concentric rings.",
    "te-IN": "నా టమోటా ఆకులపై నల్లటి మచ్చలు మరియు పసుపు రంగు వలయాలు ఉన్నాయి."
}


class SpeechService:
    """Service abstraction for audio validation, downloading, and STT transcription."""

    @staticmethod
    def validate_recording(recording_url: Optional[str]) -> bool:
        """Validate if recording URL is present and properly formatted."""
        if not recording_url or not isinstance(recording_url, str):
            return False
        return recording_url.startswith("http://") or recording_url.startswith("https://")

    @staticmethod
    def download_audio(recording_url: str) -> Optional[bytes]:
        """Placeholder abstraction for downloading audio stream from Twilio URL."""
        if not SpeechService.validate_recording(recording_url):
            return None
        # Placeholder for downloading raw audio bytes when external API requires binary payload
        return b"MOCK_AUDIO_BYTES"

    @staticmethod
    def transcribe_audio(recording_url: str, language_code: str = "en-IN") -> str:
        """Transcribe audio recording into text based on language code."""
        if not SpeechService.validate_recording(recording_url):
            return ""
        return DEMO_TRANSCRIPTS.get(language_code, DEMO_TRANSCRIPTS["en-IN"])
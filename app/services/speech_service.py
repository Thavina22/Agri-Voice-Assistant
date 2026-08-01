"""
Speech-to-Text Service
----------------------
Handles transcription of farmer voice recordings.
Uses demo transcription during development and can later
be connected to Groq Whisper, Google STT or Bhashini.
"""

import os
from typing import Dict


# --------------------------------------------------
# Demo Transcripts
# --------------------------------------------------

DEMO_TRANSCRIPTS: Dict[str, str] = {
    "ta-IN": (
        "என் தக்காளி இலையில் கருப்பு புள்ளிகள் "
        "மற்றும் மஞ்சள் நிற வளையங்கள் உள்ளன."
    ),

    "en-IN": (
        "My tomato leaves have dark brown spots "
        "with yellow concentric rings."
    ),

    "te-IN": (
        "నా టమోటా ఆకులపై నల్లటి మచ్చలు "
        "మరియు పసుపు రంగు వలయాలు ఉన్నాయి."
    ),
}


class SpeechService:
    """
    Speech-to-Text Service.
    """

    @staticmethod
    def transcribe_audio(
        recording_url: str,
        language_code: str = "en-IN"
    ) -> str:
        """
        Convert recorded speech into text.

        Parameters
        ----------
        recording_url : str
            Twilio recording URL.

        language_code : str
            Farmer language.

        Returns
        -------
        str
            Transcribed text.
        """

        print("\n========================================")
        print("Speech-to-Text")
        print("========================================")
        print(f"Recording URL : {recording_url}")
        print(f"Language      : {language_code}")

        # ----------------------------------------
        # Future Whisper / Google STT Integration
        # ----------------------------------------

        if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
            return SpeechService._transcribe_google(
                recording_url,
                language_code
            )

        if os.getenv("GROQ_API_KEY"):
            return SpeechService._transcribe_whisper(
                recording_url,
                language_code
            )

        transcript = DEMO_TRANSCRIPTS.get(
            language_code,
            DEMO_TRANSCRIPTS["en-IN"]
        )

        print(f"Transcript    : {transcript}")
        print("========================================\n")

        return transcript

    # --------------------------------------------------
    # Future Google STT
    # --------------------------------------------------

    @staticmethod
    def _transcribe_google(
        recording_url: str,
        language_code: str
    ) -> str:
        """
        Placeholder for Google Speech-to-Text.
        """

        return DEMO_TRANSCRIPTS.get(
            language_code,
            DEMO_TRANSCRIPTS["en-IN"]
        )

    # --------------------------------------------------
    # Future Groq Whisper
    # --------------------------------------------------

    @staticmethod
    def _transcribe_whisper(
        recording_url: str,
        language_code: str
    ) -> str:
        """
        Placeholder for Groq Whisper API.
        """

        return DEMO_TRANSCRIPTS.get(
            language_code,
            DEMO_TRANSCRIPTS["en-IN"]
        )
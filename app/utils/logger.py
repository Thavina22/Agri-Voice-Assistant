import logging
from typing import Any

# Configure standard logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("agriculture_assistant")


def log_call_summary(session: Any) -> None:
    """Consistently format and print call session summary to console."""
    banner = (
        "\n=================================================\n"
        "Incoming Recording Metadata\n"
        "=================================================\n"
        f"Call SID           {getattr(session, 'call_sid', 'N/A')}\n"
        f"Caller             {getattr(session, 'caller_number', 'Unknown')}\n"
        f"Language           {getattr(session, 'selected_language', 'N/A')} ({getattr(session, 'language_code', 'N/A')})\n"
        f"Stage              {getattr(session, 'current_stage', 'N/A')}\n"
        f"Recording SID      {getattr(session, 'recording_sid', 'N/A')}\n"
        f"Recording Duration {getattr(session, 'recording_duration', 'N/A')} seconds\n"
        f"Recording URL      {getattr(session, 'recording_url', 'N/A')}\n"
        f"Transcript         {getattr(session, 'transcript', None)}\n"
        f"AI Response        {getattr(session, 'ai_response', None)}\n"
        f"Timestamp          {getattr(session, 'timestamp', 'N/A')}\n"
        "=================================================\n"
    )
    print(banner)

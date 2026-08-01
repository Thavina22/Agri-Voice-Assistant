from fastapi import APIRouter, Response, Form
from typing import Optional

from app.services.twilio_service import TwilioService, LANGUAGES
from app.services.call_session_service import CallSessionService
from app.services.speech_service import SpeechService
from app.services.agri_ai_service import AgriAIService


router = APIRouter(tags=["Twilio Voice Webhook"])


# ==================================================
# Incoming Voice Call
# ==================================================

@router.post(
    "/api/v1/voice/incoming",
    response_class=Response,
    include_in_schema=True,
    operation_id="incoming_voice_call_post"
)
@router.post("/voice/incoming", response_class=Response, include_in_schema=False)
@router.post("/voice", response_class=Response, include_in_schema=False)
async def incoming_voice_call(
    CallSid: Optional[str] = Form(None),
    From: Optional[str] = Form(None)
):
    """
    Initial farmer call handler.
    Shows language selection menu.
    """

    sid = CallSid or "anonymous_call"
    caller = From or "Unknown"


    CallSessionService.get_or_create_session(
        call_sid=sid,
        caller_number=caller
    )


    twiml_xml = TwilioService.build_ivr_menu_twiml()


    return Response(
        content=twiml_xml,
        media_type="application/xml"
    )



# ==================================================
# Language Selection
# ==================================================

@router.post(
    "/api/v1/voice/language",
    response_class=Response,
    include_in_schema=True
)
@router.post(
    "/voice/language",
    response_class=Response,
    include_in_schema=False
)
async def process_language_selection(
    CallSid: Optional[str] = Form(None),
    From: Optional[str] = Form(None),
    Digits: Optional[str] = Form(None)
):

    sid = CallSid or "anonymous_call"

    digit = Digits or ""


    lang_info = LANGUAGES.get(digit)


    if lang_info:

        CallSessionService.update_language(
            call_sid=sid,
            language_name=lang_info["name"],
            language_code=lang_info["code"]
        )


    twiml_xml = TwilioService.build_recording_prompt_twiml(
        digit
    )


    return Response(
        content=twiml_xml,
        media_type="application/xml"
    )



# ==================================================
# Recording + AI Analysis
# ==================================================

@router.post(
    "/api/v1/voice/recording",
    response_class=Response,
    include_in_schema=True,
    operation_id="handle_voice_recording_post"
)
@router.post(
    "/voice/recording",
    response_class=Response,
    include_in_schema=False
)
@router.post(
    "/api/v1/voice/record",
    response_class=Response,
    include_in_schema=False
)
@router.post(
    "/voice/record",
    response_class=Response,
    include_in_schema=False
)
async def handle_voice_recording_post(
    lang: str = "en-IN",
    CallSid: Optional[str] = Form(None),
    RecordingSid: Optional[str] = Form(None),
    RecordingUrl: Optional[str] = Form(None),
    RecordingDuration: Optional[str] = Form(None)
):
    """
    Complete AI agriculture pipeline:

    Twilio Recording
        ↓
    Whisper Speech-to-Text
        ↓
    Agri AI Analysis
        ↓
    Twilio Voice Response
    """


    sid = CallSid or "anonymous_call"


    rec_sid = RecordingSid or "N/A"

    rec_url = RecordingUrl or ""


    duration = (
        int(RecordingDuration)
        if RecordingDuration and RecordingDuration.isdigit()
        else 0
    )



    # --------------------------
    # Save recording
    # --------------------------

    session = CallSessionService.update_recording(
        sid,
        rec_sid,
        rec_url,
        duration
    )



    # --------------------------
    # Whisper STT
    # --------------------------

    transcript = SpeechService.transcribe_audio(
        rec_url,
        session.language_code
    )


    session = CallSessionService.update_transcript(
        sid,
        transcript
    )



    # --------------------------
    # Agriculture AI
    # --------------------------

    try:

        advice = AgriAIService.analyze_crop_issue(
            transcript,
            session.language_code
        )

    except Exception as e:

        print("AgriAI Error:", e)

        advice = (
            "Unable to analyze your crop issue currently. "
            "Please try again."
        )



    # --------------------------
    # Logs
    # --------------------------

    print("\n=================================================")
    print("AI Agriculture Analysis Completed")
    print("=================================================")
    print(f"Call SID   : {session.call_sid}")
    print(f"Language   : {session.language_code}")
    print(f"Transcript : {transcript}")
    print(f"Advice     : {advice}")
    print("=================================================\n")



    _print_recording_summary(session)



    # --------------------------
    # AI Voice Response
    # --------------------------

    twiml_xml = TwilioService.build_ai_response_twiml(
        message=advice,
        lang_code=session.language_code
    )


    return Response(
        content=twiml_xml,
        media_type="application/xml"
    )



# ==================================================
# Debug GET Recording Endpoint
# ==================================================

@router.get(
    "/api/v1/voice/recording",
    response_class=Response,
    include_in_schema=True
)
async def handle_voice_recording_get(
    lang: str = "en-IN",
    call_sid: str = "anonymous_call",
    recording_sid: str = "TEST_RECORDING",
    recording_url: str = "https://api.twilio.com/sample.wav",
    recording_duration: int = 10
):


    session = CallSessionService.update_recording(
        call_sid,
        recording_sid,
        recording_url,
        recording_duration
    )


    transcript = SpeechService.transcribe_audio(
        recording_url,
        session.language_code
    )


    session = CallSessionService.update_transcript(
        call_sid,
        transcript
    )


    advice = AgriAIService.analyze_crop_issue(
        transcript,
        session.language_code
    )


    twiml_xml = TwilioService.build_ai_response_twiml(
        advice,
        session.language_code
    )


    return Response(
        content=twiml_xml,
        media_type="application/xml"
    )



# ==================================================
# Terminal Summary
# ==================================================

def _print_recording_summary(session):

    print("\n=================================================")
    print("Speech-to-Text Processing Completed")
    print("=================================================")
    print(f"Call SID           {session.call_sid}")
    print(f"Language           {session.selected_language} ({session.language_code})")
    print(f"Stage              {session.current_stage.value}")
    print(f"Recording SID      {session.recording_sid}")
    print(f"Recording Duration {session.recording_duration} seconds")
    print(f"Transcript         \"{session.transcript}\"")
    print(f"Timestamp          {session.timestamp}")
    print("=================================================\n")
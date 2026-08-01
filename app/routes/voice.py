from typing import Optional

from fastapi import APIRouter, Form, Response
from app.services.agri_ai_service import AgriAIService

from app.services.twilio_service import (
    TwilioService,
    LANGUAGES
)

from app.services.call_session_service import (
    CallSessionService
)

from app.services.speech_service import (
    SpeechService
)

from app.services.agri_ai_service import (
    AgriAIService
)


router = APIRouter(
    tags=["Twilio Voice Webhook"]
)


# ==========================================================
# Incoming Voice Call
# ==========================================================

@router.post(
    "/api/v1/voice/incoming",
    response_class=Response,
    include_in_schema=True,
    operation_id="incoming_voice_call_post"
)

@router.post(
    "/voice/incoming",
    response_class=Response,
    include_in_schema=False
)

@router.post(
    "/voice",
    response_class=Response,
    include_in_schema=False
)

async def incoming_voice_call(
    CallSid: Optional[str] = Form(None),
    From: Optional[str] = Form(None)
):
    """
    First endpoint hit by Twilio when the farmer calls.

    Flow

    Incoming Call
            ↓
    Create Session
            ↓
    Language IVR
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


# ==========================================================
# Language Selection
# ==========================================================

@router.post(
    "/api/v1/voice/language",
    response_class=Response,
    include_in_schema=True,
    operation_id="process_language_selection"
)

@router.post(
    "/voice/language",
    response_class=Response,
    include_in_schema=False
)

async def process_language_selection(
    CallSid: Optional[str] = Form(None),
    Digits: Optional[str] = Form(None)
): 
    """
    Receives language selection from Twilio Gather.

    1 → Tamil

    2 → English

    3 → Telugu
    """

    sid = CallSid or "anonymous_call"

    digit = Digits or ""

    lang_info = LANGUAGES.get(digit)

    # ---------------------------------------------
    # Invalid Selection
    # ---------------------------------------------

    if not lang_info:

        twiml_xml = TwilioService.build_ivr_menu_twiml()

        return Response(
            content=twiml_xml,
            media_type="application/xml"
        )

    # ---------------------------------------------
    # Save Language
    # ---------------------------------------------

    CallSessionService.update_language(
        call_sid=sid,
        language_name=lang_info["name"],
        language_code=lang_info["code"]
    )

    # ---------------------------------------------
    # Ask Farmer to Speak
    # ---------------------------------------------

    twiml_xml = TwilioService.build_recording_prompt_twiml(
        digit
    )

    return Response(
        content=twiml_xml,
        media_type="application/xml"
    )
    
# ==========================================================
# Recording Callback
# ==========================================================

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
    Complete AI Pipeline    

    Twilio Recording
            ↓
    Speech-to-Text
            ↓
    Agriculture AI
            ↓
    Twilio Voice Response
    """

    sid = CallSid or "anonymous_call"

    recording_sid = RecordingSid or "N/A"

    recording_url = RecordingUrl or ""

    recording_duration = (
        int(RecordingDuration)
        if RecordingDuration and RecordingDuration.isdigit()
        else 0
    )

    # --------------------------------------------------
    # Save Recording Details
    # --------------------------------------------------

    session = CallSessionService.update_recording(
        call_sid=sid,
        recording_sid=recording_sid,
        recording_url=recording_url,
        recording_duration=recording_duration
    )

    # --------------------------------------------------
    # Speech-to-Text
    # --------------------------------------------------

    try:

        transcript = SpeechService.transcribe_audio(
            recording_url,
            session.language_code
        )

    except Exception as e:

        print("\nSpeech-to-Text Error")
        print(e)

        transcript = (
            "Unable to transcribe the farmer's speech."
        )

    session = CallSessionService.update_transcript(
        sid,
        transcript
    )

    # --------------------------------------------------
    # Agriculture AI
    # --------------------------------------------------

    try:

        advice = AgriAIService.analyze_crop_issue(
            transcript,
            session.language_code
        )

    except Exception as e:

        print("\nAgriculture AI Error")
        print(e)

        advice = (
            "Sorry. I am unable to analyse your crop problem "
            "right now. Please try again later."
        )

    # --------------------------------------------------
    # Save AI Response
    # --------------------------------------------------

    CallSessionService.update_ai_response(
        sid,
        advice
    )

    # --------------------------------------------------
    # Console Output
    # --------------------------------------------------

    print("\n=================================================")
    print("AI Agriculture Analysis Completed")
    print("=================================================")
    print(f"Call SID           : {session.call_sid}")
    print(f"Language           : {session.selected_language}")
    print(f"Recording Duration : {session.recording_duration} sec")
    print(f"Transcript         : {transcript}")
    print(f"AI Advice          : {advice}")
    print("=================================================\n")

    _print_recording_summary(session)

    # --------------------------------------------------
    # Build Twilio Response
    # --------------------------------------------------

    twiml_xml = TwilioService.build_ai_response_twiml(
        message=advice,
        lang_code=session.language_code
    )

    # --------------------------------------------------
    # Call Completed
    # --------------------------------------------------

    CallSessionService.complete_call(sid)

    return Response(
        content=twiml_xml,
        media_type="application/xml"
    )
# ==========================================================
# Debug GET Endpoint
# ==========================================================

@router.get(
    "/api/v1/voice/recording",
    response_class=Response,
    include_in_schema=True,
    operation_id="handle_voice_recording_get"
)
async def handle_voice_recording_get(
    lang: str = "en-IN",
    call_sid: str = "TEST_CALL_001",
    recording_sid: str = "TEST_RECORDING",
    recording_url: str = "https://api.twilio.com/sample.wav",
    recording_duration: int = 15
):
    """
    Debug endpoint for browser testing without Twilio.

    Simulates the complete AI pipeline.
    """

    session = CallSessionService.update_recording(
        call_sid=call_sid,
        recording_sid=recording_sid,
        recording_url=recording_url,
        recording_duration=recording_duration
    )

    try:

        transcript = SpeechService.transcribe_audio(
            recording_url,
            session.language_code
        )

    except Exception:

        transcript = "Unable to transcribe."

    session = CallSessionService.update_transcript(
        call_sid,
        transcript
    )

    try:

        advice = AgriAIService.analyze_crop_issue(
            transcript,
            session.language_code
        )

    except Exception:

        advice = (
            "Unable to analyse crop issue currently."
        )

    CallSessionService.update_ai_response(
        call_sid,
        advice
    )

    twiml_xml = TwilioService.build_ai_response_twiml(
        message=advice,
        lang_code=session.language_code
    )

    CallSessionService.complete_call(call_sid)

    return Response(
        content=twiml_xml,
        media_type="application/xml"
    )


# ==========================================================
# Terminal Summary
# ==========================================================

def _print_recording_summary(session) -> None:
    """
    Print a clean summary of the call session
    for debugging and hackathon demo.
    """

    print("\n=================================================")
    print("AI Voice Agriculture Assistant")
    print("=================================================")
    print(f"Call SID           : {session.call_sid}")
    print(f"Caller             : {session.caller_number}")
    print(f"Language           : {session.selected_language}")
    print(f"Language Code      : {session.language_code}")
    print(f"Stage              : {session.current_stage.value}")
    print(f"Recording SID      : {session.recording_sid}")
    print(f"Recording Duration : {session.recording_duration} sec")
    print(f"Transcript         : {session.transcript}")

    if getattr(session, "detected_crop", None):
        print(f"Crop               : {session.detected_crop}")

    if getattr(session, "detected_disease", None):
        print(f"Disease            : {session.detected_disease}")

    if getattr(session, "confidence_score", None) is not None:
        print(f"Confidence         : {session.confidence_score}")

    if getattr(session, "ai_response", None):
        print(f"AI Advice          : {session.ai_response}")

    print(f"Timestamp          : {session.timestamp}")
    print("=================================================\n")
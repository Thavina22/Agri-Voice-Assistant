from fastapi import APIRouter, Response, Form
from typing import Optional

from app.services.twilio_service import TwilioService, LANGUAGES
from app.services.call_session_service import CallSessionService
from app.services.speech_service import SpeechService
from app.services.agri_ai_service import AgriAIService
from app.utils.logger import log_call_summary


router = APIRouter(tags=["Twilio Voice Webhook"])


# ===============================
# Incoming Call
# ===============================

@router.api_route("/api/v1/voice/incoming", methods=["GET", "POST"], response_class=Response)
@router.api_route("/voice/incoming", methods=["GET", "POST"], response_class=Response)
@router.api_route("/voice", methods=["GET", "POST"], response_class=Response)
async def incoming_voice_call(
    CallSid: Optional[str] = Form(None),
    From: Optional[str] = Form(None)
):

    try:
        sid = CallSid or "anonymous_call"
        caller = From or "Unknown"

        print("Incoming Call:", sid)

        CallSessionService.get_or_create_session(
            call_sid=sid,
            caller_number=caller
        )

        twiml_xml = TwilioService.build_ivr_menu_twiml()

        return Response(
            content=twiml_xml,
            media_type="application/xml"
        )

    except Exception as err:
        print("Incoming call error:", err)

        return Response(
            content=TwilioService.build_apology_twiml("en-IN"),
            media_type="application/xml"
        )


# ===============================
# Language Selection
# ===============================

@router.post("/api/v1/voice/language", response_class=Response)
@router.post("/voice/language", response_class=Response)
async def process_language_selection(
    CallSid: Optional[str] = Form(None),
    From: Optional[str] = Form(None),
    Digits: Optional[str] = Form(None),
    digits: Optional[str] = Form(None)
):
    """Processes farmer language selection digit and returns <Record> prompt TwiML."""
    try:

        sid = CallSid or "anonymous_call"
        digit = Digits or digits or ""

        print("\n===== LANGUAGE MENU =====")
        print("Call SID:", sid)
        print("Pressed Digit:", digit)


        lang_info = LANGUAGES.get(digit)

        print("Selected Language:", lang_info)


        if lang_info:

            CallSessionService.update_language(
                call_sid=sid,
                language_name=lang_info["name"],
                language_code=lang_info["code"]
            )


            # Pass actual language code
            twiml_xml = TwilioService.build_recording_prompt_twiml(
                lang_info["code"]
            )

        else:

            twiml_xml = TwilioService.build_apology_twiml(
                "en-IN"
            )


        print("Generated TwiML:")
        print(twiml_xml)


        return Response(
            content=twiml_xml,
            media_type="application/xml"
        )


    except Exception as err:

        print("Language selection error:", err)

        return Response(
            content=TwilioService.build_apology_twiml("en-IN"),
            media_type="application/xml"
        )



# ===============================
# Recording Callback
# ===============================


@router.post("/api/v1/voice/recording", response_class=Response)
@router.post("/voice/recording", response_class=Response)
@router.post("/api/v1/voice/record", response_class=Response)
@router.post("/voice/record", response_class=Response)
async def handle_voice_recording_post(
    CallSid: Optional[str] = Form(None),
    RecordingSid: Optional[str] = Form(None),
    RecordingUrl: Optional[str] = Form(None),
    RecordingDuration: Optional[str] = Form(None)
):

    sid = CallSid or "anonymous_call"


    try:

        print("\n===== RECORDING CALLBACK =====")
        print("Call SID:", sid)


        duration = (
            int(RecordingDuration)
            if RecordingDuration and RecordingDuration.isdigit()
            else 0
        )


        session = CallSessionService.update_recording(
            sid,
            RecordingSid or "N/A",
            RecordingUrl or "N/A",
            duration
        )


        print(
            "Current Language:",
            session.language_code
        )


        transcript = SpeechService.transcribe_audio(
            RecordingUrl,
            session.language_code
        )


        print(
            "Transcript:",
            transcript
        )


        session = CallSessionService.update_transcript(
            sid,
            transcript
        )


        ai_response = AgriAIService.analyze_crop_issue(
            transcript,
            session.language_code
        )


        print(
            "AI Response:",
            ai_response
        )


        log_call_summary(session)


        twiml_xml = TwilioService.build_ai_response_twiml(
            ai_response,
            lang_code=session.language_code
        )


        return Response(
            content=twiml_xml,
            media_type="application/xml"
        )


    except Exception as err:

        print(
            f"Recording error {sid}:",
            err
        )


        return Response(
            content=TwilioService.build_apology_twiml("en-IN"),
            media_type="application/xml"
        )
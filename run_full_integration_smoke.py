from fastapi.testclient import TestClient
from app.main import app
from app.services.call_session_service import CallSessionService
from app.services.agri_ai_service import AgriAIService
from app.services.twilio_service import TwilioService

client = TestClient(app)
CallSessionService.clear_all()

CALL_SID = "CA_FULL"

# 1) Incoming
r1 = client.post("/api/v1/voice/incoming", data={"CallSid": CALL_SID, "From": "+919000000000"})
print("[incoming] status:", r1.status_code)

# 2) Select language (English - 2)
r2 = client.post("/api/v1/voice/language", data={"CallSid": CALL_SID, "Digits": "2"})
print("[language] status:", r2.status_code)

# 3) Simulate recording callback
r3 = client.post(
    "/api/v1/voice/recording?lang=en-IN",
    data={
        "CallSid": CALL_SID,
        "RecordingSid": "RE_FULL",
        "RecordingUrl": "https://api.twilio.com/sample.wav",
        "RecordingDuration": "20"
    }
)
print("[recording callback] status:", r3.status_code)

# At this point, transcription should have been applied
session = CallSessionService.get_or_create_session(CALL_SID)
print("[session after transcription] stage:", session.current_stage)
print("[transcript]:", session.transcript)

# 4) Call AgriAIService to analyze transcript
advice = AgriAIService.analyze_crop_issue(session.transcript or "", language=session.language_code)
print("[AI advice]:", advice)

ai_twiml = TwilioService.build_ai_response_twiml(advice, lang_code=session.language_code)
# 5) Update session with AI response and produce TwiML
try:
    CallSessionService.update_ai_response(CALL_SID, advice)
except AttributeError:
    # older or alternate API: set directly on the session object
    s = CallSessionService.get_or_create_session(CALL_SID)
    s.ai_response = advice
    s.current_stage = "AI_RESPONSE"

ai_twiml = TwilioService.build_ai_response_twiml(advice, lang_code=session.language_code)
print("[ai twiml snippet]:", ai_twiml[:300])

# 6) Mark call complete
try:
    CallSessionService.complete_call(CALL_SID)
except AttributeError:
    s = CallSessionService.get_or_create_session(CALL_SID)
    s.current_stage = "CALL_COMPLETED"

print("[final session]:", CallSessionService.get_or_create_session(CALL_SID).dict())

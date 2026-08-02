from fastapi.testclient import TestClient
from app.main import app
from app.services.call_session_service import CallSessionService

client = TestClient(app)

# Reset sessions
CallSessionService.clear_all()

# 1) Incoming call
r1 = client.post("/api/v1/voice/incoming", data={"CallSid": "CA_SMOKE", "From": "+911234567890"})
print("incoming ->", r1.status_code)
print(r1.text[:400])

# 2) Language selection (Tamil)
r2 = client.post("/api/v1/voice/language", data={"CallSid": "CA_SMOKE", "Digits": "1"})
print("language ->", r2.status_code)
print(r2.text[:400])

# 3) Recording callback
r3 = client.post(
    "/api/v1/voice/recording?lang=ta-IN",
    data={
        "CallSid": "CA_SMOKE",
        "RecordingSid": "RE_SMK",
        "RecordingUrl": "https://api.twilio.com/sample.wav",
        "RecordingDuration": "12"
    }
)
print("recording ->", r3.status_code)
print(r3.text[:400])

# Inspect session
session = CallSessionService.get_or_create_session("CA_SMOKE")
print("session:", session.dict())

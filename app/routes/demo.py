from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from app.services.call_session_service import CallSessionService
from app.services.twilio_service import TwilioService
from app.services.speech_service import SpeechService
from app.services.agri_ai_service import AgriAIService
import time

router = APIRouter()


@router.get("/demo/call", response_class=HTMLResponse)
def demo_call(number: str = "919000000000"):
    """Simulate a Twilio voice call flow for `number` and return an interactive playback page."""

    call_sid = f"CA_DEMO_{int(time.time())}"
    caller = f"+{number}"

    # initialize session
    CallSessionService.get_or_create_session(call_sid, caller)

    # IVR menu TwiML
    ivr = TwilioService.build_ivr_menu_twiml()

    # simulate language selection (2 = English)
    CallSessionService.update_language(call_sid, "English", "en-IN")
    record_prompt = TwilioService.build_recording_prompt_twiml("2")

    # simulate recording callback
    rec_sid = "RE_DEMO_1"
    rec_url = "https://api.twilio.com/sample.wav"
    rec_dur = 18
    CallSessionService.update_recording(call_sid, rec_sid, rec_url, rec_dur)

    # transcribe
    transcript = SpeechService.transcribe_audio(rec_url, "en-IN")
    CallSessionService.update_transcript(call_sid, transcript)

    # analyze via AgriAIService (fallback if no key)
    advice = AgriAIService.analyze_crop_issue(transcript, language="en-IN")
    try:
        CallSessionService.update_ai_response(call_sid, advice)
    except Exception:
        s = CallSessionService.get_or_create_session(call_sid)
        s.ai_response = advice
        s.current_stage = "AI_RESPONSE"

    ai_twiml = TwilioService.build_ai_response_twiml(advice, lang_code="en-IN")

    # Build a frontend-like layout using Tailwind CDN so the demo matches the app style
    import json

    js_transcript = json.dumps(transcript)
    js_advice = json.dumps(advice)

    html_template = """
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>Demo Call Playback - %%CALLER%%</title>
      <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="min-h-screen bg-gray-50 text-gray-800">
      <div class="flex">
        <!-- Sidebar -->
        <aside class="w-64 bg-white border-r min-h-screen p-6">
          <div class="mb-8">
            <h1 class="text-xl font-semibold">AgriVoice AI</h1>
            <p class="text-sm text-gray-500">Demo playback</p>
          </div>
          <nav class="space-y-2 text-sm">
            <a class="block py-2 px-3 rounded bg-green-50 text-green-700">Dashboard</a>
            <a class="block py-2 px-3 rounded hover:bg-gray-100">Voice Consultation</a>
            <a class="block py-2 px-3 rounded hover:bg-gray-100">Call History</a>
            <a class="block py-2 px-3 rounded hover:bg-gray-100">Knowledge Base</a>
          </nav>
        </aside>

        <!-- Main -->
        <main class="flex-1 p-8">
          <header class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-2xl font-bold">Simulated Call — {caller}</h2>
              <p class="text-sm text-gray-500">Interactive playback of the Twilio call flow</p>
            </div>
            <div class="space-x-2">
              <button id="start" class="px-4 py-2 bg-green-600 text-white rounded">Start Playback</button>
              <button id="playTranscript" class="px-4 py-2 bg-white border rounded">Speak Transcript</button>
              <button id="playAdvice" class="px-4 py-2 bg-white border rounded">Speak Advice</button>
            </div>
          </header>

          <section class="grid grid-cols-3 gap-6">
            <div class="col-span-2 space-y-4">
              <div id="step-1" class="p-4 bg-white rounded shadow-sm">
                <h3 class="font-semibold">1) Incoming IVR</h3>
                <pre class="mt-2 text-sm bg-gray-900 text-white p-3 rounded max-h-36 overflow-auto">%%IVR%%</pre>
              </div>

              <div id="step-2" class="p-4 bg-white rounded shadow-sm">
                <h3 class="font-semibold">2) Language selection</h3>
                <pre class="mt-2 text-sm bg-gray-100 p-3 rounded">%%RECORD_PROMPT%%</pre>
              </div>

              <div id="step-3" class="p-4 bg-white rounded shadow-sm">
                <h3 class="font-semibold">3) Recording received</h3>
                <div class="mt-2 text-sm text-gray-700">Recording SID: <span class="font-mono">%%REC_SID%%</span></div>
                <div class="text-sm text-gray-700">URL: <span class="font-mono">{rec_url}</span></div>
                <div class="text-sm text-gray-700">Duration: <span class="font-mono">%%REC_DUR%%s</span></div>
              </div>

              <div id="step-4" class="p-4 bg-white rounded shadow-sm">
                <h3 class="font-semibold">4) Transcript</h3>
                <p class="mt-2 text-sm text-gray-800">%%TRANSCRIPT%%</p>
              </div>

            </div>

            <aside class="space-y-4">
              <div id="step-5" class="p-4 bg-white rounded shadow-sm">
                <h3 class="font-semibold">5) AI Advice</h3>
                <p class="mt-2 text-sm text-gray-700">%%ADVICE%%</p>
              </div>

              <div id="step-6" class="p-4 bg-white rounded shadow-sm">
                <h3 class="font-semibold">6) AI TwiML</h3>
                <pre class="mt-2 text-sm bg-gray-100 p-3 rounded max-h-48 overflow-auto">%%AI_TWIML%%</pre>
              </div>
            </aside>
          </section>
        </main>
      </div>

      <script>
        const stepEls = [
          document.getElementById('step-1'),
          document.getElementById('step-2'),
          document.getElementById('step-3'),
          document.getElementById('step-4'),
          document.getElementById('step-5'),
          document.getElementById('step-6')
        ];
        function clearActive(){ stepEls.forEach(e=>e.classList.remove('ring','ring-2','ring-green-300')); }

        document.getElementById('start').addEventListener('click', ()=>{
          let i=0; clearActive(); stepEls[0].classList.add('ring','ring-2','ring-green-300');
          const iv = setInterval(()=>{
            i++;
            if(i>=stepEls.length){ clearInterval(iv); return; }
            clearActive(); stepEls[i].classList.add('ring','ring-2','ring-green-300');
            if(i===3) speak(transcript);
            if(i===4) setTimeout(()=>speak(advice),600);
          }, 2200);
        });

        function speak(text){
          try{
            const u = new SpeechSynthesisUtterance(text);
            u.lang = 'en-IN';
            speechSynthesis.cancel();
            speechSynthesis.speak(u);
          }catch(e){ console.warn('speech error',e); }
        }

        document.getElementById('playTranscript').addEventListener('click', ()=>speak(transcript));
        document.getElementById('playAdvice').addEventListener('click', ()=>speak(advice));
      </script>
    </body>
    </html>
    """

    html = html_template.replace("%%CALLER%%", caller)
    html = html.replace("%%IVR%%", ivr)
    html = html.replace("%%RECORD_PROMPT%%", record_prompt)
    html = html.replace("%%REC_SID%%", rec_sid)
    html = html.replace("%%REC_DUR%%", str(rec_dur))
    html = html.replace("%%TRANSCRIPT%%", transcript)
    html = html.replace("%%ADVICE%%", advice)
    html = html.replace("%%AI_TWIML%%", ai_twiml)
    # inject safe JSON variables for JS
    html = html.replace('</script>', f'\n<script>const transcript = {js_transcript}; const advice = {js_advice};</script>\n</script>', 1)

    return HTMLResponse(content=html)

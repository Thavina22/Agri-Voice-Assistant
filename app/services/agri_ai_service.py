import os
import httpx
from typing import Optional
from app.config import settings

# System prompt for Gemini AI Agricultural Reasoning Engine
SYSTEM_PROMPT = (
    "You are an expert agricultural advisor for Indian farmers. "
    "Return concise practical advice. "
    "Always identify: 1 Disease 2 Possible Cause 3 Immediate Action 4 Prevention. "
    "Never hallucinate. "
    "If uncertain say 'Consult nearby agriculture officer.'"
)

# Localized fallback responses if Gemini API is unavailable or unconfigured
FALLBACK_RESPONSES = {
    "en-IN": (
        "Your crop issue has been recorded. "
        "Remove infected leaves, avoid overhead watering, and consult your local agriculture officer."
    ),
    "ta-IN": (
        "உங்கள் பயிர் பிரச்சனை பதிவு செய்யப்பட்டுள்ளது. "
        "பாதிக்கப்பட்ட இலைகளை அகற்றி, மேலிருந்து தண்ணீர் பாய்ச்சுவதை தவிர்த்து, "
        "விவசாய அலுவலரின் ஆலோசனையை பெறவும்."
    ),
    "te-IN": (
        "మీ పంట సమస్య నమోదు చేయబడింది. "
        "దెబ్బతిన్న ఆకులను తొలగించి, పై నుండి నీరు పోయకుండా ఉండండి. "
        "సమీప వ్యవసాయ అధికారిని సంప్రదించండి."
    ),
}


class AgriAIService:
    """Agricultural AI Advisory service powered by Google Gemini API with localized fallback."""

    @staticmethod
    def analyze_crop_issue(transcript: str, language: str = "en-IN") -> str:
        """
        Analyze farmer transcript and generate concise localized recommendation using Gemini.
        
        Args:
            transcript (str): Transcribed farmer speech.
            language (str): BCP-47 language code ('en-IN', 'ta-IN', 'te-IN').
            
        Returns:
            str: Localized advice in the farmer's selected language.
        """
        # Prefer Claude if configured, else Gemini, else fallback
        claude_key = settings.CLAUDE_API_KEY or os.getenv("CLAUDE_API_KEY", "")
        gemini_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")

        if claude_key and not claude_key.startswith("YOUR_"):
            try:
                return AgriAIService._call_claude_api(transcript, language, claude_key)
            except Exception as err:
                print(f"[AgriAI Service Error]: Claude API call failed - {err}")

        if gemini_key and not gemini_key.startswith("YOUR_"):
            try:
                return AgriAIService._call_gemini_api(transcript, language, gemini_key)
            except Exception as err:
                print(f"[AgriAI Service Error]: Gemini API call failed - {err}")

        return AgriAIService._get_fallback_response(language)

    @staticmethod
    def _call_gemini_api(transcript: str, language: str, api_key: str) -> str:
        """Make synchronous/blocking HTTP request to Google Gemini API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        prompt_text = (
            f"{SYSTEM_PROMPT}\n\n"
            f"Target Response Language: {language}\n"
            f"Farmer Spoken Query: \"{transcript}\"\n\n"
            f"Provide advice in {language} language."
        )

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt_text}]
                }
            ]
        }

        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return parts[0]["text"].strip()

        return AgriAIService._get_fallback_response(language)

    @staticmethod
    def _call_claude_api(transcript: str, language: str, api_key: str) -> str:
        """Call Anthropic Claude API (HTTP) to produce a localized advice string.

        Uses a conservative completion call; falls back on failure.
        """
        # Build a concise prompt targeted at Claude
        system = (
            "You are an expert agricultural advisor for Indian farmers. "
            "Return concise practical advice. Always identify: 1 Disease 2 Possible Cause 3 Immediate Action 4 Prevention. "
            "Answer in the target language requested."
        )

        prompt_text = f"{system}\n\nTarget Response Language: {language}\nFarmer Spoken Query: \"{transcript}\"\n\nProvide advice in {language}."

        url = "https://api.anthropic.com/v1/complete"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "claude-2.1",
            "prompt": prompt_text,
            "max_tokens_to_sample": 512,
            "temperature": 0.2
        }

        with httpx.Client(timeout=15.0) as client:
            resp = client.post(url, json=payload, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                # Anthropic returns 'completion' or 'completion' keys depending on model
                text = data.get("completion") or data.get("completion_text") or data.get("output")
                if isinstance(text, str):
                    return text.strip()

        return AgriAIService._get_fallback_response(language)

    @staticmethod
    def _get_fallback_response(language: str) -> str:
        """Return localized safe fallback advice."""
        return FALLBACK_RESPONSES.get(language, FALLBACK_RESPONSES["en-IN"])
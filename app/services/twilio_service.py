from twilio.twiml.voice_response import VoiceResponse, Gather

LANGUAGES = {
    "1": {
        "name": "Tamil",
        "code": "ta-IN",
        "voice": "Polly.Valluvar",
        "prompt": "நீங்கள் தமிழைத் தேர்ந்தெடுத்துள்ளீர்கள். பீப் ஒலிக்குப் பிறகு உங்கள் பயிர் பிரச்சனையை விவரிக்கவும்.",
        "received": "உங்கள் பதிவு பெறப்பட்டது. பகுப்பாய்வு செய்யப்படுகிறது."
    },
    "2": {
        "name": "English",
        "code": "en-IN",
        "voice": "Polly.Aditi",
        "prompt": "You have selected English. Please describe your crop issue after the tone.",
        "received": "Thank you. Your recording has been received and is being analyzed."
    },
    "3": {
        "name": "Telugu",
        "code": "te-IN",
        "voice": "Polly.Aditi",
        "prompt": "మీరు తెలుగును ఎంచుకున్నారు. బీప్ తర్వాత మీ పంట సమస్యను వివరించండి.",
        "received": "మీ రికార్డింగ్ స్వీకరించబడింది. విశ్లేషించబడుతోంది."
    }
}


class TwilioService:
    """
    Twilio TwiML generator for:
    - Language IVR
    - Recording
    - AI voice response
    """

    @staticmethod
    def build_ivr_menu_twiml(
        action_url: str = "/api/v1/voice/language"
    ) -> str:

        response = VoiceResponse()

        gather = Gather(
            action=action_url,
            method="POST",
            num_digits=1,
            timeout=8
        )

        gather.say(
            "Welcome to AI Agriculture Assistant.",
            voice="Polly.Aditi",
            language="en-IN"
        )

        gather.say(
            "தமிழுக்கு 1 அழுத்தவும். Press 1 for Tamil.",
            voice="Polly.Aditi",
            language="en-IN"
        )

        gather.say(
            "Press 2 for English.",
            voice="Polly.Aditi",
            language="en-IN"
        )

        gather.say(
            "తెలుగు కోసం 3 నొక్కండి. Press 3 for Telugu.",
            voice="Polly.Aditi",
            language="en-IN"
        )

        response.append(gather)

        response.say(
            "We did not receive your selection.",
            voice="Polly.Aditi",
            language="en-IN"
        )

        response.redirect(
            "/api/v1/voice/incoming",
            method="POST"
        )

        return str(response)


    @staticmethod
    def build_recording_prompt_twiml(
        digits: str
    ) -> str:

        response = VoiceResponse()

        lang_info = LANGUAGES.get(digits)

        if not lang_info:
            response.say(
                "Invalid selection. Please try again.",
                voice="Polly.Aditi",
                language="en-IN"
            )

            response.redirect(
                "/api/v1/voice/incoming",
                method="POST"
            )

            return str(response)


        response.say(
            lang_info["prompt"],
            voice=lang_info["voice"],
            language=lang_info["code"]
        )


        record_action = (
            f"/api/v1/voice/recording?lang={lang_info['code']}"
        )


        response.record(
            action=record_action,
            method="POST",
            timeout=5,
            max_length=30,
            play_beep=True,
            trim="trim-silence"
        )


        return str(response)



    @staticmethod
    def build_recording_received_twiml(
        lang_code: str = "en-IN"
    ) -> str:

        response = VoiceResponse()

        lang_config = next(
            (
                v for v in LANGUAGES.values()
                if v["code"] == lang_code
            ),
            LANGUAGES["2"]
        )


        response.say(
            lang_config["received"],
            voice=lang_config["voice"],
            language=lang_config["code"]
        )


        return str(response)



    @staticmethod
    def build_ai_response_twiml(
        message: str,
        lang_code: str = "en-IN"
    ) -> str:
        """
        Generate TwiML response for AI agriculture advice.
        Farmer hears the AI generated solution.
        """

        response = VoiceResponse()


        lang_config = next(
            (
                v for v in LANGUAGES.values()
                if v["code"] == lang_code
            ),
            LANGUAGES["2"]
        )


        response.say(
            message,
            voice=lang_config["voice"],
            language=lang_config["code"]
        )


        return str(response)
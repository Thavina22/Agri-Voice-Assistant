class AgriAIService:

    @staticmethod
    def analyze_crop_issue(transcript: str, language: str):

        advice = {
            "en-IN": (
                "Your tomato plant may have a fungal infection. "
                "Remove affected leaves and monitor the crop."
            ),

            "te-IN": (
                "మీ టమోటా మొక్కలో ఫంగస్ సమస్య ఉండవచ్చు. "
                "ప్రభావిత ఆకులను తొలగించి పంటను గమనించండి."
            ),

            "ta-IN": (
                "உங்கள் தக்காளி செடியில் பூஞ்சை தொற்று இருக்கலாம். "
                "பாதிக்கப்பட்ட இலைகளை அகற்றி கண்காணிக்கவும்."
            )
        }

        return advice.get(
            language,
            advice["en-IN"]
        )
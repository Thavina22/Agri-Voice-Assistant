"""
Agriculture AI Service
----------------------
Performs a simple rule-based diagnosis based on the farmer's transcript.
Can later be replaced with Groq + RAG without changing the API.
"""


class AgriAIService:
    """Simple Agriculture AI analysis service."""

    @staticmethod
    def analyze_crop_issue(transcript: str, language: str) -> str:
        """
        Analyze the farmer's crop issue and return advice.

        Args:
            transcript: Speech-to-text output.
            language: Language code (en-IN, ta-IN, te-IN)

        Returns:
            Localized agriculture advice.
        """

        text = transcript.lower()

        # --------------------------------------------------
        # Tomato Disease
        # --------------------------------------------------

        if any(
            keyword in text
            for keyword in [
                "tomato",
                "தக்காளி",
                "టమోటా"
            ]
        ):

            responses = {
                "en-IN": (
                    "Your tomato crop may be affected by a fungal leaf spot disease. "
                    "Remove infected leaves, avoid overhead irrigation, and apply a "
                    "recommended fungicide after consulting your local agriculture officer."
                ),

                "ta-IN": (
                    "உங்கள் தக்காளி செடியில் பூஞ்சை நோய் இருக்கலாம். "
                    "பாதிக்கப்பட்ட இலைகளை அகற்றி, மேலிருந்து தண்ணீர் பாய்ச்சுவதை தவிர்த்து, "
                    "விவசாய அலுவலரின் ஆலோசனையுடன் பூஞ்சைநாசினி பயன்படுத்துங்கள்."
                ),

                "te-IN": (
                    "మీ టమోటా పంటకు ఫంగస్ సమస్య ఉండవచ్చు. "
                    "దెబ్బతిన్న ఆకులను తొలగించి, పై నుండి నీరు పోయకుండా ఉండండి. "
                    "వ్యవసాయ అధికారుల సలహాతో ఫంగిసైడ్ ఉపయోగించండి."
                ),
            }

            return responses.get(language, responses["en-IN"])

        # --------------------------------------------------
        # Default Advice
        # --------------------------------------------------

        default_response = {
            "en-IN": (
                "Thank you. Your crop issue has been recorded. "
                "Please consult your nearest agriculture officer if the problem continues."
            ),

            "ta-IN": (
                "நன்றி. உங்கள் பயிர் பிரச்சனை பதிவு செய்யப்பட்டுள்ளது. "
                "பிரச்சனை தொடர்ந்தால் அருகிலுள்ள விவசாய அலுவலரை அணுகவும்."
            ),

            "te-IN": (
                "ధన్యవాదాలు. మీ పంట సమస్య నమోదు చేయబడింది. "
                "సమస్య కొనసాగితే సమీప వ్యవసాయ అధికారిని సంప్రదించండి."
            ),
        }

        return default_response.get(language, default_response["en-IN"])
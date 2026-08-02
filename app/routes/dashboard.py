from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard Telemetry"])


@router.get("/summary")
def get_dashboard_summary():
    """Summary metrics for Dashboard cards."""
    return {
        "total_calls": 1248,
        "weekly_growth": 18.4,
        "ai_resolution_rate": 94.8,
        "human_kvk_escalations": 6,
        "supported_crops_count": 3,
        "supported_crops": ["Tomato", "Paddy", "Chilli"],
        "top_language": "Tamil",
        "language_distribution": {
            "Tamil": 52,
            "English": 32,
            "Telugu": 16
        }
    }


@router.get("/history")
def get_consultation_history():
    """Consultation telemetry logs."""
    return [
        {
            "id": "CALL_101",
            "phone": "+91 98765 43210",
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Tomato",
            "symptoms": "Dark brown spots with target-like concentric rings on lower leaves",
            "diagnosis": "Early Blight",
            "pathogen": "Alternaria solani",
            "confidence": 96,
            "lang": "Tamil",
            "status": "Completed",
            "transcript": "என் தக்காளி இலையில் கருப்பு புள்ளிகள் மற்றும் மஞ்சள் நிற வளையங்கள் உள்ளன."
        },
        {
            "id": "CALL_102",
            "phone": "+91 91234 56789",
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Paddy",
            "symptoms": "Spindle-shaped lesions with grayish center on leaves",
            "diagnosis": "Blast Disease",
            "pathogen": "Magnaporthe oryzae",
            "confidence": 91,
            "lang": "English",
            "status": "Completed",
            "transcript": "My paddy crop has spindle-shaped lesions with grayish center on leaves."
        },
        {
            "id": "CALL_103",
            "phone": "+91 99887 76655",
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            "crop": "Chilli",
            "symptoms": "White powdery growth on lower leaf surface",
            "diagnosis": "Powdery Mildew",
            "pathogen": "Leveillula taurica",
            "confidence": 64,
            "lang": "Telugu",
            "status": "KVK Escalated",
            "transcript": "మిరప ఆకులపై తెల్లటి పొడి కనిపిస్తుంది."
        }
    ]


@router.get("/weather")
def get_dashboard_weather():
    """Regional weather telemetry & fungal risk alerts."""
    return {
        "region": "South India Agricultural Belt",
        "temperature": 29,
        "humidity": 84,
        "wind_speed": 12,
        "soil_moisture": 68,
        "risk_level": "High Humidity Risk",
        "alert_title": "Late Blight Outbreak Warning",
        "alert_message": "High atmospheric humidity (>80%) increases Late Blight risk in Tomato crops. Inspect lower leaves for white fungal growth."
    }


@router.get("/market")
def get_market_prices():
    """APMC Mandi commodity rates."""
    return [
        {
            "commodity": "Tomato (Hybrid)",
            "market": "Madanapalle APMC",
            "price": "₹2,400 / quintal",
            "trend": "+5.2%",
            "is_up": True
        },
        {
            "commodity": "Paddy (Samba Mahsuri)",
            "market": "Thanjavur Mandi",
            "price": "₹2,180 / quintal",
            "trend": "+1.8%",
            "is_up": True
        },
        {
            "commodity": "Chilli (Teja Variety)",
            "market": "Guntur APMC",
            "price": "₹18,500 / quintal",
            "trend": "-0.9%",
            "is_up": False
        }
    ]


@router.get("/schemes")
def get_government_schemes():
    """Government assistance schemes."""
    return [
        {
            "name": "PM-KISAN Samman Nidhi",
            "desc": "₹6,000 annual direct income support for farmer households.",
            "status": "Active Installment",
            "tag": "Financial"
        },
        {
            "name": "PM Fasal Bima Yojana (PMFBY)",
            "desc": "Comprehensive crop insurance against disease outbreaks and natural perils.",
            "status": "Kharif Enrollment",
            "tag": "Insurance"
        },
        {
            "name": "Soil Health Card Scheme",
            "desc": "Free soil testing & NPK nutrient recommendations.",
            "status": "Free Testing",
            "tag": "Nutrients"
        }
    ]


@router.get("/knowledge")
def get_knowledge_summary():
    """MVP crop disease matrices."""
    return {
        "total_mvp_diseases": 9,
        "crops": [
          {
            "name": "Tomato",
            "health": "Moderate Risk",
            "variant": "warning",
            "active_disease": "Early Blight (42%)",
            "total_consultations": 580,
            "diseases": ["Early Blight", "Late Blight", "Leaf Curl Virus"]
          },
          {
            "name": "Paddy",
            "health": "Good Condition",
            "variant": "success",
            "active_disease": "Blast Disease (28%)",
            "total_consultations": 420,
            "diseases": ["Blast Disease", "Brown Spot", "Stem Borer"]
          },
          {
            "name": "Chilli",
            "health": "Watch Alert",
            "variant": "warning",
            "active_disease": "Powdery Mildew (35%)",
            "total_consultations": 248,
            "diseases": ["Anthracnose", "Powdery Mildew", "Aphids Infestation"]
          }
        ]
    }


@router.get("/ai-status")
def get_ai_status():
    """AI engine telemetry and latency."""
    return {
        "status": "Operational",
        "rca_engine_latency": "0.05s",
        "groq_llama3_latency": "0.82s",
        "tts_engine": "Online (Polly Voices)",
        "active_models": ["Llama 3 70B (Groq Cloud)", "FastAPI RCA Engine"]
    }

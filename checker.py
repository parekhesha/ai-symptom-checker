import os
from groq import Groq
from dotenv import load_dotenv
from symptoms_data import EMERGENCY_SYMPTOMS

load_dotenv(override=True)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def check_emergency(symptoms: list) -> bool:
    return any(s.lower() in EMERGENCY_SYMPTOMS for s in symptoms)

def analyze_symptoms(symptoms: list, age: int, gender: str) -> dict:
    if check_emergency(symptoms):
        return {
            "severity": "EMERGENCY",
            "message": "⚠️ Call emergency services immediately!",
            "advice": "Do not wait — seek help now."
        }

    prompt = f"""
    Patient Info:
    - Age: {age}
    - Gender: {gender}
    - Symptoms: {', '.join(symptoms)}

    Analyze these symptoms and provide:
    1. Possible conditions (top 3)
    2. Severity level (mild/moderate/severe)
    3. Recommended action
    4. Warning signs to watch for

    Always recommend consulting a real doctor.
    """

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant. Always advise users to consult a real doctor."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )

    return {
        "severity": "analyzed",
        "analysis": response.choices[0].message.content,
        "disclaimer": "⚕️ This is not a substitute for professional medical advice."
    }
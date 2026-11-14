import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)


def check_safety(patient_concern: str) -> str:
    """
    Analyzes the patient's described concern for emergency red flags.
    Acts as the mandatory Safety Gate.
    """
    prompt = f"""
    You are a hospital Safety Gate Agent. Your sole job is to analyze this patient concern for emergency red flags 
    (such as chest pain, severe bleeding, breathing difficulty, stroke signs, loss of consciousness, or sudden trauma):
    
    "{patient_concern}"
    
    Rules:
    - If it sounds urgent or life-threatening, set URGENT to true and provide an immediate in-person emergency advisory.
    - If it is routine/non-urgent, set URGENT to false and set ADVISORY to None.
    - In case of emergency provide short helpline numbers (112 or 108).
    - Never diagnose any disease.
    
    Output strictly in this format:
    URGENT: [true/false]
    ADVISORY: [Your advice or "None"]
    """
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return completion.choices[0].message.content.strip()
    except Exception:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return completion.choices[0].message.content.strip()


def is_emergency(safety_response: str) -> bool:
    """Helper to detect if safety check flagged an emergency."""
    if not safety_response:
        return False
    lower = safety_response.lower()
    for line in lower.splitlines():
        if "urgent:" in line:
            return "true" in line
    return "urgent: true" in lower or ("urgent" in lower and "true" in lower)


if __name__ == "__main__":
    print("--- Test 1 (Emergency) ---")
    res1 = check_safety("I am having severe crushing chest pain and shortness of breath.")
    print(res1)
    
    print("\n--- Test 2 (Routine) ---")
    res2 = check_safety("My knee has been slightly stiff when I walk for two days.")
    print(res2)

import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)


def route_patient(structured_concern: str) -> str:
    """
    Triage Router Agent: Maps the patient concern to the correct hospital department.
    Strictly prohibits any medical diagnosis.
    """
    prompt = f"""
    You are an expert Hospital Triage Router Agent. 
    Analyze this patient concern/intake summary:
    "{structured_concern}"
    
    Your job is ONLY to map this to the correct hospital department (e.g., Orthopaedics, General Medicine, ENT, Dermatology, Ophthalmology, Cardiology, Neurology, Gastroenterology).
    
    CRITICAL RULES:
    - Never diagnose any disease or condition.
    - Output strictly in this format:
    DEPARTMENT: [Name of Department]
    RATIONALE: [One short sentence explaining why, without naming a disease]
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


def extract_department(triage_output: str, fallback_department: str = "General Medicine") -> str:
    for line in triage_output.splitlines():
        if "DEPARTMENT:" in line:
            dept = line.split("DEPARTMENT:", 1)[1].strip()
            dept = dept.replace("[", "").replace("]", "").strip()
            if dept:
                return dept
    return fallback_department


if __name__ == "__main__":
    test_concern = "Sharp pain in right knee and difficulty climbing stairs."
    print("--- Testing Triage Router Agent ---")
    print(route_patient(test_concern))

import os
from groq import Groq

client = Groq(api_key="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")

def route_patient(structured_concern: str):
    """
    Triage Router Agent: Maps the patient concern to the correct hospital department.
    Strictly prohibits any medical diagnosis.
    """
    prompt = f"""
    You are an expert Hospital Triage Router Agent. 
    Analyze this patient concern/intake summary:
    "{structured_concern}"
    
    Your job is ONLY to map this to the correct hospital department (e.g., Orthopaedics, General Medicine, ENT, Dermatology, Ophthalmology, Cardiology).
    
    CRITICAL RULES:
    - Never diagnose any disease or condition.
    - Output strictly in this format:
    DEPARTMENT: [Name of Department]
    RATIONALE: [One short sentence explaining why, without naming a disease]
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    test_concern = "Sharp pain in right knee and difficulty climbing stairs."
    print("--- Testing Triage Router Agent ---")
    print(route_patient(test_concern))
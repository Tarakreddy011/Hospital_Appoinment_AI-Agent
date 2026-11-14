import os
from groq import Groq

# Directly pass your API key as a string to avoid environment issues
client = Groq(api_key="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")


def check_safety(patient_concern: str):
    """
    Analyzes the patient's described concern for emergency red flags.
    Acts as the mandatory Safety Gate.
    """
    
    # 1. Define the system/user prompt instructions restricting the LLM to safety evaluation only
    prompt = f"""
    You are a hospital Safety Gate Agent. Your sole job is to analyze this patient concern for emergency red flags 
    (such as chest pain, severe bleeding, breathing difficulty, stroke signs, or sudden trauma):
    
    "{patient_concern}"
    
    Rules:
    - If it sounds urgent or life-threatening, set URGENT to true and provide an immediate in-person emergency advisory.
    - If it is routine/non-urgent, set URGENT to false and set ADVISORY to None.
    - If incase emergency give helpline numbers very short
    - Never diagnose any disease.
    - Incase of Emergency Use Indian Emergency services such as 112 or 108.
    
    Output strictly in this format:
    URGENT: [true/false]
    ADVISORY: [Your advice or "None"]
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    # Return the exact text content
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("--- Test 1 (Emergency) ---")
    res1 = check_safety("I am having severe crushing chest pain and shortness of breath.")
    print(res1)
    
    print("\n--- Test 2 (Routine) ---")
    res2 = check_safety("My knee has been slightly stiff when I walk for two days.")
    print(res2)
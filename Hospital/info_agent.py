import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

# Local Hospital Knowledge Base (Simulating RAG source documents)
HOSPITAL_KB = {
    "Orthopaedics": "Department: Orthopaedics. Intake Instructions: Please arrive 15 minutes prior to your slot. Wear loose clothing around joints. What to bring: Government Photo ID, previous X-ray or MRI scans, list of current medications.",
    "General Medicine": "Department: General Medicine. Intake Instructions: Fasting may be required if routine blood tests are ordered. Arrive 10 minutes early. What to bring: Government Photo ID, previous prescription records, health insurance card.",
    "ENT": "Department: Ear, Nose, and Throat (ENT). Intake Instructions: Avoid using nasal sprays or ear drops 4 hours prior to consultation. What to bring: Government Photo ID, previous audiology reports if any.",
    "Cardiology": "Department: Cardiology. Intake Instructions: Avoid caffeine and heavy exercise 2 hours before your appointment. What to bring: Government Photo ID, past ECG or heart reports, current medication list.",
    "Dermatology": "Department: Dermatology. Intake Instructions: Avoid applying cosmetic lotions or creams on affected skin on the day of appointment. What to bring: Government Photo ID, prior skin test reports.",
    "Ophthalmology": "Department: Ophthalmology. Intake Instructions: Arrive 15 minutes early. Dilating eye drops may cause temporary blurriness; arrange for an accompanist. What to bring: Government Photo ID, current prescription glasses.",
    "Neurology": "Department: Neurology. Intake Instructions: Arrive 15 minutes prior to your slot. Ensure adequate rest prior night. What to bring: Government Photo ID, past MRI/CT scans, symptom diary.",
    "Gastroenterology": "Department: Gastroenterology. Intake Instructions: Fast for 6 hours if abdominal ultrasound is planned. What to bring: Government Photo ID, past endoscopy or ultrasound reports."
}


def get_department_info(department_name: str) -> str:
    """
    Information Agent: Performs RAG over the hospital knowledge base 
    to retrieve intake instructions and required items for the routed department.
    """
    dept_doc = None
    for k in HOSPITAL_KB:
        if k.lower() in department_name.lower():
            dept_doc = HOSPITAL_KB[k]
            break
            
    if not dept_doc:
        dept_doc = f"Department: {department_name}. Intake Instructions: Arrive 10 minutes early. Register at reception. What to bring: Government Photo ID, medical records, insurance card."
    
    prompt = f"""
    You are a helpful Hospital Information Agent. Based on the retrieved department documentation below, 
    generate a clear, polite, and structured summary for the patient telling them what instructions to follow and what to bring.
    
    Retrieved Document:
    "{dept_doc}"
    
    Format nicely with headings:
    - INTAKE INSTRUCTIONS:
    - WHAT TO BRING:
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


if __name__ == "__main__":
    print("--- Testing Information Agent (RAG) ---")
    print(get_department_info("ENT"))

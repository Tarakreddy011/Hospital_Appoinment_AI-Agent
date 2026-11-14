import os
from groq import Groq

client = Groq(api_key="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")

# Local Hospital Knowledge Base (Simulating RAG source documents)
HOSPITAL_KB = {
    "Orthopaedics": "Department: Orthopaedics. Intake Instructions: Please arrive 15 minutes prior to your slot. Wear loose clothing around joints. What to bring: Government ID, previous X-ray or MRI scans, list of current medications.",
    "General Medicine": "Department: General Medicine. Intake Instructions: Fasting may be required if blood tests are ordered. Arrive 10 minutes early. What to bring: Government ID, previous prescription records, insurance card.",
    "ENT": "Department: Ear, Nose, and Throat (ENT). Intake Instructions: Avoid using nasal sprays or ear drops 4 hours prior to consultation. What to bring: Government ID, previous audiology reports if any.",
    "Cardiology": "Department: Cardiology. Intake Instructions: Avoid caffeine and heavy exercise 2 hours before your appointment. What to bring: Government ID, past ECG or heart reports, current medication list."
}

def get_department_info(department_name: str):
    """
    Information Agent: Performs RAG over the hospital knowledge base 
    to retrieve intake instructions and required items for the routed department.
    """
    # 1. Retrieve the document matching the department (or default if not found)
    dept_doc = HOSPITAL_KB.get(department_name, "Department: General Care. Intake Instructions: Arrive 10 minutes early. What to bring: Government ID and medical records.")
    
    # 2. Use Groq to format and present the information clearly to the patient
    prompt = f"""
    You are a helpful Hospital Information Agent. Based on the retrieved department documentation below, 
    generate a clear, polite, and structured summary for the patient telling them what instructions to follow and what to bring.
    
    Retrieved Document:
    "{dept_doc}"
    
    Format nicely with headings:
    - INTAKE INSTRUCTIONS:
    - WHAT TO BRING:
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("--- Testing Information Agent (RAG) ---")
    print(get_department_info("ENT"))
import os
from groq import Groq

try:
    from sqlconnections import get_patient_last_visit, insert_patient_record
except ImportError:
    from Hospital.sqlconnections import get_patient_last_visit, insert_patient_record


#TODO
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)


def run_intake_agent(name: str, phone: str, current_concern: str) -> str:
    """
    Intake Agent: Combines database memory check (returning patient history) 
    with Groq LLM reasoning to generate a structured patient intake record.
    """
    # 1. Memory Check: Query database for prior visits
    previous_visit = get_patient_last_visit(phone)
    
    if previous_visit:
        history_context = (
            f"Returning Patient! Last visit: {previous_visit.get('visit_date', 'N/A')}, "
            f"Routed Department: {previous_visit.get('routed_department', 'N/A')}, "
            f"Prior Concern: {previous_visit.get('last_concern', 'N/A')}"
        )
    else:
        history_context = "No previous records found. New patient."
    
    # 2. LLM Reasoning/Agent Promp
    prompt = f"""
    You are an intelligent Hospital Intake Agent. Your job is to process patient check-in details and historical memory to create a clean intake summary.
    
    Patient Name: {name}
    Phone: {phone}
    Current Concern: {current_concern}
    Patient History Memory: {history_context}
    
    Generate a structured intake ticket containing:
    - PATIENT_NAME: 
    - STATUS: (New or Returning)
    - MEMORY_SUMMARY: (Briefly mention prior visit if returning)
    - STRUCTURED_CONCERN: (A clean, professional phrasing of the current concern for the triage router)
    """
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        agent_output = completion.choices[0].message.content.strip()
    except Exception:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        agent_output = completion.choices[0].message.content.strip()
    
    # 3. Save this new visit to database
    insert_patient_record(name, phone, current_concern, "Pending Triage")
    
    return agent_output


def extract_structured_concern(intake_output: str, fallback_concern: str) -> str:
    for line in intake_output.splitlines():
        if "STRUCTURED_CONCERN:" in line:
            clean = line.split("STRUCTURED_CONCERN:", 1)[1].strip()
            if clean:
                return clean
    return fallback_concern


if __name__ == "__main__":
    print("--- Testing Intake Agent ---")
    print(run_intake_agent("Rahul Sharma", "9876543210", "Sharp pain in right knee when climbing stairs"))

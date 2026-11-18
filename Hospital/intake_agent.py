import re
from typing import Optional
try:
    from sqlconnections import get_patient_last_visit, insert_patient_record
except ImportError:
    from Hospital.sqlconnections import get_patient_last_visit, insert_patient_record
from groq_client import call_groq_chat


def run_intake_agent(
    name: str,
    phone: str,
    current_concern: str,
    age: Optional[int] = None,
    sex: Optional[str] = None,
    weight: Optional[float] = None,
    height: Optional[float] = None
) -> str:
    """
    Intake Agent: Combines database memory check (returning patient history)
    with patient vitals and Groq LLM clinical reasoning to generate a structured intake record.
    """
    # 1. Database Memory Check
    previous_visit = get_patient_last_visit(phone)

    if previous_visit:
        history_context = (
            f"Returning Patient! Prior visit: {previous_visit.get('visit_date', 'N/A')}, "
            f"Prior Clinic: {previous_visit.get('routed_department', 'N/A')}, "
            f"Prior Concern: {previous_visit.get('last_concern', 'N/A')}"
        )
    else:
        history_context = "No previous hospital visits recorded. New patient."

    # 2. Vitals & Demographics Formatting
    vitals_parts = []
    bmi_val = None
    if age is not None:
        vitals_parts.append(f"Age: {age} yrs")
    if sex:
        vitals_parts.append(f"Sex: {sex}")
    if weight is not None:
        vitals_parts.append(f"Weight: {weight} kg")
    if height is not None:
        vitals_parts.append(f"Height: {height} cm")
    if weight and height and height > 0:
        bmi_val = round(float(weight) / ((float(height) / 100.0) ** 2), 1)
        vitals_parts.append(f"BMI: {bmi_val}")

    vitals_text = ", ".join(vitals_parts) if vitals_parts else "Not provided"

    # 3. Groq Agent LLM Reasoning
    prompt = f"""
    You are an intelligent Hospital Intake Clinical Agent.
    Your job is to process patient registration details, vitals, and historical memory to produce a professional, structured clinical intake ticket.

    PATIENT DETAILS:
    - Full Name: {name}
    - Phone: {phone}
    - Demographics & Vitals: {vitals_text}
    - Described Symptoms / Concern: "{current_concern}"
    - Electronic Health Record Memory: {history_context}

    INSTRUCTIONS:
    - Synthesize all symptoms accurately into a clean, professional clinical description.
    - If the patient has multi-system symptoms (e.g., blurry vision, hallucinations, tachycardia, disorientation, breathing problem), retain ALL of them clearly in the STRUCTURED_CONCERN so the triage router does not lose diagnostic context.

    OUTPUT FORMAT:
    PATIENT_NAME: {name}
    STATUS: {"Returning" if previous_visit else "New"}
    VITALS: {vitals_text}
    MEMORY_SUMMARY: {history_context}
    STRUCTURED_CONCERN: [A clear, comprehensive clinical summary of the patient's concerns]
    """

    agent_output = call_groq_chat(prompt, temperature=0.0)

    if not agent_output:
        status_str = "Returning" if previous_visit else "New"
        agent_output = (
            f"PATIENT_NAME: {name}\n"
            f"STATUS: {status_str}\n"
            f"VITALS: {vitals_text}\n"
            f"MEMORY_SUMMARY: {history_context}\n"
            f"STRUCTURED_CONCERN: {current_concern.strip()}"
        )

    # 4. Save new intake to database
    try:
        insert_patient_record(
            name=name,
            phone=phone,
            concern=current_concern,
            department="Pending Triage",
            age=age,
            sex=sex,
            weight=weight,
            height=height
        )
    except Exception as e:
        print(f"[IntakeAgent] Warning: Could not log pending triage to DB: {e}")

    return agent_output


def extract_structured_concern(intake_output: str, fallback_concern: str) -> str:
    for line in intake_output.splitlines():
        if "STRUCTURED_CONCERN:" in line.upper():
            clean = line.split(":", 1)[1].strip()
            clean = clean.replace("[", "").replace("]", "").strip()
            if clean:
                return clean
    return fallback_concern

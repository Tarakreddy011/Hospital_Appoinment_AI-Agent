import os
import sys
import re
# ALL OK
if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from safety_agent import check_safety, is_emergency
from intake_agent import run_intake_agent, extract_structured_concern
from triage_agent import route_patient, extract_department
from info_agent import get_department_info, get_structured_dept_info
from appointment_agent import book_appointment, get_slots_for_department
from sqlconnections import get_patient_last_visit


def extract_rationale(triage_text: str) -> str:
    for line in triage_text.splitlines():
        if "RATIONALE:" in line:
            clean = line.split("RATIONALE:", 1)[1].strip()
            clean = clean.replace("[", "").replace("]", "").strip()
            if clean:
                return clean
    return triage_text


def clean_emergency_advisory(safety_text: str) -> str:
    """Strips raw backend tags from emergency advisory for patient-facing view."""
    if not safety_text:
        return "Immediate emergency medical care required. Call emergency services."
    lines = []
    for line in safety_text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Skip raw URGENT tag
        if re.match(r"^URGENT:\s*(true|false)", line, re.IGNORECASE):
            continue
        # Strip ADVISORY tag
        if re.match(r"^ADVISORY:\s*", line, re.IGNORECASE):
            cleaned = re.sub(r"^ADVISORY:\s*", "", line, flags=re.IGNORECASE).strip()
            if cleaned and cleaned.lower() != "none":
                lines.append(cleaned)
            continue
        lines.append(line)
    
    result = " ".join(lines).strip()
    return result or "Please call emergency services (112 or 108) or report to the nearest hospital emergency room immediately."


def run_hospital_system(name: str, phone: str, patient_concern: str, chosen_slot: dict = None) -> dict:
    """
    Executes the 5-agent hospital routing and scheduling pipeline.
    Returns focused data structure for clean UI presentation.
    """
    logs = []
    
    def log(msg: str):
        try:
            print(msg)
        except Exception:
            print(msg.encode("ascii", errors="replace").decode("ascii"))
        logs.append(msg)
        
    log("==================================================")
    log(f"🏥 PATIENT ROUTING PIPELINE FOR: {name}")
    log("==================================================\n")
    
    # ----------------------------------------------------
    # STEP 1: SAFETY GATE AGENT
    # ----------------------------------------------------
    log("[1/5] Running Safety Gate Check...")
    safety_response = check_safety(patient_concern)
    log(safety_response)
    
    urgent = is_emergency(safety_response)
    
    if urgent:
        clean_advisory = clean_emergency_advisory(safety_response)
        log("\n🚨 CRITICAL EMERGENCY DETECTED! Halting standard routing.")
        return {
            "success": False,
            "is_urgent": True,
            "raw_safety": safety_response,
            "emergency_advice": clean_advisory,
            "helpline": "112 / 108",
            "logs": "\n".join(logs)
        }

    log("\n -> Safety check passed. Proceeding to intake...\n")
    
    # ----------------------------------------------------
    # STEP 2: INTAKE AGENT (with Database Memory Check)
    # ----------------------------------------------------
    previous_visit = get_patient_last_visit(phone)
    is_returning = bool(previous_visit)
    
    log("[2/5] Running Intake Agent & Database Memory Check...")
    intake_ticket = run_intake_agent(name, phone, patient_concern)
    log(intake_ticket)
    log("\n")
    
    structured_concern = extract_structured_concern(intake_ticket, fallback_concern=patient_concern)
    
    # ----------------------------------------------------
    # STEP 3: TRIAGE ROUTER AGENT
    # ----------------------------------------------------
    log("[3/5] Running Triage Router Agent...")
    triage_output = route_patient(structured_concern)
    log(triage_output)
    
    department = extract_department(triage_output, fallback_department="General Medicine")
    rationale = extract_rationale(triage_output)
    log(f"\n -> Routed to: {department} ({rationale})\n")
    
    # ----------------------------------------------------
    # STEP 4: INFORMATION AGENT (RAG)
    # ----------------------------------------------------
    log(f"[4/5] Running Information Agent (RAG for {department})...")
    info_output = get_department_info(department)
    structured_prep = get_structured_dept_info(department)
    log(info_output)
    log("\n")
    
    # ----------------------------------------------------
    # STEP 5: APPOINTMENT AGENT & AVAILABLE SLOTS
    # ----------------------------------------------------
    log(f"[5/5] Running Appointment Agent...")
    available_slots = get_slots_for_department(department)
    selected_slot = chosen_slot or available_slots[0]
    
    appointment_output = book_appointment(phone, department, selected_slot)
    log(appointment_output)
    
    log("\n==================================================")
    log("✅ ROUTING & APPOINTMENT COMPLETE")
    log("==================================================")
    
    return {
        "success": True,
        "is_urgent": False,
        "patient_name": name,
        "phone": phone,
        "is_returning": is_returning,
        "previous_visit": {
            "visit_date": str(previous_visit.get("visit_date", "N/A")) if previous_visit else "",
            "last_concern": previous_visit.get("last_concern", "") if previous_visit else "",
            "last_department": previous_visit.get("routed_department", "") if previous_visit else ""
        } if is_returning else None,
        "department": department,
        "rationale": rationale,
        "instructions": info_output,
        "structured_instructions": structured_prep,
        "booking_options": available_slots,
        "assigned_booking": appointment_output,
        "selected_slot": selected_slot,
        "logs": "\n".join(logs)
    }


if __name__ == "__main__":
    res = run_hospital_system(
        name="Tarak", 
        phone="6303641937", 
        patient_concern="Sharp pain in right knee when climbing stairs and swelling"
    )
    print(res)

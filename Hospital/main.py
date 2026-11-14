import os
import sys

# Windows UTF-8 console output safe-guard
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
from info_agent import get_department_info
from appointment_agent import book_appointment


def run_hospital_system(name: str, phone: str, patient_concern: str) -> dict:
    """
    Executes the complete 5-agent hospital routing and scheduling pipeline.
    
    Returns structured data for the frontend and execution logs.
    """
    logs = []
    
    def log(msg: str):
        try:
            print(msg)
        except Exception:
            print(msg.encode("ascii", errors="replace").decode("ascii"))
        logs.append(msg)
        
    log("==================================================")
    log(f"🏥 STARTING PATIENT ROUTING PIPELINE FOR: {name}")
    log("==================================================\n")
    
    # ----------------------------------------------------
    # STEP 1: SAFETY GATE AGENT
    # ----------------------------------------------------
    log("[1/5] Running Safety Gate Check...")
    safety_response = check_safety(patient_concern)
    log(safety_response)
    
    urgent = is_emergency(safety_response)
    
    if urgent:
        log("\n🚨 EMERGENCY DETECTED! Halting standard routing. Immediate care advised (Dial 112/108)!")
        return {
            "success": False,
            "is_urgent": True,
            "step_results": {
                "safety": safety_response,
                "intake": None,
                "triage": None,
                "department": None,
                "info": None,
                "appointment": None
            },
            "logs": "\n".join(logs)
        }

    log("\n -> Safety check passed. Proceeding to intake...\n")
    
    # ----------------------------------------------------
    # STEP 2: INTAKE AGENT (with Database Memory Check)
    # ----------------------------------------------------
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
    log(f"\n -> Routed successfully to: {department}\n")
    
    # ----------------------------------------------------
    # STEP 4: INFORMATION AGENT (RAG)
    # ----------------------------------------------------
    log(f"[4/5] Running Information Agent (RAG for {department})...")
    info_output = get_department_info(department)
    log(info_output)
    log("\n")
    
    # ----------------------------------------------------
    # STEP 5: APPOINTMENT AGENT
    # ----------------------------------------------------
    log(f"[5/5] Running Appointment Agent & Updating Database...")
    appointment_output = book_appointment(phone, department)
    log(appointment_output)
    
    log("\n==================================================")
    log("✅ PATIENT ROUTING & BOOKING COMPLETE")
    log("==================================================")
    
    return {
        "success": True,
        "is_urgent": False,
        "step_results": {
            "safety": safety_response,
            "intake": intake_ticket,
            "triage": triage_output,
            "department": department,
            "info": info_output,
            "appointment": appointment_output
        },
        "logs": "\n".join(logs)
    }


if __name__ == "__main__":
    result = run_hospital_system(
        name="Tarak", 
        phone="6303641937", 
        patient_concern="When i stand suddenly i feel mind block type also every morning very weak me also not able to sleep at night"
    )

import os
import sys
import re
from typing import Optional, Dict, Any

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
from triage_agent import route_patient, extract_department, extract_rationale, get_department_care_levels
from info_agent import get_department_info, get_structured_dept_info
from appointment_agent import book_appointment, get_slots_for_department
from sqlconnections import get_patient_last_visit


def run_hospital_system(
    name: str,
    phone: str,
    patient_concern: str,
    age: Optional[int] = None,
    sex: Optional[str] = None,
    weight: Optional[float] = None,
    height: Optional[float] = None,
    chosen_slot: Optional[dict] = None
) -> Dict[str, Any]:
    """
    Executes the 5-agent clinical triage, routing, and scheduling pipeline with vital-sign support
    and borderline emergency red-flag detection.
    """
    logs = []

    def log(msg: str):
        try:
            print(msg)
        except Exception:
            print(msg.encode("ascii", errors="replace").decode("ascii"))
        logs.append(msg)

    # Compute BMI if weight and height provided
    bmi = None
    if weight and height and height > 0:
        bmi = round(float(weight) / ((float(height) / 100.0) ** 2), 1)

    log("==================================================")
    log(f"🏥 CLINICAL PATIENT ROUTING PIPELINE FOR: {name.upper()}")
    log(f"   Demographics: Age={age or 'N/A'}, Sex={sex or 'N/A'}, Weight={weight or 'N/A'}kg, Height={height or 'N/A'}cm (BMI: {bmi or 'N/A'})")
    log("==================================================\n")

    # ----------------------------------------------------
    # STEP 1: SAFETY GATE AGENT
    # ----------------------------------------------------
    log("[1/5] Running Safety Gate Check...")
    safety_result = check_safety(
        patient_concern=patient_concern,
        age=age,
        sex=sex,
        weight=weight,
        height=height
    )

    is_crit = safety_result.get("is_critical", False)
    has_warn = safety_result.get("has_warning", False)
    matched_red_flags = safety_result.get("matched_red_flags", [])
    safety_advisory = safety_result.get("advisory", "")

    if is_crit:
        log("\n🚨 CRITICAL EMERGENCY DETECTED! Halting standard OPD appointment routing.")
        log(f"   Advisory: {safety_advisory}")
        return {
            "success": False,
            "is_urgent": True,
            "has_warning": True,
            "matched_red_flags": matched_red_flags,
            "emergency_advice": safety_advisory or "Critical symptoms detected. Immediate emergency medical intervention required.",
            "helpline": "112 / 108",
            "patient_name": name,
            "age": age,
            "sex": sex,
            "logs": "\n".join(logs)
        }

    if has_warn:
        log(f"⚠️ Red Flag Warning Detected ({', '.join(matched_red_flags)}). Flashing emergency advisory on screen.")
    else:
        log(" -> Routine safety check passed. Proceeding to intake...\n")

    # ----------------------------------------------------
    # STEP 2: INTAKE AGENT & DATABASE MEMORY CHECK
    # ----------------------------------------------------
    previous_visit = get_patient_last_visit(phone)
    is_returning = bool(previous_visit)

    log("[2/5] Running Intake Agent & Database Memory Check...")
    intake_ticket = run_intake_agent(
        name=name,
        phone=phone,
        current_concern=patient_concern,
        age=age,
        sex=sex,
        weight=weight,
        height=height
    )
    log(intake_ticket)
    log("\n")

    structured_concern = extract_structured_concern(intake_ticket, fallback_concern=patient_concern)

    # ----------------------------------------------------
    # STEP 3: TRIAGE ROUTER AGENT
    # ----------------------------------------------------
    log("[3/5] Running Triage Router Agent with Clinical Syndrome Evaluation...")
    triage_output = route_patient(
        structured_concern=structured_concern,
        age=age,
        sex=sex,
        weight=weight,
        height=height
    )
    log(triage_output)

    department = extract_department(
        triage_output,
        fallback_department="General Medicine",
        concern=structured_concern,
        age=age
    )
    rationale = extract_rationale(triage_output, department=department)
    care_levels = get_department_care_levels(department)
    log(f"\n -> Clinically Routed to: {department} ({rationale})")
    log(f"    Available Facilities: OPD={'✓' if care_levels.get('opd') else '✗'} | IPD={'✓' if care_levels.get('ipd') else '✗'} | ICU={'✓' if care_levels.get('icu') else '✗'}\n")

    # ----------------------------------------------------
    # STEP 4: INFORMATION AGENT (RAG Knowledge Base)
    # ----------------------------------------------------
    log(f"[4/5] Running Information Agent (RAG for {department})...")
    info_output = get_department_info(department)
    structured_prep = get_structured_dept_info(department)
    log("Retrieved department guidelines and what-to-bring instructions successfully.")
    log("\n")

    # ----------------------------------------------------
    # STEP 5: APPOINTMENT AGENT & AVAILABLE SLOTS
    # ----------------------------------------------------
    log(f"[5/5] Running Appointment Agent for {department}...")
    available_slots = get_slots_for_department(department)
    selected_slot = chosen_slot or available_slots[0]

    appointment_output = book_appointment(phone, department, selected_slot)
    log(appointment_output)

    # Multi-helpline directory for patient support
    helpline_numbers = [
        {"name": "National Emergency & Ambulance", "number": "112", "tel": "tel:112"},
        {"name": "Medical Emergency & Trauma", "number": "108", "tel": "tel:108"},
        {"name": "LifeCare Central Triage Desk", "number": "080-456-7890", "tel": "tel:0804567890"}
    ]

    log("\n==================================================")
    log("✅ CLINICAL ROUTING & APPOINTMENT COMPLETE")
    log("==================================================")

    return {
        "success": True,
        "is_urgent": False,
        "has_warning": has_warn,
        "matched_red_flags": matched_red_flags,
        "warning_advisory": safety_advisory,
        "emergency_helpline": "112 / 108" if has_warn else None,
        "helplines": helpline_numbers,
        "patient_name": name,
        "phone": phone,
        "age": age,
        "sex": sex,
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "is_returning": is_returning,
        "previous_visit": {
            "visit_date": str(previous_visit.get("visit_date", "N/A")) if previous_visit else "",
            "last_concern": previous_visit.get("last_concern", "") if previous_visit else "",
            "last_department": previous_visit.get("routed_department", "") if previous_visit else ""
        } if is_returning else None,
        "department": department,
        "rationale": rationale,
        "care_levels": care_levels,
        "instructions": info_output,
        "structured_instructions": structured_prep,
        "booking_options": available_slots,
        "assigned_booking": appointment_output,
        "selected_slot": selected_slot,
        "logs": "\n".join(logs)
    }

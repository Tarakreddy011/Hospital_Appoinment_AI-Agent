# Import all individual agent modules
from safety_agent import check_safety
from intake_agent import run_intake_agent
from triage_agent import route_patient
from info_agent import get_department_info
from appointment_agent import book_appointment

def run_hospital_system(name: str, phone: str, patient_concern: str):
    print("==================================================")
    print(f"🏥 STARTING PATIENT ROUTING PIPELINE FOR: {name}")
    print("==================================================\n")
    
    # ----------------------------------------------------
    # STEP 1: SAFETY GATE AGENT
    # ----------------------------------------------------
    print("[1/5] Running Safety Gate Check...")
    safety_response = check_safety(patient_concern)
    print(safety_response)
    
    # Check if the output indicates an emergency (simple substring check for true)
    if "URGENT: true" in safety_response.lower() or "true" in safety_response.lower() and "urgent" in safety_response.lower():
        print("\n🚨 EMERGENCY DETECTED! Halting standard routing. Please seek immediate emergency medical care!")
        return

    print("\n -> Safety check passed. Proceeding to intake...\n")
    
    # ----------------------------------------------------
    # STEP 2: INTAKE AGENT (with MySQL Memory Check)
    # ----------------------------------------------------
    print("[2/5] Running Intake Agent & Database Memory Check...")
    intake_ticket = run_intake_agent(name, phone, patient_concern)
    print(intake_ticket)
    print("\n")
    
    # ----------------------------------------------------
    # STEP 3: TRIAGE ROUTER AGENT
    # ----------------------------------------------------
    print("[3/5] Running Triage Router Agent...")
    triage_output = route_patient(patient_concern)
    print(triage_output)
    
    # Extract department name simply from triage output for downstream use
    department = "General Medicine" # Default fallback
    for line in triage_output.split('\n'):
        if "DEPARTMENT:" in line:
            department = line.replace("DEPARTMENT:", "").strip()
            # Clean up brackets if any
            department = department.replace("[", "").replace("]", "").strip()
    
    print(f"\n -> Routed successfully to: {department}\n")
    
    # ----------------------------------------------------
    # STEP 4: INFORMATION AGENT (RAG)
    # ----------------------------------------------------
    print(f"[4/5] Running Information Agent (RAG for {department})...")
    info_output = get_department_info(department)
    print(info_output)
    print("\n")
    
    # ----------------------------------------------------
    # STEP 5: APPOINTMENT AGENT
    # ----------------------------------------------------
    print(f"[5/5] Running Appointment Agent & Updating MySQL Database...")
    appointment_output = book_appointment(phone, department)
    print(appointment_output)
    
    print("\n==================================================")
    print("✅ PATIENT ROUTING & BOOKING COMPLETE")
    print("==================================================")

if __name__ == "__main__":
    # Test the complete integrated pipeline with a routine patient concern
    run_hospital_system(
        name="Tarak", 
        phone="6303641937", 
        patient_concern="When i stand sunddly i feel nmind block type also every morning very weak me also not able to sleep at night"
    )
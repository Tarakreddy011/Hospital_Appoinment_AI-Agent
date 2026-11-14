import os
from groq import Groq

try:
    from sqlconnections import update_patient_department
except ImportError:
    from Hospital.sqlconnections import update_patient_department

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

# Mock Hospital Schedule (Simulating available slots per department)
DOCTOR_SLOTS = {
    "Orthopaedics": "Dr. Mehta - Tomorrow at 10:30 AM (Room 204)",
    "General Medicine": "Dr. Verma - Today at 4:00 PM (Room 102)",
    "ENT": "Dr. Nair - Tomorrow at 11:15 AM (Room 305)",
    "Cardiology": "Dr. Reddy - Tomorrow at 9:30 AM (Room 401)",
    "Dermatology": "Dr. Priya Patel - Tomorrow at 2:00 PM (Room 108)",
    "Ophthalmology": "Dr. Ananya Sen - Today at 4:30 PM (Room 210)",
    "Neurology": "Dr. Vikram Joshi - Tomorrow at 11:45 AM (Room 312)",
    "Gastroenterology": "Dr. K. S. Rao - Tomorrow at 1:30 PM (Room 205)"
}


def get_slot_for_department(department: str) -> str:
    for key, slot in DOCTOR_SLOTS.items():
        if key.lower() in department.lower():
            return slot
    return "Duty Medical Officer - Today at 5:00 PM (General OPD Room 101)"


def book_appointment(phone: str, department: str) -> str:
    """
    Appointment Agent: Checks available department slots, generates a 
    confirmation slip via Groq, and updates the database record.
    """
    # 1. Look up available slot for the routed department
    assigned_slot = get_slot_for_department(department)
    
    # 2. Update the patient's latest visit record in database
    slot_detail = f"{department} ({assigned_slot})"
    update_patient_department(phone, slot_detail)
    
    # 3. Use Groq LLM to generate a clean confirmation slip
    prompt = f"""
    You are a Hospital Appointment Booking Agent. Generate a brief, polite appointment confirmation slip using these exact details:
    - Department: {department}
    - Assigned Slot & Doctor: {assigned_slot}
    - Status: Confirmed & Logged in Hospital Database
    
    Format clearly with:
    - Confirmation Code (e.g. APPT-12345)
    - Department & Doctor
    - Date, Time & Room
    - Status: Confirmed
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
    print("--- Testing Appointment Agent ---")
    print(book_appointment("9876543210", "Orthopaedics"))

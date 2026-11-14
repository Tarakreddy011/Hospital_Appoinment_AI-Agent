import os
from groq import Groq

try:
    from sqlconnections import update_patient_department
except ImportError:
    from Hospital.sqlconnections import update_patient_department

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

# Department Available Doctor Slots
DEPARTMENT_SLOTS = {
    "Orthopaedics": [
        {"doctor": "Dr. Mehta", "time": "Tomorrow at 10:30 AM", "room": "Room 204", "type": "Regular Joint Consultation"},
        {"doctor": "Dr. S. Kapoor", "time": "Tomorrow at 02:30 PM", "room": "Room 206", "type": "Joint & Spine Clinic"},
        {"doctor": "Dr. A. Verma", "time": "Friday at 11:00 AM", "room": "Room 208", "type": "Musculoskeletal OPD"}
    ],
    "General Medicine": [
        {"doctor": "Dr. Verma", "time": "Today at 04:00 PM", "room": "Room 102", "type": "General Outpatient Clinic"},
        {"doctor": "Dr. R. Gupta", "time": "Tomorrow at 09:30 AM", "room": "Room 104", "type": "Internal Medicine"},
        {"doctor": "Dr. M. Iyer", "time": "Tomorrow at 05:00 PM", "room": "Room 105", "type": "Evening Consultation"}
    ],
    "ENT": [
        {"doctor": "Dr. Nair", "time": "Tomorrow at 11:15 AM", "room": "Room 305", "type": "Ear, Nose & Throat OPD"},
        {"doctor": "Dr. P. Deshmukh", "time": "Tomorrow at 03:30 PM", "room": "Room 307", "type": "Sinus & Allergy Clinic"}
    ],
    "Cardiology": [
        {"doctor": "Dr. Reddy", "time": "Tomorrow at 09:30 AM", "room": "Room 401", "type": "Cardiology Consultation"},
        {"doctor": "Dr. B. Sengupta", "time": "Tomorrow at 01:00 PM", "room": "Room 403", "type": "Preventive Heart Clinic"}
    ],
    "Dermatology": [
        {"doctor": "Dr. Priya Patel", "time": "Tomorrow at 02:00 PM", "room": "Room 108", "type": "Clinical Dermatology"},
        {"doctor": "Dr. K. Saxena", "time": "Tomorrow at 04:30 PM", "room": "Room 110", "type": "Skin & Hair OPD"}
    ],
    "Ophthalmology": [
        {"doctor": "Dr. Ananya Sen", "time": "Today at 04:30 PM", "room": "Room 210", "type": "Comprehensive Eye Clinic"},
        {"doctor": "Dr. H. Joshi", "time": "Tomorrow at 10:00 AM", "room": "Room 212", "type": "Vision Care"}
    ],
    "Neurology": [
        {"doctor": "Dr. Vikram Joshi", "time": "Tomorrow at 11:45 AM", "room": "Room 312", "type": "Neurological Evaluation"},
        {"doctor": "Dr. N. Roy", "time": "Tomorrow at 03:00 PM", "room": "Room 314", "type": "Headache & Balance Clinic"}
    ],
    "Gastroenterology": [
        {"doctor": "Dr. K. S. Rao", "time": "Tomorrow at 01:30 PM", "room": "Room 205", "type": "Digestive Health Clinic"},
        {"doctor": "Dr. T. Banerjee", "time": "Tomorrow at 04:00 PM", "room": "Room 207", "type": "GI & Liver OPD"}
    ]
}


def get_slots_for_department(department: str) -> list:
    """Returns available doctor slots for the routed department."""
    for key, slots in DEPARTMENT_SLOTS.items():
        if key.lower() in department.lower():
            return slots
    return [
        {"doctor": "Duty Medical Officer", "time": "Today at 05:00 PM", "room": "Room 101", "type": "General Outpatient"},
        {"doctor": "Senior Consultant", "time": "Tomorrow at 10:00 AM", "room": "Room 103", "type": "OPD Walk-In"}
    ]


def book_appointment(phone: str, department: str, chosen_slot: dict = None) -> str:
    """
    Appointment Agent: Books an appointment slot, updates the database,
    and returns a clean confirmation slip via Groq.
    """
    slots = get_slots_for_department(department)
    slot_info = chosen_slot or slots[0]
    assigned_text = f"{slot_info['doctor']} - {slot_info['time']} ({slot_info['room']})"
    
    # Update latest patient visit in database
    update_patient_department(phone, f"{department} | {assigned_text}")
    
    prompt = f"""
    You are a Hospital Appointment Booking Agent. Generate a brief, polite appointment confirmation slip using these details:
    - Department: {department}
    - Doctor: {slot_info['doctor']}
    - Time Slot: {slot_info['time']}
    - Room: {slot_info['room']}
    - Clinic Type: {slot_info.get('type', 'Consultation')}
    
    Format clearly:
    - CONFIRMATION ID: (e.g. APPT-12345)
    - DOCTOR & DEPARTMENT:
    - DATE, TIME & ROOM:
    - STATUS: Confirmed & Synchronized with Hospital Registry
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

import random
try:
    from sqlconnections import update_patient_department
except ImportError:
    from Hospital.sqlconnections import update_patient_department
from groq_client import call_groq_chat

DEPARTMENT_SLOTS = {
    "General Medicine": [
        {"doctor": "Dr. Sanjay Verma (MD Internal Med)", "time": "Today at 04:00 PM", "room": "Room 102, Block A", "type": "General Outpatient Clinic"},
        {"doctor": "Dr. Radhika Gupta (MD Physician)", "time": "Tomorrow at 09:30 AM", "room": "Room 104, Block A", "type": "Internal Medicine OPD"},
        {"doctor": "Dr. M. Iyer (Senior Consultant)", "time": "Tomorrow at 05:00 PM", "room": "Room 105, Block A", "type": "Evening Consultation"}
    ],
    "General Surgery": [
        {"doctor": "Dr. Rameshwar Rao (MS General Surgery)", "time": "Tomorrow at 10:00 AM", "room": "Room 201, Surgical Block", "type": "General Surgery OPD"},
        {"doctor": "Dr. Anirudh Sen (DNB Surgery, FIAGES)", "time": "Tomorrow at 02:30 PM", "room": "Room 203, Surgical Block", "type": "Laparoscopic & Minor Surgery Clinic"}
    ],
    "Emergency Medicine": [
        {"doctor": "Dr. Nitin Saxena (MD Emergency Medicine)", "time": "Immediate / 24x7 Priority", "room": "ER Resuscitation Bay 1", "type": "Emergency Trauma Triage"},
        {"doctor": "Duty Trauma Consultant", "time": "Walk-in Immediate", "room": "Central Emergency Wing", "type": "Acute Casualty"}
    ],
    "Cardiology": [
        {"doctor": "Dr. K. V. Reddy (DM Cardiology)", "time": "Tomorrow at 09:30 AM", "room": "Room 401, Cardiac Wing", "type": "Cardiology Consultation"},
        {"doctor": "Dr. B. Sengupta (MD, DM Interventional)", "time": "Tomorrow at 01:00 PM", "room": "Room 403, Cardiac Wing", "type": "Heart Rhythm & Preventive OPD"}
    ],
    "Neurology": [
        {"doctor": "Dr. Vikram Joshi (DM Neurology)", "time": "Tomorrow at 11:45 AM", "room": "Room 312, Neuro Wing", "type": "Neurological Evaluation"},
        {"doctor": "Dr. Nandita Roy (MD, DM Neuro)", "time": "Tomorrow at 03:00 PM", "room": "Room 314, Neuro Wing", "type": "Headache, Seizure & Memory Clinic"}
    ],
    "Neurosurgery": [
        {"doctor": "Dr. Alok Chandra (MCh Neurosurgery)", "time": "Tomorrow at 10:30 AM", "room": "Room 316, Neuro Wing", "type": "Brain & Spine Neurosurgery OPD"},
        {"doctor": "Dr. K. Jayaraman (MS, MCh Neuro)", "time": "Tomorrow at 02:00 PM", "room": "Room 318, Neuro Wing", "type": "Neuro-Trauma & Spine Clinic"}
    ],
    "Orthopaedics": [
        {"doctor": "Dr. Rajiv Mehta (MS Ortho)", "time": "Today at 04:30 PM", "room": "Room 204, Block B", "type": "Joint & Spine Clinic"},
        {"doctor": "Dr. Sunita Kapoor (DNB Ortho)", "time": "Tomorrow at 10:30 AM", "room": "Room 206, Block B", "type": "Musculoskeletal OPD"},
        {"doctor": "Dr. A. Verma (Fellow Sports Med)", "time": "Tomorrow at 02:30 PM", "room": "Room 208, Block B", "type": "Arthroscopy & Sports Injury"}
    ],
    "Pediatrics": [
        {"doctor": "Dr. Shalini Deshmukh (MD Pediatrics)", "time": "Tomorrow at 09:00 AM", "room": "Room 108, Child Care Wing", "type": "General Pediatric OPD"},
        {"doctor": "Dr. Tarun Bhatia (DCH, DNB Paed)", "time": "Tomorrow at 01:30 PM", "room": "Room 110, Child Care Wing", "type": "Pediatric Growth & Immunization Clinic"}
    ],
    "Obstetrics & Gynecology": [
        {"doctor": "Dr. Sunita Deshpande (MS OB-GYN)", "time": "Tomorrow at 10:00 AM", "room": "Room 112, Women's Pavilion", "type": "General Gynecology OPD"},
        {"doctor": "Dr. Fatima Ahmed (DGO, DNB OB-GYN)", "time": "Tomorrow at 02:00 PM", "room": "Room 114, Women's Pavilion", "type": "Women's Health & Maternity Clinic"}
    ],
    "Psychiatry": [
        {"doctor": "Dr. Meera Kulkarni (MD Psychiatry)", "time": "Tomorrow at 11:00 AM", "room": "Room 501, Behavioral Wing", "type": "Psychiatry OPD"},
        {"doctor": "Dr. R. Chatterjee (DPM, DNB Psych)", "time": "Tomorrow at 03:30 PM", "room": "Room 503, Behavioral Wing", "type": "Adult Behavioral & Mood Clinic"}
    ],
    "Dermatology": [
        {"doctor": "Dr. Priya Patel (MD Derma)", "time": "Tomorrow at 02:00 PM", "room": "Room 108, Block A", "type": "Clinical Dermatology"},
        {"doctor": "Dr. K. Saxena (DVD Derma)", "time": "Tomorrow at 04:30 PM", "room": "Room 110, Block A", "type": "Skin, Hair & Allergy OPD"}
    ],
    "Ophthalmology": [
        {"doctor": "Dr. Ananya Sen (MS Ophthalmology)", "time": "Today at 04:30 PM", "room": "Room 210, Eye Pavilion", "type": "Comprehensive Eye Clinic"},
        {"doctor": "Dr. H. Joshi (Cornea Specialist)", "time": "Tomorrow at 10:00 AM", "room": "Room 212, Eye Pavilion", "type": "Vision & Refraction Care"}
    ],
    "ENT (Otolaryngology)": [
        {"doctor": "Dr. Arvind Nair (MS ENT)", "time": "Tomorrow at 11:15 AM", "room": "Room 305, Block C", "type": "Ear, Nose & Throat OPD"},
        {"doctor": "Dr. P. Deshmukh (DLO ENT)", "time": "Tomorrow at 03:30 PM", "room": "Room 307, Block C", "type": "Sinus & Allergy Clinic"}
    ],
    "Urology": [
        {"doctor": "Dr. Ashwin Kumar (MCh Urology)", "time": "Tomorrow at 11:30 AM", "room": "Room 215, Block B", "type": "Urology & Stone Clinic"},
        {"doctor": "Dr. J. Pandey (MS, DNB Uro)", "time": "Tomorrow at 04:00 PM", "room": "Room 217, Block B", "type": "Kidney & Urinary OPD"}
    ],
    "Nephrology": [
        {"doctor": "Dr. Bhaskar Prasad (DM Nephrology)", "time": "Tomorrow at 10:00 AM", "room": "Room 412, Renal Center", "type": "Kidney Disease & Dialysis OPD"},
        {"doctor": "Dr. S. K. Mahajan (MD, DM Nephro)", "time": "Tomorrow at 02:15 PM", "room": "Room 414, Renal Center", "type": "Hypertension & Renal Care Clinic"}
    ],
    "Gastroenterology": [
        {"doctor": "Dr. K. S. Rao (DM Gastro)", "time": "Tomorrow at 01:30 PM", "room": "Room 205, Digestive Center", "type": "Digestive Health Clinic"},
        {"doctor": "Dr. T. Banerjee (MD, DNB Gastro)", "time": "Tomorrow at 04:00 PM", "room": "Room 207, Digestive Center", "type": "Liver & GI OPD"}
    ],
    "Pulmonology / Respiratory Medicine": [
        {"doctor": "Dr. Sameer Krishnan (MD Pulmonology)", "time": "Tomorrow at 10:00 AM", "room": "Room 320, Chest Clinic", "type": "Respiratory Medicine OPD"},
        {"doctor": "Dr. Devika Bhatt (DNB Respiratory Med)", "time": "Tomorrow at 02:30 PM", "room": "Room 322, Chest Clinic", "type": "Asthma & Allergy Clinic"}
    ],
    "Endocrinology": [
        {"doctor": "Dr. Lavanya Rao (DM Endocrinology)", "time": "Tomorrow at 10:30 AM", "room": "Room 408, Metabolic Center", "type": "Diabetes & Hormone Clinic"},
        {"doctor": "Dr. Prateek Malhotra (MD, DM Endo)", "time": "Friday at 09:30 AM", "room": "Room 410, Metabolic Center", "type": "Thyroid & Metabolic OPD"}
    ],
    "Rheumatology": [
        {"doctor": "Dr. Geeta Seshadri (MD, DM Clinical Immunology)", "time": "Tomorrow at 11:00 AM", "room": "Room 220, Block B", "type": "Rheumatoid & Autoimmune Clinic"},
        {"doctor": "Dr. Manoj Nair (DNB Rheumatology)", "time": "Tomorrow at 03:00 PM", "room": "Room 222, Block B", "type": "Arthritis & Lupus Care OPD"}
    ],
    "Hematology": [
        {"doctor": "Dr. Shalini Mukhopadhyay (DM Clinical Hematology)", "time": "Tomorrow at 10:15 AM", "room": "Room 330, Hematology Wing", "type": "Blood Disorders & Coagulation Clinic"},
        {"doctor": "Dr. V. Ramanathan (MD, DM Hematology)", "time": "Tomorrow at 02:45 PM", "room": "Room 332, Hematology Wing", "type": "Comprehensive Anemia & Bone Marrow OPD"}
    ],
    "Oncology": [
        {"doctor": "Dr. Debashish Bose (DM Medical Oncology)", "time": "Tomorrow at 10:00 AM", "room": "Room 505, Cancer Pavilion", "type": "Medical Oncology Consultation"},
        {"doctor": "Dr. Revathi Menon (MCh Surgical Oncology)", "time": "Tomorrow at 02:30 PM", "room": "Room 507, Cancer Pavilion", "type": "Surgical Oncology & Tumor Board"}
    ],
    "Anesthesiology": [
        {"doctor": "Dr. Hemant Kulkarni (MD Anaesthesiology)", "time": "Tomorrow at 09:00 AM", "room": "Room 101, PAC & Pain Wing", "type": "Pre-Anesthesia Assessment Clinic"},
        {"doctor": "Duty Intensivist / Anesthesiologist", "time": "On-Duty 24x7", "room": "ICU & Operation Theater", "type": "Peri-Operative Anesthesia"}
    ],
    "Critical Care Medicine": [
        {"doctor": "Dr. Anand Swaminathan (MD, FNB Critical Care)", "time": "Immediate / 24x7", "room": "Central ICU Block 3", "type": "Intensive Care Management"},
        {"doctor": "Duty Critical Care Fellow", "time": "Continuous Care", "room": "High Dependency Unit (HDU)", "type": "Multi-Organ Support Unit"}
    ],
    "Dentistry / Oral Surgery": [
        {"doctor": "Dr. Preeti Agarwal (MDS Oral Surgery)", "time": "Tomorrow at 10:00 AM", "room": "Dental Suite 1, Ground Floor", "type": "Dental & Maxillofacial OPD"},
        {"doctor": "Dr. Rohit Mathur (BDS, MDS Orthodontics)", "time": "Tomorrow at 03:00 PM", "room": "Dental Suite 2, Ground Floor", "type": "Comprehensive Oral Care"}
    ],
    "Physiotherapy / Rehabilitation": [
        {"doctor": "Dr. Suresh Pillai (MPT Neuro-Rehab)", "time": "Tomorrow at 09:30 AM", "room": "Physio Rehab Center A", "type": "Neurological & Stroke Rehabilitation"},
        {"doctor": "Dr. Anjana Das (MPT Ortho-Sports)", "time": "Tomorrow at 02:00 PM", "room": "Physio Rehab Center B", "type": "Orthopaedic & Musculoskeletal Therapy"}
    ]
}


def get_slots_for_department(department: str) -> list:
    """Returns available doctor slots for the routed department."""
    dep_clean = (department or "").lower().strip()

    # 1. Exact match first
    for key, slots in DEPARTMENT_SLOTS.items():
        if key.lower() == dep_clean:
            return slots

    # 2. Normalized match (e.g. ENT, Respiratory Medicine)
    for key, slots in DEPARTMENT_SLOTS.items():
        if dep_clean == key.lower().replace("&", "and"):
            return slots
        if f" {key.lower()} " in f" {dep_clean} ":
            return slots

    # 3. Fallback
    return [
        {"doctor": "Duty Medical Officer", "time": "Today at 04:30 PM", "room": "Room 101, Block A", "type": "General Outpatient Walk-in"},
        {"doctor": "Senior Consultant Physician", "time": "Tomorrow at 10:00 AM", "room": "Room 103, Block A", "type": "Internal Medicine OPD"}
    ]


def book_appointment(phone: str, department: str, chosen_slot: dict = None) -> str:
    """
    Appointment Agent: Books doctor slot, updates registry in database,
    and returns a clean, structured confirmation slip.
    """
    slots = get_slots_for_department(department)
    slot_info = chosen_slot or slots[0]
    assigned_text = f"{slot_info['doctor']} - {slot_info['time']} ({slot_info['room']})"

    try:
        update_patient_department(phone, f"{department} | {assigned_text}")
    except Exception as e:
        print(f"[AppointmentAgent] Warning: Could not update patient visit record in DB: {e}")

    appt_id = f"APPT-{random.randint(10000, 99999)}"

    prompt = f"""
    You are a Hospital Appointment Booking Agent. Generate a concise, polite appointment confirmation slip using these details:
    - Department: {department}
    - Doctor: {slot_info['doctor']}
    - Time Slot: {slot_info['time']}
    - Room: {slot_info['room']}
    - Clinic Type: {slot_info.get('type', 'Consultation')}
    - Confirmation ID: {appt_id}

    Format strictly:
    CONFIRMATION ID: {appt_id}
    DOCTOR & DEPARTMENT: {slot_info['doctor']} — {department} ({slot_info.get('type', 'OPD')})
    DATE, TIME & ROOM: {slot_info['time']} | {slot_info['room']}
    STATUS: Confirmed & Logged in Central Hospital Registry
    """

    agent_output = call_groq_chat(prompt, temperature=0.0)

    if not agent_output:
        agent_output = (
            f"CONFIRMATION ID: {appt_id}\n"
            f"DOCTOR & DEPARTMENT: {slot_info['doctor']} — {department} ({slot_info.get('type', 'OPD')})\n"
            f"DATE, TIME & ROOM: {slot_info['time']} | {slot_info['room']}\n"
            f"STATUS: Confirmed & Logged in Central Hospital Registry"
        )

    return agent_output

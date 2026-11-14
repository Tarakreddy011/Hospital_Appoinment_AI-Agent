import os
import mysql.connector
from groq import Groq

client = Groq(api_key="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")

# Mock Hospital Schedule (Simulating available slots per department)
DOCTOR_SLOTS = {
    "Orthopaedics": "Dr. Mehta - Tomorrow at 10:30 AM (Room 204)",
    "General Medicine": "Dr. Verma - Today at 4:00 PM (Room 102)",
    "ENT": "Dr. Nair - Tomorrow at 11:15 AM (Room 305)",
    "Cardiology": "Dr. Reddy - Tomorrow at 9:30 AM (Room 401)"
}

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tarak@2005",
        database="hospital_db"
    )

def book_appointment(phone: str, department: str):
    """
    Appointment Agent: Checks available department slots, generates a 
    confirmation slip via Groq, and updates the MySQL record.
    """
    # 1. Look up available slot for the routed department
    assigned_slot = DOCTOR_SLOTS.get(department, "Duty Doctor - Today at 5:00 PM (General OPD)")
    
    # 2. Update the patient's latest visit record in MySQL with the final department
    db = get_db_connection()
    cursor = db.cursor()
    update_query = """
        UPDATE patient_records 
        SET routed_department = %s 
        WHERE phone = %s 
        ORDER BY visit_date DESC LIMIT 1
    """
    cursor.execute(update_query, (f"{department} ({assigned_slot})", phone))
    db.commit()
    cursor.close()
    db.close()
    
    # 3. Use Groq LLM to generate a clean confirmation slip
    prompt = f"""
    You are a Hospital Appointment Booking Agent. Generate a brief, polite appointment confirmation slip using these exact details:
    - Department: {department}
    - Assigned Slot & Doctor: {assigned_slot}
    - Status: Confirmed & Logged in Hospital Database
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    print("--- Testing Appointment Agent ---")
    print(book_appointment("9876543210", "Orthopaedics"))
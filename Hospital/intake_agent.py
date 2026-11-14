import os
import mysql.connector
from groq import Groq

# Initialize Groq client
client = Groq(api_key="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")

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tarak@2005",
        database="hospital_db"
    )

def run_intake_agent(name: str, phone: str, current_concern: str):
    """
    Intake Agent: Combines MySQL memory check (returning patient history) 
    with Groq LLM reasoning to generate a structured patient intake record.
    """
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    
    # 1. Memory Check: Query MySQL for prior visits
    cursor.execute("SELECT * FROM patient_records WHERE phone = %s ORDER BY visit_date DESC LIMIT 1", (phone,))
    previous_visit = cursor.fetchone()
    
    history_context = "No previous records found. New patient."
    if previous_visit:
        history_context = f"Returning Patient! Last visit date: {previous_visit['visit_date']}, Routed Department: {previous_visit['routed_department']}, Prior Concern: {previous_visit['last_concern']}"
    
    # 2. LLM Reasoning/Agent Prompt
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
    - STRUCTURED_CONCERN: (A clean, professional phrasing of the current concern for the triage doctor)
    """
    
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b", 
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )
    
    agent_output = completion.choices[0].message.content
    
    # 3. Save this new visit to MySQL
    insert_query = """
        INSERT INTO patient_records (name, phone, last_concern, routed_department) 
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (name, phone, current_concern, "Pending Triage"))
    db.commit()
    
    cursor.close()
    db.close()
    
    return agent_output

if __name__ == "__main__":
    print("--- Testing Intake Agent ---")
    print(run_intake_agent("Rahul Sharma", "9876543210", "Sharp pain in right knee when climbing stairs"))
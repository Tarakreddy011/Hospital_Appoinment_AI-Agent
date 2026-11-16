import os
import sys
import re
from typing import Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOSPITAL_DIR = os.path.join(BASE_DIR, "Hospital")
if HOSPITAL_DIR not in sys.path:
    sys.path.insert(0, HOSPITAL_DIR)

from main import run_hospital_system
from appointment_agent import book_appointment
from sqlconnections import get_patient_last_visit

app = FastAPI(title="LifeCare Hospital Patient Routing AI")
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static",
)

class PatientRequest(BaseModel):
    name: str
    phone: str
    patient_concern: str
    chosen_slot: Optional[dict] = None

class SlotBookingRequest(BaseModel):
    phone: str
    department: str
    slot: dict


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(BASE_DIR, "templates", "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Template index.html not found.")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/check-patient")
async def check_patient(phone: str):
    """Checks database for returning patient history using contact phone."""
    clean_phone = phone.strip()
    if not clean_phone or len(clean_phone) < 4:
        return {"found": False}
    try:
        record = get_patient_last_visit(clean_phone)
        if record:
            return {
                "found": True,
                "name": record.get("name", ""),
                "last_visit": str(record.get("visit_date", "N/A")),
                "last_concern": record.get("last_concern", ""),
                "last_department": record.get("routed_department", "")
            }
        return {"found": False}
    except Exception as e:
        return {"found": False, "error": str(e)}


@app.post("/api/route")
async def route_patient_api(payload: PatientRequest):
    """Executes the patient routing and triage system."""
    try:
        result = run_hospital_system(
            name=payload.name.strip(),
            phone=payload.phone.strip(),
            patient_concern=payload.patient_concern.strip(),
            chosen_slot=payload.chosen_slot
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Routing error: {str(e)}")


@app.post("/api/book-slot")
async def update_booking_slot(payload: SlotBookingRequest):
    """Allows patient to switch to an alternative available doctor slot."""
    try:
        confirmation = book_appointment(payload.phone, payload.department, payload.slot)
        # Extract confirmation code if present
        code_match = re.search(r"APPT-[\w\d]+", confirmation, re.IGNORECASE)
        code = code_match.group(0) if code_match else "APPT-CONFIRMED"
        
        return {
            "success": True, 
            "confirmation": confirmation,
            "code": code,
            "slot": payload.slot,
            "department": payload.department
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("🏥 Starting Hospital Patient Routing Web Server on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)

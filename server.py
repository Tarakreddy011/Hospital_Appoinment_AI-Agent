import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
import uvicorn

# Ensure Hospital directory is in sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HOSPITAL_DIR = os.path.join(BASE_DIR, "Hospital")
if HOSPITAL_DIR not in sys.path:
    sys.path.insert(0, HOSPITAL_DIR)

from main import run_hospital_system
from sqlconnections import get_active_db_type, get_all_patient_records

app = FastAPI(title="Hospital Patient Routing AI Agent")

# Pydantic schema for patient check-in
class PatientRequest(BaseModel):
    name: str
    phone: str
    patient_concern: str


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = os.path.join(BASE_DIR, "templates", "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend template index.html not found.")
    with open(index_path, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


@app.get("/api/status")
async def get_system_status():
    """Returns database and engine status."""
    return {
        "status": "online",
        "database": get_active_db_type(),
        "model": "openai/gpt-oss-120b"
    }


@app.get("/api/records")
async def get_patient_records():
    """Returns recent patient database records for live inspection."""
    try:
        records = get_all_patient_records(limit=50)
        return records
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/route")
async def route_patient_api(payload: PatientRequest):
    """Executes the multi-agent pipeline for a patient check-in."""
    try:
        result = run_hospital_system(
            name=payload.name.strip(),
            phone=payload.phone.strip(),
            patient_concern=payload.patient_concern.strip()
        )
        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {str(e)}")


if __name__ == "__main__":
    print("🏥 Starting Hospital AI Agent Web Server on http://127.0.0.1:8000 ...")
    uvicorn.run(app, host="127.0.0.1", port=8000)

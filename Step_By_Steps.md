# Step-by-Step Setup & Execution Guide

Follow these steps to set up and run the Multi-Agent Hospital Routing System:

### 1. Install Required Dependencies
Open a terminal in the project directory and run:
```bash
pip install groq mysql-connector-python fastapi uvicorn pydantic
```

### 2. Database Setup (MySQL with Automatic SQLite Fallback)
The project connects to MySQL (`hospital_db`) by default with credentials defined in `Hospital/sqlconnections.py`.
- If MySQL is running on `localhost:3306`, it creates the database and table automatically.
- If MySQL is offline, the system automatically falls back to a local SQLite database (`Hospital/hospital.db`) without crashing.

### 3. Run the Web Application
Start the web application server:
```bash
python server.py
```
Open your browser and navigate to:
```
http://127.0.0.1:8000
```
This opens the web interface featuring:
- Patient check-in form (Name, Phone, Symptoms).
- Quick demo presets for university viva evaluation (Emergency, Ortho, Returning Patient).
- Real-time step-by-step progress cards across all 5 agents:
  1. **Safety Gate Agent** (Emergency red-flag highlight & 112/108 advisory)
  2. **Intake & Memory Agent** (Database history recall)
  3. **Triage Router Agent** (Department routing without disease diagnosis)
  4. **Information Agent (RAG)** (Knowledge base intake instructions & required items)
  5. **Appointment Agent** (Doctor slot, room assignment & database logging)
- Live database viewer showing stored patient visits in real time.

### 4. Run via Terminal / CLI
You can also run the pipeline directly via terminal:
```bash
python Hospital/main.py
```

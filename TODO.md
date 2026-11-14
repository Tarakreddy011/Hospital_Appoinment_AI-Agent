# Hospital Patient Routing AI Agent — Project Tracker

## Project Overview
Multi-Agent Hospital Outpatient Routing and Triage System built with Groq LLMs, dual MySQL/SQLite database memory, and a clean, responsive web frontend.

### Architecture & Agent Pipeline Status
- [x] **Step 1: Safety Gate Agent (`Hospital/safety_agent.py`)**
  - Evaluates inputs first for emergency red flags (chest pain, trauma, stroke signs).
  - Intercepts urgent cases with immediate 112/108 advisory; halts outpatient routing.
- [x] **Step 2: Intake & Memory Agent (`Hospital/intake_agent.py`)**
  - Recalls prior visits from database memory by patient phone number.
  - Distinguishes New vs. Returning patients and formats structured intake ticket.
- [x] **Step 3: Triage Router Agent (`Hospital/triage_agent.py`)**
  - Maps described symptoms to clinical department (Orthopaedics, ENT, Cardiology, etc.).
  - Strictly prohibits clinical disease diagnosis.
- [x] **Step 4: Information Agent (RAG) (`Hospital/info_agent.py`)**
  - Uses RAG over hospital knowledge base documents.
  - Generates intake instructions and what to bring (fasting, previous scans, IDs).
- [x] **Step 5: Appointment Agent (`Hospital/appointment_agent.py`)**
  - Assigns available doctor slot and room number.
  - Generates digital confirmation slip and updates database in real time.
- [x] **Unified Database Layer (`Hospital/sqlconnections.py`)**
  - Dual-mode persistence: MySQL with resilient SQLite fallback (`hospital.db`).
- [x] **Web Frontend (`templates/index.html` & `server.py`)**
  - Modern, responsive HTML/CSS/JS frontend without Streamlit.
  - Step-by-step visual cards for all 5 agents.
  - Emergency red banner and advisory intercept.
  - One-click viva presentation presets (Emergency, Ortho, Returning Patient).
  - Live database viewer table.

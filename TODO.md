# **hospital-router**

**│**

**├── main.py            # FastAPI server entry point**

**├── agents/**

**│   ├── safety.py      # Safety Gate Agent**

**│   ├── intake.py      # Intake \& Memory Check Agent**

**│   ├── triage.py      # Triage Router Agent**

**│   ├── info.py        # Information Agent (RAG)**

**│   └── appointment.py # Appointment Agent**

**└── templates/**

&#x20;   **└── index.html     # Basic frontend UI**





**--**

**----------------------------------------------------------------------------------------------------------**

* **Safety Gate: Evaluates inputs first for emergency red flags, intercepting urgent cases with an immediate in-person care advisory.**
* **gsk\_tpTMZPPk2k0zDf8pHmMUWGdyb3FYsS3B9zZRRV5xofh4RHZDv3uA|gsk\_tpTMZPPk2k0zDf8pHmMUWGdyb3FYsS3B9zZRRV5xofh4RHZDv3uA**
* 
* **Intake \& Memory Check: Captures basic details and queries a shared memory store to recall prior patient visits (group-of-three requirement).**
* 
* **Triage Router: Maps the described concern to a clinical department (e.g., Orthopaedics, ENT) without diagnosing.**
* 
* **Information Agent: Uses RAG over department documents to fetch instructions and required items.**
* 
* **Appointment Agent: Proposes available time slots for the routed department.**

**--**

**--------------------------------------------------------------------------------------------------------**

**--**








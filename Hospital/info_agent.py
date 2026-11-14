import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

# Structured Hospital Knowledge Base
HOSPITAL_KB_STRUCTURED = {
    "Orthopaedics": {
        "guidelines": [
            "Please arrive 15 minutes prior to your scheduled slot for registration.",
            "Wear loose, comfortable clothing around joints to allow easy physical examination.",
            "Avoid strenuous joint exertion right before your examination."
        ],
        "what_to_bring": [
            "Government Photo ID (e.g., driver's license, passport, Aadhaar)",
            "Previous X-ray, CT, or MRI scan films and reports",
            "List of current medications and pain relievers",
            "Health insurance card if applicable"
        ]
    },
    "General Medicine": {
        "guidelines": [
            "Please arrive 10-15 minutes early to complete vital checks (BP, temperature, pulse).",
            "Fasting (8-10 hours) may be required if routine blood chemistry tests are ordered.",
            "Bring your daily symptom tracker or temperature log if recorded."
        ],
        "what_to_bring": [
            "Government Photo ID",
            "Previous prescription records and current medication bottles",
            "Health insurance card",
            "Vaccination and allergy history"
        ]
    },
    "ENT": {
        "guidelines": [
            "Please arrive 10 minutes early at Central OPD Block B.",
            "Avoid using over-the-counter nasal sprays or ear drops for at least 4 hours before consultation.",
            "Avoid loud music or earphones on the morning of hearing evaluation."
        ],
        "what_to_bring": [
            "Government Photo ID",
            "Previous audiology/hearing reports or sinus CT scans",
            "List of known drug or seasonal allergies",
            "Current medication list"
        ]
    },
    "Cardiology": {
        "guidelines": [
            "Please arrive 15 minutes early for baseline ECG and vitals measurement.",
            "Avoid caffeine, energy drinks, nicotine, and heavy exercise 2 hours before consultation.",
            "Wear comfortable button-up clothing for easy chest examination."
        ],
        "what_to_bring": [
            "Government Photo ID",
            "Previous ECG, 2D Echo, or Holter reports",
            "Blood pressure log and current cardiac medication list with exact dosages",
            "Health insurance card"
        ]
    },
    "Dermatology": {
        "guidelines": [
            "Arrive 10 minutes early for triage check-in.",
            "Do not apply cosmetic lotions, makeup, or topical medicated creams to affected areas on the morning of visit.",
            "Take note of when the skin symptoms first appeared."
        ],
        "what_to_bring": [
            "Government Photo ID",
            "Previous biopsy or skin allergy test reports",
            "Names or photos of skincare products and soaps currently used"
        ]
    },
    "Ophthalmology": {
        "guidelines": [
            "Arrive 15 minutes early. Dilating eye drops may cause temporary blurriness for 2-3 hours.",
            "Please arrange for an accompanist or driver, as driving post-dilation is not advised.",
            "Wear sunglasses after your appointment to protect dilated eyes."
        ],
        "what_to_bring": [
            "Government Photo ID",
            "Current prescription eyeglasses and contact lens case",
            "Previous ophthalmology reports or eye surgery history"
        ]
    },
    "Neurology": {
        "guidelines": [
            "Arrive 15 minutes prior to your slot. Ensure adequate rest the night before.",
            "Document symptom triggers, headache frequency, and balance issues.",
            "Bring an accompanist if dizziness or fainting episodes have occurred."
        ],
        "what_to_bring": [
            "Government Photo ID",
            "Previous brain MRI / CT scans and EEG recordings",
            "Detailed headache or symptom diary",
            "Complete list of all ongoing medications"
        ]
    },
    "Gastroenterology": {
        "guidelines": [
            "Arrive 15 minutes early at the GI clinic reception.",
            "Maintain 6 hours of fasting if abdominal ultrasound or endoscopy may be considered.",
            "Keep a record of digestive symptoms related to meal timings."
        ],
        "what_to_bring": [
            "Government Photo ID",
            "Previous endoscopy, colonoscopy, or ultrasound reports",
            "Recent liver function lab tests and blood work",
            "Current medication list"
        ]
    }
}


def get_structured_dept_info(department_name: str) -> dict:
    """Returns guaranteed clean structured guidelines and items to bring."""
    for key, data in HOSPITAL_KB_STRUCTURED.items():
        if key.lower() in department_name.lower():
            return data
    return {
        "guidelines": [
            "Please arrive 10-15 minutes prior to your scheduled consultation slot.",
            "Check in at the outpatient reception desk for token verification.",
            "Follow any specific fasting or preparation instructions communicated by your clinic."
        ],
        "what_to_bring": [
            "Government-issued Photo ID (driver's license, passport, or Aadhaar)",
            "All previous medical records, scan reports, and prescription slips",
            "Health insurance card and policy details",
            "List of current medications and allergies"
        ]
    }


def get_department_info(department_name: str) -> str:
    """Legacy RAG string output generator."""
    info = get_structured_dept_info(department_name)
    guidelines_str = "\n".join([f"- {g}" for g in info["guidelines"]])
    bring_str = "\n".join([f"- {b}" for b in info["what_to_bring"]])
    
    return f"INTAKE INSTRUCTIONS:\n{guidelines_str}\n\nWHAT TO BRING:\n{bring_str}"


if __name__ == "__main__":
    print(get_structured_dept_info("ENT"))

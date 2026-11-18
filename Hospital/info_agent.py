import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
client = Groq(api_key=GROQ_API_KEY)

# Structured Hospital Knowledge Base
HOSPITAL_KB_STRUCTURED = [
{
  "metadata": {
    "knowledge_base_name": "Outpatient Department Preparation Knowledge Base",
    "schema_version": "2.0.0",
    "language": "en-IN",
    "prepared_on": "2026-11-18",
    "clinical_approval_status": "Pending clinician and hospital-policy review",
    "scope": "Routine outpatient consultation preparation and conditional preparation for selected tests or procedures.",
    "important_note": "This knowledge base provides appointment-preparation information only. It must not diagnose conditions, prescribe treatment, or replace instructions issued by the patient's clinician or the hospital performing a test or procedure.",
    "retrieval_recommendation": "Index each department as a separate retrieval document. Retrieve global_safety_rules alongside the matching department document. Use conditional_guidelines only when the patient has explicitly said that the relevant test or procedure is scheduled."
  },
  "global_safety_rules": [
    {
      "id": "GLOBAL_001",
      "rule": "Do not advise fasting for a routine consultation. Recommend fasting only when a specific test or procedure has been ordered and the ordering clinician or performing facility has provided the required instructions.",
      "response_behavior": "Ask which test or procedure is scheduled when that detail is missing. Do not invent a fasting duration."
    },
    {
      "id": "GLOBAL_002",
      "rule": "Never tell a patient to start, stop, skip, or change a prescribed medicine, including blood thinners, diabetes medicines, seizure medicines, heart medicines, eye drops, ear drops, or nasal sprays, unless a qualified clinician has explicitly instructed them to do so.",
      "response_behavior": "Tell the patient to contact the prescribing clinician or the facility performing the procedure for medication-specific instructions."
    },
    {
      "id": "GLOBAL_003",
      "rule": "Keep routine specialist consultations separate from investigations and procedures. Preparation for an ECG, exercise stress test, audiometry, ultrasound, endoscopy, colonoscopy, or other procedure is not automatically required for every visit to that specialty.",
      "response_behavior": "Only present conditional_guidelines when the patient confirms that the named test or procedure is scheduled."
    },
    {
      "id": "GLOBAL_004",
      "rule": "Arrival time, clinic location, accepted identity documents, insurance requirements, and registration procedures are hospital-specific administrative policies.",
      "response_behavior": "Use approved facility configuration or the appointment confirmation. Never invent a block, room, arrival buffer, or document requirement."
    },
    {
      "id": "GLOBAL_005",
      "rule": "Do not diagnose, estimate disease severity, or reassure a patient that a potentially serious symptom can wait for a routine appointment.",
      "response_behavior": "If the patient describes a potentially life-threatening or sudden severe symptom, direct them to local emergency services or the nearest emergency department according to the hospital's approved escalation policy."
    },
    {
      "id": "GLOBAL_006",
      "rule": "Do not claim that every item in what_to_bring is mandatory. Some items are relevant only when available or applicable.",
      "response_behavior": "Use wording such as 'bring if available' or 'if applicable' for previous reports, insurance documents, symptom logs, and medical devices."
    }
  ],
  "departments": {
    "Orthopaedics": {
      "department_id": "orthopaedics",
      "aliases": ["orthopedics", "bone and joint", "joint clinic", "musculoskeletal clinic", "bone specialist"],
      "guidelines": [
        "Wear loose, comfortable clothing that allows the doctor to examine the affected joint, limb, back, or other painful area.",
        "Note which body part is affected, when the problem began, whether an injury occurred, and what makes the pain or movement difficulty better or worse.",
        "Mention any swelling, stiffness, weakness, reduced movement, falls, previous injuries, or difficulty with daily activities.",
        "Bring and use your usual mobility aid, such as a walking stick, walker, brace, or support, if applicable.",
        "Continue your usual routine unless your treating clinician has given you different instructions. Do not stop pain medicines or deliberately change your activity level just to prepare for the consultation."
      ],
      "conditional_guidelines": [
        {
          "when": "The patient has already had an X-ray, CT scan, or MRI for the current problem.",
          "instruction": "Bring the report and the actual images if available, such as a CD, USB drive, or accessible digital image link. A report alone may not contain all the information the specialist needs."
        }
      ],
      "what_to_bring": [
        "Photo identification accepted by the hospital and appointment confirmation.",
        "Previous X-ray, CT, or MRI reports and image files related to the current problem, if available.",
        "A current medication list, including prescription medicines, over-the-counter pain relievers, supplements, and doses.",
        "Records of previous treatment for the problem, such as physiotherapy, injections, braces, surgery, or discharge summaries, if available.",
        "Health insurance or cashless-treatment documents, if applicable."
      ],
      "safety_notes": [
        "Do not advise the patient to stop prescribed pain medicines or blood thinners before a routine orthopaedic consultation.",
        "Do not promise that imaging will or will not be required; that decision belongs to the treating clinician."
      ],
      "keywords": ["joint pain", "knee pain", "back pain", "neck pain", "fracture", "sprain", "arthritis", "swelling", "bone", "muscle", "ligament", "mobility", "X-ray", "MRI", "CT scan"],
      "source_ids": ["SRC_001", "SRC_002"]
    },
    "General Medicine": {
      "department_id": "general_medicine",
      "aliases": ["general physician", "internal medicine", "physician", "primary care", "medicine OPD"],
      "guidelines": [
        "Arrive according to the time and registration instructions on your appointment confirmation.",
        "Write down your main symptoms, when they started, how often they occur, and whether they are improving, worsening, or changing.",
        "Bring a temperature, blood pressure, blood glucose, or symptom log if you have been recording one and it is relevant to your visit.",
        "Tell the doctor about known allergies and what happened during any previous allergic reaction.",
        "Do not fast merely because you are attending a General Medicine consultation."
      ],
      "conditional_guidelines": [
        {
          "when": "A fasting blood test has been specifically ordered.",
          "instruction": "Follow the exact fasting duration and instructions given by the ordering clinician or laboratory. The required duration depends on the test. Ask the laboratory what is permitted, including water and regular medicines. Do not independently stop prescribed medicines."
        }
      ],
      "what_to_bring": [
        "Photo identification accepted by the hospital and appointment confirmation.",
        "Previous prescriptions, consultation notes, discharge summaries, and recent laboratory reports, if available.",
        "A current medication list or medication strips/bottles, including doses and timing.",
        "Known drug, food, or other allergies and details of previous reactions.",
        "Vaccination records or relevant home-monitoring logs, if applicable.",
        "Health insurance documents, if applicable."
      ],
      "safety_notes": [
        "Never present fasting as a standard requirement for every General Medicine visit.",
        "Do not advise changes to regular medicines based only on a planned blood test; refer medication questions to the ordering clinician or laboratory."
      ],
      "keywords": ["fever", "cold", "infection", "weakness", "fatigue", "blood pressure", "diabetes", "sugar test", "blood test", "general physician", "routine checkup", "allergy", "prescription"],
      "source_ids": ["SRC_003"]
    },
    "ENT": {
      "department_id": "ent",
      "aliases": ["ear nose throat", "otorhinolaryngology", "ENT specialist", "hearing clinic", "audiology"],
      "guidelines": [
        "Note whether the problem affects the right ear, left ear, both ears, one side of the nose, or both sides, and record when it began.",
        "Describe relevant symptoms such as hearing difficulty, ringing in the ears, ear pain, discharge, dizziness, nasal blockage, sinus symptoms, sore throat, or voice changes.",
        "Bring your hearing aids or other usual hearing devices if you use them.",
        "Do not stop prescribed ear drops, nasal sprays, or other medicines unless the prescribing clinician tells you to. Tell the ENT specialist about all products you use."
      ],
      "conditional_guidelines": [
        {
          "when": "A formal hearing test or audiometry appointment is scheduled.",
          "instruction": "Avoid loud noise exposure, including loud music and high-volume headphones, for about 24 hours before the test if possible. If you have a cold or ear infection, contact the audiology clinic because it may affect testing or scheduling."
        }
      ],
      "what_to_bring": [
        "Photo identification accepted by the hospital and appointment confirmation.",
        "Previous hearing tests, audiograms, ENT reports, or relevant sinus/ear imaging, if available.",
        "A list of current medicines, ear drops, nasal sprays, and known allergies.",
        "Hearing aids or other hearing devices, if used."
      ],
      "safety_notes": [
        "Do not instruct patients to discontinue prescribed ear drops or nasal sprays before a routine ENT consultation.",
        "Avoid inserting objects into the ear canal or attempting aggressive ear cleaning as appointment preparation."
      ],
      "keywords": ["ear pain", "hearing loss", "ringing ear", "tinnitus", "vertigo", "dizziness", "sinus", "nasal blockage", "throat pain", "voice", "audiometry", "hearing test", "ear drops"],
      "source_ids": ["SRC_004"]
    },
    "Cardiology": {
      "department_id": "cardiology",
      "aliases": ["heart specialist", "heart clinic", "cardiac clinic", "cardiologist"],
      "guidelines": [
        "Record the timing, duration, and pattern of symptoms such as chest discomfort, palpitations, breathlessness, dizziness, or reduced exercise tolerance.",
        "Bring a home blood pressure or heart-rate log if you maintain one.",
        "Wear comfortable clothing that allows access to the chest if an examination or ECG is planned.",
        "Tell the cardiologist about all current medicines, including exact doses and timing, and any previous heart conditions or procedures.",
        "Do not stop heart medicines or change caffeine, nicotine, or other routines solely because of a routine consultation unless the clinician or test centre has instructed you."
      ],
      "conditional_guidelines": [
        {
          "when": "A resting ECG is scheduled.",
          "instruction": "Wear clothing that allows access to the chest and follow any instructions from the ECG unit. Avoid applying lotions, oils, or powder to the areas where electrodes may be attached if possible."
        },
        {
          "when": "An exercise ECG or cardiac stress test is scheduled.",
          "instruction": "Follow the testing centre's specific preparation instructions. The centre may ask you to avoid caffeine or a heavy meal before the test. Do not apply routine consultation instructions to this test, and do not stop medicines unless the cardiology team explicitly tells you to."
        }
      ],
      "what_to_bring": [
        "Photo identification accepted by the hospital and appointment confirmation.",
        "Previous ECG, echocardiogram (2D Echo), Holter monitor, stress-test, angiography, or hospital-discharge reports, if available.",
        "A current cardiac medication list showing exact doses and timing.",
        "Home blood pressure and heart-rate readings, if available.",
        "Health insurance documents, if applicable."
      ],
      "safety_notes": [
        "Do not state that fasting or caffeine avoidance is mandatory for every cardiology consultation or routine resting ECG.",
        "Do not tell patients to stop blood thinners, blood pressure medicines, or other cardiac medicines without explicit clinician instructions.",
        "Potentially emergency symptoms must be handled using the hospital's emergency escalation policy, not routine appointment-preparation advice."
      ],
      "keywords": ["chest pain", "palpitations", "heart", "blood pressure", "ECG", "EKG", "2D echo", "echocardiogram", "Holter", "stress test", "cardiac", "heart rate", "angiography"],
      "source_ids": ["SRC_005"]
    },
    "Dermatology": {
      "department_id": "dermatology",
      "aliases": ["skin specialist", "skin clinic", "dermatologist"],
      "guidelines": [
        "Note when the skin, hair, or nail problem first appeared, where it started, whether it has spread, and whether it comes and goes.",
        "Record possible triggers such as new skincare products, soaps, cosmetics, medicines, foods, or workplace exposures when relevant.",
        "For an examination of the skin or nails, avoid makeup, nail polish, and heavy cosmetic products on the area being assessed where practical.",
        "Do not stop prescribed creams, ointments, or other treatments unless the prescribing clinician tells you to. Bring their names or photographs of the labels."
      ],
      "conditional_guidelines": [
        {
          "when": "The patient is attending for assessment of a changing or intermittent skin problem.",
          "instruction": "Photographs showing how the affected area looked at different times may help explain changes, especially if the appearance varies before the appointment."
        }
      ],
      "what_to_bring": [
        "Photo identification accepted by the hospital and appointment confirmation.",
        "Previous skin biopsy, allergy-test, or relevant laboratory reports, if available.",
        "A list or photographs of current skincare products, cosmetics, soaps, and topical medicines.",
        "A current medication list and known allergy details, including previous reactions."
      ],
      "safety_notes": [
        "Do not tell patients to discontinue prescribed topical medicines before the visit. The dermatologist may want to know exactly what has been used.",
        "Avoid making a diagnosis based only on a patient's description or photographs."
      ],
      "keywords": ["rash", "itching", "acne", "pimples", "eczema", "psoriasis", "hair loss", "skin allergy", "mole", "pigmentation", "nail problem", "biopsy", "skin specialist"],
      "source_ids": ["SRC_006"]
    },
    "Ophthalmology": {
      "department_id": "ophthalmology",
      "aliases": ["eye specialist", "eye doctor", "ophthalmologist", "eye clinic"],
      "guidelines": [
        "Bring your current prescription glasses and details of any contact lenses you use.",
        "Note changes in vision, which eye is affected, when the change began, and any eye pain, redness, flashes, floaters, or light sensitivity.",
        "Tell the eye doctor about previous eye injuries, eye surgery, and current eye drops or other medicines."
      ],
      "conditional_guidelines": [
        {
          "when": "Pupil dilation is planned or may be part of the examination.",
          "instruction": "Bring sunglasses because the eyes may become sensitive to bright light. Dilating drops can cause temporary blurry vision and light sensitivity for several hours, and the duration varies. Arrange transport if possible. Do not drive, ride a two-wheeler, cycle, or operate machinery while your vision is blurred or otherwise unsafe."
        },
        {
          "when": "The patient wears contact lenses and may need to remove them for the examination.",
          "instruction": "Bring a contact lens case and solution, if applicable, and follow the eye clinic's instructions about lens use."
        }
      ],
      "what_to_bring": [
        "Photo identification accepted by the hospital and appointment confirmation.",
        "Current prescription glasses and contact lens details; case and solution if applicable.",
        "Previous eye examination reports, prescriptions, scan results, and eye-surgery records, if available.",
        "A list of current eye drops and other medicines."
      ],
      "safety_notes": [
        "Do not promise that dilation-related blurriness will end within a fixed number of hours.",
        "Do not advise driving after dilation when the patient's vision is blurred or light sensitivity makes driving unsafe."
      ],
      "keywords": ["eye pain", "blurred vision", "vision test", "glasses", "contact lenses", "red eye", "cataract", "glaucoma", "retina", "dilation", "eye drops", "ophthalmologist"],
      "source_ids": ["SRC_007"]
    },
    "Neurology": {
      "department_id": "neurology",
      "aliases": ["brain specialist", "nerve specialist", "neurologist", "neurology clinic"],
      "guidelines": [
        "Record when symptoms began, how often they occur, how long they last, and whether they are changing over time.",
        "Note possible triggers and any relationship between symptoms and medication timing, sleep, meals, or activities.",
        "For headaches, note frequency, duration, location, severity, associated symptoms, and medicines taken, if known.",
        "Get your usual rest before the appointment where possible; do not intentionally skip regular medicines to prepare for the consultation.",
        "Consider bringing a trusted adult if you have experienced fainting, seizures, significant dizziness, memory difficulty, or balance problems."
      ],
      "conditional_guidelines": [
        {
          "when": "The patient has had previous brain imaging or neurological tests.",
          "instruction": "Bring the reports and image files for MRI or CT scans, and previous EEG or other neurological test reports, if available."
        }
      ],
      "what_to_bring": [
        "Photo identification accepted by the hospital and appointment confirmation.",
        "Previous brain MRI or CT reports and image files, EEG reports, and other relevant neurological test results, if available.",
        "A current medication list with doses and timing, including over-the-counter medicines and supplements.",
        "A headache, seizure, dizziness, or other symptom diary, if maintained.",
        "Relevant previous consultation notes and mobility aids, if used."
      ],
      "safety_notes": [
        "Do not advise patients to stop anti-seizure medicines or other neurological medicines before a routine consultation.",
        "Do not interpret an EEG, MRI, or CT result as a diagnosis; refer interpretation to the treating clinician."
      ],
      "keywords": ["headache", "migraine", "seizure", "epilepsy", "fainting", "dizziness", "vertigo", "numbness", "tingling", "weakness", "tremor", "memory", "MRI brain", "CT brain", "EEG"],
      "source_ids": ["SRC_008"]
    },
    "Gastroenterology": {
      "department_id": "gastroenterology",
      "aliases": ["gastro", "GI specialist", "digestive specialist", "stomach specialist", "gastro clinic"],
      "guidelines": [
        "Note the type of digestive symptoms, when they occur, how long they have been present, and whether they are related to meals or bowel movements.",
        "Record relevant changes in appetite, bowel habits, weight, or symptom triggers when known.",
        "Bring details of previous digestive conditions, abdominal procedures, and treatments.",
        "Do not fast for a routine gastroenterology consultation unless the clinic has specifically instructed you to do so."
      ],
      "conditional_guidelines": [
        {
          "when": "An abdominal ultrasound, upper endoscopy, colonoscopy, or another GI investigation/procedure is scheduled.",
          "instruction": "Obtain the exact written preparation instructions for the named test from the performing facility. Fasting, permitted fluids, bowel preparation, diet changes, and medication instructions vary by procedure and patient. Do not start bowel preparation or stop/change medicines, including blood thinners or diabetes medicines, without instructions from the treating team."
        }
      ],
      "what_to_bring": [
        "Photo identification accepted by the hospital and appointment confirmation.",
        "Previous endoscopy, colonoscopy, abdominal ultrasound, CT, or other relevant investigation reports, if available.",
        "Recent blood test results, including liver-function tests, if available and relevant.",
        "A current medication list, including blood thinners, diabetes medicines, pain medicines, and supplements.",
        "Known allergies, previous abdominal surgery records, and health insurance documents, if applicable."
      ],
      "safety_notes": [
        "Never provide a generic fasting duration for all gastroenterology visits or procedures.",
        "Do not advise patients to independently stop anticoagulants, antiplatelet medicines, insulin, diabetes tablets, or other regular medicines before a procedure.",
        "Colonoscopy bowel preparation and endoscopy fasting instructions must come from the facility performing the procedure."
      ],
      "keywords": ["stomach pain", "acidity", "heartburn", "reflux", "constipation", "diarrhea", "bloating", "vomiting", "digestive problem", "liver", "endoscopy", "colonoscopy", "ultrasound", "GI"],
      "source_ids": ["SRC_009", "SRC_010"]
    }
  },
  "sources": [
    {
      "source_id": "SRC_001",
      "title": "Your Visit With an Orthopaedic Surgeon",
      "publisher": "OrthoInfo / American Academy of Orthopaedic Surgeons",
      "url": "https://www.orthoinfo.org/treatment/your-visit-with-an-orthopaedic-surgeon/",
      "supports": ["Medication lists", "Previous imaging and reports", "Preparing for an orthopaedic consultation"]
    },
    {
      "source_id": "SRC_002",
      "title": "Preparing for Your Visit With an Orthopaedic Surgeon",
      "publisher": "OrthoInfo / American Academy of Orthopaedic Surgeons",
      "url": "https://www.orthoinfo.org/treatment/surgical-treatment/getting-the-most-out-of-your-doctors-visit/",
      "supports": ["Symptom and treatment history", "Loose clothing", "Arriving early", "Medical records"]
    },
    {
      "source_id": "SRC_003",
      "title": "Fasting for a Blood Test",
      "publisher": "MedlinePlus / U.S. National Library of Medicine",
      "url": "https://www.medlineplus.gov/lab-tests/fasting-for-a-blood-test/",
      "supports": ["Fasting only when instructed", "Test-specific fasting duration", "Checking instructions with the provider"]
    },
    {
      "source_id": "SRC_004",
      "title": "Preparing for Your Hearing Test",
      "publisher": "UCSF EARS Program",
      "url": "https://ears.ucsf.edu/en/getting-care-guide/first-visit-preparation",
      "supports": ["Avoiding loud noise before a scheduled hearing test", "Contacting the clinic about cold or ear infection"]
    },
    {
      "source_id": "SRC_005",
      "title": "Electrocardiogram (ECG)",
      "publisher": "NHS",
      "url": "https://www.nhs.uk/tests-and-treatments/electrocardiogram/",
      "supports": ["ECG preparation", "Clothing", "Exercise ECG and caffeine/heavy meal considerations"]
    },
    {
      "source_id": "SRC_006",
      "title": "How to Select a Dermatologist",
      "publisher": "American Academy of Dermatology",
      "url": "https://www.aad.org/public/fad/how-to-select-a-derm",
      "supports": ["Avoiding makeup and heavy products for skin examination", "Bringing previous test results"]
    },
    {
      "source_id": "SRC_007",
      "title": "What Are Dilating Eye Drops?",
      "publisher": "American Academy of Ophthalmology",
      "url": "https://www.aao.org/eye-health/Drugs/dilating-eyedrops",
      "supports": ["Variable duration of dilation effects", "Blurred vision", "Light sensitivity", "Sunglasses and transport planning"]
    },
    {
      "source_id": "SRC_008",
      "title": "Guide to Preparing for Doctors Appointments",
      "publisher": "Parkinson's Foundation",
      "url": "https://www.psp.org/assets/uploads/2024/06/66675818703b3GuideToPreparingForDoctorsAppointments.pdf",
      "supports": ["Neurological symptom history", "Medication list", "Previous scans and test results", "Bringing a companion"]
    },
    {
      "source_id": "SRC_009",
      "title": "Patient Corner: Preparation Instructions",
      "publisher": "GastroPlus Digestive Disease Centre, India",
      "url": "https://www.gastroplusindia.com/patient-corner/",
      "supports": ["Procedure-specific fasting, medication, and bowel preparation instructions"]
    },
    {
      "source_id": "SRC_010",
      "title": "Endoscopy Preparation Instructions",
      "publisher": "American College of Gastroenterology",
      "url": "https://webfiles.gi.org/links/pm/ACGEndoscopyManual.pdf",
      "supports": ["Colonoscopy bowel preparation", "Procedure- and sedation-specific fasting instructions"]
    }
  ]
}
]



def get_structured_dept_info(department_name: str) -> dict:
    """Returns structured guidelines for a department."""
    knowledge_base = HOSPITAL_KB_STRUCTURED[0]
    normalized_name = "".join(
        character for character in department_name.casefold() if character.isalnum()
    )

    matched_name = department_name
    department_info = None
    for name, info in knowledge_base["departments"].items():
        candidates = [name, info["department_id"], *info["aliases"]]
        if any(
            normalized_name
            == "".join(character for character in candidate.casefold() if character.isalnum())
            for candidate in candidates
        ):
            matched_name = name
            department_info = info
            break

    if department_info is None:
        department_info = {
            "guidelines": ["Follow preparation instructions provided by your clinic."],
            "conditional_guidelines": [],
            "what_to_bring": [],
            "safety_notes": [],
        }

    return {
        **department_info,
        "department": matched_name,
        "global_safety_rules": knowledge_base["global_safety_rules"],
    }



def get_department_info(department_name: str) -> str:
    """Legacy RAG string output generator."""
    info = get_structured_dept_info(department_name)
    guidelines_str = "\n".join([f"- {g}" for g in info["guidelines"]])
    bring_str = "\n".join([f"- {b}" for b in info["what_to_bring"]])
    safety_rules = [
        rule["rule"] for rule in info["global_safety_rules"]
    ] + info["safety_notes"]
    safety_str = "\n".join(f"- {rule}" for rule in safety_rules)
    
    return (
        f"INTAKE INSTRUCTIONS:\n{guidelines_str}\n\n"
        f"SAFETY NOTES:\n{safety_str}\n\n"
        f"WHAT TO BRING:\n{bring_str}"
    )


if __name__ == "__main__":
    print(get_structured_dept_info("ENT"))

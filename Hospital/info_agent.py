# Structured Hospital Outpatient Knowledge Base for RAG Information Agent
# Covers all 25 Hospital Departments with OPD | IPD | ICU Care Tiers

HOSPITAL_KB_STRUCTURED = [
{
  "metadata": {
    "knowledge_base_name": "Outpatient & Inpatient Clinical Care Knowledge Base",
    "schema_version": "4.0.0",
    "language": "en-IN",
    "prepared_on": "2026-11-18",
    "clinical_approval_status": "Approved for LifeCare Outpatient & Emergency Triage",
    "scope": "Comprehensive preparation guidelines for 25 hospital departments across OPD, IPD, and ICU.",
    "important_note": "This knowledge base provides preparation and navigation information only. It must not diagnose conditions or replace direct clinician orders."
  },
  "global_safety_rules": [
    {
      "id": "GLOBAL_001",
      "rule": "Do not advise fasting for routine consultation unless an explicit fasting procedure or fasting lab panel has been ordered by the physician."
    },
    {
      "id": "GLOBAL_002",
      "rule": "Never tell a patient to start, stop, or adjust prescription medicines (including cardiac, blood thinner, epilepsy, or inhaler drugs) without direct clinician instructions."
    },
    {
      "id": "GLOBAL_003",
      "rule": "Arrive 10 to 15 minutes before the scheduled time slot for nursing vital checks and registration verification at Block B."
    },
    {
      "id": "GLOBAL_004",
      "rule": "If acute life-threatening symptoms (chest pain, severe breathlessness, uncontrolled bleeding, sudden numbness) emerge before your appointment, go directly to the 24/7 Emergency Department."
    }
  ],
  "departments": {
    "General Medicine": {
      "department_id": "general_medicine",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Write down your primary symptoms, timeline of occurrence, and any recorded temperature or blood pressure readings.",
        "Disclose all known allergies to medications, foods, or environmental substances.",
        "Do not fast merely for a general consultation unless specifically booked for fasting blood sugar tests.",
        "Bring a trusted family member or caregiver if feeling weak or unsteady."
      ],
      "what_to_bring": [
        "Government Photo ID and LifeCare appointment confirmation.",
        "Current medication bottles, dosage strips, or prescriptions.",
        "Recent laboratory reports (complete blood counts, metabolic panels) from the past 6 months."
      ],
      "safety_notes": ["Persistent high fever (>103°F) with neck stiffness or confusion requires urgent medical escalation."]
    },
    "General Surgery": {
      "department_id": "general_surgery",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Wear loose, easily removable clothing to facilitate physical examination of the abdomen, groin, or surgical site.",
        "Note how long the lump, swelling, or abdominal pain has been present and whether it increases when coughing or standing.",
        "Do not apply topical ointments or bandages over fresh wounds right before surgical inspection."
      ],
      "what_to_bring": [
        "Previous abdominal ultrasound, CT scan reports, or biopsy records if available.",
        "List of all regular medications, especially blood thinners (aspirin, clopidogrel, warfarin).",
        "Previous surgical discharge summaries if evaluating a post-operative site."
      ],
      "safety_notes": ["Sudden severe abdominal pain with rigid abdomen, high fever, or vomiting requires immediate emergency evaluation."]
    },
    "Emergency Medicine": {
      "department_id": "emergency_medicine",
      "care_levels": {"opd": True, "ipd": True, "icu": True},
      "guidelines": [
        "Emergency cases are prioritized strictly by clinical triage acuity, not arrival order.",
        "Report immediately to the Emergency Red Triage Desk upon arrival at the hospital casualty gate.",
        "Family members must notify the triage nurse immediately if the patient's breathing worsens or consciousness drops."
      ],
      "what_to_bring": [
        "Any immediately accessible identification and current medication list.",
        "Do not delay reporting to gather documents; life-saving stabilization takes precedence."
      ],
      "safety_notes": ["Immediate priority resuscitation area. In transit, call 112 / 108 for advanced life-support ambulance support."]
    },
    "Cardiology": {
      "department_id": "cardiology",
      "care_levels": {"opd": True, "ipd": True, "icu": True},
      "guidelines": [
        "Wear comfortable two-piece clothing allowing easy access to the chest for routine ECG recording.",
        "Keep a log of when palpitations, tightness, or shortness of breath occur.",
        "Do not stop blood pressure or cardiac medication unless explicitly ordered by your physician."
      ],
      "what_to_bring": [
        "Previous ECG tracings, 2D Echocardiogram reports, or Holter monitor summaries.",
        "Complete and accurate cardiac medication list with exact milligram dosages.",
        "Recent home blood pressure readings and heart rate recordings."
      ],
      "safety_notes": ["Crushing chest pain radiating to left arm or jaw with cold sweats requires immediate ER admission (Dial 112)."]
    },
    "Neurology": {
      "department_id": "neurology",
      "care_levels": {"opd": True, "ipd": True, "icu": True},
      "guidelines": [
        "Prepare a chronological timeline of symptoms: headaches, seizures, sensory tingling, tremors, or memory changes.",
        "Bring an accompanying family member or witness if episodes involve fainting, disorientation, or blackouts.",
        "Ensure adequate rest before consultation; do not skip prescribed anti-seizure medicines."
      ],
      "what_to_bring": [
        "All previous Brain MRI, Spine MRI, or CT scan films and digital discs.",
        "Past EEG recordings, nerve conduction studies (NCS), or EMG reports.",
        "Complete list of neurological, psychiatric, or sleep medications."
      ],
      "safety_notes": ["Sudden facial droop, arm weakness, or slurred speech are acute stroke signs: call 112 / 108 immediately."]
    },
    "Neurosurgery": {
      "department_id": "neurosurgery",
      "care_levels": {"opd": True, "ipd": True, "icu": True},
      "guidelines": [
        "Bring all original MRI and CT scan image discs (DICOM format) and paper radiological reports.",
        "Note any progressive weakness in limbs, bowel or bladder incontinence, or numbness.",
        "Ensure an adult family member accompanies the patient for clinical discussion of surgical options."
      ],
      "what_to_bring": [
        "Neuro-imaging films and digital CD/USB of brain or spine scans.",
        "Electromyography (EMG) or nerve conduction studies (NCS) reports.",
        "Prior operative notes if patient has undergone previous spinal or cranial surgery."
      ],
      "safety_notes": ["Sudden severe headache with vomiting, unequal pupils, or loss of consciousness requires emergency admission."]
    },
    "Orthopaedics": {
      "department_id": "orthopaedics",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Wear loose, comfortable clothing that allows easy examination of the affected joint, back, or limb.",
        "Note which specific movement triggers discomfort and whether swelling or stiffness is worse in the morning.",
        "Bring and use your usual walking aid, knee brace, or orthotic support if applicable."
      ],
      "what_to_bring": [
        "Hospital registration ID or appointment pass.",
        "Previous X-ray, MRI, or CT scan films and digital reports if available.",
        "List of all current medications, analgesics, and bone supplements."
      ],
      "safety_notes": ["Inability to bear any weight accompanied by bone deformity or open skin break requires emergency room care."]
    },
    "Pediatrics": {
      "department_id": "pediatrics",
      "care_levels": {"opd": True, "ipd": True, "icu": True},
      "guidelines": [
        "Keep the child comfortable and bring a favorite toy or blanket to ease anxiety during clinical examination.",
        "Record the exact temperature readings, times taken, and fluid intake / urine output over the past 24 hours.",
        "Do not give over-the-counter cold medicines or adult analgesics to infants or children without pediatric prescription."
      ],
      "what_to_bring": [
        "Child's official immunization / vaccination record booklet.",
        "Birth history summary if infant is under 1 year old.",
        "Any current syrup bottles, dosage syringes, or nebulizer medicines."
      ],
      "safety_notes": ["Lethargy, refusal to feed, blue discoloration around lips, or breathing with chest retractions requires immediate pediatric emergency care."]
    },
    "Obstetrics & Gynecology": {
      "department_id": "obstetrics_gynecology",
      "care_levels": {"opd": True, "ipd": True, "icu": True},
      "guidelines": [
        "Note the first day of your last menstrual period (LMP) and the regularity of your cycle.",
        "Wear comfortable two-piece clothing suitable for pelvic or abdominal physical examination.",
        "Record any obstetric history including previous pregnancies, deliveries, or miscarriages."
      ],
      "what_to_bring": [
        "Previous pelvic ultrasound, Pap smear, or mammogram reports.",
        "Antenatal records and blood test reports if pregnant.",
        "List of iron, calcium, folic acid, or hormone supplements."
      ],
      "safety_notes": ["Heavy vaginal bleeding (soaking more than two pads per hour) or severe sudden pelvic pain requires emergency medical care."]
    },
    "Psychiatry": {
      "department_id": "psychiatry",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "All consultations are completely confidential and conducted in a private, supportive clinical setting.",
        "You are welcome to bring a trusted family member or attend the session independently.",
        "Note how your sleep, appetite, energy, and daily functioning have been affected."
      ],
      "what_to_bring": [
        "List of any psychotropic medications, sleep aids, or mood stabilizers previously taken.",
        "Records of past psychotherapy, counseling, or psychiatric evaluations.",
        "Government ID and emergency family contact details."
      ],
      "safety_notes": ["If you are experiencing acute thoughts of self-harm, call Tele-MANAS (14416) or national emergency (112) immediately."]
    },
    "Dermatology": {
      "department_id": "dermatology",
      "care_levels": {"opd": True, "ipd": False, "icu": False},
      "guidelines": [
        "Avoid applying heavy makeup, thick ointments, or concealers over the affected skin area on the appointment day.",
        "Take clear photos of the rash or lesion if it tends to fluctuate or flare up intermittently.",
        "Note any recent changes in soaps, detergents, cosmetics, or new oral medications."
      ],
      "what_to_bring": [
        "List of all topical creams, ointments, lotions, and soaps currently used.",
        "Previous biopsy reports or allergy patch test findings.",
        "Photographs of earlier lesion stages if condition has transformed."
      ],
      "safety_notes": ["Rapidly spreading rash with high fever or blistering of lips/mouth requires immediate urgent medical evaluation."]
    },
    "Ophthalmology": {
      "department_id": "ophthalmology",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Bring all pairs of currently used eyeglasses and contact lens boxes.",
        "Arrange for an accompanying person or cab ride home, as pupil-dilating drops may temporarily blur near vision for 2-4 hours.",
        "Bring sunglasses to minimize glare sensitivity after pupil dilation."
      ],
      "what_to_bring": [
        "Current glasses prescription and eye drop medications.",
        "Previous visual field, OCT, or glaucoma pressure records.",
        "Sunglasses for comfortable post-dilation travel."
      ],
      "safety_notes": ["Sudden painless vision loss or sensation of curtain falling over eyes requires immediate emergency eye care."]
    },
    "ENT (Otolaryngology)": {
      "department_id": "ent",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Note whether symptoms affect right, left, or both ears/nostrils, and the exact duration of symptoms.",
        "Bring existing hearing aids or ear moulds if you use them.",
        "Avoid using cotton swabs or probing inside the ear canal before your appointment."
      ],
      "what_to_bring": [
        "Appointment pass and ID.",
        "Previous audiograms, hearing evaluations, or sinus CT scan reports.",
        "Current nasal sprays, antihistamines, or ear drop bottles."
      ],
      "safety_notes": ["Sudden acute loss of hearing or severe nosebleed that does not stop after 15 minutes of firm pressure requires emergency care."]
    },
    "Urology": {
      "department_id": "urology",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Arrive with a comfortably full bladder if an outpatient pelvic or urinary tract ultrasound is scheduled.",
        "Note your urinary stream strength, frequency of nighttime urination, and any burning sensations.",
        "Disclose any history of kidney stones or prior urinary tract catheterizations."
      ],
      "what_to_bring": [
        "Recent Urine Routine & Microscopy and Urine Culture sensitivity reports.",
        "Serum Creatinine, Blood Urea Nitrogen (BUN), or PSA test reports.",
        "Ultrasound KUB (Kidney, Ureter, Bladder) or CT KUB scan images and reports."
      ],
      "safety_notes": ["Complete inability to pass urine (acute urinary retention) with severe lower abdominal pain is an emergency."]
    },
    "Nephrology": {
      "department_id": "nephrology",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Bring a record of your daily fluid intake and 24-hour urine volume if you have been asked to measure it.",
        "Do not skip regular blood pressure medications on the morning of your clinic visit.",
        "Note any swelling in feet, ankles, or around the eyes upon waking up."
      ],
      "what_to_bring": [
        "Serial blood tests showing Serum Creatinine, Blood Urea, and Electrolytes over time.",
        "Urine protein / creatinine ratio or 24-hour urinary protein estimation reports.",
        "Renal ultrasound Doppler or biopsy reports if available."
      ],
      "safety_notes": ["Severe shortness of breath with high blood pressure and inability to pass urine indicates acute fluid overload requiring emergency dialysis evaluation."]
    },
    "Gastroenterology": {
      "department_id": "gastroenterology",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Note the relation of pain or discomfort to food intake (before meals, immediately after, or during night).",
        "Record bowel movement frequency and notice any changes in stool color or consistency.",
        "Do not fast for a routine OPD consultation unless scheduled specifically for upper endoscopy or ultrasound."
      ],
      "what_to_bring": [
        "Previous endoscopy or colonoscopy procedural reports and biopsy findings.",
        "Recent abdominal ultrasound or CT scan reports.",
        "Liver function test (LFT) and recent complete blood count records."
      ],
      "safety_notes": ["Vomiting blood or passing black tarry stools is an emergency requiring immediate ER evaluation."]
    },
    "Pulmonology / Respiratory Medicine": {
      "department_id": "pulmonology",
      "care_levels": {"opd": True, "ipd": True, "icu": True},
      "guidelines": [
        "Bring all current inhalers, nebulizer solutions, and spacer devices for technique review.",
        "Avoid smoking or heavy physical exertion for at least 2 hours before pulmonary function testing.",
        "Wear loose, unrestrictive clothing that facilitates deep breathing during chest examination."
      ],
      "what_to_bring": [
        "Previous Chest X-rays, HRCT Chest scans, or Spirometry / PFT printouts.",
        "List of all oral bronchodilators, steroids, and allergy medicines.",
        "Home pulse oximeter readings and peak flow diary if maintained."
      ],
      "safety_notes": ["Severe breathlessness with inability to speak full sentences or cyanosis requires immediate emergency triage."]
    },
    "Endocrinology": {
      "department_id": "endocrinology",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Bring your glucometer and blood glucose log (fasting and post-meal readings) for the last 2-4 weeks.",
        "Take your morning thyroid medication as usual with water unless a specific laboratory draw requires fasting.",
        "Note any sudden unexplained weight fluctuations, excessive sweating, or extreme fatigue."
      ],
      "what_to_bring": [
        "Recent HbA1c, Thyroid Profile (TSH, Free T3/T4), and lipid panel reports.",
        "Current insulin pens, dosage schedule, and oral hypoglycemic tablets.",
        "Records of previous DEXA bone density scans or endocrine workups."
      ],
      "safety_notes": ["Symptoms of severe hypoglycemia (shakiness, cold sweat, confusion) require immediate intake of fast-acting sugar."]
    },
    "Rheumatology": {
      "department_id": "rheumatology",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Note which specific joints are painful, swollen, or stiff, and how long morning stiffness lasts.",
        "Photograph any transient skin rashes, mouth sores, or color changes in fingers when exposed to cold.",
        "Do not stop prescribed DMARDs (methotrexate, sulfasalazine) without clinical discussion."
      ],
      "what_to_bring": [
        "Recent inflammatory blood markers: ESR, CRP, Rheumatoid Factor (RF), and Anti-CCP reports.",
        "Autoimmune antibody profiles: ANA (Antinuclear Antibodies), ENA panel if conducted.",
        "X-rays of hands, feet, or affected joints."
      ],
      "safety_notes": ["Sudden acute joint redness, swelling, and high fever may indicate septic arthritis requiring urgent emergency aspiration."]
    },
    "Hematology": {
      "department_id": "hematology",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Do not stop any prescribed blood thinners, anticoagulants, or iron supplements unless instructed by your physician.",
        "Keep a clear record of when abnormal bruising, bleeding gums, nosebleeds, or extreme tiredness began.",
        "Avoid taking aspirin or NSAID painkillers right before evaluation without doctor approval."
      ],
      "what_to_bring": [
        "Recent Complete Blood Count (CBC / Hemogram) with peripheral smear and platelet count reports.",
        "Coagulation profile reports (PT / INR / aPTT) if previously conducted.",
        "List of all current medications, over-the-counter painkillers, blood thinners, and herbal supplements."
      ],
      "safety_notes": ["Nosebleeds that cannot be stopped after 20 minutes of direct pressure or widespread petechial rashes require immediate emergency care."]
    },
    "Oncology": {
      "department_id": "oncology",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Bring all original histopathology tissue biopsy reports, immunohistochemistry (IHC) markers, and molecular genetic testing.",
        "Ensure an adult family member accompanies the patient for multidisciplinary care planning.",
        "Maintain a detailed record of current functional energy level, appetite, and pain scores."
      ],
      "what_to_bring": [
        "All PET-CT scan CDs and written reports, diagnostic MRI/CT films, and surgical pathology blocks if available.",
        "Summaries of previous chemotherapy cycles, radiation therapy records, or surgery notes.",
        "Full list of ongoing prescription medications, pain medicines, and nutritional supplements."
      ],
      "safety_notes": ["Fever in a patient currently undergoing chemotherapy (neutropenic fever) is a medical emergency requiring immediate hospitalization."]
    },
    "Anesthesiology": {
      "department_id": "anesthesiology",
      "care_levels": {"opd": False, "ipd": False, "icu": True},
      "guidelines": [
        "Attend the Pre-Anesthesia Checkup (PAC) clinic prior to scheduled elective surgical procedures.",
        "Disclose all prior anesthesia experiences, family history of adverse anesthesia reactions, and loose dental teeth or crowns.",
        "Follow precise NPO (fasting) instructions provided by the surgical team."
      ],
      "what_to_bring": [
        "PAC evaluation clearance slip from the attending surgeon.",
        "Recent ECG, Chest X-ray, and comprehensive pre-operative blood investigation panel.",
        "Cardiology or Pulmonology specialty clearance letters if patient has heart or lung disease."
      ],
      "safety_notes": ["Strict adherence to preoperative fasting times is mandatory to prevent pulmonary aspiration during anesthesia induction."]
    },
    "Critical Care Medicine": {
      "department_id": "critical_care_medicine",
      "care_levels": {"opd": False, "ipd": False, "icu": True},
      "guidelines": [
        "Direct admission and transfer facility for patients experiencing acute organ failure or severe shock.",
        "Strict sterile entry protocols apply for visiting family members during designated ICU counseling hours.",
        "Continuous 1:1 nursing monitoring and multi-parameter vital telemetry active 24/7."
      ],
      "what_to_bring": [
        "Primary contact person contact details and hospital registration file.",
        "Insurance cashless pre-authorization documents for intensive care."
      ],
      "safety_notes": ["Emergency intensive care unit reserved for life-threatened and hemodynamically unstable patients."]
    },
    "Dentistry / Oral Surgery": {
      "department_id": "dentistry_oral_surgery",
      "care_levels": {"opd": True, "ipd": False, "icu": False},
      "guidelines": [
        "Brush and rinse your teeth before attending your dental consultation.",
        "Disclose if you are taking blood thinners (aspirin, clopidogrel) or bone-density medications (bisphosphonates) before extractions.",
        "Note whether tooth sensitivity occurs with hot liquids, cold drinks, or sweets."
      ],
      "what_to_bring": [
        "Previous dental X-rays (OPG / Intra-Oral Periapical radiographs) if available.",
        "Details of past dental procedures (root canals, crowns, implants, or braces).",
        "Medication list and allergy history."
      ],
      "safety_notes": ["Rapidly swelling facial swelling with high fever or difficulty opening mouth/swallowing requires urgent surgical assessment."]
    },
    "Physiotherapy / Rehabilitation": {
      "department_id": "physiotherapy_rehabilitation",
      "care_levels": {"opd": True, "ipd": True, "icu": False},
      "guidelines": [
        "Wear loose athletic or comfortable stretchable clothing and supportive walking shoes.",
        "Do not take heavy doses of pain relievers right before your therapy session so true physical limits can be evaluated.",
        "Inform the physiotherapist if exercises cause sharp pain or dizziness during movements."
      ],
      "what_to_bring": [
        "Physician or orthopaedic referral slip recommending physical therapy.",
        "Recent post-surgical protocols, fracture union X-rays, or MRI spine reports.",
        "Mobility aids (crutches, walker, braces) currently in use."
      ],
      "safety_notes": ["Sudden chest pain, acute shortness of breath, or loss of balance during rehabilitation exercises requires immediate medical evaluation."]
    }
  }
}
]


def get_structured_dept_info(department_name: str) -> dict:
    """Returns structured guidelines and preparation for any of the 25 requested departments."""
    knowledge_base = HOSPITAL_KB_STRUCTURED[0]
    norm_query = "".join(ch for ch in (department_name or "").casefold() if ch.isalnum())

    matched_name = "General Medicine"
    department_info = knowledge_base["departments"]["General Medicine"]

    for name, info in knowledge_base["departments"].items():
        candidates = [name, info.get("department_id", "")]
        if any(norm_query == "".join(ch for ch in cand.casefold() if ch.isalnum()) for cand in candidates):
            matched_name = name
            department_info = info
            break

    # Substring search if not exact
    if department_info == knowledge_base["departments"]["General Medicine"] and norm_query != "generalmedicine":
        for name, info in knowledge_base["departments"].items():
            candidates = [name, info.get("department_id", "")]
            if any(norm_query in "".join(ch for ch in c.casefold() if ch.isalnum()) for c in candidates):
                matched_name = name
                department_info = info
                break

    return {
        **department_info,
        "department": matched_name,
        "global_safety_rules": [r["rule"] for r in knowledge_base["global_safety_rules"]],
    }


def get_department_info(department_name: str) -> str:
    """Generates clean RAG text advisory for LLM and UI views."""
    info = get_structured_dept_info(department_name)
    guidelines_str = "\n".join([f"- {g}" for g in info.get("guidelines", [])])
    bring_str = "\n".join([f"- {b}" for b in info.get("what_to_bring", [])])
    safety_str = "\n".join([f"- {s}" for s in (info.get("safety_notes", []) + info.get("global_safety_rules", []))])

    return (
        f"INTAKE PREPARATION FOR {info.get('department', department_name).upper()}:\n{guidelines_str}\n\n"
        f"WHAT TO BRING TO HOSPITAL:\n{bring_str}\n\n"
        f"CLINICAL SAFETY NOTES:\n{safety_str}"
    )

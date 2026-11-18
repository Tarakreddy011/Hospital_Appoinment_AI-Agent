import re
from typing import Tuple, Optional, Dict, Any, List
from groq_client import call_groq_chat

# Complete Hospital Departments Configuration with Care Levels (OPD | IPD | ICU)
DEPARTMENT_CONFIG = {
    "General Medicine": {"opd": True, "ipd": True, "icu": False},
    "General Surgery": {"opd": True, "ipd": True, "icu": False},
    "Emergency Medicine": {"opd": True, "ipd": True, "icu": True},
    "Cardiology": {"opd": True, "ipd": True, "icu": True},
    "Neurology": {"opd": True, "ipd": True, "icu": True},
    "Neurosurgery": {"opd": True, "ipd": True, "icu": True},
    "Orthopaedics": {"opd": True, "ipd": True, "icu": False},
    "Pediatrics": {"opd": True, "ipd": True, "icu": True},
    "Obstetrics & Gynecology": {"opd": True, "ipd": True, "icu": True},
    "Psychiatry": {"opd": True, "ipd": True, "icu": False},
    "Dermatology": {"opd": True, "ipd": False, "icu": False},
    "Ophthalmology": {"opd": True, "ipd": True, "icu": False},
    "ENT (Otolaryngology)": {"opd": True, "ipd": True, "icu": False},
    "Urology": {"opd": True, "ipd": True, "icu": False},
    "Nephrology": {"opd": True, "ipd": True, "icu": False},
    "Gastroenterology": {"opd": True, "ipd": True, "icu": False},
    "Pulmonology / Respiratory Medicine": {"opd": True, "ipd": True, "icu": True},
    "Endocrinology": {"opd": True, "ipd": True, "icu": False},
    "Rheumatology": {"opd": True, "ipd": True, "icu": False},
    "Hematology": {"opd": True, "ipd": True, "icu": False},
    "Oncology": {"opd": True, "ipd": True, "icu": False},
    "Anesthesiology": {"opd": False, "ipd": False, "icu": True},
    "Critical Care Medicine": {"opd": False, "ipd": False, "icu": True},
    "Dentistry / Oral Surgery": {"opd": True, "ipd": False, "icu": False},
    "Physiotherapy / Rehabilitation": {"opd": True, "ipd": True, "icu": False},
}

VALID_DEPARTMENTS = {
    # 1. General Medicine
    "general medicine": "General Medicine", "general physician": "General Medicine",
    "internal medicine": "General Medicine", "general opd": "General Medicine",
    "medicine": "General Medicine", "primary care": "General Medicine",

    # 2. General Surgery
    "general surgery": "General Surgery", "surgery": "General Surgery",
    "surgical": "General Surgery", "surgeon": "General Surgery",

    # 3. Emergency Medicine
    "emergency medicine": "Emergency Medicine", "emergency": "Emergency Medicine",
    "er": "Emergency Medicine", "trauma center": "Emergency Medicine",
    "casualty": "Emergency Medicine", "acute care": "Emergency Medicine",

    # 4. Cardiology
    "cardiology": "Cardiology", "heart clinic": "Cardiology",
    "cardiac": "Cardiology", "heart": "Cardiology",

    # 5. Neurology
    "neurology": "Neurology", "neuro": "Neurology",
    "nervous system": "Neurology", "neuro clinic": "Neurology",

    # 6. Neurosurgery
    "neurosurgery": "Neurosurgery", "neuro surgery": "Neurosurgery",
    "brain surgery": "Neurosurgery", "spine surgery": "Neurosurgery",

    # 7. Orthopaedics
    "orthopaedics": "Orthopaedics", "orthopedics": "Orthopaedics",
    "orthopaedic": "Orthopaedics", "orthopedic": "Orthopaedics",
    "ortho": "Orthopaedics", "bone and joint": "Orthopaedics",
    "bone": "Orthopaedics", "musculoskeletal": "Orthopaedics", "spine": "Orthopaedics",

    # 8. Pediatrics
    "pediatrics": "Pediatrics", "paediatrics": "Pediatrics",
    "pediatric": "Pediatrics", "paediatric": "Pediatrics",
    "child specialist": "Pediatrics", "child clinic": "Pediatrics", "baby": "Pediatrics",

    # 9. Obstetrics & Gynecology
    "obstetrics and gynecology": "Obstetrics & Gynecology",
    "obstetrics & gynecology": "Obstetrics & Gynecology",
    "ob-gyn": "Obstetrics & Gynecology", "gynecology": "Obstetrics & Gynecology",
    "gynecologist": "Obstetrics & Gynecology", "maternity": "Obstetrics & Gynecology",
    "women's health": "Obstetrics & Gynecology",

    # 10. Psychiatry
    "psychiatry": "Psychiatry", "mental health": "Psychiatry",
    "psychiatric": "Psychiatry", "behavioral health": "Psychiatry",
    "psychology": "Psychiatry",

    # 11. Dermatology
    "dermatology": "Dermatology", "skin clinic": "Dermatology",
    "skin": "Dermatology", "derma": "Dermatology",

    # 12. Ophthalmology
    "ophthalmology": "Ophthalmology", "eye clinic": "Ophthalmology",
    "eye": "Ophthalmology", "vision": "Ophthalmology",

    # 13. ENT (Otolaryngology)
    "ent": "ENT (Otolaryngology)", "ent (otolaryngology)": "ENT (Otolaryngology)",
    "ear nose throat": "ENT (Otolaryngology)", "otolaryngology": "ENT (Otolaryngology)",
    "ear nose and throat": "ENT (Otolaryngology)",

    # 14. Urology
    "urology": "Urology", "urologist": "Urology",
    "urinary": "Urology", "prostate": "Urology",

    # 15. Nephrology
    "nephrology": "Nephrology", "nephrologist": "Nephrology",
    "kidney": "Nephrology", "renal": "Nephrology", "dialysis": "Nephrology",

    # 16. Gastroenterology
    "gastroenterology": "Gastroenterology", "gastro": "Gastroenterology",
    "digestive": "Gastroenterology", "gi clinic": "Gastroenterology", "gi": "Gastroenterology",

    # 17. Pulmonology / Respiratory Medicine
    "pulmonology": "Pulmonology / Respiratory Medicine",
    "pulmonology / respiratory medicine": "Pulmonology / Respiratory Medicine",
    "pulmonary": "Pulmonology / Respiratory Medicine",
    "respiratory medicine": "Pulmonology / Respiratory Medicine",
    "respiratory": "Pulmonology / Respiratory Medicine",
    "chest medicine": "Pulmonology / Respiratory Medicine",
    "lungs": "Pulmonology / Respiratory Medicine",

    # 18. Endocrinology
    "endocrinology": "Endocrinology", "endocrine": "Endocrinology",
    "diabetes clinic": "Endocrinology", "thyroid clinic": "Endocrinology",
    "metabolic": "Endocrinology",

    # 19. Rheumatology
    "rheumatology": "Rheumatology", "rheumatologist": "Rheumatology",
    "arthritis clinic": "Rheumatology", "autoimmune": "Rheumatology",

    # 20. Hematology
    "hematology": "Hematology", "haematology": "Hematology",
    "hematologist": "Hematology", "haematologist": "Hematology",
    "blood specialist": "Hematology", "blood clinic": "Hematology",

    # 21. Oncology
    "oncology": "Oncology", "oncologist": "Oncology",
    "cancer clinic": "Oncology", "tumor clinic": "Oncology",
    "chemotherapy": "Oncology", "cancer": "Oncology",

    # 22. Anesthesiology
    "anesthesiology": "Anesthesiology", "anaesthesiology": "Anesthesiology",
    "anesthesia": "Anesthesiology", "pain management": "Anesthesiology",

    # 23. Critical Care Medicine
    "critical care medicine": "Critical Care Medicine", "critical care": "Critical Care Medicine",
    "icu": "Critical Care Medicine", "intensive care": "Critical Care Medicine",

    # 24. Dentistry / Oral Surgery
    "dentistry": "Dentistry / Oral Surgery", "dentistry / oral surgery": "Dentistry / Oral Surgery",
    "dental": "Dentistry / Oral Surgery", "oral surgery": "Dentistry / Oral Surgery",
    "dentist": "Dentistry / Oral Surgery", "teeth": "Dentistry / Oral Surgery",

    # 25. Physiotherapy / Rehabilitation
    "physiotherapy": "Physiotherapy / Rehabilitation",
    "physiotherapy / rehabilitation": "Physiotherapy / Rehabilitation",
    "rehabilitation": "Physiotherapy / Rehabilitation",
    "physical therapy": "Physiotherapy / Rehabilitation",
    "physio": "Physiotherapy / Rehabilitation",
}

DEPARTMENT_RATIONALES = {
    "General Medicine": "General multi-system symptoms or complex internal pathology requiring primary internal medicine clinical evaluation (Available in OPD, IPD).",
    "General Surgery": "Surgical pathology, hernia, acute abdominal conditions, or excised lesions requiring general surgeon evaluation (Available in OPD, IPD).",
    "Emergency Medicine": "Acute, critical trauma or severe clinical distress requiring immediate resuscitation and emergency triage (Available in OPD, IPD, ICU).",
    "Cardiology": "Cardiovascular signs, arrhythmia, chest pain, or ischemic heart disease requiring cardiologist care (Available in OPD, IPD, ICU).",
    "Neurology": "Central, peripheral, or autonomic neurological symptoms requiring specialized neurologist evaluation (Available in OPD, IPD, ICU).",
    "Neurosurgery": "Intracranial lesions, brain trauma, structural spine compression, or aneurysms requiring neurosurgeon evaluation (Available in OPD, IPD, ICU).",
    "Orthopaedics": "Musculoskeletal trauma, fractures, ligament tears, or degenerative joint conditions requiring orthopaedic surgeon examination (Available in OPD, IPD).",
    "Pediatrics": "Symptoms in children or infants requiring specialized pediatric evaluation (Available in OPD, IPD, ICU).",
    "Obstetrics & Gynecology": "Obstetric, reproductive, or female pelvic pathology requiring specialized OB-GYN assessment (Available in OPD, IPD, ICU).",
    "Psychiatry": "Psychiatric, behavioral, or mood symptoms requiring confidential clinical evaluation (Available in OPD, IPD).",
    "Dermatology": "Cutaneous, hair, or nail manifestations requiring outpatient dermatologist examination (Available in OPD).",
    "Ophthalmology": "Visual disturbances, ocular trauma, or eye pathology requiring ophthalmologist assessment (Available in OPD, IPD).",
    "ENT (Otolaryngology)": "Ear, nose, or throat pathology requiring specialist otolaryngologist examination (Available in OPD, IPD).",
    "Urology": "Urinary tract, stone disease, or male reproductive tract disorders requiring urologist care (Available in OPD, IPD).",
    "Nephrology": "Renal parenchymal disease, chronic kidney dysfunction, proteinuria, or dialysis needs requiring nephrologist care (Available in OPD, IPD).",
    "Gastroenterology": "Digestive, luminal GI, or hepatobiliary symptoms requiring gastroenterologist evaluation (Available in OPD, IPD).",
    "Pulmonology / Respiratory Medicine": "Airway, lung parenchymal, or respiratory failure symptoms requiring specialized pulmonologist care (Available in OPD, IPD, ICU).",
    "Endocrinology": "Hormonal, metabolic, thyroid, or glycemic dysregulation requiring endocrinologist management (Available in OPD, IPD).",
    "Rheumatology": "Systemic autoimmune disease, inflammatory polyarthritis, or connective tissue disorders requiring rheumatologist evaluation (Available in OPD, IPD).",
    "Hematology": "Abnormal bleeding, coagulopathy, bone marrow disorders, or chronic anemia requiring clinical hematologist assessment (Available in OPD, IPD).",
    "Oncology": "Suspected neoplasm, malignant tumors, or post-biopsy staging requiring comprehensive oncologist evaluation (Available in OPD, IPD).",
    "Anesthesiology": "Pre-operative anesthesia assessment, peri-operative care, or chronic intractable pain intervention (Available in ICU).",
    "Critical Care Medicine": "Life-threatening multi-organ failure, septic shock, or acute hemodynamic collapse requiring intensive care admission (Available in ICU).",
    "Dentistry / Oral Surgery": "Dental caries, toothache, gum infection, or maxillofacial oral surgery requirements (Available in OPD).",
    "Physiotherapy / Rehabilitation": "Functional motor recovery, post-surgical physical rehabilitation, or musculoskeletal physiotherapy (Available in OPD, IPD).",
}

DEPARTMENT_KEYWORDS = {
    "General Medicine": [
        "fever", "high temperature", "chills", "cold and cough", "flu symptoms", "body aches",
        "fatigue", "general weakness", "exhaustion", "unexplained fatigue", "routine checkup",
        "annual physical", "general consultation", "blood test review", "sugar checkup",
        "mild infection", "viral fever", "allergy general", "prescription refill",
        "malaise", "vitamin deficiency", "anemia"
    ],
    "General Surgery": [
        "hernia", "inguinal hernia", "umbilical hernia", "lump in groin", "painful lump",
        "appendicitis", "appendix pain", "gallbladder stones", "cholecystitis",
        "abscess drainage", "boil incision", "cyst removal", "lipoma", "sebaceous cyst",
        "diabetic foot ulcer", "gangrene", "surgical wound", "post-surgery wound infection",
        "piles surgery", "fistula", "fissure surgery", "wound stitches", "suture removal"
    ],
    "Emergency Medicine": [
        "emergency", "acute trauma", "severe trauma", "road accident", "car crash", "bike accident",
        "fall with head injury", "unconscious", "shock", "hypovolemic shock", "anaphylaxis",
        "acute poisoning", "snake bite", "cardiac arrest", "unresponsive", "severe burns",
        "gushing blood", "massive bleeding", "sudden collapse", "resuscitation"
    ],
    "Cardiology": [
        "chest pain", "chest tightness", "chest pressure", "heart attack", "heart palpitation",
        "palpitations", "irregular heartbeat", "high blood pressure", "cardiac", "cardiology",
        "cardiologist", "angina", "arrhythmia", "tachycardia", "bradycardia", "coronary",
        "heart flutter", "rapid heart rate", "racing heart", "heart beating fast", "heart pounding",
        "skipped heartbeat", "shortness of breath on exertion", "ecg", "ekg", "cholesterol",
        "hypertension", "swollen ankles cardiac", "cardiovascular"
    ],
    "Neurology": [
        "hallucination", "hallucinations", "hallucinating", "disorientation", "disoriented",
        "confusion", "severe confusion", "altered mental status", "delirium", "seeing things",
        "severe headache", "migraine", "headache", "cluster headache", "dizziness", "vertigo",
        "loss of balance", "unsteady gait", "numbness", "tingling", "pins and needles",
        "tremor", "shaking hands", "seizure", "convulsions", "epilepsy", "fainting spell",
        "syncope", "memory loss", "brain fog", "nerve pain", "neuropathy", "carpal tunnel",
        "bell's palsy", "facial drooping", "stroke symptoms", "paralysis", "neurological",
        "slurred speech", "weakness one side", "ataxia", "loss of coordination"
    ],
    "Neurosurgery": [
        "brain tumor", "brain haemorrhage", "brain bleeding", "subdural hematoma",
        "skull fracture", "head injury surgical", "aneurysm brain", "hydrocephalus",
        "spinal cord compression", "cauda equina", "severe herniated disc needing surgery",
        "spinal tumor", "lumbar canal stenosis surgery", "neurosurgical", "pituitary tumor"
    ],
    "Orthopaedics": [
        "joint pain", "knee pain", "back pain", "neck pain", "shoulder pain", "hip pain",
        "ankle pain", "wrist pain", "elbow pain", "bone fracture", "broken bone", "ligament tear",
        "sprained ankle", "difficulty walking", "unable to walk", "knee swelling", "joint stiffness",
        "arthritis", "arthritic", "sciatica", "slip disc", "spine pain", "spinal", "osteoporosis",
        "muscle tear", "tendonitis", "tendon", "ortho", "orthopedic", "orthopaedics", "cartilage",
        "dislocation", "fracture", "sprain", "joint", "joints", "knee", "knees", "bone", "bones",
        "hip", "hips", "shoulder", "spine", "backache", "lumbago", "gout", "swollen joint", "leg pain",
        "frozen shoulder", "rotator cuff", "meniscus tear", "heel pain", "plantar fasciitis"
    ],
    "Pediatrics": [
        "child", "children", "baby", "infant", "toddler", "pediatric", "paediatric",
        "child fever", "baby cold", "baby crying continuously", "child diarrhea",
        "childhood vaccination", "pediatric immunization", "failure to thrive", "delayed milestones",
        "child rash", "pediatric asthma", "croup", "chickenpox child", "mumps"
    ],
    "Obstetrics & Gynecology": [
        "pregnancy", "pregnant", "missed period", "irregular periods", "heavy menstrual bleeding",
        "menstrual cramps", "severe period pain", "pelvic pain", "vaginal discharge", "vaginal itching",
        "yeast infection", "breast lump", "breast pain", "pap smear", "prenatal checkup",
        "postnatal", "menopause symptoms", "hot flashes", "ovarian cyst", "uterine fibroids", "infertility",
        "morning sickness", "labor pain", "contraception",
        "vaginal bleeding", "bleeding from vagina", "bleeding vaginally", "vaginal spotting", "spotting",
        "bleeding between periods", "heavy period", "period cramps", "abdominal cramps", "pelvic cramps",
        "lower abdominal cramps", "cramps in pelvis", "abnormal uterine bleeding", "uterine bleeding",
        "cervical pain", "ovary pain", "ectopic pregnancy", "miscarriage", "post coital bleeding"
    ],
    "Psychiatry": [
        "depression", "depressed", "extreme sadness", "hopelessness", "loss of interest in life",
        "anxiety", "anxious", "panic attack", "panic disorder", "severe social anxiety",
        "insomnia", "sleeplessness", "mood swings", "bipolar", "mania", "paranoia", "paranoid thoughts",
        "hearing voices in head", "obsessive thoughts", "ocd", "compulsions", "ptsd", "nightmares trauma",
        "substance abuse", "alcohol addiction", "drug dependence", "eating disorder", "anorexia", "bulimia",
        "burnout", "mental exhaustion", "stress breakdown"
    ],
    "Dermatology": [
        "skin rash", "itchy skin", "itching", "severe itching", "skin allergy", "acne breakout",
        "pimples", "eczema", "psoriasis", "hives", "urticaria", "dermatitis", "skin lesion",
        "skin peeling", "ringworm", "fungal infection", "hair loss", "alopecia", "dandruff",
        "mole check", "pigmentation", "blister", "blisters", "boil", "boils", "nail fungus",
        "rash", "rashes", "skin", "mole", "melanoma", "scalp", "pimple", "vitiligo", "warts"
    ],
    "Ophthalmology": [
        "blurry vision", "blurred vision", "loss of vision", "eye pain", "red eye", "redness in eye",
        "dry eyes", "watery eyes", "eye strain", "double vision", "diplopia", "cataract",
        "glaucoma", "cornea", "retina", "conjunctivitis", "pink eye", "glasses prescription",
        "vision check", "stye", "itchy eyes", "swollen eyelid", "eye irritation", "eye", "eyes",
        "vision", "ophthalmic", "ophthalmology", "sight", "floaters", "flashes of light", "night blindness"
    ],
    "ENT (Otolaryngology)": [
        "sore throat", "ear pain", "ear ache", "ear infection", "hearing loss", "ringing in ear",
        "tinnitus", "nasal congestion", "blocked nose", "runny nose", "sinus headache", "sinus pain",
        "sinusitis", "nose bleed", "epistaxis", "throat infection", "swollen tonsils", "tonsillitis",
        "hoarse voice", "loss of voice", "laryngitis", "pharyngitis", "vertigo ear", "blocked ear",
        "ear discharge", "ear", "ears", "nose", "throat", "tonsils", "adenoids", "audiometry", "hoarse",
        "snoring", "difficulty swallowing solids"
    ],
    "Urology": [
        "burning urination", "painful urination", "difficulty urinating", "frequent urination",
        "blood in urine", "hematuria", "urinary tract infection", "uti", "kidney stone", "renal calculus",
        "flank pain", "kidney pain", "prostate enlargement", "bph", "prostate issue", "urinary incontinence",
        "weak urine stream", "bladder pain", "testicular pain", "testicular swelling", "testicle pain",
        "swollen testicles", "scrotal pain", "scrotal swelling", "testicular torsion", "epididymitis",
        "orchitis", "prostatitis", "blood in semen", "erectile dysfunction", "penile discharge", "penile pain"
    ],
    "Nephrology": [
        "chronic kidney disease", "ckd", "kidney failure", "renal failure", "dialysis",
        "high creatinine", "elevated bun", "protein in urine", "proteinuria", "swelling around eyes renal",
        "nephrotic syndrome", "glomerulonephritis", "electrolyte disturbance renal", "kidney transplant followup"
    ],
    "Gastroenterology": [
        "stomach pain", "abdominal pain", "stomach ache", "belly ache", "acid reflux", "gerd",
        "heartburn", "acidity", "indigestion", "bloating", "gas pain", "severe constipation",
        "chronic diarrhea", "loose motions", "nausea", "vomiting", "blood in stool", "jaundice",
        "liver problem", "fatty liver", "gastritis", "ulcer", "stomach ulcer", "peptic ulcer",
        "abdominal cramps", "stomach cramps", "cramps stomach", "gut cramps", "gut health",
        "colonoscopy", "endoscopy", "stomach", "abdomen", "digestive",
        "gallbladder", "gallstones", "pancreatitis", "hepatitis", "hemorrhoids", "piles"
    ],
    "Pulmonology / Respiratory Medicine": [
        "breathing problem", "breathing difficulty", "difficulty breathing", "problem in breathing",
        "shortness of breath", "breathlessness", "hard to breathe", "labored breathing", "rapid breathing",
        "chronic cough", "persistent cough", "cough with phlegm", "wheezing", "asthma", "asthma attack",
        "bronchitis", "pneumonia", "chest congestion", "mucus in chest", "copd", "emphysema",
        "lung infection", "oxygen saturation low", "hypoxia", "respiratory", "pulmonary", "inhaler"
    ],
    "Endocrinology": [
        "thyroid", "thyroid problem", "hypothyroid", "hyperthyroid", "goiter", "high tsh",
        "diabetes", "high blood sugar", "low blood sugar", "hba1c", "insulin resistance",
        "hormonal imbalance", "hormone test", "pcos", "pcod", "unexplained weight gain",
        "unexplained weight loss", "excessive thirst", "excessive hunger", "adrenal", "cushing"
    ],
    "Rheumatology": [
        "rheumatoid arthritis", "joint pain multiple joints", "morning joint stiffness > 1 hour",
        "lupus", "sle", "autoimmune joint", "swollen knuckles", "ankylosing spondylitis",
        "sjogren", "scleroderma", "raynaud", "psoriatic arthritis", "inflammatory arthritis",
        "connective tissue disease", "high esr joint pain"
    ],
    "Hematology": [
        "bruising easily", "easy bruising", "frequent bruising", "unexplained bruising", "bruises easily",
        "nosebleed", "nosebleeds", "frequent nosebleeds", "bleeding gums", "bleeding from gums",
        "petechiae", "purpura", "pinpoint red spots", "blood clotting", "clotting problem",
        "hemophilia", "thrombocytopenia", "low platelets", "platelet count low",
        "anemia severe", "pale skin and fatigue", "enlarged spleen", "splenomegaly", "swollen lymph nodes fatigue",
        "blood disorder", "leukemia", "lymphoma", "sickle cell", "thalassemia", "prolonged bleeding"
    ],
    "Oncology": [
        "cancer", "tumor", "tumour", "malignancy", "malignant mass", "chemotherapy consult",
        "radiation oncology", "cancer recurrence", "biopsy positive for carcinoma", "breast cancer",
        "lung cancer", "colon cancer", "oral cancer", "lymph node enlargement painless",
        "unexplained massive weight loss cancer", "oncologist consultation"
    ],
    "Anesthesiology": [
        "pre-anesthesia checkup", "pac clearance", "fitness for surgery anesthesia",
        "chronic intractable pain", "nerve block injection", "epidural injection",
        "post-operative pain management"
    ],
    "Critical Care Medicine": [
        "icu care", "intensive care needed", "ventilator support", "multi organ failure",
        "septic shock", "severe sepsis", "arterial line monitoring", "inotropic support",
        "critical hemodynamic instability"
    ],
    "Dentistry / Oral Surgery": [
        "toothache", "tooth pain", "dental pain", "bleeding tooth", "cavity", "dental caries",
        "wisdom tooth pain", "swollen gums tooth", "dental abscess", "root canal", "broken tooth",
        "jaw pain dental", "jaw clicking", "gum disease", "periodontitis", "mouth ulcer dental",
        "teeth cleaning", "orthodontic braces"
    ],
    "Physiotherapy / Rehabilitation": [
        "physiotherapy", "rehabilitation", "stroke recovery rehab", "post stroke physiotherapy",
        "post fracture stiffness rehab", "post surgery walking therapy", "physiotherapy for back pain",
        "physiotherapy for knee", "mobility training", "muscle strengthening", "paralysis rehabilitation",
        "ergonomic therapy", "tens therapy", "ultrasound therapy muscle"
    ]
}

# CLINICAL COMBINATION RULES
COMBINATION_RULES = [
    {
        "name": "Head Trauma with Neurological Deficit",
        "keywords": ["head injury", "hit head", "fall with head", "skull fracture", "head trauma"],
        "co_keywords": ["bleeding from ear", "vomiting", "unconscious", "slurred speech", "seizure"],
        "route_to": "Neurosurgery",
        "rationale": "Acute head trauma with neurological signs or basilar skull bleeding requires urgent neurosurgical and emergency trauma evaluation (Available in OPD, IPD, ICU)."
    },
    {
        "name": "Coagulopathy / Hematological Disturbance",
        "keywords": ["nosebleed", "nosebleeds", "nose bleed", "bruising easily", "easy bruising", "bruising", "bleeding gums"],
        "co_keywords": ["fatigue", "tiredness", "weakness", "pale", "bruises easily", "frequent bruising"],
        "route_to": "Hematology",
        "rationale": "Presentation of abnormal mucosal/dermal bleeding (nosebleeds, easy bruising) along with systemic signs suggests coagulopathy or hematological disorder (Available in OPD, IPD)."
    },
    {
        "name": "Neuro-Psychiatric Crisis with Autonomic Disturbance",
        "keywords": ["hallucination", "hallucinations", "disorientation", "disoriented", "delirium", "confusion"],
        "co_keywords": ["tachycardia", "rapid heart", "breathing problem", "blurry vision", "tremor"],
        "route_to": "Neurology",
        "rationale": "Sensory/cognitive alteration (hallucination/disorientation) alongside autonomic signs (tachycardia, vision or respiratory changes) points to acute central nervous system or toxic-metabolic pathology (Available in OPD, IPD, ICU)."
    },
    {
        "name": "Cardio-Respiratory Presentation",
        "keywords": ["chest pain", "chest tightness", "chest pressure"],
        "co_keywords": ["breathing problem", "shortness of breath", "tachycardia", "sweating", "left arm"],
        "route_to": "Cardiology",
        "rationale": "Chest discomfort co-occurring with respiratory difficulty or tachycardia requires urgent cardiovascular evaluation by a cardiologist (Available in OPD, IPD, ICU)."
    },
    {
        "name": "Pulmonary Distress with Airway Symptoms",
        "keywords": ["breathing problem", "breathing difficulty", "shortness of breath", "wheezing"],
        "co_keywords": ["cough", "fever", "chest congestion", "mucus", "phlegm", "asthma"],
        "route_to": "Pulmonology / Respiratory Medicine",
        "rationale": "Primary respiratory distress accompanied by airway symptoms indicates acute pulmonary pathology requiring specialized chest physician care (Available in OPD, IPD, ICU)."
    },
    {
        "name": "Endocrine-Metabolic Complex",
        "keywords": ["diabetes", "thyroid", "sugar high", "sugar low"],
        "co_keywords": ["fatigue", "weight loss", "weight gain", "frequent urination", "blurry vision"],
        "route_to": "Endocrinology",
        "rationale": "Glycemic or hormonal dysregulation co-occurring with systemic metabolic symptoms warrants specialized endocrinologist consultation (Available in OPD, IPD)."
    },
    {
        "name": "Autoimmune / Polyarthritis",
        "keywords": ["rheumatoid arthritis", "lupus", "autoimmune", "swollen knuckles"],
        "co_keywords": ["morning stiffness", "joint pain", "fatigue"],
        "route_to": "Rheumatology",
        "rationale": "Multiple joint involvement with prolonged morning stiffness or autoimmune signs requires specialized rheumatologist care (Available in OPD, IPD)."
    },
    {
        "name": "Dental / Oral Origin",
        "keywords": ["toothache", "tooth pain", "dental caries", "cavity", "wisdom tooth", "gum swelling"],
        "co_keywords": ["jaw", "mouth", "bleeding gum", "teeth"],
        "route_to": "Dentistry / Oral Surgery",
        "rationale": "Dental or oral cavity symptoms requiring specialized dentist / oral surgeon examination (Available in OPD)."
    },
    {
        "name": "Nephrology / Renal Failure",
        "keywords": ["dialysis", "chronic kidney", "renal failure", "high creatinine"],
        "co_keywords": ["swelling", "urine protein", "edema"],
        "route_to": "Nephrology",
        "rationale": "Renal parenchymal dysfunction or dialysis requirements warrant specialized nephrology assessment (Available in OPD, IPD)."
    },
    {
        "name": "Acute Gynecological / Obstetric Presentation",
        "keywords": [
            "vaginal bleeding", "bleeding from vagina", "vaginal spotting", "spotting",
            "heavy period", "period cramps", "missed period", "pregnancy", "pregnant",
            "abnormal uterine bleeding", "bleeding between periods", "heavy menstrual bleeding"
        ],
        "co_keywords": [
            "abdominal cramps", "pelvic cramps", "cramps", "dizziness", "fainting",
            "weakness", "vomiting", "pelvic pain", "nausea"
        ],
        "route_to": "Obstetrics & Gynecology",
        "rationale": "Acute gynecological presentation: Vaginal bleeding accompanied by abdominal/pelvic cramps or dizziness (suggestive of blood loss or ectopic pregnancy risk) requires immediate specialized OB-GYN evaluation (Available in OPD, IPD, ICU)."
    },
    {
        "name": "Acute Urological / Scrotal Presentation",
        "keywords": [
            "testicular pain", "testicle pain", "testicular swelling", "scrotal pain",
            "scrotal swelling", "swollen testicles", "testicular torsion", "epididymitis"
        ],
        "co_keywords": [
            "pain", "swelling", "severe", "burning urination", "fever", "groin pain"
        ],
        "route_to": "Urology",
        "rationale": "Acute testicular or scrotal symptoms require urgent urologist evaluation to rule out testicular torsion, epididymo-orchitis, or structural pathology (Available in OPD, IPD)."
    }
]

# Sex-Specific Anatomical Keywords for Biological Consistency Validation
FEMALE_SPECIFIC_KEYWORDS = [
    "vaginal bleeding", "bleeding from vagina", "bleeding vaginally", "vaginal spotting",
    "vaginal discharge", "vaginal itching", "vaginal pain", "vulva pain", "cervical",
    "missed period", "late period", "heavy menstrual bleeding", "menstrual cramps",
    "period cramps", "period pain", "severe period pain", "irregular periods",
    "pregnancy", "pregnant", "ectopic pregnancy", "miscarriage", "morning sickness",
    "pap smear", "ovarian cyst", "ovary pain", "uterine fibroids", "uterine bleeding",
    "labor pain", "menopause symptoms", "hot flashes menopause", "endometriosis"
]

MALE_SPECIFIC_KEYWORDS = [
    "testicular pain", "testicle pain", "testicular swelling", "swollen testicles",
    "scrotal pain", "scrotal swelling", "swollen scrotum", "testicular torsion",
    "epididymitis", "orchitis", "prostate enlargement", "enlarged prostate", "prostate issue",
    "prostatitis", "bph", "blood in semen", "penile discharge", "penile pain",
    "foreskin pain", "erectile dysfunction"
]


def check_sex_consistency(concern: str, sex: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Validates patient biological sex against reported anatomical symptoms.
    Detects demographic data-entry errors or anatomical discrepancies.
    """
    if not sex or not concern:
        return None
    normalized = concern.lower()
    sex_norm = sex.strip().capitalize()

    # Case 1: Male profile presenting with female-specific symptoms
    if sex_norm == "Male":
        matched_female = [kw for kw in FEMALE_SPECIFIC_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', normalized)]
        if matched_female:
            symptoms_str = ", ".join(matched_female)
            return {
                "detected": True,
                "type": "male_with_female_symptoms",
                "registered_sex": "Male",
                "matched_symptoms": matched_female,
                "title": "Biological Sex / Demographic Discrepancy Detected",
                "message": (
                    f"The patient is registered as MALE, but presenting symptoms report female-specific anatomy ({symptoms_str}). "
                    f"If the patient is female, immediate evaluation by Obstetrics & Gynecology is indicated. "
                    f"If the patient is male, symptoms of abdominal cramping, dizziness, and suspected blood loss indicate internal gastrointestinal or urinary bleeding requiring urgent General Medicine / Emergency evaluation."
                ),
                "safe_routing": "General Medicine"
            }

    # Case 2: Female profile presenting with male-specific symptoms
    elif sex_norm == "Female":
        matched_male = [kw for kw in MALE_SPECIFIC_KEYWORDS if re.search(r'\b' + re.escape(kw) + r'\b', normalized)]
        if matched_male:
            symptoms_str = ", ".join(matched_male)
            return {
                "detected": True,
                "type": "female_with_male_symptoms",
                "registered_sex": "Female",
                "matched_symptoms": matched_male,
                "title": "Biological Sex / Demographic Discrepancy Detected",
                "message": (
                    f"The patient is registered as FEMALE, but presenting symptoms report male-specific anatomy ({symptoms_str}). "
                    f"Please verify demographic registration. General Medicine / General Surgery evaluation is recommended to examine for groin hernia, pelvic, or soft-tissue pathology."
                ),
                "safe_routing": "General Medicine"
            }

    return None


def _normalize_department(department: str) -> Optional[str]:
    """Matches raw department strings against canonical names."""
    if not department:
        return None
    raw = re.sub(r"[^a-z0-9&/]+", " ", department.lower()).strip()
    if raw in VALID_DEPARTMENTS:
        return VALID_DEPARTMENTS[raw]
    for alias, canonical in VALID_DEPARTMENTS.items():
        if alias in raw or raw in alias:
            return canonical
    return None


def get_department_care_levels(department: str) -> Dict[str, bool]:
    """Returns availability flags for OPD, IPD, ICU."""
    canonical = _normalize_department(department) or "General Medicine"
    return DEPARTMENT_CONFIG.get(canonical, {"opd": True, "ipd": True, "icu": False})


def route_concern_by_keywords(
    concern: str,
    age: Optional[int] = None,
    sex: Optional[str] = None
) -> Tuple[str, str]:
    """
    Deterministic symptom matching engine with:
    1. Biological sex consistency & anatomical verification
    2. Pediatric age override
    3. Clinical combination rules (gynecology, urology, trauma, etc.)
    4. Weighted multi-word keyword scoring
    """
    normalized = (concern or "").lower().strip()
    if not normalized:
        return "General Medicine", DEPARTMENT_RATIONALES["General Medicine"]

    # 1. Biological Sex Discrepancy & Consistency Check
    mismatch = check_sex_consistency(normalized, sex=sex)
    if mismatch:
        if mismatch["type"] == "male_with_female_symptoms":
            return (
                "General Medicine",
                (
                    "Demographic / Biological Sex Discrepancy: Patient registered as Male but symptoms report female reproductive anatomy "
                    f"({', '.join(mismatch['matched_symptoms'])}). If patient is biologically female, route immediately to Obstetrics & Gynecology. "
                    "For male patients, symptoms of abdominal cramping and dizziness with suspected blood loss warrant urgent internal evaluation by General Medicine (Available in OPD, IPD)."
                )
            )
        elif mismatch["type"] == "female_with_male_symptoms":
            return (
                "General Medicine",
                (
                    "Demographic / Biological Sex Discrepancy: Patient registered as Female but symptoms report male reproductive anatomy "
                    f"({', '.join(mismatch['matched_symptoms'])}). Routed to General Medicine for demographic verification and pelvic/hernia examination (Available in OPD, IPD)."
                )
            )

    # 2. Pediatric Age Check (Patients < 14 yrs with general complaints)
    if age is not None and age < 14:
        is_adult_specific = any(term in normalized for term in ["tooth", "dental", "eye", "vision", "ear", "fracture", "bone"])
        if not is_adult_specific:
            if any(term in normalized for term in ["fever", "cold", "cough", "vomiting", "diarrhea", "rash", "crying"]):
                return "Pediatrics", DEPARTMENT_RATIONALES["Pediatrics"]

    # 3. Check clinical combination rules
    for rule in COMBINATION_RULES:
        has_primary = any(re.search(r'\b' + re.escape(kw) + r'\b', normalized) for kw in rule["keywords"])
        if has_primary:
            has_co = any(re.search(r'\b' + re.escape(kw) + r'\b', normalized) for kw in rule["co_keywords"])
            if has_co:
                return rule["route_to"], rule["rationale"]

    # 4. Special multi-symptom safeguard for neuro crisis (when not a sex mismatch):
    if any(h in normalized for h in ["hallucination", "hallucinations", "disorientation", "disoriented"]):
        return "Neurology", DEPARTMENT_RATIONALES["Neurology"]

    # 5. Deterministic keyword scoring across all 25 departments
    scores = {dept: 0 for dept in DEPARTMENT_KEYWORDS}
    for dept, keywords in DEPARTMENT_KEYWORDS.items():
        for kw in keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            matches = len(re.findall(pattern, normalized))
            if matches > 0:
                weight = 3 if " " in kw else 1
                scores[dept] += matches * weight

    best_dept = max(scores, key=lambda d: scores[d])
    if scores[best_dept] > 0:
        return best_dept, DEPARTMENT_RATIONALES[best_dept]

    return "General Medicine", DEPARTMENT_RATIONALES["General Medicine"]


def route_patient(
    structured_concern: str,
    age: Optional[int] = None,
    sex: Optional[str] = None,
    weight: Optional[float] = None,
    height: Optional[float] = None
) -> str:
    """
    Triage Router Agent: Maps patient concerns and vitals to the optimal hospital department
    from the full 25 hospital departments with biological sex validation.
    """
    kw_dept, kw_rationale = route_concern_by_keywords(structured_concern, age=age, sex=sex)

    vitals_parts = []
    if age is not None:
        vitals_parts.append(f"Age: {age}")
    if sex:
        vitals_parts.append(f"Sex: {sex}")
    if weight and height and height > 0:
        bmi = round(float(weight) / ((float(height) / 100.0) ** 2), 1)
        vitals_parts.append(f"Weight: {weight}kg, Height: {height}cm (BMI: {bmi})")
    vitals_text = ", ".join(vitals_parts) if vitals_parts else "Not provided"

    all_depts_list = list(DEPARTMENT_CONFIG.keys())
    depts_str = ", ".join(all_depts_list)

    prompt = f"""
    You are an expert Chief Triage Medical Officer in a high-volume multi-speciality hospital.
    Your mission is to route the patient to the MOST clinically appropriate department from our hospital directory:

    AVAILABLE 25 SPECIALITY DEPARTMENTS:
    {depts_str}

    PATIENT PROFILE:
    - Vitals & Demographics: {vitals_text}
    - Reported Symptoms / Concern: "{structured_concern}"

    CLINICAL REASONING RULES:
    1. If age < 14 and general illness is present -> Route to Pediatrics.
    2. BIOLOGICAL SEX CONSISTENCY: Cross-reference biological sex with symptoms. 
       - If sex is Male but symptoms report female reproductive anatomy (vaginal bleeding/cramps), do NOT route to Neurology or OB-GYN. Route to General Medicine with an anatomical discrepancy note.
       - If sex is Female and symptoms report vaginal bleeding, pelvic cramps, or dizziness, route to Obstetrics & Gynecology.
       - If sex is Male and symptoms report testicular pain or scrotal swelling, route to Urology.
    3. Analyze ALL symptoms together (e.g., toothache/cavity -> Dentistry / Oral Surgery; 
       rheumatoid arthritis/lupus -> Rheumatology; dialysis/creatinine -> Nephrology; 
       cancer/mass -> Oncology; post-stroke rehab -> Physiotherapy / Rehabilitation).
    4. Never diagnose a disease. Explain why the department is appropriate for evaluation.

    OUTPUT STRICTLY IN THIS FORMAT:
    DEPARTMENT: [Exact Department Name from Available List]
    RATIONALE: [One clear, professional sentence explaining the clinical matching rationale]
    """

    llm_output = call_groq_chat(prompt, temperature=0.0)

    if llm_output:
        extracted_dept = None
        extracted_rationale = None

        for line in llm_output.splitlines():
            line_str = line.strip()
            if line_str.upper().startswith("DEPARTMENT:"):
                raw_dept = line_str.split(":", 1)[1].strip().replace("[", "").replace("]", "").strip()
                extracted_dept = _normalize_department(raw_dept)
            elif line_str.upper().startswith("RATIONALE:"):
                extracted_rationale = line_str.split(":", 1)[1].strip().replace("[", "").replace("]", "").strip()

        if extracted_dept:
            return f"DEPARTMENT: {extracted_dept}\nRATIONALE: {extracted_rationale or DEPARTMENT_RATIONALES.get(extracted_dept, kw_rationale)}"

    return f"DEPARTMENT: {kw_dept}\nRATIONALE: {kw_rationale}"


def extract_department(
    triage_output: str,
    fallback_department: str = "General Medicine",
    concern: str = "",
    age: Optional[int] = None,
    sex: Optional[str] = None
) -> str:
    """Extracts clean canonical department name from triage output."""
    if triage_output:
        for line in triage_output.splitlines():
            if line.strip().upper().startswith("DEPARTMENT:"):
                dept = line.split(":", 1)[1].strip().replace("[", "").replace("]", "").strip()
                normalized = _normalize_department(dept)
                if normalized:
                    return normalized

    if concern:
        kw_dept, _ = route_concern_by_keywords(concern, age=age, sex=sex)
        if kw_dept:
            return kw_dept

    return fallback_department


def extract_rationale(triage_text: str, department: str = "General Medicine") -> str:
    """Extracts clean clinical rationale from triage output."""
    if triage_text:
        for line in triage_text.splitlines():
            if line.strip().upper().startswith("RATIONALE:"):
                clean = line.split(":", 1)[1].strip().replace("[", "").replace("]", "").strip()
                if clean:
                    return clean

    return DEPARTMENT_RATIONALES.get(department, DEPARTMENT_RATIONALES["General Medicine"])

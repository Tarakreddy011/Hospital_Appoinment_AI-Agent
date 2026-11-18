import re
from typing import Optional, Dict, Any, List
from groq_client import call_groq_chat

# =====================================================================
# 1. IMMEDIATE LIFE-THREATENING EMERGENCIES (Halt standard routing completely)
# =====================================================================
CRITICAL_EMERGENCY_PHRASES = (
    # Head Trauma & Basilar Skull Signs
    "head injury", "head trauma", "hit on head", "hit head", "injury to head",
    "blow to head", "fall with head", "fall on head", "struck on head",
    "bleeding from ear", "blood from ear", "bleeding ear", "fluid from ear",
    "csf leak", "skull fracture", "broken skull",
    
    # Severe Bleeding & Hemorrhage
    "severe bleeding", "heavy bleeding", "bleeding heavily", "blood will not stop",
    "blood won't stop", "uncontrolled bleeding", "gushing blood", "spurting blood",
    "bleeding profusely", "massive bleeding", "coughing blood", "vomiting blood",
    "coughing up blood", "vomiting large amounts of blood",
    
    # Acute Cardiovascular
    "crushing chest pain", "severe chest pain", "chest pain", "heart attack",
    "cardiac arrest", "heart stopped", "severe crushing chest",
    
    # Acute Respiratory Failure
    "cannot breathe", "can't breathe", "unable to breathe", "stopped breathing",
    "gasping for air", "suffocating", "choking", "cyanosis", "blue lips",
    "stridor", "airway blocked",
    
    # Acute Neurological & Consciousness
    "loss of consciousness", "unconscious", "passed out completely",
    "unresponsive", "sudden collapse", "collapsed", "coma",
    "facial drooping", "face drooping", "slurred speech", "stroke signs",
    "acute stroke", "having a stroke", "actively seizing", "seizure now", "status epilepticus",
    "sudden paralysis", "acute paralysis", "sudden loss of vision both eyes",
    
    # Severe Trauma & Accidents
    "major accident", "car crash", "bike accident", "hit by vehicle",
    "fall from height", "severe burn", "third degree burn", "electrocution",
    "compound fracture", "bone exposed", "bone sticking out",
    "stab wound", "stabbing", "gunshot", "penetrating injury",
    
    # Toxic & Poisoning
    "poisoning", "swallowed poison", "poison", "drug overdose", "acute overdose",
    "chemical ingestion", "snake bite", "snakebite",
    "suicidal attempt", "suicide attempt", "hanging",
    
    # Severe Allergic / Anaphylaxis
    "anaphylaxis", "anaphylactic shock", "throat closing up", "tongue swelling can't breathe",
    
    # Acute Reproductive / Gynecological & Urological Emergencies
    "heavy vaginal bleeding with fainting", "vaginal bleeding during pregnancy",
    "testicular torsion", "sudden severe testicular pain",
)

# Multi-condition emergency combinations (Trauma + Intracranial / Autonomic red flags)
TRAUMA_TRIGGERS = (
    "head injury", "hit head", "hit on head", "head trauma", "fall", "fell down",
    "accident", "bike fall", "car accident", "blow to head", "concussion", "injury"
)

INTRACRANIAL_SIGNS = (
    "vomiting", "vomit", "bleeding from ear", "blood from ear", "ear bleeding",
    "unconscious", "passed out", "blacked out", "seizure", "convulsions",
    "slurred speech", "drowsy", "unresponsive", "severe confusion", "pupil unequal",
    "amnesia", "clear fluid from nose", "clear fluid from ear"
)

CARDIAC_TRIGGERS = (
    "chest pain", "chest pressure", "crushing chest", "chest tightness", "chest heaviness"
)

CARDIAC_EMERGENCY_CO_SIGNS = (
    "shortness of breath", "breathing problem", "difficulty breathing", "sweating",
    "cold sweat", "left arm", "jaw pain", "fainting", "passed out", "dizziness severe"
)

# Gynecological Hemorrhage & Hypovolemic Shock Combinations
GYN_BLEEDING_TRIGGERS = (
    "vaginal bleeding", "bleeding from vagina", "heavy vaginal bleeding", "vaginal blood",
    "bleeding during pregnancy", "spotting with pain", "abnormal uterine bleeding"
)

GYN_HYPOVOLEMIC_CO_SIGNS = (
    "dizziness", "fainting", "passed out", "blacked out", "lightheaded",
    "lightheadedness", "faint", "pale", "rapid heart", "tachycardia",
    "abdominal cramps", "pelvic cramps", "severe cramps", "severe pain"
)


# =====================================================================
# 2. HIGH-RISK / RED FLAG SYMPTOMS (Flashing Emergency Alert Banner on Screen)
# =====================================================================
RED_FLAG_WARNING_PHRASES = (
    "breathing problem", "breathing difficulty", "difficulty breathing",
    "trouble breathing", "problem in breathing", "shortness of breath",
    "hard to breathe", "breathlessness", "labored breathing", "rapid breathing",
    "gasping", "wheezing badly",
    "tachycardia", "rapid heart rate", "racing heart", "heart racing",
    "heart beating fast", "heart pounding", "irregular heartbeat", "fluttering heart",
    "palpitations", "skipped beats",
    "hallucination", "hallucinations", "hallucinating", "seeing things",
    "hearing voices", "delusions", "paranoia",
    "disorientation", "disoriented", "severe confusion", "confused",
    "altered mental status", "not making sense", "delirium",
    "blurry vision with headache", "sudden blurry vision", "sudden vision loss",
    "double vision sudden", "diplopia sudden",
    "dizziness with palpitations", "feeling faint", "almost passed out",
    "chest heaviness", "burning in chest",
    "severe high fever", "fever with chills and confusion", "fever above 103",
    "blood in urine", "blood in stool", "black stool",
    "unbearable headache", "worst headache of life", "thunderclap headache",
    "sudden numbness", "sudden weakness in arm", "sudden weakness in leg",
    "suicidal thoughts", "severe self harm",
    "severe allergic reaction", "throat tightness", "swollen tongue",
    "uncontrollable shaking", "fits",
    "bruising easily", "easy bruising", "frequent nosebleeds",
    "vaginal bleeding", "bleeding from vagina", "vaginal bleeding with dizziness",
    "vaginal bleeding with cramps", "severe testicular pain", "testicular swelling",
)


def has_critical_emergency(text: str) -> bool:
    """Evaluates whether the complaint is an outright emergency."""
    lower = (text or "").lower()
    
    # 1. Direct emergency phrase match
    if any(phrase in lower for phrase in CRITICAL_EMERGENCY_PHRASES):
        return True

    # 2. Clinical combination rule: Head Trauma / Fall + Intracranial / Hemorrhagic Signs
    # e.g., "fall with head injury, vomiting, bleeding from ear"
    has_trauma = any(re.search(r'\b' + re.escape(t) + r'\b', lower) for t in TRAUMA_TRIGGERS)
    if has_trauma:
        has_intracranial = any(re.search(r'\b' + re.escape(s) + r'\b', lower) for s in INTRACRANIAL_SIGNS)
        if has_intracranial:
            return True

    # 3. Clinical combination rule: Cardiac symptoms + Autonomic / Hemodynamic distress
    has_cardiac = any(re.search(r'\b' + re.escape(c) + r'\b', lower) for c in CARDIAC_TRIGGERS)
    if has_cardiac:
        has_cardiac_co = any(re.search(r'\b' + re.escape(s) + r'\b', lower) for s in CARDIAC_EMERGENCY_CO_SIGNS)
        if has_cardiac_co:
            return True

    return False


def has_red_flag_warning(text: str) -> bool:
    lower = (text or "").lower()
    return any(phrase in lower for phrase in RED_FLAG_WARNING_PHRASES)


def extract_matched_red_flags(text: str) -> list:
    lower = (text or "").lower()
    found = []
    for phrase in RED_FLAG_WARNING_PHRASES:
        if phrase in lower:
            found.append(phrase)
    return list(dict.fromkeys(found))[:4]


def check_safety(
    patient_concern: str,
    age: Optional[int] = None,
    sex: Optional[str] = None,
    weight: Optional[float] = None,
    height: Optional[float] = None
) -> Dict[str, Any]:
    """
    Safety Gate Agent: Evaluates patient concern for acute emergencies and deceptive symptoms.
    Acts as the mandatory gateway in the 5-agent pipeline.
    """
    concern_clean = (patient_concern or "").strip()
    
    vitals_summary = []
    if age is not None:
        vitals_summary.append(f"Age: {age}")
    if sex:
        vitals_summary.append(f"Sex: {sex}")
    if weight and height and height > 0:
        bmi = round(float(weight) / ((float(height) / 100.0) ** 2), 1)
        vitals_summary.append(f"Weight: {weight}kg, Height: {height}cm (BMI: {bmi})")
    vitals_str = ", ".join(vitals_summary) if vitals_summary else "Vitals: Not specified"

    # 1. Deterministic Clinical Emergency Rule Check (FAST-PATH)
    if has_critical_emergency(concern_clean):
        return {
            "is_critical": True,
            "has_warning": True,
            "matched_red_flags": ["Critical Trauma / Acute Life Threat"],
            "advisory": (
                "Critical emergency detected (e.g. acute head trauma, bleeding, or life-threatening distress). "
                "Do NOT wait for an outpatient appointment. Call emergency dispatch (112 or 108) or report to the nearest hospital Emergency Room immediately."
            ),
            "helpline": "112 / 108"
        }

    # 2. Detect high-risk / deceptive red flags
    deterministic_warnings = extract_matched_red_flags(concern_clean)
    has_deterministic_warning = len(deterministic_warnings) > 0

    # 3. Agent LLM Clinical Safety Analysis via Groq (if available)
    prompt = f"""
    You are an Emergency Physician triage director.
    Evaluate the following patient concern and vitals for acute life-threat or deceptive red flags:

    Patient Vitals: {vitals_str}
    Patient Symptoms / Concern: "{concern_clean}"

    CRITICAL RULES:
    1. Acute head injuries, bleeding from ear/nose, sudden collapse, respiratory failure, or severe chest pain 
       are ALWAYS emergencies (CRITICAL: true).
    2. Subtle red flags like "breathing problem", "tachycardia", "disorientation", "hallucination", or "easy bruising"
       require RED_FLAG: true.

    OUTPUT STRICTLY IN THIS FORMAT:
    CRITICAL: [true/false]
    RED_FLAG: [true/false]
    ADVISORY: [Clear medical advice, 1-2 sentences]
    """

    llm_output = call_groq_chat(prompt, temperature=0.0)

    if llm_output:
        is_crit = False
        is_red = has_deterministic_warning
        adv_text = ""

        for line in llm_output.splitlines():
            line_str = line.strip()
            if line_str.upper().startswith("CRITICAL:"):
                is_crit = "true" in line_str.lower()
            elif line_str.upper().startswith("RED_FLAG:"):
                if "true" in line_str.lower():
                    is_red = True
            elif line_str.upper().startswith("ADVISORY:"):
                adv_text = line_str.split(":", 1)[1].strip()

        if is_crit:
            return {
                "is_critical": True,
                "has_warning": True,
                "matched_red_flags": deterministic_warnings or ["Acute clinical distress"],
                "advisory": adv_text or "Critical symptoms detected. Report to the Emergency Department or dial 112 immediately.",
                "helpline": "112 / 108"
            }

        return {
            "is_critical": False,
            "has_warning": is_red,
            "matched_red_flags": deterministic_warnings,
            "advisory": adv_text if adv_text and adv_text.lower() != "none" else (
                "Symptoms warrant close clinical observation. If breathing worsens or chest pain develops, seek immediate emergency care." if is_red else None
            ),
            "helpline": "112 / 108" if is_red else None
        }

    # Fallback when LLM is unavailable
    if has_deterministic_warning:
        return {
            "is_critical": False,
            "has_warning": True,
            "matched_red_flags": deterministic_warnings,
            "advisory": f"Potential red-flag symptoms detected ({', '.join(deterministic_warnings)}). While routing you to the appropriate specialist, please seek immediate emergency care if symptoms escalate.",
            "helpline": "112 / 108"
        }

    return {
        "is_critical": False,
        "has_warning": False,
        "matched_red_flags": [],
        "advisory": None,
        "helpline": None
    }


def is_emergency(safety_result: Dict[str, Any], patient_concern: str = "") -> bool:
    """Helper to detect if routing should be completely halted for ER."""
    if isinstance(safety_result, dict):
        return bool(safety_result.get("is_critical", False))
    return has_critical_emergency(str(safety_result))

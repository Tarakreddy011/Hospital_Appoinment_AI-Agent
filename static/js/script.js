let currentRoutingData = null;

// Calculate BMI Live Preview
function calculateBMIPreview() {
  const weight = parseFloat(document.getElementById('patient-weight').value);
  const height = parseFloat(document.getElementById('patient-height').value);
  const container = document.getElementById('bmi-preview-container');
  const valSpan = document.getElementById('bmi-value');
  const catSpan = document.getElementById('bmi-category');

  if (weight > 0 && height > 0) {
    const bmi = (weight / Math.pow(height / 100, 2)).toFixed(1);
    container.style.display = 'block';
    valSpan.innerText = bmi;

    if (bmi < 18.5) {
      catSpan.innerText = 'Underweight';
      catSpan.className = 'bmi-pill bmi-underweight';
    } else if (bmi < 25) {
      catSpan.innerText = 'Normal';
      catSpan.className = 'bmi-pill bmi-normal';
    } else if (bmi < 30) {
      catSpan.innerText = 'Overweight';
      catSpan.className = 'bmi-pill bmi-overweight';
    } else {
      catSpan.innerText = 'Obese';
      catSpan.className = 'bmi-pill bmi-obese';
    }
  } else {
    container.style.display = 'none';
  }
}

function clearForm() {
  document.getElementById('triage-form').reset();
  document.getElementById('bmi-preview-container').style.display = 'none';
  document.getElementById('returning-banner').style.display = 'none';
  hideFlashEmergencyBanner();
  document.getElementById('output-container').innerHTML = `
    <div class="white-card" style="min-height: 480px; display:flex; align-items:center; justify-content:center;">
      <div class="empty-output-state">
        <div class="empty-output-icon">🩺</div>
        <h3 style="font-size:1.15rem; color:#334155;">Ready for Clinical Evaluation</h3>
        <p style="font-size:0.88rem; max-width:340px; margin:0.4rem auto 0 auto; color:#64748b;">
          Fill in patient demographics, vitals, and symptoms on the left to initiate safety screening, RAG guideline retrieval, and specialty doctor booking.
        </p>
      </div>
    </div>
  `;
}

// Flash Emergency Banner Handlers
function showFlashEmergencyBanner(title, desc, isCritical = false) {
  const banner = document.getElementById('flash-emergency-banner');
  const titleEl = document.getElementById('flash-title');
  const descEl = document.getElementById('flash-desc');

  if (!banner) return;
  titleEl.innerText = title;
  descEl.innerText = desc;
  banner.className = isCritical ? 'flash-emergency-top flash-critical-blink' : 'flash-emergency-top flash-warning-amber';
  banner.style.display = 'block';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function hideFlashEmergencyBanner() {
  const banner = document.getElementById('flash-emergency-banner');
  if (banner) banner.style.display = 'none';
}

// Database Memory Check when user enters phone
async function checkPatientHistory() {
  const phone = document.getElementById('patient-phone').value.trim();
  const banner = document.getElementById('returning-banner');
  const nameInput = document.getElementById('patient-name');
  const ageInput = document.getElementById('patient-age');
  const sexInput = document.getElementById('patient-sex');
  const weightInput = document.getElementById('patient-weight');
  const heightInput = document.getElementById('patient-height');

  if (!phone || phone.length < 5) {
    banner.style.display = 'none';
    return;
  }

  try {
    const res = await fetch(`/api/check-patient?phone=${encodeURIComponent(phone)}`);
    const data = await res.json();

    if (data.found) {
      banner.style.display = 'block';
      document.getElementById('returning-welcome').innerText = `Welcome back, ${data.name || 'Patient'}!`;
      document.getElementById('ret-date').innerText = data.last_visit || 'Recent';

      let cleanDept = data.last_department || 'General Medicine';
      cleanDept = cleanDept.replace(/\|/g, '•').replace(/\(|\)/g, '');
      document.getElementById('ret-dept').innerText = cleanDept;
      document.getElementById('ret-concern').innerText = `"${data.last_concern || 'Prior consultation'}"`;

      if (!nameInput.value.trim() && data.name) nameInput.value = data.name;
      if (!ageInput.value && data.age) ageInput.value = data.age;
      if (!sexInput.value && data.sex) sexInput.value = data.sex;
      if (!weightInput.value && data.weight) weightInput.value = data.weight;
      if (!heightInput.value && data.height) heightInput.value = data.height;

      calculateBMIPreview();
    } else {
      banner.style.display = 'none';
    }
  } catch (err) {
    banner.style.display = 'none';
  }
}

// Form Submission & Pipeline Execution
async function handleTriageSubmit(e) {
  e.preventDefault();

  const name = document.getElementById('patient-name').value.trim();
  const phone = document.getElementById('patient-phone').value.trim();
  const ageVal = document.getElementById('patient-age').value.trim();
  const sex = document.getElementById('patient-sex').value;
  const weightVal = document.getElementById('patient-weight').value.trim();
  const heightVal = document.getElementById('patient-height').value.trim();
  const patient_concern = document.getElementById('patient-concern').value.trim();

  if (!name || !phone || !patient_concern || !ageVal || !sex) {
    alert("Please fill in all required fields (Name, Phone, Age, Sex, Symptoms).");
    return;
  }

  const age = parseInt(ageVal, 10);
  const weight = weightVal ? parseFloat(weightVal) : null;
  const height = heightVal ? parseFloat(heightVal) : null;

  const submitBtn = document.getElementById('submit-btn');
  const btnText = document.getElementById('btn-text');
  const btnSpinner = document.getElementById('btn-spinner');
  const outputContainer = document.getElementById('output-container');

  submitBtn.disabled = true;
  btnText.innerText = "Evaluating AI Clinical Triage...";
  btnSpinner.style.display = "inline-block";

  outputContainer.innerHTML = `
    <div class="white-card" style="min-height: 480px; display:flex; align-items:center; justify-content:center;">
      <div style="text-align:center; padding:2rem; color:var(--text-muted);">
        <div class="spinner" style="width:40px; height:40px; border-color: rgba(2,132,199,0.25); border-top-color: var(--primary); margin-bottom:1rem;"></div>
        <h4 style="color:#0f172a; margin-bottom:0.35rem; font-size:1.1rem;">Running 5-Agent Clinical Pipeline...</h4>
        <p style="font-size:0.85rem; max-width:320px; margin:0 auto;">
          Evaluating safety gate red flags, multi-system syndrome patterns, RAG preparation guidelines, and doctor slots.
        </p>
      </div>
    </div>
  `;

  try {
    const response = await fetch('/api/route', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        phone,
        patient_concern,
        age,
        sex,
        weight,
        height
      })
    });

    const data = await response.json();
    currentRoutingData = data;
    renderOutput(data);
  } catch (err) {
    outputContainer.innerHTML = `
      <div class="white-card" style="border-left: 4px solid var(--danger);">
        <h3 style="color:var(--danger); margin-bottom:0.5rem;">Clinical Evaluation Error</h3>
        <p style="color:var(--text-muted); font-size:0.9rem;">Could not complete routing: ${escapeHtml(err.message)}</p>
      </div>
    `;
  } finally {
    submitBtn.disabled = false;
    btnText.innerText = "Submit for AI Clinical Triage";
    btnSpinner.style.display = "none";
  }
}

// Render Results Card
function renderOutput(data) {
  const outputContainer = document.getElementById('output-container');

  // 1. CRITICAL EMERGENCY CASE
  if (data.is_urgent) {
    showFlashEmergencyBanner(
      "🚨 CRITICAL MEDICAL EMERGENCY DETECTED",
      "Immediate life threat identified. Outpatient appointment halted. Call 112 / 108 or report to ER now.",
      true
    );

    outputContainer.innerHTML = `
      <div class="emergency-card">
        <div class="emergency-icon">🚨</div>
        <div class="emergency-title">IMMEDIATE EMERGENCY CARE REQUIRED</div>
        <p style="color:#7f1d1d; font-size:0.92rem; font-weight:600; margin-bottom:1rem;">
          Routine outpatient appointment routing has been halted immediately to safeguard patient life.
        </p>

        <div class="emergency-advice-box">
          <div class="emergency-advice-header">
            <span>⚠️</span> <span>Critical Clinical Evaluation</span>
          </div>
          <div class="emergency-advice-body">
            ${escapeHtml(data.emergency_advice || 'Acute emergency symptoms detected requiring immediate resuscitation or urgent hospital care.')}
          </div>
        </div>

        <p style="font-size:0.88rem; color:#991b1b; margin-bottom:1.35rem;">
          Do not wait for a clinic consultation. Please dial emergency medical dispatch immediately or proceed to the nearest hospital Emergency Department.
        </p>

        <a href="tel:112" class="emergency-call-btn">
          📞 Call Emergency Services (Dial 112 / 108)
        </a>
      </div>
    `;
    return;
  }

  // 2. BORDERLINE / RED-FLAG WARNING FLASH (e.g. breathing problem, tachycardia, disorientation)
  if (data.has_warning) {
    const redFlagsList = (data.matched_red_flags && data.matched_red_flags.length > 0)
      ? data.matched_red_flags.join(', ')
      : "Potentially serious symptoms";
    showFlashEmergencyBanner(
      `⚠️ POTENTIAL HIGH-RISK SYMPTOMS DETECTED (${redFlagsList.toUpperCase()})`,
      `While you are being routed, if symptoms suddenly deteriorate (severe breathlessness, chest pain, or loss of balance), call 112/108 or visit ER immediately.`,
      false
    );
  } else {
    hideFlashEmergencyBanner();
  }

  // 3. ROUTINE OUTPATIENT ROUTING WITH VITALS & SCHEDULE
  const slots = data.booking_options || [];
  const slotsHtml = slots.map((s, idx) => `
    <div class="slot-card ${idx === 0 ? 'active' : ''}" onclick="selectSlot(${idx}, this)">
      <div class="slot-doctor">${escapeHtml(s.doctor)}</div>
      <div class="slot-time">${escapeHtml(s.time)}</div>
      <div class="slot-room">${escapeHtml(s.room)} • ${escapeHtml(s.type || 'Consultation')}</div>
    </div>
  `).join('');

  const cleanSlipHtml = formatAppointmentSlip(data.assigned_booking, data.selected_slot || slots[0], data.department);
  const cleanDownDetailsHtml = renderDownDetails(data);

  // Vitals Pill summary
  const vitalsPills = [];
  if (data.age) vitalsPills.push(`Age: <b>${data.age} yrs</b>`);
  if (data.sex) vitalsPills.push(`Sex: <b>${data.sex}</b>`);
  if (data.weight) vitalsPills.push(`Weight: <b>${data.weight} kg</b>`);
  if (data.height) vitalsPills.push(`Height: <b>${data.height} cm</b>`);
  if (data.bmi) vitalsPills.push(`BMI: <b>${data.bmi}</b>`);

  outputContainer.innerHTML = `
    <div class="result-box">
      <!-- TOP DEPARTMENT BADGE -->
      <div class="result-header">
        <div>
          <span style="font-size:0.72rem; font-weight:700; text-transform:uppercase; color:var(--text-muted); display:block; margin-bottom:0.2rem;">
            Recommended Specialty Department
          </span>
          <div class="dept-badge">
            <span>🏥</span>
            <span>${escapeHtml(data.department || 'General Medicine')}</span>
          </div>
        </div>
        <div style="text-align:right;">
          <span class="safe-badge">
            ✓ Cleared for Outpatient OPD
          </span>
        </div>
      </div>

      <!-- PROMINENT DEPARTMENT DISPATCH & 2-3 HELPLINES CALLOUT -->
      <div class="dept-helpline-box">
        <div class="dept-helpline-header">
          <div class="dept-icon-pill">🏥</div>
          <div style="flex:1;">
            <div class="dept-title-sub">CLINICAL DEPARTMENT ASSIGNED</div>
            <div class="dept-title-main">${escapeHtml(data.department || 'General Medicine')}</div>
            <div class="care-levels-strip">
              <span class="care-level-pill ${data.care_levels && data.care_levels.opd ? 'care-available' : 'care-unavailable'}">
                ${data.care_levels && data.care_levels.opd ? '✓' : '✗'} OPD
              </span>
              <span class="care-level-pill ${data.care_levels && data.care_levels.ipd ? 'care-available' : 'care-unavailable'}">
                ${data.care_levels && data.care_levels.ipd ? '✓' : '✗'} IPD
              </span>
              <span class="care-level-pill ${data.care_levels && data.care_levels.icu ? 'care-available' : 'care-unavailable'}">
                ${data.care_levels && data.care_levels.icu ? '✓' : '✗'} ICU
              </span>
            </div>
          </div>
        </div>
        <div class="helplines-grid">
          <a href="tel:112" class="helpline-card emergency-hl">
            <span class="hl-badge">24/7 National</span>
            <span class="hl-name">National Emergency & Ambulance</span>
            <span class="hl-number">📞 Dial 112</span>
          </a>
          <a href="tel:108" class="helpline-card trauma-hl">
            <span class="hl-badge">Medical</span>
            <span class="hl-name">Medical Emergency & Trauma</span>
            <span class="hl-number">🚑 Dial 108</span>
          </a>
          <a href="tel:0804567890" class="helpline-card hospital-hl">
            <span class="hl-badge">Hospital Desk</span>
            <span class="hl-name">LifeCare Central Triage Desk</span>
            <span class="hl-number">☎️ 080-456-7890</span>
          </a>
        </div>
      </div>

      <!-- PATIENT VITALS CHIP ROW -->
      ${vitalsPills.length > 0 ? `
        <div class="patient-vitals-strip">
          <span style="color:#64748b; font-size:0.75rem; font-weight:600;">Patient Profile:</span>
          ${vitalsPills.map(p => `<span class="vital-pill">${p}</span>`).join('')}
        </div>
      ` : ''}

      <!-- WARNING ADVISORY CALLOUT (IF RED FLAG PRESENT) -->
      ${data.has_warning ? `
        <div class="warning-callout-box">
          <div class="warning-callout-header">
            <span>⚠️ Clinical Caution Notice</span>
            <span class="call-helpline-tag">Emergency: 112 / 108</span>
          </div>
          <p style="font-size:0.84rem; color:#854d0e; margin:0.3rem 0 0 0; line-height:1.45;">
            ${escapeHtml(data.warning_advisory || 'Some symptoms (such as breathing difficulty or tachycardia) require close observation. Seek immediate emergency admission if condition worsens.')}
          </p>
        </div>
      ` : ''}

      <!-- CLINICAL RATIONALE -->
      <div class="clinical-rationale-box">
        <strong>Clinical Triage Rationale:</strong><br>
        ${escapeHtml(data.rationale || 'Patient symptoms and physical indicators correspond to this specialty.')}
      </div>

      <!-- DOCTOR SLOTS SELECTION -->
      <div class="section-title">
        <span>👨‍⚕️</span> Select Consulting Doctor & Time Slot
      </div>
      <div class="slots-grid">
        ${slotsHtml}
      </div>

      <!-- CONFIRMED APPOINTMENT PASS -->
      <div id="booking-slip-container">
        ${cleanSlipHtml}
      </div>

      <!-- RAG INSTRUCTIONS & CHECKLIST -->
      <div class="section-title" style="margin-top:1.75rem;">
        <span>📋</span> Clinic Preparation & Required Documents
      </div>
      ${cleanDownDetailsHtml}
    </div>
  `;
}

// Appointment Slip Formatter
function formatAppointmentSlip(rawText, slot, department) {
  let code = "APPT-" + Math.floor(10000 + Math.random() * 90000);
  if (rawText) {
    const match = rawText.match(/APPT-[\w\d]+/i);
    if (match) code = match[0];
  }

  const doctor = slot ? slot.doctor : "Assigned Medical Officer";
  const time = slot ? slot.time : "Today, 04:00 PM";
  const room = slot ? slot.room : "Room 102, Block A";
  const clinicType = slot && slot.type ? slot.type : "OPD Consultation";

  return `
    <div class="appointment-pass-card">
      <div class="pass-top-bar">
        <div>
          <div class="pass-label">CONFIRMED OPD APPOINTMENT PASS</div>
          <div class="pass-code">${escapeHtml(code)}</div>
        </div>
        <div class="pass-status-badge">
          <span style="display:inline-block; width:6px; height:6px; background:#16a34a; border-radius:50%;"></span>
          Confirmed & Logged in Registry
        </div>
      </div>

      <div class="pass-grid">
        <div class="pass-cell">
          <span class="cell-label">CONSULTING SPECIALIST</span>
          <span class="cell-value">👨‍⚕️ ${escapeHtml(doctor)}</span>
        </div>
        <div class="pass-cell">
          <span class="cell-label">DEPARTMENT & CLINIC</span>
          <span class="cell-value">🏥 ${escapeHtml(department)} (${escapeHtml(clinicType)})</span>
        </div>
        <div class="pass-cell">
          <span class="cell-label">SCHEDULED DATE & TIME</span>
          <span class="cell-value" style="color:var(--primary);">🕒 ${escapeHtml(time)}</span>
        </div>
        <div class="pass-cell">
          <span class="cell-label">CLINIC LOCATION</span>
          <span class="cell-value">📍 ${escapeHtml(room)}</span>
        </div>
      </div>

      <div class="pass-footer-note">
        <span>ℹ️</span>
        <span>Please arrive 10-15 minutes prior to your slot and show this digital pass at OPD Reception Block B.</span>
      </div>
    </div>
  `;
}

// RAG Instructions & What to Bring Dual-Card UI
function renderDownDetails(data) {
  let guidelines = [];
  let whatToBring = [];

  if (data.structured_instructions) {
    guidelines = data.structured_instructions.guidelines || [];
    whatToBring = data.structured_instructions.what_to_bring || [];
  }

  if (guidelines.length === 0) {
    guidelines = [
      "Arrive 10-15 minutes prior for nursing vitals measurement.",
      "Check in at OPD Reception Desk Block B for token verification.",
      "Bring all current medication strips or bottles."
    ];
  }

  if (whatToBring.length === 0) {
    whatToBring = [
      "Government Photo ID card (Aadhaar / Driver's License).",
      "Previous medical records, prescription slips, and recent lab/scan reports.",
      "Active health insurance or cashless card if applicable."
    ];
  }

  return `
    <div class="prep-dual-grid">
      <!-- CARD 1: PRE-VISIT GUIDELINES -->
      <div class="prep-box-card card-guidelines">
        <div class="prep-box-header">
          <div class="prep-icon-wrapper icon-blue">⏳</div>
          <div>
            <div class="prep-box-title">Pre-Visit Preparation</div>
            <div class="prep-box-subtitle">Instructions to follow before your slot</div>
          </div>
        </div>
        <ul class="prep-item-list">
          ${guidelines.map(g => `
            <li class="prep-list-item">
              <span class="check-pill check-blue">✓</span>
              <span>${escapeHtml(g)}</span>
            </li>
          `).join('')}
        </ul>
      </div>

      <!-- CARD 2: REQUIRED CHECKLIST -->
      <div class="prep-box-card card-bring">
        <div class="prep-box-header">
          <div class="prep-icon-wrapper icon-teal">📑</div>
          <div>
            <div class="prep-box-title">Required Documents</div>
            <div class="prep-box-subtitle">Checklist to bring to the hospital</div>
          </div>
        </div>
        <ul class="prep-item-list">
          ${whatToBring.map(b => `
            <li class="prep-list-item">
              <span class="check-pill check-teal">✓</span>
              <span>${escapeHtml(b)}</span>
            </li>
          `).join('')}
        </ul>
      </div>
    </div>

    <div class="opd-help-banner">
      <span style="font-size:1.1rem;">ℹ️</span>
      <div>
        <b>Need hospital assistance?</b> Contact the LifeCare Outpatient Desk at <a href="tel:0804567890">080-456-7890</a> or visit Central OPD Registration Block B upon arrival.
      </div>
    </div>
  `;
}

async function selectSlot(index, element) {
  if (!currentRoutingData || !currentRoutingData.booking_options) return;

  const slots = currentRoutingData.booking_options;
  const selected = slots[index];
  if (!selected) return;

  document.querySelectorAll('.slot-card').forEach(el => el.classList.remove('active'));
  element.classList.add('active');

  try {
    const res = await fetch('/api/book-slot', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone: currentRoutingData.phone,
        department: currentRoutingData.department,
        slot: selected
      })
    });
    const respData = await res.json();
    if (respData.success) {
      document.getElementById('booking-slip-container').innerHTML =
        formatAppointmentSlip(respData.confirmation || respData.code, selected, currentRoutingData.department);
    }
  } catch (err) {
    console.error("Failed to update slot booking", err);
  }
}

function escapeHtml(text) {
  if (!text) return '';
  const div = document.createElement('div');
  div.innerText = text;
  return div.innerHTML;
}

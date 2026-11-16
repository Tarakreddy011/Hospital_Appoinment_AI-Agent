let currentRoutingData = null;

    // Real-time Database Memory Check when user enters phone
    async function checkPatientHistory() {
      const phone = document.getElementById('patient-phone').value.trim();
      const banner = document.getElementById('returning-banner');
      const nameInput = document.getElementById('patient-name');

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
          
          // Clean up prior clinic string (remove pipeline brackets/pipes)
          let cleanDept = data.last_department || 'General Medicine';
          cleanDept = cleanDept.replace(/\|/g, '•').replace(/\(|\)/g, '');
          document.getElementById('ret-dept').innerText = cleanDept;
          
          document.getElementById('ret-concern').innerText = `"${data.last_concern || 'Prior consultation'}"`;

          if (!nameInput.value.trim() && data.name) {
            nameInput.value = data.name;
          }
        } else {
          banner.style.display = 'none';
        }
      } catch (err) {
        banner.style.display = 'none';
      }
    }

    async function handleTriageSubmit(e) {
      e.preventDefault();

      const name = document.getElementById('patient-name').value.trim();
      const phone = document.getElementById('patient-phone').value.trim();
      const patient_concern = document.getElementById('patient-concern').value.trim();

      if (!name || !phone || !patient_concern) return;

      const submitBtn = document.getElementById('submit-btn');
      const btnText = document.getElementById('btn-text');
      const btnSpinner = document.getElementById('btn-spinner');
      const outputContainer = document.getElementById('output-container');

      submitBtn.disabled = true;
      btnText.innerText = "Evaluating Routing...";
      btnSpinner.style.display = "inline-block";

      outputContainer.innerHTML = `
        <div class="white-card" style="min-height: 440px; display:flex; align-items:center; justify-content:center;">
          <div style="text-align:center; padding:2rem; color:var(--text-muted);">
            <div class="spinner" style="width:36px; height:36px; border-color: rgba(2,132,199,0.25); border-top-color: var(--primary); margin-bottom:1rem;"></div>
            <h4 style="color:#0f172a; margin-bottom:0.25rem;">Analyzing Symptoms & Triage Rules...</h4>
            <p style="font-size:0.85rem;">Checking safety protocols, medical speciality matching, and doctor schedules.</p>
          </div>
        </div>
      `;

      try {
        const response = await fetch('/api/route', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, phone, patient_concern })
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
        btnText.innerText = "Submit for Clinical Routing";
        btnSpinner.style.display = "none";
      }
    }

    // Helper: Clean raw backend tags from emergency advice
    function getCleanEmergencyAdvice(data) {
      if (data.emergency_advice) {
        let text = data.emergency_advice;
        text = text.replace(/URGENT:\s*(true|false)/gi, '');
        text = text.replace(/ADVISORY:\s*/gi, '');
        return text.trim();
      }
      return "Immediate in-person emergency care required. Please go to the nearest emergency department.";
    }

    // Helper: Formats appointment pass cleanly
    function formatAppointmentSlip(rawText, slot, department) {
      let code = "APPT-" + Math.floor(10000 + Math.random() * 90000);
      if (rawText) {
        const match = rawText.match(/APPT-[\w\d]+/i);
        if (match) code = match[0];
      }

      const doctor = slot ? slot.doctor : "Assigned Medical Officer";
      const time = slot ? slot.time : "Today, 04:00 PM";
      const room = slot ? slot.room : "Room 102";
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
              <span class="cell-label">CONSULTING DOCTOR</span>
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
            <span>Please arrive 10-15 minutes prior to your slot and show this pass at OPD Reception Block B.</span>
          </div>
        </div>
      `;
    }

    // Helper: Builds beautiful, dual-card UI for down details (Pre-Visit & What to Bring)
    function renderDownDetails(data) {
      let guidelines = [];
      let whatToBring = [];

      // Use structured instructions if available from backend
      if (data.structured_instructions) {
        guidelines = data.structured_instructions.guidelines || [];
        whatToBring = data.structured_instructions.what_to_bring || [];
      } else if (data.instructions) {
        // Fallback robust parser
        const lines = data.instructions.split(/\r?\n/);
        let curr = 'guide';
        for (let l of lines) {
          l = l.trim();
          if (!l || l === '---') continue;
          if (/WHAT TO BRING/i.test(l)) { curr = 'bring'; continue; }
          if (/INTAKE INSTRUCTIONS/i.test(l)) { curr = 'guide'; continue; }
          
          // Check for bullet lines
          if (/^[-*]\s+/.test(l)) {
            let item = l.replace(/^[-*]\s+/, '').trim();
            item = item.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            if (curr === 'bring') whatToBring.push(item);
            else guidelines.push(item);
          }
        }
      }

      // Default fallbacks if empty
      if (guidelines.length === 0) {
        guidelines = [
          "Please arrive 10-15 minutes early for initial vital sign checks.",
          "Check in at the Central OPD Reception Block B for token verification.",
          "Follow any fasting or medication guidance prescribed by your doctor."
        ];
      }

      if (whatToBring.length === 0) {
        whatToBring = [
          "Government Photo ID (e.g. driver's license, Aadhaar, or passport)",
          "All previous medical records, prescription slips, and recent scan reports",
          "Active health insurance card and policy documents"
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
                  <span>${g}</span>
                </li>
              `).join('')}
            </ul>
          </div>

          <!-- CARD 2: REQUIRED ITEMS TO BRING -->
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
                  <span>${b}</span>
                </li>
              `).join('')}
            </ul>
          </div>
        </div>

        <!-- OPD Helpdesk Info Banner -->
        <div class="opd-help-banner">
          <span style="font-size:1.1rem;">ℹ️</span>
          <div>
            <b>Need assistance before your visit?</b> Contact the LifeCare Outpatient Helpdesk at <a href="tel:0804567890">080-456-7890</a> or visit Central OPD Registration Block B upon arrival.
          </div>
        </div>
      `;
    }

    function renderOutput(data) {
      const outputContainer = document.getElementById('output-container');

      // 1. EMERGENCY CASE (No raw backend tags, clean advice + call button)
      if (data.is_urgent) {
        const cleanAdvice = getCleanEmergencyAdvice(data);

        outputContainer.innerHTML = `
          <div class="emergency-card">
            <div class="emergency-icon">🚨</div>
            <div class="emergency-title">URGENT MEDICAL ADVISORY DETECTED</div>
            <p style="color:#7f1d1d; font-size:0.92rem; font-weight:600;">
              Standard outpatient appointment routing has been halted immediately to prioritize patient life safety.
            </p>

            <div class="emergency-advice-box">
              <div class="emergency-advice-header">
                <span>⚠️</span> <span>Critical Clinical Evaluation</span>
              </div>
              <div class="emergency-advice-body">
                ${escapeHtml(cleanAdvice)}
              </div>
            </div>

            <p style="font-size:0.88rem; color:#991b1b; margin-bottom:1.35rem;">
              Do not wait for a clinic appointment. Please call emergency medical dispatch immediately or report directly to the nearest hospital Emergency Room.
            </p>

            <a href="tel:112" class="emergency-call-btn">
              📞 Call Emergency Services (Dial 112 / 108)
            </a>
          </div>
        `;
        return;
      }

      // 2. ROUTINE OUTPATIENT ROUTING: Clean single box
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

      outputContainer.innerHTML = `
        <div class="result-box">
          <!-- Top Department & Status -->
          <div class="result-header">
            <div>
              <span style="font-size:0.75rem; font-weight:700; text-transform:uppercase; color:var(--text-muted); display:block; margin-bottom:0.2rem;">Recommended Department</span>
              <div class="dept-badge">
                <span>🏥</span>
                <span>${escapeHtml(data.department || 'General Medicine')}</span>
              </div>
            </div>
            <div style="text-align:right;">
              <span style="display:inline-block; font-size:0.75rem; font-weight:700; color:#15803d; background:#dcfce7; padding:0.25rem 0.65rem; border-radius:9999px;">
                ✓ Safe for Outpatient OPD
              </span>
            </div>
          </div>

          <!-- Clinical Rationale -->
          <div class="clinical-rationale-box">
            <strong>Clinical Routing Rationale:</strong><br>
            ${escapeHtml(data.rationale || 'Patient symptoms are appropriate for clinical evaluation in this department.')}
          </div>

          <!-- Doctor Booking Options -->
          <div class="section-title">
            <span>👨‍⚕️</span> Select Doctor Consultation Slot
          </div>
          <div class="slots-grid">
            ${slotsHtml}
          </div>

          <!-- Current Confirmed Booking Slip -->
          <div id="booking-slip-container">
            ${cleanSlipHtml}
          </div>

          <!-- DOWN DETAILS: BEAUTIFUL DUAL-CARD MEDICAL UI -->
          <div class="section-title" style="margin-top:1.75rem;">
            <span>📋</span> Instructions & Required Items to Bring
          </div>
          ${cleanDownDetailsHtml}
        </div>
      `;
    }

    async function selectSlot(index, element) {
      if (!currentRoutingData || !currentRoutingData.booking_options) return;
      
      const slots = currentRoutingData.booking_options;
      const selected = slots[index];
      if (!selected) return;

      // Update UI active card
      document.querySelectorAll('.slot-card').forEach(el => el.classList.remove('active'));
      element.classList.add('active');

      // Update booking via API
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

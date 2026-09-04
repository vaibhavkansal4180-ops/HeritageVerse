/**
 * HeritageVerse - Citizen Heritage Watch & AI Damage Analysis Controller
 */

const CitizenWatch = {
  async init() {
    await this.loadSitesDropdown();
    this.bindEvents();
  },

  async loadSitesDropdown() {
    const select = document.getElementById('report-site-select');
    if (!select) return;

    try {
      const res = await APIClient.get('/api/heritage');
      const sites = res.data || [];
      select.innerHTML = '<option value="">-- Select Monitored Heritage Monument * --</option>' +
        sites.map(s => `<option value="${s.id}">${s.name} (${s.city}, ${s.state_name || 'India'})</option>`).join('');

      // If site_id in URL params, pre-select
      const params = new URLSearchParams(window.location.search);
      const preSelectId = params.get('site_id');
      if (preSelectId) {
        select.value = preSelectId;
      }
    } catch (err) {
      console.error('[CitizenWatch] Failed to load monuments:', err);
    }
  },

  bindEvents() {
    const form = document.getElementById('citizen-report-form');
    if (form) {
      form.addEventListener('submit', (e) => this.submitReport(e));
    }

    // Live AI Damage Analysis Trigger
    const descInput = document.getElementById('report-description');
    const issueSelect = document.getElementById('report-issue-type');
    if (descInput && issueSelect) {
      let debounceTimer = null;
      const triggerPreview = () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => this.fetchAIPreview(), 400);
      };

      descInput.addEventListener('input', triggerPreview);
      issueSelect.addEventListener('change', triggerPreview);
    }

    // Image Upload Preview
    const imageInput = document.getElementById('report-image-input');
    const imagePreviewWrap = document.getElementById('image-preview-wrap');
    const imagePreviewImg = document.getElementById('image-preview-img');
    if (imageInput && imagePreviewWrap && imagePreviewImg) {
      imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (re) => {
            imagePreviewImg.src = re.target.result;
            imagePreviewWrap.style.display = 'block';
          };
          reader.readAsDataURL(file);
        } else {
          imagePreviewWrap.style.display = 'none';
        }
      });
    }

    // Fast Tracking Lookup Form
    const trackForm = document.getElementById('fast-track-form');
    if (trackForm) {
      trackForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const uidInput = document.getElementById('track-uid-input');
        if (uidInput && uidInput.value.trim()) {
          window.location.href = `/track.html?uid=${encodeURIComponent(uidInput.value.trim().toUpperCase())}`;
        }
      });
    }
  },

  async fetchAIPreview() {
    const issueType = document.getElementById('report-issue-type')?.value;
    const description = document.getElementById('report-description')?.value;
    const location = document.getElementById('report-location')?.value || '';
    const previewContainer = document.getElementById('ai-preview-container');

    if (!previewContainer || !description || description.trim().length < 8) {
      if (previewContainer) previewContainer.style.display = 'none';
      return;
    }

    try {
      const res = await APIClient.post('/api/reports/analyze-preview', {
        issue_type: issueType,
        description: description,
        location: location
      });
      const ai = res.data;

      previewContainer.innerHTML = `
        <div class="ai-findings-card">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="ai-badge-tag"><i class="fas fa-brain"></i> AI Preliminary Analysis</span>
            <span style="font-size:0.75rem; font-weight:700; color:var(--primary);">Confidence: ${ai.confidence_score}%</span>
          </div>
          <div style="margin-top:0.35rem; font-size:0.88rem; line-height:1.5;">
            <div><strong>Estimated Severity:</strong> <span class="risk-badge risk-${ai.severity_estimated.toLowerCase()}">${ai.severity_estimated}</span></div>
            <div style="margin-top:0.25rem;"><strong>Visible Damage Signs:</strong> ${ai.damage_signs}</div>
            <div style="margin-top:0.25rem;"><strong>Urgency Assessment:</strong> <span style="color:var(--accent); font-weight:600;">${ai.urgency}</span></div>
          </div>
          <div class="ai-disclaimer"><i class="fas fa-info-circle"></i> ${ai.disclaimer}</div>
        </div>
      `;
      previewContainer.style.display = 'block';
    } catch (err) {
      console.warn('[AI Preview] Error:', err);
    }
  },

  async submitReport(e) {
    e.preventDefault();
    const submitBtn = document.getElementById('report-submit-btn');
    const form = document.getElementById('citizen-report-form');

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting & Analyzing...';
    }

    try {
      const formData = new FormData(form);
      const res = await APIClient.postFormData('/api/reports', formData);
      const report = res.data;

      Toast.success(`Report #${report.report_uid} submitted successfully!`);

      // Display Success Modal / View with Tracking UID
      const successModal = document.getElementById('report-success-modal');
      if (successModal) {
        document.getElementById('modal-report-uid').textContent = report.report_uid;
        document.getElementById('modal-view-track-btn').href = `/track.html?uid=${report.report_uid}`;
        successModal.style.display = 'flex';
      } else {
        setTimeout(() => {
          window.location.href = `/track.html?uid=${report.report_uid}`;
        }, 1500);
      }
    } catch (err) {
      Toast.error(err.message || 'Failed to submit report. Please verify inputs.');
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Submit Incident Report';
      }
    }
  },

  async loadMyReports() {
    const listContainer = document.getElementById('my-reports-list');
    if (!listContainer) return;

    if (!Auth.isLoggedIn()) {
      listContainer.innerHTML = `
        <div class="kpi-card" style="padding:2.5rem; text-align:center;">
          <i class="fas fa-lock" style="font-size:2rem; color:var(--accent); margin-bottom:0.75rem; display:block;"></i>
          <h3 style="font-family:var(--font-serif); font-size:1.2rem; color:var(--primary); margin-bottom:0.5rem;">Authentication Required</h3>
          <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:1.25rem;">Please log in to view and track your submitted citizen preservation reports.</p>
          <a href="/login.html" class="btn btn-primary btn-sm"><i class="fas fa-sign-in-alt"></i> Sign In to Account</a>
        </div>
      `;
      return;
    }

    try {
      const res = await APIClient.get('/api/reports/my');
      const reports = res.data || [];

      if (reports.length === 0) {
        listContainer.innerHTML = `
          <div class="kpi-card" style="padding:3rem; text-align:center;">
            <i class="fas fa-clipboard-check" style="font-size:2.5rem; color:var(--text-dim); margin-bottom:0.75rem; display:block;"></i>
            <h3 style="font-family:var(--font-serif); font-size:1.2rem; color:var(--primary); margin-bottom:0.35rem;">No Reports Logged Yet</h3>
            <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:1.5rem;">You haven't submitted any heritage damage or vandalism incident reports yet.</p>
            <a href="/report.html" class="btn btn-primary btn-sm"><i class="fas fa-bullhorn"></i> Submit New Report</a>
          </div>
        `;
        return;
      }

      listContainer.innerHTML = reports.map(r => {
        const ai = r.ai_analysis || {};
        return `
          <div class="kpi-card" style="text-align:left; padding:1.5rem; margin-bottom:1.25rem;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.75rem;">
              <div>
                <span style="font-size:0.75rem; font-weight:700; color:var(--accent); text-transform:uppercase;">Tracking ID: ${r.report_uid}</span>
                <h3 style="font-family:var(--font-serif); font-size:1.2rem; color:var(--primary); margin:0.15rem 0;">
                  <a href="/site-detail.html?id=${r.heritage_site_id}">${r.heritage_site_name || 'Monument'}</a> — ${r.issue_type}
                </h3>
                <div style="font-size:0.8rem; color:var(--text-dim);"><i class="fas fa-map-marker-alt"></i> ${r.location || 'Site perimeter'} &bull; <i class="fas fa-calendar-alt"></i> Logged: ${r.created_at || r.incident_date}</div>
              </div>
              <div style="display:flex; flex-direction:column; align-items:flex-end; gap:0.35rem;">
                <span class="badge" style="background:var(--bg-card-alt); font-weight:700; color:var(--primary);">${r.status}</span>
                <span class="risk-badge risk-${r.severity.toLowerCase()}">${r.severity} Severity</span>
              </div>
            </div>

            <p style="font-size:0.88rem; color:var(--text-main); margin-bottom:1rem; line-height:1.5;">${r.description}</p>

            ${ai.damage_signs ? `
              <div style="background:rgba(184,92,56,0.06); border:1px solid rgba(184,92,56,0.2); padding:0.75rem; border-radius:var(--radius-sm); margin-bottom:1rem; font-size:0.8rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:0.25rem;">
                  <strong style="color:var(--accent);"><i class="fas fa-brain"></i> AI Preliminary Finding:</strong>
                  <span style="color:var(--text-muted);">${ai.confidence_score || 85}% confidence</span>
                </div>
                <div>${ai.damage_signs}</div>
              </div>
            ` : ''}

            ${r.admin_remarks ? `
              <div style="background:var(--bg-card-alt); border-left:3px solid var(--primary); padding:0.75rem 1rem; border-radius:var(--radius-sm); margin-bottom:1rem; font-size:0.85rem;">
                <strong style="color:var(--primary); font-size:0.78rem; text-transform:uppercase; display:block; margin-bottom:0.25rem;">
                  <i class="fas fa-shield-alt"></i> Official Archaeological Remarks:
                </strong>
                <p style="color:var(--text-main); margin:0;">${r.admin_remarks}</p>
              </div>
            ` : ''}

            <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--border-subtle); padding-top:0.75rem; font-size:0.82rem;">
              <span style="color:var(--text-dim);"><i class="fas fa-user-check"></i> ${r.user_name || 'Citizen'}</span>
              <a href="/track.html?uid=${r.report_uid}" class="btn btn-secondary btn-sm" style="font-size:0.78rem; padding:0.3rem 0.75rem;">
                <i class="fas fa-search-location"></i> View Public Timeline
              </a>
            </div>
          </div>
        `;
      }).join('');

    } catch (err) {
      console.error('[My Reports] Error:', err);
      listContainer.innerHTML = `<div class="kpi-card" style="padding:2rem; text-align:center; color:var(--accent);">Failed to load your reports.</div>`;
    }
  }
};


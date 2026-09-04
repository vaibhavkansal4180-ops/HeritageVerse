/**
 * HeritageVerse - Preservation Intelligence Command Center & Moderation Controller
 */

const CommandCenter = {
  currentAlertId: null,
  currentReportId: null,
  alertsCache: [],
  reportsCache: [],
  charts: {},

  async init() {
    if (!Auth.isLoggedIn() || !Auth.isAdmin()) {
      Toast.error('Unauthorized access. Admin conservation credentials required.');
      setTimeout(() => { window.location.href = '/login.html'; }, 1000);
      return;
    }

    await this.loadDashboardMetrics();
    await this.loadAlerts();
    await this.loadReports();
    await this.loadEncroachments();
    this.bindEvents();
  },

  bindEvents() {
    // Alert Filter
    const alertFilter = document.getElementById('admin-alert-priority-filter');
    if (alertFilter) {
      alertFilter.addEventListener('change', (e) => this.loadAlerts(e.target.value));
    }

    // Report Filter
    const reportFilter = document.getElementById('admin-report-status-filter');
    if (reportFilter) {
      reportFilter.addEventListener('change', (e) => this.loadReports(e.target.value));
    }

    // Alert Action Form
    const alertActionForm = document.getElementById('admin-alert-action-form');
    if (alertActionForm) {
      alertActionForm.addEventListener('submit', (e) => this.submitAlertAction(e));
    }

    // Report Status Form
    const reportStatusForm = document.getElementById('admin-report-moderate-form');
    if (reportStatusForm) {
      reportStatusForm.addEventListener('submit', (e) => this.submitReportModeration(e));
    }
  },

  async loadDashboardMetrics() {
    try {
      const res = await APIClient.get('/api/preservation/dashboard');
      const data = res.data;
      const s = data.summary || {};

      document.getElementById('stat-total-sites').textContent = s.total_monitored_sites || 0;
      document.getElementById('stat-healthy-sites').textContent = s.healthy_sites || 0;
      document.getElementById('stat-attention-sites').textContent = s.attention_sites || 0;
      document.getElementById('stat-high-risk-sites').textContent = s.high_risk_sites || 0;
      document.getElementById('stat-critical-sites').textContent = s.critical_sites || 0;
      document.getElementById('stat-open-reports').textContent = s.open_reports_count || 0;
      document.getElementById('stat-active-alerts').textContent = s.active_alerts_count || 0;
      document.getElementById('stat-encroachments').textContent = s.total_encroachments_detected || 0;

      // Render Charts
      this.renderHealthDistributionChart(data.health_distribution);
      this.renderCategoriesChart(data.issue_categories);

    } catch (err) {
      console.error('[CommandCenter] Metrics error:', err);
    }
  },

  renderHealthDistributionChart(dist = {}) {
    const ctx = document.getElementById('health-dist-chart');
    if (!ctx || typeof Chart === 'undefined') return;

    if (this.charts.health) this.charts.health.destroy();

    this.charts.health = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: Object.keys(dist),
        datasets: [{
          data: Object.values(dist),
          backgroundColor: ['#1E824C', '#D97706', '#EA580C', '#DC2626'],
          borderWidth: 2,
          borderColor: '#FFFFFF'
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 12, font: { family: 'Inter', size: 11 } } }
        },
        cutout: '65%'
      }
    });
  },

  renderCategoriesChart(cats = {}) {
    const ctx = document.getElementById('categories-chart');
    if (!ctx || typeof Chart === 'undefined') return;

    if (this.charts.categories) this.charts.categories.destroy();

    this.charts.categories = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: Object.keys(cats),
        datasets: [{
          label: 'Incidents Logged',
          data: Object.values(cats),
          backgroundColor: '#173F35',
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: { beginAtZero: true, grid: { color: 'rgba(23, 63, 53, 0.06)' } },
          x: { grid: { display: false } }
        }
      }
    });
  },

  // ==========================================
  // EARLY WARNING ALERTS DESK
  // ==========================================
  async loadAlerts(priority = 'all') {
    const container = document.getElementById('admin-alerts-container');
    if (!container) return;

    container.innerHTML = `<div style="text-align:center; padding:2rem;"><i class="fas fa-spinner fa-spin" style="font-size:1.5rem; color:var(--primary);"></i> Loading alerts...</div>`;

    try {
      const endpoint = priority && priority !== 'all' ? `/api/alerts?priority=${priority}` : '/api/alerts';
      const res = await APIClient.get(endpoint);
      this.alertsCache = res.data || [];

      if (this.alertsCache.length === 0) {
        container.innerHTML = `<div style="text-align:center; padding:2rem; color:var(--text-muted);">No active alerts matching this filter.</div>`;
        return;
      }

      container.innerHTML = this.alertsCache.map(a => `
        <div class="alert-card priority-${a.priority}">
          <div>
            <span class="risk-badge risk-${a.priority.toLowerCase()}">${a.priority}</span>
          </div>
          <div>
            <div style="font-size:0.75rem; color:var(--accent); font-weight:700;">${a.alert_uid} &bull; ${a.alert_type}</div>
            <h4 style="font-family:var(--font-serif); font-size:1.1rem; color:var(--primary); margin:0.15rem 0;">
              <a href="/site-detail.html?id=${a.heritage_site_id}">${a.heritage_site_name || 'Monument'}</a> — ${a.title}
            </h4>
            <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.35rem;">${a.description}</p>
            <div style="font-size:0.78rem; color:var(--text-dim);">
              <strong>Trigger:</strong> ${a.trigger_reason} &bull; 
              <strong>Assigned:</strong> ${a.assigned_to || 'Unassigned'}
            </div>
          </div>
          <div style="display:flex; flex-direction:column; gap:0.4rem; align-items:flex-end;">
            <span class="badge" style="background:var(--bg-card-alt); font-size:0.75rem; font-weight:700; color:var(--primary);">${a.status}</span>
            <button onclick="CommandCenter.openAlertActionModal(${a.id})" class="btn btn-primary btn-sm">
              <i class="fas fa-tasks"></i> Dispatch Action
            </button>
          </div>
        </div>
      `).join('');
    } catch (err) {
      console.error('[Alerts] Load error:', err);
    }
  },

  openAlertActionModal(alertId) {
    const alert = this.alertsCache.find(a => a.id === alertId);
    if (!alert) return;

    this.currentAlertId = alertId;
    document.getElementById('modal-alert-uid').textContent = alert.alert_uid;
    document.getElementById('modal-alert-site').textContent = alert.heritage_site_name;
    document.getElementById('modal-alert-title').textContent = alert.title;
    document.getElementById('modal-alert-recommended').textContent = alert.recommended_action;

    document.getElementById('modal-alert-status').value = alert.status;
    document.getElementById('modal-alert-priority').value = alert.priority;
    document.getElementById('modal-alert-assigned').value = alert.assigned_to || '';
    document.getElementById('modal-alert-notes').value = alert.action_notes || '';

    document.getElementById('admin-alert-action-modal').style.display = 'flex';
  },

  closeAlertActionModal() {
    document.getElementById('admin-alert-action-modal').style.display = 'none';
    this.currentAlertId = null;
  },

  async submitAlertAction(e) {
    e.preventDefault();
    if (!this.currentAlertId) return;

    const newStatus = document.getElementById('modal-alert-status').value;
    const newPriority = document.getElementById('modal-alert-priority').value;
    const assignedTo = document.getElementById('modal-alert-assigned').value.trim();
    const actionNotes = document.getElementById('modal-alert-notes').value.trim();

    try {
      const res = await APIClient.put(`/api/alerts/${this.currentAlertId}/action`, {
        status: newStatus,
        priority: newPriority,
        assigned_to: assignedTo,
        action_notes: actionNotes
      });

      Toast.success(res.message || 'Alert updated successfully.');
      this.closeAlertActionModal();
      await this.loadAlerts();
      await this.loadDashboardMetrics();
    } catch (err) {
      Toast.error(err.message || 'Failed to update alert.');
    }
  },

  // ==========================================
  // CITIZEN REPORTS MODERATION DESK
  // ==========================================
  async loadReports(status = 'all') {
    const tbody = document.getElementById('admin-reports-tbody');
    if (!tbody) return;

    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem;"><i class="fas fa-spinner fa-spin"></i> Loading reports...</td></tr>`;

    try {
      const endpoint = status && status !== 'all' ? `/api/admin/reports?status=${status}` : '/api/admin/reports';
      const res = await APIClient.get(endpoint);
      this.reportsCache = res.data || [];

      if (this.reportsCache.length === 0) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding:2rem; color:var(--text-muted);">No reports found matching this filter.</td></tr>`;
        return;
      }

      tbody.innerHTML = this.reportsCache.map(r => {
        const hasImg = r.images && r.images.length > 0;
        const ai = r.ai_analysis || {};

        return `
          <tr>
            <td><strong style="font-family:var(--font-serif); color:var(--primary);">${r.report_uid}</strong></td>
            <td>
              <strong>${r.heritage_site_name || 'Monument'}</strong><br>
              <span style="font-size:0.75rem; color:var(--text-dim);">${r.location}</span>
            </td>
            <td><span class="badge" style="background:var(--bg-card-alt); font-size:0.75rem; font-weight:600;">${r.issue_type}</span></td>
            <td>
              <span class="risk-badge risk-${r.severity.toLowerCase()}">${r.severity}</span>
              <div style="font-size:0.7rem; color:var(--text-dim); margin-top:0.2rem;">AI: ${ai.confidence_score || 85}% conf.</div>
            </td>
            <td><span style="font-size:0.8rem; color:var(--text-muted);">${r.incident_date}</span></td>
            <td>
              <span class="badge" style="background:var(--bg-card-alt); font-weight:700;">${r.status}</span>
            </td>
            <td>
              <button onclick="CommandCenter.openReportModerationModal(${r.id})" class="btn btn-secondary btn-sm">
                <i class="fas fa-edit"></i> Moderate
              </button>
            </td>
          </tr>
        `;
      }).join('');
    } catch (err) {
      console.error('[Admin Reports] Error:', err);
    }
  },

  openReportModerationModal(reportId) {
    const report = this.reportsCache.find(r => r.id === reportId);
    if (!report) return;

    this.currentReportId = reportId;
    document.getElementById('mod-report-uid').textContent = report.report_uid;
    document.getElementById('mod-site-name').textContent = report.heritage_site_name;
    document.getElementById('mod-reporter-name').textContent = report.user_name || 'Anonymous Citizen';
    document.getElementById('mod-issue-type').textContent = report.issue_type;
    document.getElementById('mod-location').textContent = report.location;
    document.getElementById('mod-description').textContent = report.description;
    
    // AI findings block
    const ai = report.ai_analysis || {};
    document.getElementById('mod-ai-category').textContent = ai.category_detected || report.issue_type;
    document.getElementById('mod-ai-severity').textContent = ai.severity_estimated || report.severity;
    document.getElementById('mod-ai-confidence').textContent = `${ai.confidence_score || 85}%`;
    document.getElementById('mod-ai-signs').textContent = ai.damage_signs || 'Visual surface change recorded.';
    document.getElementById('mod-ai-urgency').textContent = ai.urgency || 'Standard review';

    document.getElementById('mod-status-select').value = report.status;
    document.getElementById('mod-admin-remarks').value = report.admin_remarks || '';

    const imgBox = document.getElementById('mod-evidence-box');
    if (report.images && report.images.length > 0) {
      imgBox.innerHTML = `
        <img src="${report.images[0].image_url}" alt="Evidence" style="max-height:180px; border-radius:var(--radius-sm); border:1px solid var(--border-subtle); cursor:pointer;" onclick="window.open('${report.images[0].image_url}', '_blank')" onerror="handleImageError(this)">
      `;
      imgBox.style.display = 'block';
    } else {
      imgBox.style.display = 'none';
    }

    document.getElementById('admin-report-moderation-modal').style.display = 'flex';
  },

  closeReportModerationModal() {
    document.getElementById('admin-report-moderation-modal').style.display = 'none';
    this.currentReportId = null;
  },

  async submitReportModeration(e) {
    e.preventDefault();
    if (!this.currentReportId) return;

    const newStatus = document.getElementById('mod-status-select').value;
    const adminRemarks = document.getElementById('mod-admin-remarks').value.trim();

    try {
      const res = await APIClient.put(`/api/admin/reports/${this.currentReportId}`, {
        status: newStatus,
        admin_remarks: adminRemarks
      });

      Toast.success(res.message || 'Report updated.');
      this.closeReportModerationModal();
      await this.loadReports();
      await this.loadDashboardMetrics();
    } catch (err) {
      Toast.error(err.message || 'Failed to update report.');
    }
  },

  // ==========================================
  // ENCROACHMENT OBSERVATIONS TABLE
  // ==========================================
  async loadEncroachments() {
    const tbody = document.getElementById('admin-encroachment-tbody');
    if (!tbody) return;

    try {
      const res = await APIClient.get('/api/preservation/encroachments');
      const items = res.data || [];

      tbody.innerHTML = items.map(enc => `
        <tr>
          <td><strong style="color:var(--primary);">${enc.heritage_site_name || 'Monument'}</strong></td>
          <td><span style="font-size:0.8rem; color:var(--accent); font-weight:600;">${enc.monitored_zone}</span></td>
          <td>${enc.detected_change}</td>
          <td><span class="risk-badge risk-${enc.risk_level.toLowerCase()}">${enc.risk_level}</span></td>
          <td><span style="font-size:0.8rem; color:var(--text-muted);">${enc.latest_date}</span></td>
          <td>
            ${enc.latest_image_url ? `
              <a href="${enc.latest_image_url}" target="_blank" class="btn btn-secondary btn-sm"><i class="fas fa-eye"></i> Evidence</a>
            ` : 'None'}
          </td>
        </tr>
      `).join('');
    } catch (err) {
      console.error('[Encroachment] Load error:', err);
    }
  }
};

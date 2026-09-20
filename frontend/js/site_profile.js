/**
 * HeritageVerse - Monument Profile 2.0 Controller
 * Combines Discovery, Historical Storytelling, Living Culture,
 * Heritage Doctor Diagnostics, What-If Simulation, and Community Stories.
 */

let currentSiteData = null;
let currentSiteId = 1;

document.addEventListener('DOMContentLoaded', async () => {
  const params = new URLSearchParams(window.location.search);
  currentSiteId = parseInt(params.get('id')) || 1;

  // Initialize Tab Switchers
  initTabNavigation();

  // Load Full Monument Dossier
  await loadFullMonumentProfile(currentSiteId);

  // Initialize What-If Simulator Listeners
  initWhatIfSimulator();

  // Initialize Community Story Modal
  initCommunityStoryModal();
});

function initTabNavigation() {
  const tabBtns = document.querySelectorAll('.profile-tab-btn');
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      tabBtns.forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetTab = btn.getAttribute('data-tab');
      const pane = document.getElementById(targetTab);
      if (pane) pane.classList.add('active');
    });
  });
}

async function loadFullMonumentProfile(siteId) {
  try {
    const res = await fetch(`/api/heritage/sites/${siteId}/full-profile`);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    currentSiteData = data;

    renderHeroAndMeta(data);
    renderOverviewTab(data);
    renderHistoryTimeline(data.history_events || []);
    renderLivingCulture(data.crafts || [], data.traditions || []);
    renderThenVsNow(data.then_vs_now || []);
    renderHeritageSurroundings(data.surroundings || []);
    renderHeritageDoctor(data.heritage_doctor || {});
    renderCommunityStories(data.community_stories || []);
    renderPreservationIntelligence(data.site || {}, data.health_analysis || {});
    
    // Initial What-If baseline
    runWhatIfSimulation();
  } catch (err) {
    console.error('Failed to load monument full profile:', err);
    // Fallback to preservation dossier endpoint if needed
    loadPreservationDossierFallback(siteId);
  }
}

async function loadPreservationDossierFallback(siteId) {
  try {
    const res = await fetch(`/api/preservation/site/${siteId}/dossier`);
    const json = await res.json();
    const site = json.data;
    if (site) {
      renderHeroAndMeta({ site });
      renderPreservationIntelligence(site, site.health_score_breakdown || {});
    }
  } catch (e) {
    console.error('Preservation dossier fallback error:', e);
  }
}

function renderHeroAndMeta(data) {
  const site = data.site || {};
  document.title = `${site.name} – HeritageVerse Monument Dossier`;

  const nameEl = document.getElementById('site-name-heading');
  if (nameEl) nameEl.textContent = site.name;

  const uidEl = document.getElementById('site-dossier-uid');
  if (uidEl) uidEl.innerHTML = `<i class="fas fa-fingerprint"></i> NAT-ASI-00${site.id}`;

  const catBadge = document.getElementById('site-category-badge');
  if (catBadge) catBadge.textContent = site.heritage_category || 'Monuments & Forts';

  const locEl = document.getElementById('site-location-text');
  if (locEl) locEl.innerHTML = `<i class="fas fa-map-marker-alt"></i> <strong>${site.city}, ${site.state_name || 'India'}</strong>`;

  const coordsEl = document.getElementById('site-coords-text');
  if (coordsEl) {
    coordsEl.innerHTML = (site.latitude && site.longitude) 
      ? `<i class="fas fa-globe"></i> <strong>${site.latitude.toFixed(4)}° N, ${site.longitude.toFixed(4)}° E</strong>`
      : `<i class="fas fa-globe"></i> <strong>Geo-Spatial Surveyed</strong>`;
  }

  const eraEl = document.getElementById('site-era-text');
  if (eraEl) eraEl.innerHTML = `<i class="fas fa-hourglass-half"></i> <strong>${site.historical_period || 'Ancient India'}</strong>`;

  const statusEl = document.getElementById('site-status-text');
  if (statusEl) statusEl.innerHTML = `<i class="fas fa-tools"></i> <strong>${site.preservation_status || 'Well Preserved'}</strong>`;

  const riskBadge = document.getElementById('site-risk-badge');
  if (riskBadge) {
    riskBadge.textContent = `${site.risk_level} Risk`;
    riskBadge.className = `risk-badge risk-${(site.risk_level || 'low').toLowerCase()}`;
  }

  const heroImg = document.getElementById('site-hero-image');
  if (heroImg) {
    heroImg.src = site.image_url || '/assets/images/heritage-placeholder.svg';
    heroImg.alt = `${site.name} architectural survey`;
  }

  const captionEl = document.getElementById('site-hero-caption');
  if (captionEl) captionEl.textContent = `${site.name} — Verified Architectural Reference`;

  const scoreNumEl = document.getElementById('site-hero-score-num');
  const scoreBadge = document.getElementById('site-hero-score-badge');
  if (scoreNumEl && scoreBadge) {
    const score = site.current_health_score || 82;
    scoreNumEl.textContent = score;
    let scoreCls = 'score-healthy';
    if (score < 50) scoreCls = 'score-critical';
    else if (score < 70) scoreCls = 'score-high';
    else if (score < 85) scoreCls = 'score-attention';
    scoreBadge.className = `health-score-badge ${scoreCls}`;
  }

  // Quick Action Links
  const reportBtn = document.getElementById('site-hero-report-btn');
  if (reportBtn) reportBtn.href = `/report.html?site_id=${site.id}`;
}

function renderOverviewTab(data) {
  const site = data.site || {};
  const descEl = document.getElementById('site-description-text');
  if (descEl) descEl.textContent = site.description;

  const cultEl = document.getElementById('site-cultural-text');
  if (cultEl) cultEl.innerHTML = `<strong>Cultural Significance:</strong> ${site.cultural_significance || 'UNESCO World Heritage monument of exceptional universal value.'}`;

  const archEl = document.getElementById('site-architecture-text');
  if (archEl) archEl.innerHTML = `<strong>Architectural Engineering:</strong> ${site.architecture || 'Classical indigenous stone masonry and geometric design.'}`;

  // Gallery
  const gallery = data.gallery || site.gallery || [];
  const galleryEl = document.getElementById('site-gallery-container');
  if (galleryEl) {
    if (gallery.length === 0) {
      galleryEl.innerHTML = `<div style="padding:1.5rem; color:var(--text-muted); grid-column:1/-1;">High-resolution archival photographic plates available in primary documentation record.</div>`;
    } else {
      galleryEl.innerHTML = gallery.map(img => `
        <div class="gallery-item">
          <span class="gallery-verified-badge"><i class="fas fa-check-circle"></i> VERIFIED ASI</span>
          <img src="${img.image_url}" alt="${img.caption || site.name}" onerror="this.src='/assets/images/heritage-placeholder.svg'">
          <div class="gallery-caption">${img.caption || site.name}</div>
        </div>
      `).join('');
    }
  }
}

function renderHistoryTimeline(events) {
  const container = document.getElementById('history-timeline-container');
  if (!container) return;

  if (events.length === 0) {
    container.innerHTML = `<p style="color:var(--text-muted); padding:1rem;">Historical event chronology records being synchronized.</p>`;
    return;
  }

  container.innerHTML = events.map(ev => {
    let provClass = 'provenance-official';
    if (ev.source_type === 'ACADEMIC') provClass = 'provenance-academic';
    else if (ev.source_type === 'CURATED') provClass = 'provenance-curated';
    else if (ev.source_type === 'COMMUNITY') provClass = 'provenance-community';

    return `
      <div class="history-milestone">
        <div class="milestone-card">
          <div class="milestone-header">
            <div class="milestone-year"><i class="fas fa-landmark" style="color:var(--accent); font-size:0.9rem;"></i> ${ev.year_display}</div>
            <div style="display:flex; gap:0.4rem; align-items:center;">
              <span class="badge" style="background:var(--bg-card-alt); font-size:0.75rem; color:var(--primary); font-weight:600;">${ev.category}</span>
              <span class="provenance-tag ${provClass}"><i class="fas fa-certificate"></i> ${ev.source_type}</span>
            </div>
          </div>
          <h4 style="font-family:var(--font-serif); font-size:1.05rem; color:var(--primary); margin-bottom:0.4rem;">${ev.title}</h4>
          <p style="font-size:0.9rem; color:var(--text-main); line-height:1.6; margin-bottom:0.6rem;">${ev.description}</p>
          <div style="font-size:0.75rem; color:var(--text-dim); display:flex; align-items:center; gap:0.35rem;">
            <i class="fas fa-book-open"></i> <span>Source: <strong>${ev.source_name}</strong></span>
          </div>
        </div>
      </div>
    `;
  }).join('');
}

function renderLivingCulture(crafts, traditions) {
  // Crafts
  const craftsContainer = document.getElementById('living-crafts-grid');
  if (craftsContainer) {
    if (crafts.length === 0) {
      craftsContainer.innerHTML = `<p style="color:var(--text-muted); padding:1rem; grid-column:1/-1;">Local living crafts documentation currently being compiled with artisan guilds.</p>`;
    } else {
      craftsContainer.innerHTML = crafts.map(cr => `
        <div class="craft-card">
          <div class="craft-img-wrap">
            <img src="${cr.image_url || '/assets/images/heritage-placeholder.svg'}" alt="${cr.name}" onerror="this.src='/assets/images/heritage-placeholder.svg'">
            <span class="provenance-tag provenance-curated" style="position:absolute; top:10px; right:10px;"><i class="fas fa-hands"></i> ${cr.category}</span>
          </div>
          <div class="craft-body">
            <h4 style="font-family:var(--font-serif); font-size:1.1rem; color:var(--primary); margin-bottom:0.4rem;">${cr.name}</h4>
            <p style="font-size:0.86rem; color:var(--text-muted); line-height:1.55; margin-bottom:0.75rem;">${cr.description}</p>
            ${cr.materials_and_technique ? `
              <div style="background:var(--bg-card-alt); padding:0.6rem 0.8rem; border-radius:var(--radius-sm); font-size:0.8rem; margin-bottom:0.6rem;">
                <strong><i class="fas fa-tools" style="color:var(--accent);"></i> Materials & Technique:</strong> ${cr.materials_and_technique}
              </div>
            ` : ''}
            <div class="craft-cluster-tag">
              <i class="fas fa-map-marker-alt" style="color:var(--accent);"></i> <strong>Artisan Cluster:</strong> ${cr.artisan_cluster_location || 'Regional Guilds'}
            </div>
          </div>
        </div>
      `).join('');
    }
  }

  // Traditions
  const traditionsContainer = document.getElementById('cultural-traditions-grid');
  if (traditionsContainer) {
    if (traditions.length === 0) {
      traditionsContainer.innerHTML = `<p style="color:var(--text-muted); padding:1rem; grid-column:1/-1;">Cultural festivals and living traditions registry being updated.</p>`;
    } else {
      traditionsContainer.innerHTML = traditions.map(tr => `
        <div class="craft-card">
          <div class="craft-img-wrap">
            <img src="${tr.image_url || '/assets/images/heritage-placeholder.svg'}" alt="${tr.title}" onerror="this.src='/assets/images/heritage-placeholder.svg'">
            <span class="provenance-tag provenance-curated" style="position:absolute; top:10px; right:10px;"><i class="fas fa-drum"></i> ${tr.tradition_type}</span>
          </div>
          <div class="craft-body">
            <h4 style="font-family:var(--font-serif); font-size:1.1rem; color:var(--primary); margin-bottom:0.4rem;">${tr.title}</h4>
            <div style="font-size:0.8rem; font-weight:700; color:var(--accent); margin-bottom:0.5rem;"><i class="far fa-calendar-alt"></i> ${tr.season_or_timing || 'Seasonal Celebration'}</div>
            <p style="font-size:0.86rem; color:var(--text-muted); line-height:1.55; margin-bottom:0.75rem;">${tr.description}</p>
            ${tr.community_role ? `
              <div style="background:var(--bg-card-alt); padding:0.6rem 0.8rem; border-radius:var(--radius-sm); font-size:0.8rem;">
                <strong><i class="fas fa-users" style="color:var(--primary);"></i> Community Participation:</strong> ${tr.community_role}
              </div>
            ` : ''}
          </div>
        </div>
      `).join('');
    }
  }
}

function renderThenVsNow(comparisons) {
  const container = document.getElementById('then-vs-now-container');
  if (!container) return;

  if (comparisons.length === 0) {
    container.innerHTML = `<p style="color:var(--text-muted); padding:1rem;">Archival photographic comparison plates currently being calibrated with state archives.</p>`;
    return;
  }

  container.innerHTML = comparisons.map(tvn => `
    <div class="then-vs-now-card">
      <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; margin-bottom:0.75rem;">
        <h4 style="font-family:var(--font-serif); font-size:1.2rem; color:var(--primary);">${tvn.title}</h4>
        <span class="badge" style="background:var(--bg-card-alt); color:var(--primary); font-weight:600;"><i class="fas fa-layer-group"></i> ${tvn.comparison_category}</span>
      </div>

      <div class="then-vs-now-grid">
        <div class="then-box">
          <span class="then-badge"><i class="fas fa-camera-retro"></i> THEN: ${tvn.historical_year}</span>
          <img src="${tvn.historical_image_url}" alt="Historical archival survey" onerror="this.src='/assets/images/heritage-placeholder.svg'">
        </div>
        <div class="now-box">
          <span class="now-badge"><i class="fas fa-camera"></i> NOW: ${tvn.current_year}</span>
          <img src="${tvn.current_image_url}" alt="Present day condition" onerror="this.src='/assets/images/heritage-placeholder.svg'">
        </div>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:1.5rem; font-size:0.82rem; color:var(--text-muted); margin-bottom:1rem;">
        <div><em>${tvn.historical_image_caption || 'Archival plate'}</em></div>
        <div><em>${tvn.current_image_caption || 'Present condition'}</em></div>
      </div>

      <div style="background:var(--bg-card-alt); padding:1rem; border-radius:var(--radius-md); border-left:4px solid var(--accent); font-size:0.88rem; line-height:1.6;">
        <strong style="color:var(--primary);"><i class="fas fa-microscope" style="color:var(--accent);"></i> Architectural Preservation Analysis:</strong>
        <p style="margin-top:0.25rem; color:var(--text-main);">${tvn.observations_text}</p>
        <div style="font-size:0.75rem; color:var(--text-dim); margin-top:0.4rem;"><i class="fas fa-archive"></i> Source: ${tvn.source_name}</div>
      </div>
    </div>
  `).join('');
}

function renderHeritageSurroundings(surroundings) {
  const container = document.getElementById('heritage-surroundings-container');
  if (!container) return;

  if (surroundings.length === 0) {
    container.innerHTML = `<p style="color:var(--text-muted); padding:1rem;">Contextual surroundings buffer telemetry active.</p>`;
    return;
  }

  container.innerHTML = `
    <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:1rem;">
      ${surroundings.map(sr => `
        <div style="background:var(--bg-card-alt); padding:1.25rem; border-radius:var(--radius-md); border:1px solid var(--border-subtle);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <span class="badge" style="background:#FFFFFF; color:var(--primary); font-weight:700; font-size:0.72rem;">${sr.factor_type}</span>
            <span style="font-size:0.78rem; font-weight:700; color:var(--accent);"><i class="fas fa-ruler-horizontal"></i> ${sr.distance_meters}m</span>
          </div>
          <h5 style="font-family:var(--font-serif); font-size:0.95rem; color:var(--primary); margin-bottom:0.35rem;">${sr.name}</h5>
          <p style="font-size:0.83rem; color:var(--text-muted); line-height:1.5;">${sr.description}</p>
          <div style="margin-top:0.5rem; font-size:0.75rem; font-weight:700; color:var(--primary-light);">
            <i class="fas fa-shield-alt"></i> Impact: ${sr.impact_nature}
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

function renderHeritageDoctor(doctor) {
  const container = document.getElementById('heritage-doctor-content');
  if (!container) return;

  const grade = doctor.clinical_grade || 'Grade B: Monitored Stable Condition';
  const badgeCls = (doctor.grade_badge || 'GRADE_B').toLowerCase().replace('_', '-');
  const confidence = doctor.diagnostic_confidence_percentage || 91;

  container.innerHTML = `
    <div class="doctor-dossier-card">
      <div class="doctor-header-strip">
        <div>
          <div style="font-size:0.78rem; font-weight:700; color:var(--accent); text-transform:uppercase; letter-spacing:0.5px;">
            <i class="fas fa-user-md"></i> Clinical Diagnostic Condition Assessment
          </div>
          <div style="font-family:var(--font-serif); font-size:1.35rem; color:var(--primary); font-weight:700; margin-top:0.25rem;">
            ${doctor.site_name || 'Monument'} Diagnostic Appraisal
          </div>
        </div>
        <div style="display:flex; gap:0.75rem; align-items:center;">
          <span class="clinical-grade-pill ${badgeCls}">${grade}</span>
          <span class="badge" style="background:var(--bg-card-alt); color:var(--primary); font-weight:700;">
            <i class="fas fa-chart-line"></i> ${confidence}% Confidence
          </span>
        </div>
      </div>

      <!-- Identified Pathologies -->
      <h4 style="font-family:var(--font-serif); font-size:1.1rem; color:var(--primary); margin-bottom:0.75rem;">
        <i class="fas fa-stethoscope" style="color:var(--accent);"></i> Identified Pathologies & Vulnerabilities
      </h4>
      <div style="margin-bottom:1.5rem;">
        ${(doctor.identified_pathologies || []).map(p => `
          <div class="pathology-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.35rem;">
              <strong style="color:var(--primary); font-size:0.95rem;">${p.pathology}</strong>
              <span class="risk-badge risk-${(p.severity || 'moderate').toLowerCase()}">${p.severity} Severity</span>
            </div>
            <div style="font-size:0.8rem; color:var(--text-dim); margin-bottom:0.4rem;">
              <i class="fas fa-crosshairs"></i> Structural Area: <strong>${p.organ_affected}</strong>
            </div>
            <p style="font-size:0.86rem; color:var(--text-main); margin-bottom:0.5rem; line-height:1.5;">${p.symptoms}</p>
            <div style="background:#FFFFFF; padding:0.6rem 0.8rem; border-radius:var(--radius-sm); font-size:0.82rem; color:var(--primary-light);">
              <strong><i class="fas fa-prescription" style="color:var(--accent);"></i> Conservation Rx:</strong> ${p.remedy}
            </div>
          </div>
        `).join('')}
      </div>

      <!-- 3-Phase Clinical Prescription -->
      <h4 style="font-family:var(--font-serif); font-size:1.1rem; color:var(--primary); margin-bottom:0.75rem;">
        <i class="fas fa-clipboard-list" style="color:var(--primary);"></i> Structured Conservation Treatment Protocol
      </h4>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:1rem; margin-bottom:1.5rem;">
        ${(doctor.clinical_prescriptions || []).map(rx => `
          <div style="background:var(--bg-card-alt); padding:1rem; border-radius:var(--radius-md); border-top:3px solid var(--accent);">
            <div style="font-size:0.78rem; font-weight:700; color:var(--accent); text-transform:uppercase;">${rx.phase}</div>
            <p style="font-size:0.85rem; color:var(--text-main); margin:0.4rem 0; line-height:1.5;">${rx.action}</p>
            <div style="font-size:0.75rem; color:var(--text-muted);"><i class="fas fa-building"></i> Lead: ${rx.responsible}</div>
          </div>
        `).join('')}
      </div>

      <!-- AMASR Act Statutory Compliance -->
      ${doctor.statutory_compliance ? `
        <div style="background:rgba(23,63,53,0.05); padding:1rem; border-radius:var(--radius-md); border:1px solid var(--border-subtle); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem; font-size:0.84rem;">
          <div>
            <strong><i class="fas fa-balance-scale" style="color:var(--primary);"></i> Statutory Compliance:</strong> ${doctor.statutory_compliance.act_name}
          </div>
          <span class="badge" style="background:var(--primary); color:#FFFFFF; font-weight:700;">
            Compliance Score: ${doctor.statutory_compliance.compliance_score}/100
          </span>
        </div>
      ` : ''}
    </div>
  `;
}

function initWhatIfSimulator() {
  const touristSlider = document.getElementById('whatif-tourist-slider');
  const aqiSlider = document.getElementById('whatif-aqi-slider');
  const monsoonSelect = document.getElementById('whatif-monsoon-select');
  const bufferSelect = document.getElementById('whatif-buffer-select');
  const maintenanceSelect = document.getElementById('whatif-maintenance-select');
  const greenToggle = document.getElementById('whatif-green-toggle');
  const ticketingToggle = document.getElementById('whatif-ticketing-toggle');

  const triggers = [touristSlider, aqiSlider, monsoonSelect, bufferSelect, maintenanceSelect, greenToggle, ticketingToggle];
  triggers.forEach(el => {
    if (el) {
      el.addEventListener('input', runWhatIfSimulation);
      el.addEventListener('change', runWhatIfSimulation);
    }
  });

  // Slider value labels
  if (touristSlider) {
    touristSlider.addEventListener('input', (e) => {
      const lbl = document.getElementById('whatif-tourist-label');
      if (lbl) lbl.textContent = `${Math.round(parseFloat(e.target.value) * 100)}%`;
    });
  }

  if (aqiSlider) {
    aqiSlider.addEventListener('input', (e) => {
      const lbl = document.getElementById('whatif-aqi-label');
      if (lbl) lbl.textContent = `${e.target.value} AQI`;
    });
  }
}

async function runWhatIfSimulation() {
  const touristSlider = document.getElementById('whatif-tourist-slider');
  const aqiSlider = document.getElementById('whatif-aqi-slider');
  const monsoonSelect = document.getElementById('whatif-monsoon-select');
  const bufferSelect = document.getElementById('whatif-buffer-select');
  const maintenanceSelect = document.getElementById('whatif-maintenance-select');
  const greenToggle = document.getElementById('whatif-green-toggle');
  const ticketingToggle = document.getElementById('whatif-ticketing-toggle');

  const params = {
    site_id: currentSiteId,
    tourist_multiplier: touristSlider ? parseFloat(touristSlider.value) : 1.0,
    aqi: aqiSlider ? parseInt(aqiSlider.value) : 120,
    monsoon_severity: monsoonSelect ? monsoonSelect.value : 'normal',
    buffer_intrusion: bufferSelect ? bufferSelect.value : 'none',
    maintenance_regime: maintenanceSelect ? maintenanceSelect.value : 'regular',
    green_buffer_expanded: greenToggle ? greenToggle.checked : false,
    visitor_timed_entry: ticketingToggle ? ticketingToggle.checked : false
  };

  try {
    const res = await fetch('/api/preservation/what-if', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    });
    if (!res.ok) throw new Error('Simulation failed');
    const json = await res.json();
    renderWhatIfResults(json.data);
  } catch (err) {
    console.error('What-If simulation error:', err);
  }
}

function renderWhatIfResults(data) {
  if (!data) return;

  const projScoreEl = document.getElementById('whatif-projected-score');
  if (projScoreEl) projScoreEl.textContent = data.projected.health_score;

  const deltaEl = document.getElementById('whatif-score-delta');
  if (deltaEl) {
    const delta = data.score_delta;
    const sign = delta > 0 ? `+${delta}` : `${delta}`;
    deltaEl.textContent = `${sign} pts`;
    deltaEl.className = `delta-tag ${delta >= 0 ? 'delta-pos' : 'delta-neg'}`;
  }

  const transEl = document.getElementById('whatif-risk-transition');
  if (transEl) transEl.textContent = data.risk_transition;

  const statusSummaryEl = document.getElementById('whatif-status-summary');
  if (statusSummaryEl) statusSummaryEl.textContent = data.projected.status_summary;

  // Factor Attribution
  const attr = data.factor_attribution || {};
  const attrList = document.getElementById('whatif-factor-attribution');
  if (attrList) {
    attrList.innerHTML = `
      <div style="display:flex; justify-content:space-between; font-size:0.82rem; padding:0.25rem 0;">
        <span><i class="fas fa-users"></i> Visitor Density Shift:</span>
        <strong style="color:${attr.visitor_pressure_shift >= 0 ? 'var(--risk-low)' : 'var(--risk-crit)'};">${attr.visitor_pressure_shift >= 0 ? '+' : ''}${attr.visitor_pressure_shift} pts</strong>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:0.82rem; padding:0.25rem 0;">
        <span><i class="fas fa-smog"></i> Air Quality (AQI) Shift:</span>
        <strong style="color:${attr.environmental_air_shift >= 0 ? 'var(--risk-low)' : 'var(--risk-crit)'};">${attr.environmental_air_shift >= 0 ? '+' : ''}${attr.environmental_air_shift} pts</strong>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:0.82rem; padding:0.25rem 0;">
        <span><i class="fas fa-tools"></i> Maintenance Strategy:</span>
        <strong style="color:${attr.structural_maintenance_shift >= 0 ? 'var(--risk-low)' : 'var(--risk-crit)'};">${attr.structural_maintenance_shift >= 0 ? '+' : ''}${attr.structural_maintenance_shift} pts</strong>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:0.82rem; padding:0.25rem 0;">
        <span><i class="fas fa-vector-square"></i> Buffer Zone Integrity:</span>
        <strong style="color:${attr.buffer_encroachment_shift >= 0 ? 'var(--risk-low)' : 'var(--risk-crit)'};">${attr.buffer_encroachment_shift >= 0 ? '+' : ''}${attr.buffer_encroachment_shift} pts</strong>
      </div>
      <div style="display:flex; justify-content:space-between; font-size:0.82rem; padding:0.25rem 0;">
        <span><i class="fas fa-cloud-showers-heavy"></i> Weather / Climate Shift:</span>
        <strong style="color:${attr.disaster_weather_shift >= 0 ? 'var(--risk-low)' : 'var(--risk-crit)'};">${attr.disaster_weather_shift >= 0 ? '+' : ''}${attr.disaster_weather_shift} pts</strong>
      </div>
    `;
  }

  // Preventative Recommendations
  const actionsList = document.getElementById('whatif-recommended-actions');
  if (actionsList) {
    actionsList.innerHTML = (data.recommended_preventative_actions || []).map(act => `
      <div style="display:flex; gap:0.5rem; align-items:flex-start; font-size:0.84rem; margin-bottom:0.4rem;">
        <i class="fas fa-arrow-right" style="color:var(--accent); margin-top:0.2rem;"></i>
        <span>${act}</span>
      </div>
    `).join('');
  }
}

function renderCommunityStories(stories) {
  const container = document.getElementById('community-stories-container');
  if (!container) return;

  if (stories.length === 0) {
    container.innerHTML = `
      <div style="text-align:center; padding:2rem; background:var(--bg-card-alt); border-radius:var(--radius-md); grid-column:1/-1;">
        <i class="fas fa-feather-alt" style="font-size:2rem; color:var(--accent); margin-bottom:0.75rem;"></i>
        <p style="color:var(--text-main); font-weight:600;">Be the first to contribute a memory or oral history for this monument!</p>
        <p style="font-size:0.85rem; color:var(--text-muted); margin-top:0.25rem;">Share family traditions, artisan knowledge, or architectural reflections.</p>
      </div>
    `;
    return;
  }

  container.innerHTML = stories.map(st => `
    <div class="story-card">
      <div class="story-author-row">
        <div class="author-avatar">${st.author_name.charAt(0).toUpperCase()}</div>
        <div>
          <strong style="color:var(--primary); font-size:0.95rem;">${st.author_name}</strong>
          <div style="font-size:0.78rem; color:var(--text-muted);">${st.author_role} &bull; ${st.historical_period || 'Living Memory'}</div>
        </div>
      </div>
      <h4 style="font-family:var(--font-serif); font-size:1.05rem; color:var(--primary); margin-bottom:0.4rem;">${st.title}</h4>
      <p style="font-size:0.88rem; color:var(--text-main); line-height:1.6; margin-bottom:0.75rem;">${st.story_content}</p>
      <div style="margin-top:auto; display:flex; justify-content:space-between; align-items:center;">
        <span class="provenance-tag provenance-community"><i class="fas fa-users"></i> ${st.story_type || 'Community Oral History'}</span>
        <span style="font-size:0.75rem; color:var(--text-dim);"><i class="fas fa-check-circle" style="color:var(--risk-low);"></i> Verified Citizen Memory</span>
      </div>
    </div>
  `).join('');
}

function initCommunityStoryModal() {
  const modal = document.getElementById('community-story-modal');
  const openBtn = document.getElementById('open-story-modal-btn');
  const closeBtn = document.getElementById('close-story-modal-btn');
  const form = document.getElementById('community-story-form');

  if (openBtn && modal) {
    openBtn.addEventListener('click', () => modal.classList.add('open'));
  }
  if (closeBtn && modal) {
    closeBtn.addEventListener('click', () => modal.classList.remove('open'));
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        heritage_site_id: currentSiteId,
        author_name: document.getElementById('story-author-name').value,
        author_role: document.getElementById('story-author-role').value,
        author_email: document.getElementById('story-author-email').value,
        title: document.getElementById('story-title').value,
        story_content: document.getElementById('story-content').value,
        story_type: document.getElementById('story-type').value,
        historical_period: document.getElementById('story-period').value
      };

      try {
        const res = await fetch('/api/community/stories', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Submission failed');
        const data = await res.json();
        alert('Thank you! Your oral history story has been published to HeritageVerse.');
        if (modal) modal.classList.remove('open');
        form.reset();
        // Refresh full profile
        loadFullMonumentProfile(currentSiteId);
      } catch (err) {
        alert('Error submitting story: ' + err.message);
      }
    });
  }
}

function renderPreservationIntelligence(site, healthAnalysis) {
  // Factor breakdown list
  const factorList = document.getElementById('factor-breakdown-list');
  if (factorList && healthAnalysis.factor_breakdown) {
    const f = healthAnalysis.factor_breakdown;
    factorList.innerHTML = Object.entries(f).map(([key, item]) => `
      <div>
        <div style="display:flex; justify-content:space-between; font-size:0.86rem; margin-bottom:0.25rem;">
          <strong style="color:var(--primary); text-transform:capitalize;">${key.replace(/_/g, ' ')}</strong>
          <span><strong>${item.points_earned}</strong> / ${item.max_points} pts (${item.percentage}%)</span>
        </div>
        <div class="progress-bar-wrap" style="height:6px; background:var(--bg-card-alt); border-radius:3px; overflow:hidden;">
          <div style="height:100%; width:${item.percentage}%; background:${item.percentage > 75 ? 'var(--risk-low)' : (item.percentage > 50 ? 'var(--risk-mod)' : 'var(--risk-crit)')};"></div>
        </div>
        <div style="font-size:0.75rem; color:var(--text-muted); margin-top:0.2rem;">${item.description}</div>
      </div>
    `).join('');
  }

  // Environmental sensors
  const envGrid = document.getElementById('environmental-sensor-grid');
  const env = (site.environmental_records && site.environmental_records.length > 0) ? site.environmental_records[site.environmental_records.length - 1] : null;
  if (envGrid && env) {
    envGrid.innerHTML = `
      <div class="kpi-mini-card">
        <div class="kpi-mini-label"><i class="fas fa-smog"></i> Air Quality (AQI)</div>
        <div class="kpi-mini-val" style="color:${env.air_quality_aqi > 150 ? 'var(--risk-crit)' : 'var(--primary)'};">${env.air_quality_aqi}</div>
        <div style="font-size:0.72rem; color:var(--text-dim);">${env.aqi_category || 'Moderate'}</div>
      </div>
      <div class="kpi-mini-card">
        <div class="kpi-mini-label"><i class="fas fa-tint"></i> Humidity</div>
        <div class="kpi-mini-val">${env.humidity_pct || 55}%</div>
        <div style="font-size:0.72rem; color:var(--text-dim);">${env.humidity_pct > 75 ? 'High Moisture' : 'Optimal'}</div>
      </div>
      <div class="kpi-mini-card">
        <div class="kpi-mini-label"><i class="fas fa-thermometer-half"></i> Ambient Temp</div>
        <div class="kpi-mini-val">${env.temperature_c || 28}°C</div>
        <div style="font-size:0.72rem; color:var(--text-dim);">Micro-climate</div>
      </div>
      <div class="kpi-mini-card">
        <div class="kpi-mini-label"><i class="fas fa-shield-virus"></i> Risk Status</div>
        <div class="kpi-mini-val" style="font-size:0.95rem; color:var(--primary);">${env.exposure_risk_status || 'Normal'}</div>
        <div style="font-size:0.72rem; color:var(--text-dim);">Telemetry Node</div>
      </div>
    `;
  }

  // Tourist pressure
  const touristContent = document.getElementById('tourist-pressure-content');
  const tourist = (site.tourist_pressures && site.tourist_pressures.length > 0) ? site.tourist_pressures[site.tourist_pressures.length - 1] : null;
  if (touristContent && tourist) {
    const pct = Math.round((tourist.occupancy_ratio || 0.7) * 100);
    touristContent.innerHTML = `
      <div style="margin-bottom:0.75rem;">
        <div style="display:flex; justify-content:space-between; font-size:0.86rem; margin-bottom:0.3rem;">
          <span>Daily Footfall vs Carrying Capacity</span>
          <strong>${(tourist.daily_visitors || 3000).toLocaleString()} / ${(site.carrying_capacity_daily || 5000).toLocaleString()}</strong>
        </div>
        <div class="progress-bar-wrap" style="height:8px; background:var(--bg-card-alt); border-radius:4px; overflow:hidden;">
          <div style="height:100%; width:${Math.min(100, pct)}%; background:${pct > 100 ? 'var(--risk-crit)' : (pct > 80 ? 'var(--risk-mod)' : 'var(--risk-low)')};"></div>
        </div>
      </div>
      <div style="font-size:0.82rem; color:var(--text-muted); display:flex; justify-content:space-between;">
        <span>Monthly Traffic: <strong>${(tourist.monthly_visitors || 90000).toLocaleString()}</strong></span>
        <span>Trend: <strong>${tourist.trend || 'Stable'}</strong></span>
      </div>
    `;
  }
}

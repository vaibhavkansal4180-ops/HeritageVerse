/**
 * HeritageVerse - Heritage Catalog & Search Explorer
 */

const HeritageCatalog = {
  sites: [],
  filters: {
    q: '',
    risk_level: '',
    heritage_category: '',
    preservation: ''
  },
  debounceTimer: null,

  async init() {
    this.parseQueryParams();
    await this.fetchSites();
    this.bindEvents();
  },

  parseQueryParams() {
    const params = new URLSearchParams(window.location.search);
    if (params.has('q')) this.filters.q = params.get('q');
    if (params.has('risk')) this.filters.risk_level = params.get('risk');
    if (params.has('category')) this.filters.heritage_category = params.get('category');

    const searchInput = document.getElementById('catalog-search');
    if (searchInput && this.filters.q) searchInput.value = this.filters.q;
  },

  bindEvents() {
    const searchInput = document.getElementById('catalog-search');
    const riskSelect = document.getElementById('filter-risk');
    const catSelect = document.getElementById('filter-category');
    const resetBtn = document.getElementById('catalog-reset-btn');

    if (searchInput) {
      searchInput.addEventListener('input', (e) => {
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
          this.filters.q = e.target.value.trim();
          this.fetchSites();
        }, 300);
      });
    }

    if (riskSelect) {
      riskSelect.addEventListener('change', (e) => {
        this.filters.risk_level = e.target.value;
        this.fetchSites();
      });
    }

    if (catSelect) {
      catSelect.addEventListener('change', (e) => {
        this.filters.heritage_category = e.target.value;
        this.fetchSites();
      });
    }

    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        this.filters = { q: '', risk_level: '', heritage_category: '', preservation: '' };
        if (searchInput) searchInput.value = '';
        if (riskSelect) riskSelect.value = '';
        if (catSelect) catSelect.value = '';
        this.fetchSites();
      });
    }
  },

  async fetchSites() {
    const grid = document.getElementById('heritage-sites-grid');
    const countEl = document.getElementById('results-count');
    if (!grid) return;

    grid.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:3rem;">
        <i class="fas fa-spinner fa-spin" style="font-size:1.75rem; color:var(--primary); margin-bottom:0.75rem;"></i>
        <p style="color:var(--text-muted);">Querying National Heritage Archives...</p>
      </div>
    `;

    const queryParams = new URLSearchParams();
    if (this.filters.q) queryParams.append('q', this.filters.q);
    if (this.filters.risk_level) queryParams.append('risk_level', this.filters.risk_level);
    if (this.filters.heritage_category) queryParams.append('category', this.filters.heritage_category);

    try {
      const res = await APIClient.get(`/api/heritage/search?${queryParams.toString()}`);
      this.sites = res.data || [];
      
      if (countEl) {
        countEl.textContent = `${this.sites.length} Monitored Monument${this.sites.length === 1 ? '' : 's'}`;
      }

      this.renderSitesGrid();
    } catch (err) {
      console.error('[Catalog] Search error:', err);
      grid.innerHTML = `
        <div style="grid-column:1/-1; text-align:center; padding:3rem;">
          <i class="fas fa-exclamation-triangle" style="font-size:2.5rem; color:var(--accent); margin-bottom:1rem;"></i>
          <p style="color:var(--primary);">Unable to load heritage monuments. Please try again.</p>
        </div>
      `;
    }
  },

  renderSitesGrid() {
    const grid = document.getElementById('heritage-sites-grid');
    if (!grid) return;

    if (this.sites.length === 0) {
      grid.innerHTML = `
        <div class="kpi-card" style="grid-column:1/-1; text-align:center; padding:3rem;">
          <i class="fas fa-search" style="font-size:2.5rem; color:var(--text-dim); margin-bottom:0.75rem;"></i>
          <h3 style="font-family:var(--font-serif); font-size:1.2rem; color:var(--primary); margin-bottom:0.35rem;">No Monitored Monuments Found</h3>
          <p style="color:var(--text-muted); font-size:0.9rem; margin-bottom:1.25rem;">Try adjusting your search query or removing risk/category filters.</p>
          <button onclick="HeritageCatalog.resetFilters()" class="btn btn-secondary btn-sm">Clear Filters</button>
        </div>
      `;
      return;
    }

    grid.innerHTML = this.sites.map(site => {
      const score = site.current_health_score !== undefined ? site.current_health_score : 80;
      const risk = (site.risk_level || 'Low').toLowerCase();
      const fallbackImg = '/assets/images/heritage-placeholder.svg';
      const imgUrl = site.image_url || fallbackImg;

      let scoreClass = 'score-healthy';
      if (score < 50) scoreClass = 'score-critical';
      else if (score < 70) scoreClass = 'score-high';
      else if (score < 85) scoreClass = 'score-attention';

      return `
        <div class="site-card">
          <div class="site-card-img-wrap">
            <img 
              src="${imgUrl}" 
              alt="${site.name} architectural survey" 
              class="site-card-img" 
              loading="lazy" 
              onerror="handleImageError(this)"
            >
            <div class="site-card-badges-top">
              <span class="health-score-badge ${scoreClass}">
                <i class="fas fa-heart-pulse"></i> ${score}/100
              </span>
            </div>
            <div class="site-card-badges-bottom">
              <span class="risk-badge risk-${risk}">${site.risk_level || 'Low'} Risk</span>
            </div>
          </div>

          <div class="site-card-body">
            <div class="site-category-tag">
              ${site.heritage_category || 'National Monument'} &bull; ${site.state_name || 'India'}
            </div>
            
            <h2 class="site-title">
              <a href="/site-detail.html?id=${site.id}">${site.name}</a>
            </h2>

            <div class="site-meta">
              <i class="fas fa-map-marker-alt"></i> ${site.city}, ${site.state_name || 'India'} &bull; <i class="fas fa-history"></i> ${site.historical_period || 'Historical Era'}
            </div>

            <p class="site-desc">
              ${site.description ? site.description : 'Monitored national monument undergoing continuous preservation telemetry.'}
            </p>

            <div class="site-card-footer">
              <div style="font-size:0.75rem; color:var(--text-dim); font-weight:600;">
                <i class="fas fa-flag"></i> ${site.reports_count || 0} Reports &bull; <i class="fas fa-bell"></i> ${site.active_alerts_count || 0} Alerts
              </div>
              <a href="/site-detail.html?id=${site.id}" class="btn btn-primary btn-sm">
                <i class="fas fa-file-contract"></i> Preservation Dossier
              </a>
            </div>
          </div>
        </div>
      `;
    }).join('');
  },

  resetFilters() {
    this.filters = { q: '', risk_level: '', heritage_category: '', preservation: '' };
    const searchInput = document.getElementById('catalog-search');
    const riskSelect = document.getElementById('filter-risk');
    const catSelect = document.getElementById('filter-category');
    if (searchInput) searchInput.value = '';
    if (riskSelect) riskSelect.value = '';
    if (catSelect) catSelect.value = '';
    this.fetchSites();
  }
};

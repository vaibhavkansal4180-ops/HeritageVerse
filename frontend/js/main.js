/**
 * HeritageVerse - Global Main Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Mobile Menu Toggle
  const mobileToggle = document.getElementById('mobile-toggle-btn');
  const navMenu = document.getElementById('site-nav-menu');

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      const icon = mobileToggle.querySelector('i');
      if (icon) {
        icon.classList.toggle('fa-bars');
        icon.classList.toggle('fa-times');
      }
    });
  }

  // 2. Header Scroll Effect
  const header = document.querySelector('.site-header');
  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 40) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  // 3. Homepage Global Search Bar
  const heroSearchForm = document.getElementById('hero-search-form');
  if (heroSearchForm) {
    heroSearchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const input = document.getElementById('hero-search-input');
      if (input && input.value.trim()) {
        window.location.href = `/heritage.html?q=${encodeURIComponent(input.value.trim())}`;
      }
    });
  }

  // 4. Preservation Live Stats Count-Up
  initPreservationCounters();
});

async function initPreservationCounters() {
  const sitesEl = document.getElementById('counter-sites');
  const statesEl = document.getElementById('counter-states');
  const digitizedEl = document.getElementById('counter-digitized');
  const resolvedEl = document.getElementById('counter-resolved');

  if (!sitesEl) return;

  try {
    const res = await APIClient.get('/api/stats/preservation');
    const stats = res.data;

    animateValue(sitesEl, 0, stats.heritage_sites_count || 22, 1200);
    animateValue(statesEl, 0, stats.states_covered_count || 10, 1000);
    animateValue(digitizedEl, 0, stats.digitized_3d_count || 12, 1200);
    animateValue(resolvedEl, 0, stats.reports_resolved_count || 4, 800);
  } catch (err) {
    console.warn('[Stats] Fallback default values used:', err);
  }
}

function animateValue(obj, start, end, duration) {
  if (!obj) return;
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    obj.innerHTML = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    } else {
      obj.innerHTML = end;
    }
  };
  window.requestAnimationFrame(step);
}

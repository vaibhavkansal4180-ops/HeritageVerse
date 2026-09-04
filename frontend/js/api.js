/**
 * HeritageVerse - Unified REST API Client & Toast Utility
 */

const API_BASE_URL = window.location.origin;

class APIClient {
  static getToken() {
    return localStorage.getItem('hv_token');
  }

  static setToken(token) {
    if (token) {
      localStorage.setItem('hv_token', token);
    } else {
      localStorage.removeItem('hv_token');
    }
  }

  static getUser() {
    const raw = localStorage.getItem('hv_user');
    try {
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  }

  static setUser(user) {
    if (user) {
      localStorage.setItem('hv_user', JSON.stringify(user));
    } else {
      localStorage.removeItem('hv_user');
    }
  }

  static async request(endpoint, options = {}) {
    const url = endpoint.startsWith('http') ? endpoint : `${API_BASE_URL}${endpoint}`;
    const headers = options.headers || {};

    const token = this.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    if (!(options.body instanceof FormData) && !headers['Content-Type']) {
      headers['Content-Type'] = 'application/json';
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.message || `Request failed with status ${response.status}`);
      }

      return data;
    } catch (error) {
      console.error(`[API Error] ${endpoint}:`, error);
      throw error;
    }
  }

  static get(endpoint) {
    return this.request(endpoint, { method: 'GET' });
  }

  static post(endpoint, body) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(body)
    });
  }

  static postFormData(endpoint, formData) {
    return this.request(endpoint, {
      method: 'POST',
      body: formData
    });
  }

  static put(endpoint, body) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(body)
    });
  }

  static delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

// Global Toast System
const Toast = {
  container: null,

  init() {
    if (!this.container) {
      this.container = document.createElement('div');
      this.container.id = 'toast-container';
      document.body.appendChild(this.container);
    }
  },

  show(message, type = 'info', duration = 4000) {
    this.init();
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'fa-info-circle';
    if (type === 'success') icon = 'fa-check-circle';
    if (type === 'error') icon = 'fa-exclamation-triangle';
    if (type === 'warning') icon = 'fa-exclamation-circle';

    toast.innerHTML = `
      <i class="fas ${icon}"></i>
      <div>${message}</div>
    `;

    this.container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(100%)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  },

  success(msg) { this.show(msg, 'success'); },
  error(msg) { this.show(msg, 'error'); },
  warning(msg) { this.show(msg, 'warning'); },
  info(msg) { this.show(msg, 'info'); }
};

// Global Image Error Fallback Handler
const HERITAGE_PLACEHOLDER_SVG = '/assets/images/heritage-placeholder.svg';

function handleImageError(img) {
  if (!img) return;
  img.onerror = null; // Prevent infinite loop
  img.src = HERITAGE_PLACEHOLDER_SVG;
  img.alt = 'Verified heritage image unavailable';
  img.classList.add('image-fallback-active');
}

// Auto-attach error fallback to all images on page
document.addEventListener('error', (e) => {
  if (e.target && e.target.tagName === 'IMG') {
    handleImageError(e.target);
  }
}, true);


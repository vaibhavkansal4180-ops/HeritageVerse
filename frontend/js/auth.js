/**
 * HeritageVerse - Authentication & Navigation State Controller
 */

const Auth = {
  isLoggedIn() {
    return !!APIClient.getToken() && !!APIClient.getUser();
  },

  getUser() {
    return APIClient.getUser();
  },

  isAdmin() {
    const user = this.getUser();
    return user && (user.role === 'admin' || user.is_admin === true);
  },

  async login(email, password) {
    try {
      const res = await APIClient.post('/api/auth/login', { email, password });
      if (res && res.data) {
        APIClient.setToken(res.data.token);
        APIClient.setUser(res.data.user);
        this.updateUI();
        Toast.success(res.message || 'Signed in successfully.');
        return res.data;
      }
      throw new Error(res.message || 'Login failed.');
    } catch (err) {
      Toast.error(err.message || 'Invalid email or password.');
      throw err;
    }
  },

  async register(name, email, password) {
    try {
      const res = await APIClient.post('/api/auth/register', { name, email, password });
      if (res && res.data) {
        APIClient.setToken(res.data.token);
        APIClient.setUser(res.data.user);
        this.updateUI();
        Toast.success(res.message || 'Account registered successfully.');
        return res.data;
      }
      throw new Error(res.message || 'Registration failed.');
    } catch (err) {
      Toast.error(err.message || 'Registration failed.');
      throw err;
    }
  },

  logout() {
    APIClient.setToken(null);
    APIClient.setUser(null);
    Toast.info('You have been logged out.');
    this.updateUI();
    setTimeout(() => {
      window.location.href = '/login.html';
    }, 500);
  },

  updateUI() {
    const authContainer = document.getElementById('nav-auth-container');
    const adminLink = document.getElementById('nav-admin-link');
    const myReportsLink = document.getElementById('nav-my-reports-link');

    if (this.isLoggedIn()) {
      const user = this.getUser();
      if (authContainer) {
        authContainer.innerHTML = `
          <div style="display:flex; align-items:center; gap:0.75rem;">
            <span style="font-size:0.85rem; font-weight:600; color:var(--primary);">
              <i class="fas fa-user-circle"></i> ${user.name || 'User'}
            </span>
            <button onclick="Auth.logout()" class="auth-btn" style="cursor:pointer; background:#FFFFFF;">
              <i class="fas fa-sign-out-alt"></i> Logout
            </button>
          </div>
        `;
      }

      if (myReportsLink) myReportsLink.style.display = 'block';
      if (adminLink) adminLink.style.display = this.isAdmin() ? 'block' : 'none';
    } else {
      if (authContainer) {
        authContainer.innerHTML = `
          <a href="/login.html" class="auth-btn"><i class="fas fa-user-shield"></i> Portal Login</a>
        `;
      }
      if (myReportsLink) myReportsLink.style.display = 'none';
      if (adminLink) adminLink.style.display = 'none';
    }
  },

  requireAuth(adminOnly = false) {
    if (!this.isLoggedIn()) {
      Toast.warning('Please log in to access this section.');
      window.location.href = '/login.html';
      return false;
    }
    if (adminOnly && !this.isAdmin()) {
      Toast.error('Access restricted. Administrative privileges required.');
      window.location.href = '/';
      return false;
    }
    return true;
  }
};

document.addEventListener('DOMContentLoaded', () => {
  Auth.updateUI();

  // Mobile menu toggle
  const toggleBtn = document.getElementById('mobile-toggle-btn');
  const navMenu = document.getElementById('site-nav-menu');
  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      navMenu.classList.toggle('active');
    });
  }
});

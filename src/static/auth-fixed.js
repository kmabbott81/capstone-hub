// Simple Authentication Manager
class AuthManager {
    constructor() {
        this.init();
    }

    init() {
        // Check if user is already logged in
        const role = this.getUserRole();
        this.updateUserInterface();
        
        // Add admin login button if not admin
        if (role !== 'admin') {
            this.addAdminLoginButton();
        }
    }

    getUserRole() {
        const saved = localStorage.getItem('userRole');
        if (saved) return saved;
        // Auto-admin on localhost, viewer on production
        const isLocal = ['localhost', '127.0.0.1'].includes(location.hostname);
        return isLocal ? 'admin' : 'viewer';
    }

    setUserRole(role) {
        localStorage.setItem('userRole', role);
    }

    addAdminLoginButton() {
        // Remove any existing login buttons
        const existingButton = document.querySelector('.floating-admin-login');
        if (existingButton) {
            existingButton.remove();
        }

        // Add floating admin login button in bottom right
        const loginButton = document.createElement('div');
        loginButton.className = 'floating-admin-login';
        loginButton.innerHTML = `
            <button class="floating-login-btn" data-action="admin-login" title="Admin Login">
                <span class="login-icon">🔐</span>
            </button>
        `;
        document.body.appendChild(loginButton);

        // Add event listener (CSP-compliant)
        const btn = loginButton.querySelector('[data-action="admin-login"]');
        btn.addEventListener('click', () => this.showAdminLogin());
    }

    async showAdminLogin() {
        const password = prompt('Enter admin password to enable editing:');
        if (!password) return;

        try {
            // Verify password with server
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ password })
            });

            const data = await response.json();

            if (data.success && data.role === 'admin') {
                this.setUserRole('admin');
                alert('✅ Admin access granted! You can now edit content.');
                location.reload();
            } else {
                alert('❌ Incorrect password. Access denied.');
            }
        } catch (error) {
            console.error('Login error:', error);
            alert('❌ Login failed. Please try again.');
        }
    }

    updateUserInterface() {
        const role = this.getUserRole();
        document.body.className = `role-${role}`;
        
        // Add admin status indicator
        if (role === 'admin') {
            this.addAdminStatusIndicator();
        } else {
            this.removeAdminStatusIndicator();
        }
    }
    
    addAdminStatusIndicator() {
        // Remove existing indicator
        const existing = document.querySelector('.admin-status-indicator');
        if (existing) existing.remove();

        // Add admin status indicator
        const indicator = document.createElement('div');
        indicator.className = 'admin-status-indicator';
        indicator.innerHTML = `
            <div class="admin-badge">
                <span class="admin-icon">👑</span>
                <span class="admin-text">Admin</span>
                <button class="backup-btn" data-action="backup-database" title="Backup Database">💾</button>
                <button class="logout-btn" data-action="logout">Logout</button>
            </div>
        `;
        document.body.appendChild(indicator);

        // Add event listeners (CSP-compliant)
        const logoutBtn = indicator.querySelector('[data-action="logout"]');
        logoutBtn.addEventListener('click', () => this.logout());

        const backupBtn = indicator.querySelector('[data-action="backup-database"]');
        backupBtn.addEventListener('click', () => this.triggerBackup());
    }
    
    removeAdminStatusIndicator() {
        const indicator = document.querySelector('.admin-status-indicator');
        if (indicator) indicator.remove();
    }
    
    async triggerBackup() {
        if (!confirm('Create a backup of the database now?')) return;

        try {
            const token = await getCSRFToken();
            const response = await fetch('/api/admin/backup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': token
                }
            });

            const data = await response.json();

            if (data.success) {
                alert('✅ ' + data.message);
            } else {
                alert('❌ ' + data.message);
            }
        } catch (error) {
            console.error('Backup error:', error);
            alert('❌ Backup failed. Check console for details.');
        }
    }

    logout() {
        this.setUserRole('viewer');
        alert('✅ Logged out successfully');
        location.reload();
    }
}

// Initialize authentication when page loads
let authManager;
document.addEventListener('DOMContentLoaded', function() {
    authManager = new AuthManager();
});

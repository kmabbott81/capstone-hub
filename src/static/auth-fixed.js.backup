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
        return localStorage.getItem('userRole') || 'viewer';
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
            <button class="floating-login-btn" onclick="authManager.showAdminLogin()" title="Admin Login">
                <span class="login-icon">🔐</span>
            </button>
        `;
        document.body.appendChild(loginButton);
    }

    showAdminLogin() {
        const password = prompt('Enter admin password to enable editing:');
        if (password === 'HLStearns2025!') {
            this.setUserRole('admin');
            alert('✅ Admin access granted! You can now edit content.');
            location.reload();
        } else if (password !== null) {
            alert('❌ Incorrect password. Access denied.');
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
                <button class="logout-btn" onclick="authManager.logout()">Logout</button>
            </div>
        `;
        document.body.appendChild(indicator);
    }
    
    removeAdminStatusIndicator() {
        const indicator = document.querySelector('.admin-status-indicator');
        if (indicator) indicator.remove();
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


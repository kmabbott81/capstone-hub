// Authentication and Role Management - View-Only by Default

class AuthManager {
    constructor() {
        this.userRole = 'viewer'; // Default to viewer mode
        this.userPermissions = {
            can_edit: false,
            can_delete: false,
            can_export: true,
            can_manage_integrations: false,
            can_view_analytics: true
        };
        this.init();
    }

    async init() {
        // Check if we're on the login page
        if (window.location.pathname.includes('login.html')) {
            return; // Don't check auth on login page
        }

        // Check if user has admin session
        await this.checkAdminStatus();
        
        // Always allow access - just update UI based on role
        this.updateUIBasedOnRole();
    }

    async checkAdminStatus() {
        try {
            const response = await fetch('/api/auth/status');
            const data = await response.json();
            
            if (data.authenticated && data.role === 'admin') {
                this.userRole = 'admin';
                this.userPermissions = data.permissions;
                
                // Store in localStorage for quick access
                localStorage.setItem('userRole', 'admin');
                localStorage.setItem('userPermissions', JSON.stringify(data.permissions));
                
                return true;
            } else {
                // Default to viewer mode
                this.userRole = 'viewer';
                this.userPermissions = {
                    can_edit: false,
                    can_delete: false,
                    can_export: true,
                    can_manage_integrations: false,
                    can_view_analytics: true
                };
                
                localStorage.setItem('userRole', 'viewer');
                localStorage.setItem('userPermissions', JSON.stringify(this.userPermissions));
                return false;
            }
        } catch (error) {
            console.log('No admin session - defaulting to viewer mode');
            // Default to viewer mode on any error
            this.userRole = 'viewer';
            return false;
        }
    }

    updateUIBasedOnRole() {
        const isAdmin = this.userRole === 'admin';
        
        // Update header to show role and login option
        this.addUserInfo();
        
        // Show/hide edit buttons based on permissions
        this.toggleEditControls(this.userPermissions.can_edit);
        
        // Add admin login button for viewers
        if (!isAdmin) {
            this.addAdminLoginButton();
        } else {
            this.addLogoutButton();
        }
        
        // Update navigation based on permissions
        this.updateNavigationPermissions();
        
        // Add role-specific styling
        document.body.classList.add(`role-${this.userRole}`);
    }

    addUserInfo() {
        const header = document.querySelector('.main-header');
        if (header && !document.querySelector('.user-info')) {
            const userInfo = document.createElement('div');
            userInfo.className = 'user-info';
            
            if (this.userRole === 'admin') {
                userInfo.innerHTML = `
                    <div class="role-indicator admin">
                        <span class="role-badge admin">Admin</span>
                        <span class="role-permissions">Full Access</span>
                    </div>
                `;
            } else {
                userInfo.innerHTML = `
                    <div class="role-indicator viewer">
                        <span class="role-badge viewer">Viewer</span>
                        <span class="role-permissions">Read Only</span>
                    </div>
                `;
            }
            header.appendChild(userInfo);
        }
    }

    addAdminLoginButton() {
        // Remove any existing login buttons
        const existingButton = document.querySelector('.admin-login-section');
        if (existingButton) {
            existingButton.remove();
        }
        
        // Add floating admin login button in bottom right
        if (!document.querySelector('.floating-admin-login')) {
            const loginButton = document.createElement('div');
            loginButton.className = 'floating-admin-login';
            loginButton.innerHTML = `
                <button class="floating-login-btn" onclick="authManager.showAdminLogin()" title="Admin Login">
                    <span class="login-icon">🔐</span>
                </button>
            `;
            document.body.appendChild(loginButton);
        }
    }

    showAdminLogin() {
        const password = prompt('Enter admin password to enable editing:');
        if (password === 'HLStearns2025!') {
            this.setUserRole('admin');
            alert('Admin access granted! You can now edit content.');
            location.reload(); // Refresh to show admin interface
        } else if (password !== null) {
            alert('Incorrect password. Access denied.');
        }
    }JSON.stringify(data.permissions));
                
                // Refresh the page to update UI
                window.location.reload();
            } else {
                alert('Invalid admin password');
            }
        } catch (error) {
            alert('Login failed. Please try again.');
        }
    }

    toggleEditControls(canEdit) {
        // Hide all edit/add/delete buttons for viewers
        const editElements = document.querySelectorAll(`
            .add-btn, 
            .edit-btn, 
            .delete-btn, 
            .btn-primary:not(.export-btn),
            input:not([readonly]),
            textarea:not([readonly]),
            select:not([disabled])
        `);
        
        editElements.forEach(element => {
            if (canEdit) {
                element.style.display = '';
                element.disabled = false;
            } else {
                if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                    element.readOnly = true;
                    element.style.backgroundColor = '#f8f9fa';
                } else if (element.tagName === 'SELECT') {
                    element.disabled = true;
                } else {
                    element.style.display = 'none';
                }
            }
        });
        
        // Add visual indicators for read-only mode
        if (!canEdit) {
            const sections = document.querySelectorAll('.content-section');
            sections.forEach(section => {
                section.classList.add('read-only');
            });
            
            // Add read-only notice
            this.addReadOnlyNotice();
        }
    }

    addReadOnlyNotice() {
        if (!document.querySelector('.read-only-notice')) {
            const notice = document.createElement('div');
            notice.className = 'read-only-notice';
            notice.innerHTML = `
                <div class="notice-content">
                    <span class="notice-icon">👁️</span>
                    <span class="notice-text">You have view-only access to this capstone project</span>
                </div>
            `;
            document.body.appendChild(notice);
        }
    }

    addLogoutButton() {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar && !document.querySelector('.logout-section')) {
            const logoutSection = document.createElement('div');
            logoutSection.className = 'logout-section';
            logoutSection.innerHTML = `
                <button class="logout-btn" onclick="authManager.logout()">
                    <span class="logout-icon">🚪</span>
                    <span class="logout-text">Logout</span>
                </button>
            `;
            sidebar.appendChild(logoutSection);
        }
    }

    async logout() {
        try {
            await fetch('/api/auth/logout', { method: 'POST' });
        } catch (error) {
            console.error('Logout error:', error);
        } finally {
            localStorage.removeItem('userRole');
            localStorage.removeItem('userPermissions');
            window.location.href = '/login.html';
        }
    }

    updateNavigationPermissions() {
        // Disable integration management for viewers
        if (!this.userPermissions.can_manage_integrations) {
            const integrationNav = document.querySelector('[data-section="integrations"]');
            if (integrationNav) {
                integrationNav.style.opacity = '0.7';
                integrationNav.title = 'View only - Admin access required for management';
            }
        }
    }

    // Helper method to check if user can perform action
    canPerformAction(action) {
        return this.userPermissions[action] || false;
    }

    // Helper method to get user role
    getUserRole() {
        return this.userRole;
    }

    // Helper method to show permission denied message
    showPermissionDenied(action = 'perform this action') {
        const message = document.createElement('div');
        message.className = 'permission-denied-toast';
        message.innerHTML = `
            <div class="toast-content">
                <span class="toast-icon">🔒</span>
                <span class="toast-text">Admin access required to ${action}</span>
            </div>
        `;
        document.body.appendChild(message);
        
        setTimeout(() => {
            message.remove();
        }, 3000);
    }
}

// Initialize auth manager when DOM is loaded
let authManager;
document.addEventListener('DOMContentLoaded', () => {
    authManager = new AuthManager();
});

// Export for global access
window.authManager = authManager;


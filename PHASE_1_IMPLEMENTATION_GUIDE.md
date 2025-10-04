# Phase 1 Implementation Guide: Core CRUD & Security
**Version:** 0.35.0
**Status:** Ready for Implementation
**Estimated Time:** 8-10 hours

---

## Progress So Far

### ✅ Completed
- Created `src/version.py` with version 0.35.0
- Fixed inline onclick on modal cancel buttons (changed to `data-action="close-modal"`)
- Fixed inline onclick on "Edit Dropdown Options" button
- Added event handler for `edit-process-dropdowns` action

### 🚧 In Progress
- Removing remaining inline onclick handlers in editProcessDropdowns function

---

## Remaining Tasks for Phase 1

### 1. Complete Inline onclick Removal

**Files:** `src/static/app.js`

**Issue:** The `editProcessDropdowns()` function (line 1570+) and related functions (`addOption`, `removeOption`, `resetDropdownOptions`) use inline onclick handlers.

**Solution:** Refactor to use event delegation with data attributes.

**Implementation:**

```javascript
// Replace lines 1570-1700 with this refactored version:

function editProcessDropdowns() {
    const options = getDropdownOptions();

    const form = `
        <form id="dropdown-options-form">
            <div class="dropdown-editor-section">
                <h3 style="margin-bottom: 1rem; color: var(--gray-700);">Departments</h3>
                <div id="departments-list" class="options-list">
                    ${options.departments.map((dept, index) => `
                        <div class="option-item">
                            <input type="text" value="${escapeHTML(dept)}" class="form-control" data-type="department" data-index="${index}">
                            <button type="button" class="btn-danger-sm" data-action="remove-option" data-option-type="department" data-index="${index}">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `).join('')}
                </div>
                <button type="button" class="btn-secondary-sm" data-action="add-option" data-option-type="department">
                    <i class="fas fa-plus"></i> Add Department
                </button>
            </div>

            <div class="dropdown-editor-section" style="margin-top: 2rem;">
                <h3 style="margin-bottom: 1rem; color: var(--gray-700);">Automation Potential</h3>
                <div id="automation-list" class="options-list">
                    ${options.automationLevels.map((auto, index) => `
                        <div class="option-item">
                            <input type="text" value="${escapeHTML(auto)}" class="form-control" data-type="automation" data-index="${index}">
                            <button type="button" class="btn-danger-sm" data-action="remove-option" data-option-type="automation" data-index="${index}">
                                <i class="fas fa-trash"></i>
                            </button>
                        </div>
                    `).join('')}
                </div>
                <button type="button" class="btn-secondary-sm" data-action="add-option" data-option-type="automation">
                    <i class="fas fa-plus"></i> Add Option
                </button>
            </div>

            <div class="form-actions">
                <button type="button" class="btn-secondary" data-action="close-modal">Cancel</button>
                <button type="button" class="btn-secondary" data-action="reset-dropdown-options">Reset to Defaults</button>
                <button type="submit" class="btn-primary">Save Changes</button>
            </div>
        </form>

        <style>
        .dropdown-editor-section {
            margin-bottom: 1.5rem;
        }
        .options-list {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }
        .option-item {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        .option-item input {
            flex: 1;
        }
        .btn-danger-sm, .btn-secondary-sm {
            padding: 0.5rem 0.75rem;
            font-size: 0.875rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s;
        }
        .btn-danger-sm {
            background-color: var(--error-color);
            color: white;
        }
        .btn-danger-sm:hover {
            background-color: #dc2626;
        }
        .btn-secondary-sm {
            background-color: var(--gray-200);
            color: var(--gray-700);
        }
        .btn-secondary-sm:hover {
            background-color: var(--gray-300);
        }
        </style>
    `;

    capstoneHub.showModal('Edit Dropdown Options', form);

    // Add event listeners using event delegation
    setTimeout(() => {
        const modal = document.querySelector('.modal');
        if (!modal) return;

        // Handle add-option
        modal.addEventListener('click', (e) => {
            const target = e.target.closest('[data-action="add-option"]');
            if (target) {
                const type = target.dataset.optionType;
                addDropdownOption(type);
            }
        });

        // Handle remove-option
        modal.addEventListener('click', (e) => {
            const target = e.target.closest('[data-action="remove-option"]');
            if (target) {
                target.closest('.option-item').remove();
            }
        });

        // Handle reset
        modal.addEventListener('click', (e) => {
            const target = e.target.closest('[data-action="reset-dropdown-options"]');
            if (target) {
                resetDropdownOptions();
            }
        });

        // Handle form submit
        const formElement = document.getElementById('dropdown-options-form');
        if (formElement) {
            formElement.addEventListener('submit', (e) => {
                e.preventDefault();
                saveDropdownOptionsForm();
            });
        }
    }, 100);
}

function addDropdownOption(type) {
    const listId = type === 'department' ? 'departments-list' : 'automation-list';
    const list = document.getElementById(listId);
    if (!list) return;

    const currentItems = list.querySelectorAll('.option-item');
    const newIndex = currentItems.length;

    const newItem = document.createElement('div');
    newItem.className = 'option-item';
    newItem.innerHTML = `
        <input type="text" value="" class="form-control" data-type="${type}" data-index="${newIndex}" placeholder="Enter ${type === 'department' ? 'department name' : 'automation level'}">
        <button type="button" class="btn-danger-sm" data-action="remove-option" data-option-type="${type}" data-index="${newIndex}">
            <i class="fas fa-trash"></i>
        </button>
    `;

    list.appendChild(newItem);
    newItem.querySelector('input').focus();
}

function resetDropdownOptions() {
    if (!confirm('Reset to default options? This will discard your custom options.')) {
        return;
    }

    const defaults = {
        departments: ['Sales', 'Operations', 'Customer Service', 'Finance', 'IT', 'Human Resources', 'Marketing', 'Procurement'],
        automationLevels: ['High', 'Medium', 'Low']
    };

    saveDropdownOptions(defaults);
    capstoneHub.closeModal();
    showNotification('Dropdown options reset to defaults', 'success');

    // Refresh the form if it's still open
    setTimeout(() => editProcessDropdowns(), 200);
}

function saveDropdownOptionsForm() {
    const departmentInputs = document.querySelectorAll('[data-type="department"]');
    const automationInputs = document.querySelectorAll('[data-type="automation"]');

    const departments = Array.from(departmentInputs)
        .map(input => input.value.trim())
        .filter(val => val.length > 0);

    const automationLevels = Array.from(automationInputs)
        .map(input => input.value.trim())
        .filter(val => val.length > 0);

    if (departments.length === 0) {
        showNotification('Please add at least one department', 'error');
        return;
    }

    if (automationLevels.length === 0) {
        showNotification('Please add at least one automation level', 'error');
        return;
    }

    const options = {
        departments,
        automationLevels
    };

    saveDropdownOptions(options);
    capstoneHub.closeModal();
    showNotification('Dropdown options saved successfully', 'success');
}
```

**Add these event handlers to the main event delegation block (around line 1385):**

```javascript
// Special actions
if (action === 'edit-process-dropdowns') return editProcessDropdowns();
if (action === 'reset-dropdown-options') return resetDropdownOptions();
```

---

### 2. Complete Edit Functions for All Entities

Currently only `editProcess` and `updateProcess` are fully implemented. Need to implement for:
- Deliverables
- AI Technologies
- Software Tools
- Research Items
- Integrations

**Pattern to follow:** (based on existing editProcess implementation)

#### 2.1 Edit Deliverables

Add after `deleteDeliverable` function:

```javascript
editDeliverable(id) {
    const item = this.data.deliverables.find(d => d.id === id);
    if (!item) {
        showNotification('Deliverable not found', 'error');
        return;
    }

    const form = `
        <form id="deliverable-form">
            <div class="form-group mb-3">
                <label for="deliverable-title">Title</label>
                <input type="text" id="deliverable-title" class="form-control"
                       value="${escapeHTML(item.title)}" required>
            </div>
            <div class="form-group mb-3">
                <label for="deliverable-description">Description</label>
                <textarea id="deliverable-description" class="form-control" rows="3">${escapeHTML(item.description || '')}</textarea>
            </div>
            <div class="form-group mb-3">
                <label for="deliverable-phase">Phase</label>
                <select id="deliverable-phase" class="form-control">
                    <option value="Planning" ${item.phase === 'Planning' ? 'selected' : ''}>Planning</option>
                    <option value="Research" ${item.phase === 'Research' ? 'selected' : ''}>Research</option>
                    <option value="Analysis" ${item.phase === 'Analysis' ? 'selected' : ''}>Analysis</option>
                    <option value="Writing" ${item.phase === 'Writing' ? 'selected' : ''}>Writing</option>
                    <option value="Review" ${item.phase === 'Review' ? 'selected' : ''}>Review</option>
                </select>
            </div>
            <div class="form-group mb-3">
                <label for="deliverable-due-date">Due Date</label>
                <input type="date" id="deliverable-due-date" class="form-control"
                       value="${item.due_date || ''}">
            </div>
            <div class="form-group mb-3">
                <label for="deliverable-status">Status</label>
                <select id="deliverable-status" class="form-control">
                    <option value="Not Started" ${item.status === 'Not Started' ? 'selected' : ''}>Not Started</option>
                    <option value="In Progress" ${item.status === 'In Progress' ? 'selected' : ''}>In Progress</option>
                    <option value="Complete" ${item.status === 'Complete' ? 'selected' : ''}>Complete</option>
                </select>
            </div>
            <div class="form-actions">
                <button type="button" class="btn-secondary" data-action="close-modal">Cancel</button>
                <button type="submit" class="btn-primary">Update Deliverable</button>
            </div>
        </form>
    `;

    this.showModal('Edit Deliverable', form);

    setTimeout(() => {
        const formElement = document.getElementById('deliverable-form');
        if (formElement) {
            formElement.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.updateDeliverable(id);
            });
        }
    }, 100);
}

async updateDeliverable(id) {
    const title = document.getElementById('deliverable-title').value;
    const description = document.getElementById('deliverable-description').value;
    const phase = document.getElementById('deliverable-phase').value;
    const dueDate = document.getElementById('deliverable-due-date').value;
    const status = document.getElementById('deliverable-status').value;

    try {
        const response = await fetch(`/api/deliverables/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                title: title,
                description: description,
                phase: phase,
                due_date: dueDate,
                status: status
            })
        });

        if (response.ok) {
            this.closeModal();
            this.loadDeliverables();
            this.updateDashboard();
            showNotification('Deliverable updated successfully!', 'success');
        } else {
            showNotification('Error updating deliverable', 'error');
        }
    } catch (error) {
        console.error('Error updating deliverable:', error);
        showNotification('Error updating deliverable', 'error');
    }
}
```

#### 2.2 Edit AI Technologies, Software Tools, Research Items, Integrations

Follow the same pattern - for brevity, I'm providing the structure only. Each needs:
- `editXXX(id)` function with form modal
- `updateXXX(id)` async function with PUT request
- Form fields matching the entity's schema

The form should populate existing values and submit updates.

---

### 3. Update requirements.txt

Add new dependencies:

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-Cors==4.0.0
Flask-WTF==1.2.1
Flask-Limiter==3.5.0
python-dotenv==1.0.0
Werkzeug==2.3.7
```

---

### 4. Add CSRF Protection

**File:** `src/app.py`

```python
from flask_wtf.csrf import CSRFProtect

# After app initialization
csrf = CSRFProtect(app)

# Configure CSRF
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_TIME_LIMIT'] = None  # No expiration
app.config['WTF_CSRF_CHECK_DEFAULT'] = False  # Don't check by default (use decorator)

# Add CSRF token endpoint
@app.route('/api/csrf-token', methods=['GET'])
def get_csrf_token():
    from flask_wtf.csrf import generate_csrf
    return jsonify({'csrf_token': generate_csrf()})
```

**File:** `src/static/index.html`

Add meta tag in `<head>`:

```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```

**File:** `src/static/app.js`

Add CSRF token to all fetch requests:

```javascript
// Add this helper function near the top of app.js
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
}

// Update all fetch calls to include CSRF token in headers
const response = await fetch('/api/endpoint', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify(data)
});
```

**Apply @csrf.exempt or manual validation to all API routes that need it.**

---

### 5. Add Rate Limiting

**File:** `src/app.py`

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["2000 per day", "500 per hour"],
    storage_uri="memory://"
)
```

**File:** `src/routes/auth.py`

```python
from src.app import limiter

@auth_bp.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per 15 minutes")
def login():
    # ... existing code
```

---

### 6. Session Timeout (30 minutes)

**File:** `src/app.py`

```python
from datetime import timedelta

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

@app.before_request
def make_session_permanent():
    session.permanent = True
    session.modified = True
```

**File:** `src/static/app.js`

Add heartbeat to keep session alive:

```javascript
// Add to CapstoneHub init() method
this.startSessionHeartbeat();

// Add method to CapstoneHub class
startSessionHeartbeat() {
    // Ping server every 5 minutes to keep session alive
    setInterval(async () => {
        try {
            await fetch('/api/auth/status');
        } catch (error) {
            console.warn('Session heartbeat failed:', error);
        }
    }, 5 * 60 * 1000); // 5 minutes
}
```

---

### 7. Backup System

**File:** `backup_database.py` (new file in root)

```python
#!/usr/bin/env python3
"""
Database Backup Script
Backs up SQLite database with timestamp
"""

import shutil
import os
from datetime import datetime

def backup_database():
    """Create timestamped backup of database"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    source = 'src/database/app.db'
    backup_dir = 'src/database/backups'
    destination = f'{backup_dir}/app_{timestamp}.db'

    # Create backups directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)

    # Copy database
    shutil.copy2(source, destination)
    print(f'✅ Backup created: {destination}')

    # Cleanup old backups (keep last 14)
    cleanup_old_backups(backup_dir, keep=14)

    return destination

def cleanup_old_backups(backup_dir, keep=14):
    """Remove old backups, keeping only the most recent"""
    backups = sorted([
        os.path.join(backup_dir, f)
        for f in os.listdir(backup_dir)
        if f.startswith('app_') and f.endswith('.db')
    ])

    if len(backups) > keep:
        for old_backup in backups[:-keep]:
            os.remove(old_backup)
            print(f'🗑️  Removed old backup: {os.path.basename(old_backup)}')

if __name__ == '__main__':
    backup_database()
```

**File:** `src/routes/admin.py` (new file)

```python
from flask import Blueprint, jsonify
from src.routes.auth import require_admin
import subprocess
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/backup', methods=['POST'])
@require_admin
def trigger_backup():
    """Manually trigger database backup"""
    try:
        # Run backup script
        result = subprocess.run(
            ['python', 'backup_database.py'],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Backup created successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Backup failed',
                'error': result.stderr
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Backup error: {str(e)}'
        }), 500
```

**Register blueprint in** `src/app.py`:

```python
from src.routes.admin import admin_bp
app.register_blueprint(admin_bp)
```

**Add backup button to admin badge in** `src/static/auth-fixed.js`:

```javascript
addAdminStatusIndicator() {
    const existing = document.querySelector('.admin-status-indicator');
    if (existing) existing.remove();

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

    // Add event listeners
    const logoutBtn = indicator.querySelector('[data-action="logout"]');
    logoutBtn.addEventListener('click', () => this.logout());

    const backupBtn = indicator.querySelector('[data-action="backup-database"]');
    backupBtn.addEventListener('click', () => this.triggerBackup());
}

async triggerBackup() {
    if (!confirm('Create a backup of the database now?')) return;

    try {
        const response = await fetch('/api/admin/backup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
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
```

**Schedule nightly backups** (Railway cron or external scheduler):

Create `.railway/cron.json`:
```json
{
  "jobs": [
    {
      "schedule": "0 2 * * *",
      "command": "python backup_database.py"
    }
  ]
}
```

---

## Testing Checklist

### CSP & Inline JS
- [ ] No console errors about CSP violations
- [ ] All buttons work without inline onclick
- [ ] Edit dropdown options modal functions correctly

### CRUD Operations
- [ ] Edit deliverable - form populates, save persists
- [ ] Edit AI technology - form populates, save persists
- [ ] Edit software tool - form populates, save persists
- [ ] Edit research item - form populates, save persists
- [ ] Edit integration - form populates, save persists

### Security
- [ ] Login fails after 5 attempts in 15 minutes (rate limiting)
- [ ] Session expires after 30 minutes of inactivity
- [ ] CSRF token required for all POST/PUT/DELETE
- [ ] Backup button creates timestamped .db file

### General
- [ ] All existing functionality still works
- [ ] No JavaScript errors in console
- [ ] Database operations commit properly
- [ ] Error messages are user-friendly

---

## Deployment Steps

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Test locally:**
```bash
python src/app.py
```

3. **Commit changes:**
```bash
git add .
git commit -m "Phase 1: Core CRUD & Security - v0.35.0"
git push
```

4. **Deploy to Railway:**
```bash
railway up --service capstone-hub
```

5. **Verify deployment:**
- Check Railway logs for errors
- Test login rate limiting
- Test backup functionality
- Test edit functions

---

## Files Changed/Created Summary

### Modified Files
- `src/static/app.js` - Fixed onclick, added edit functions
- `src/static/index.html` - Fixed onclick on dropdown button
- `src/static/auth-fixed.js` - Added backup button and handler
- `src/app.py` - Added CSRF, rate limiting, session timeout
- `src/routes/auth.py` - Added rate limiting to login
- `requirements.txt` - Added Flask-WTF and Flask-Limiter

### New Files
- `src/version.py` - Version information
- `src/routes/admin.py` - Admin endpoints (backup)
- `backup_database.py` - Backup script
- `.railway/cron.json` - Scheduled backup job

---

## Next Steps (Phase 2 & 3)

This guide covers Phase 1. Once complete, proceed to:

**Phase 2:** Attachments, Comments, Search/Sort/Pagination
**Phase 3:** Exports, iCal, Tests, Documentation, PR

---

**End of Phase 1 Implementation Guide**

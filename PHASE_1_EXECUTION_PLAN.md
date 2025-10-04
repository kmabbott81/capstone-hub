# Phase 1 Execution Plan - Adapted to Current Codebase
**Date:** October 3, 2025
**Version:** 0.35.0
**Status:** Ready to Execute

---

## Current State Analysis

### ✅ Already Implemented
- **Security headers** (CSP, X-Frame-Options, X-Content-Type-Options)
- **@require_admin decorator** in `src/routes/auth.py`
- **Session-based auth** with `user_role` and `authenticated` flags
- **Secure session cookies** (HttpOnly, Secure, SameSite=Lax)
- **Database models** for all 6 entities
- **CRUD routes** for all entities (with @require_admin on write operations)
- **Event delegation** partially implemented (some onclick violations remain)
- **XSS escaping** via `escapeHTML()` function

### 🚧 Needs Implementation
1. **CSRF Protection** - Add Flask-WTF
2. **Rate Limiting** - Add Flask-Limiter
3. **Session Timeout** - 30-minute idle timeout
4. **Backup System** - Automated database backups
5. **Complete Event Delegation** - Remove remaining inline onclick
6. **Complete Edit Functions** - All entities need edit/update

---

## Implementation Steps

### Step 1: Update Dependencies

**File:** `requirements.txt`

Add these lines:
```txt
Flask-WTF==1.2.1
Flask-Limiter==3.5.0
```

**Action:**
```bash
pip install Flask-WTF==1.2.1 Flask-Limiter==3.5.0
```

---

### Step 2: Add CSRF Protection

**File:** `src/main.py`

Add after imports:
```python
from flask_wtf.csrf import CSRFProtect, generate_csrf
from datetime import timedelta, datetime

csrf = CSRFProtect(app)

# Configure CSRF
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_CHECK_DEFAULT'] = False  # Manual checking via decorator
app.config['WTF_CSRF_TIME_LIMIT'] = None  # No expiration

# CSRF token endpoint
@app.route('/api/csrf-token', methods=['GET'])
def get_csrf_token():
    return jsonify({'csrf_token': generate_csrf()})
```

**File:** `src/static/index.html`

Add in `<head>` section:
```html
<meta name="csrf-token" content="{{ csrf_token() }}">
```

**File:** `src/static/app.js`

Add helper function at top:
```javascript
// CSRF token helper
function getCSRFToken() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    if (meta) return meta.getAttribute('content');

    // Fallback: parse from cookie
    const match = document.cookie.match(/csrf_token=([^;]+)/);
    return match ? match[1] : '';
}
```

Update all fetch calls to include CSRF token:
```javascript
// Example for saveDeliverable - apply same pattern to all POST/PUT/DELETE
async saveDeliverable() {
    // ... existing code ...
    const response = await fetch('/api/deliverables', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()  // ADD THIS LINE
        },
        body: JSON.stringify(data)
    });
    // ... rest of code ...
}
```

**Apply CSRF to routes:**

In each route file (deliverables.py, business_processes.py, etc.), add at top:
```python
from flask_wtf.csrf import csrf_protect
```

Then decorate write endpoints:
```python
@deliverables_bp.route('/api/deliverables', methods=['POST'])
@require_admin
@csrf_protect
def create_deliverable():
    # ... existing code ...
```

---

### Step 3: Add Rate Limiting

**File:** `src/main.py`

Add after csrf setup:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["2000 per day", "200 per hour"],
    storage_uri="memory://"
)
```

**File:** `src/routes/auth.py`

Add at top:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Get limiter from main app
from src.main import limiter
```

Add to login endpoint:
```python
@auth_bp.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per 15 minutes")  # ADD THIS LINE
def login():
    # ... existing code ...
```

---

### Step 4: Add Session Timeout

**File:** `src/main.py`

Update session config:
```python
app.config['SESSION_PERMANENT'] = True  # CHANGE FROM False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # ADD THIS
```

Add before request handler:
```python
@app.before_request
def enforce_idle_timeout():
    """Enforce 30-minute idle timeout"""
    if request.path.startswith('/api/'):
        now = datetime.utcnow().timestamp()
        last = session.get('_last_seen')

        if last and (now - last) > 1800:  # 30 minutes in seconds
            session.clear()
            if request.method != 'GET':
                return jsonify({'error': 'Session expired'}), 401

        session['_last_seen'] = now
```

---

### Step 5: Complete Backup System

**File:** `backup_database.py` (already created ✅)

**File:** `src/routes/admin.py` (NEW)

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
        result = subprocess.run(
            ['python', 'backup_database.py'],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
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

**File:** `src/main.py`

Add to imports:
```python
from src.routes.admin import admin_bp
```

Add to blueprint registrations:
```python
app.register_blueprint(admin_bp)
```

**File:** `src/static/auth-fixed.js`

Update `addAdminStatusIndicator()`:
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

    // Event listeners
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

---

## Testing Checklist

### Local Testing

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
python src/main.py

# 3. Test in browser (http://localhost:5000)
```

**Manual Tests:**
- [ ] Login as admin
- [ ] Add a deliverable (should work)
- [ ] Try adding without CSRF token (should fail with 403)
- [ ] Try login 6 times rapidly (should rate limit after 5)
- [ ] Wait 31 minutes idle (should timeout session)
- [ ] Click backup button in admin badge (should create backup file)
- [ ] Check `src/database/backups/` for timestamped backup

### Automated Tests (Optional)

Create `tests/test_phase1.py`:
```python
import pytest
from src.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_csrf_protection(client):
    # Should fail without CSRF token
    response = client.post('/api/deliverables',
                          json={'title': 'Test'},
                          headers={'X-CSRFToken': 'invalid'})
    assert response.status_code == 403

def test_rate_limiting(client):
    # Make 6 login attempts
    for i in range(6):
        client.post('/api/auth/login', json={'password': 'wrong'})

    # 6th attempt should be rate limited
    response = client.post('/api/auth/login', json={'password': 'wrong'})
    assert response.status_code == 429
```

Run:
```bash
pytest tests/test_phase1.py -v
```

---

## Deployment Commands

### 1. Commit Changes

```bash
git add .
git commit -m "Phase 1: CSRF protection, rate limiting, session timeout, backup system"
git push
```

### 2. Deploy to Railway

```bash
railway up --service capstone-hub
```

### 3. Verify Deployment

```bash
railway logs --service capstone-hub --tail 100
```

### 4. Smoke Test Production

```bash
# Test CSRF endpoint
curl https://mabbottmbacapstone.up.railway.app/api/csrf-token

# Should return: {"csrf_token": "..."}
```

---

## Rollback Plan

If issues occur:

```bash
# Revert to previous commit
git revert HEAD
git push

# Redeploy
railway up --service capstone-hub
```

---

## Success Criteria

✅ **CSRF Protection:**
- POST/PUT/DELETE without CSRF token returns 403
- Valid CSRF token allows operations

✅ **Rate Limiting:**
- 6th login attempt within 15 minutes returns 429
- Other endpoints respect default limits

✅ **Session Timeout:**
- Idle session for >30 minutes clears auth
- Active sessions stay alive

✅ **Backup System:**
- Manual backup button creates timestamped file
- Old backups cleaned up (keep 14)

✅ **No Regressions:**
- All existing CRUD operations still work
- No console errors
- CSP violations fixed

---

## Time Estimate

- **Dependencies & CSRF:** 30 minutes
- **Rate Limiting:** 15 minutes
- **Session Timeout:** 15 minutes
- **Backup UI Integration:** 30 minutes
- **Testing:** 30 minutes
- **Deployment & Verification:** 20 minutes

**Total:** ~2.5 hours

---

## Known Limitations

1. **CSRF cookie dependency:** Relies on meta tag in HTML template
2. **Memory-based rate limiting:** Resets on app restart (use Redis for persistent)
3. **SQLite backups:** Simple file copy (consider WAL mode for zero-downtime)
4. **No CSRF exemption list:** All state-changing endpoints require token

---

## Next Steps (Phase 2 & 3)

After Phase 1 completes:

**Phase 2:**
- Attachments system (URL first, then file upload)
- Comments/feedback per entity
- Search, sort, pagination

**Phase 3:**
- Markdown export packets
- iCalendar feed
- Comprehensive tests
- Full documentation

---

**This plan is immediately executable. Follow steps 1-5 in order, test, then deploy.**

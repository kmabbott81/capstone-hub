# Deployment Guide
**Capstone Hub v0.36.1 - Phase 1b**

## Quick Start

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/kmabbott81/capstone-hub.git
cd capstone-hub

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.sample .env
# Edit .env with your settings

# 5. Validate environment
python scripts/validate_env.py

# 6. Run application
python src/main.py
```

Access at: http://localhost:5000

---

### Railway Deployment

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and link project
railway login
railway link

# 3. Set environment variables
railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")
railway variables set ADMIN_PASSWORD_HASH=$(python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YourPassword'))")
railway variables set VIEWER_PASSWORD_HASH=$(python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('ViewerPassword'))")
railway variables set FLASK_ENV=production
railway variables set LOG_LEVEL=INFO
railway variables set ENABLE_DEBUG_ROUTES=0

# 4. Verify build
bash scripts/verify_build.sh

# 5. Deploy
railway up

# 6. Open deployment
railway open
```

---

## Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `SECRET_KEY` | ✅ Yes | Flask session encryption key | `secrets.token_hex(32)` |
| `ADMIN_PASSWORD_HASH` | ⚠️ Prod | Hashed admin password | `pbkdf2:sha256:...` |
| `ADMIN_PASSWORD` | ⚠️ Dev | Plain admin password (dev only) | `MySecurePass123!` |
| `VIEWER_PASSWORD_HASH` | ⚠️ Prod | Hashed viewer password | `pbkdf2:sha256:...` |
| `VIEWER_PASSWORD` | ⚠️ Dev | Plain viewer password (dev only) | `ViewerPass` |
| `FLASK_ENV` | No | Environment mode | `production` or `development` |
| `LOG_LEVEL` | No | Logging verbosity | `INFO` (default) |
| `DATABASE_URL` | No | Database connection | `sqlite:///src/database/app.db` |
| `ENABLE_DEBUG_ROUTES` | No | Debug endpoints (0=disabled) | `0` (must be 0 in prod) |

---

## Password Hashing

### Generate Hashed Password

```python
from werkzeug.security import generate_password_hash

# Generate hash
password = "YourSecurePassword123!"
hashed = generate_password_hash(password)
print(hashed)
# Output: pbkdf2:sha256:600000$...
```

```bash
# One-liner
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YourPassword'))"
```

### Production vs Development

**Production** (Railway, public deployment):
- Use `ADMIN_PASSWORD_HASH` and `VIEWER_PASSWORD_HASH`
- Never commit plain passwords to git
- Store hashes in Railway environment variables

**Development** (local machine):
- Use `ADMIN_PASSWORD` and `VIEWER_PASSWORD` (plain)
- Add `.env` to `.gitignore`
- Faster iteration without re-hashing

---

## Pre-Deployment Checklist

### 1. Validate Environment
```bash
python scripts/validate_env.py
```

**Expected output:**
```
✅ ENVIRONMENT READY
```

### 2. Verify Build
```bash
bash scripts/verify_build.sh
```

**Expected output:**
```
✅ BUILD VERIFICATION PASSED
```

### 3. Security Checks
- [ ] `ENABLE_DEBUG_ROUTES=0`
- [ ] `FLASK_ENV=production`
- [ ] Passwords are hashed (not plain)
- [ ] `SECRET_KEY` is unique (not default)
- [ ] `.env` is in `.gitignore`

### 4. Test Locally
```bash
# Start server
python src/main.py

# In another terminal
python scripts/verify_admin_guard.py
```

---

## Troubleshooting

### "Environment Not Ready"
**Problem:** `validate_env.py` shows missing variables

**Fix:**
```bash
cp .env.sample .env
# Edit .env with your values
```

### "Build Verification Failed"
**Problem:** `verify_build.sh` reports errors

**Fix:**
- Check test failures: `pytest -v`
- Check security audit: `python -m pip_audit`
- Check manifest: `python scripts/generate_route_manifest.py`

### Login Fails with Correct Password
**Problem:** Can't log in despite correct credentials

**Possible causes:**
1. Using `ADMIN_PASSWORD_HASH` but password is wrong
2. Hash was generated incorrectly
3. Environment variable not loaded

**Fix:**
```bash
# Verify env var is set
python -c "import os; print('ADMIN_PASSWORD_HASH' in os.environ)"

# Test hash directly
python -c "from werkzeug.security import check_password_hash; print(check_password_hash('YOUR_HASH', 'YOUR_PASSWORD'))"
```

### Railway Deployment Crashes
**Problem:** App won't start on Railway

**Common fixes:**
1. Check Railway logs: `railway logs --tail 100`
2. Verify all required env vars set
3. Ensure `FLASK_ENV=production`
4. Check `Procfile` or Railway start command

---

## Maintenance

### View Logs
```bash
# Local
ls logs/
tail -f logs/app.log
tail -f logs/error.log

# Railway
railway logs --tail 100
railway logs --follow
```

### Database Backup
```bash
# Via API (as admin)
curl -X POST -H "X-CSRFToken: $TOKEN" \
  https://your-app.railway.app/api/admin/backup

# Manual backup
cp src/database/app.db src/database/app.db.backup-$(date +%Y%m%d)
```

### Update Dependencies
```bash
pip list --outdated
pip install --upgrade package-name
pip freeze > requirements.txt

# Security audit
python -m pip_audit
```

---

## Support

- **Repository:** https://github.com/kmabbott81/capstone-hub
- **Documentation:** See `security/AUDIT_INDEX.md` for security evidence
- **Issues:** https://github.com/kmabbott81/capstone-hub/issues

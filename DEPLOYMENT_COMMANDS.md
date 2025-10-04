# Capstone Hub - Deployment Commands
## Staging → Production Release Pack

**Based on:** FINAL_PRE_PRODUCTION_REVIEW.md
**Platform:** Windows PowerShell + Python 3 + Railway CLI
**Version:** 2.0 - Separate Staging/Production Environments

---

## 🔑 Environment Separation

**IMPORTANT:** This deployment uses **separate Railway environments** for staging and production:

| Environment | Secret Key | Admin Password | URL |
|-------------|-----------|----------------|-----|
| **Staging** | Auto-generated | `HLStearns2025!` (fixed) | Saved to `.staging_url` |
| **Production** | **Different** auto-generated | **NEW** (you choose) | Saved to `.production_url` |

**Key Benefits:**
- ✅ Changes to staging don't affect production
- ✅ Different secrets prevent credential sharing
- ✅ Test thoroughly before promoting
- ✅ Rollback by switching environments

---

## 📋 Prerequisites

Verify you have everything installed:

```powershell
# Check Railway CLI
railway --version

# Check Python
python --version

# Check requests library
pip show requests
# If not installed: pip install requests

# Verify logged into Railway
railway whoami
# If not logged in: railway login
```

---

## 🚀 Complete Deployment Workflow

### Overview: Staging → Test → Promote → Verify

```
1. Deploy to Staging
2. Run Smoke Tests
3. Review Results
4. Promote to Production (if tests pass)
5. Verify Production
```

---

## 🚀 Deployment Steps

### Step 1: Deploy to Staging

```powershell
.\staging_deploy.ps1
```

**What it does:**
- ✓ Verifies Railway CLI login
- ✓ Generates fresh `SECRET_KEY` (32-byte hex)
- ✓ Sets environment variables:
  - `FLASK_ENV=production`
  - `SECRET_KEY=<generated>`
  - `PORT=5000`
  - `ADMIN_PASSWORD=HLStearns2025!` (staging default)
- ✓ Deploys to Railway staging
- ✓ Saves staging URL to `.staging_url`
- ✓ Opens staging URL in browser
- ✓ Auto-runs smoke test after 10 seconds

**Expected Output:**
```
========================================
Capstone Hub - Staging Deployment
========================================

[1/5] Verifying Railway CLI login...
✓ Railway CLI authenticated

[2/5] Generating fresh SECRET_KEY...
✓ Generated 32-byte hex key

[3/5] Setting staging environment variables...
✓ FLASK_ENV=production
✓ SECRET_KEY=<generated>
✓ PORT=5000
✓ ADMIN_PASSWORD=HLStearns2025! (staging default)

[4/5] Deploying to Railway staging...
This may take 2-3 minutes...
✓ Deployment successful

[5/5] Retrieving staging URL...
✓ Staging URL saved to .staging_url

========================================
STAGING DEPLOYMENT COMPLETE
========================================

Staging URL: https://your-app-staging.railway.app

NEXT STEPS:
1. Opening staging URL in browser...
2. Run smoke test: python smoke_staging.py
3. Review: staging_smoke_report.txt
4. If tests pass: .\promote_to_prod.ps1
```

---

### Step 2: Run Smoke Test

If the script didn't auto-run the smoke test, run manually:

```powershell
python smoke_staging.py
```

**Or test a specific URL:**

```powershell
python smoke_staging.py --url https://your-staging-url.railway.app
```

**What it tests:**

**Test #1: Viewer Access (No Login)**
- ✓ Homepage loads (200 OK)
- ✓ No "Add" buttons visible
- ✓ No admin badge visible
- ✓ Lock icon present
- ✓ Unauthorized POST returns 403

**Test #2: Admin Access (After Login)**
- ✓ Login with `HLStearns2025!`
- ✓ Session cookie received
- ✓ "Add" buttons visible (≥6 buttons)
- ✓ Create Business Process succeeds
- ✓ New process appears in list

**Test #3: XSS Protection**
- ✓ Create deliverable with `<script>alert(1)</script>`
- ✓ Verify HTML is escaped (renders as text)

**Test #4: Security Headers**
- ✓ X-Robots-Tag: noindex, nofollow
- ✓ X-Content-Type-Options: nosniff
- ✓ X-Frame-Options: DENY
- ✓ X-XSS-Protection: 1; mode=block
- ✓ Content-Security-Policy present
- ✓ Session cookies: Secure + HttpOnly + SameSite=Lax

**Expected Output:**
```
========================================
Capstone Hub - Staging Smoke Test
========================================
Base URL: https://your-app-staging.railway.app

=== Test #1: Viewer Access (No Login) ===
✓ Homepage loads
✓ No 'Add' buttons visible (viewer mode)
✓ No admin badge visible
✓ Lock icon present (for login)
✓ Unauthorized POST blocked

=== Test #2: Admin Access (After Login) ===
✓ Admin login successful
✓ Session cookie received
✓ 'Add' buttons visible (admin mode)
✓ Create Business Process
✓ New process appears in list

=== Test #3: XSS Protection ===
✓ XSS test deliverable creation
✓ XSS payload escaped

=== Test #4: Security Headers ===
✓ Header: X-Robots-Tag
✓ Header: X-Content-Type-Options
✓ Header: X-Frame-Options
✓ Header: X-XSS-Protection
✓ Header: Content-Security-Policy
✓ Header: Cache-Control
✓ Cookie 'session' - Secure flag
✓ Cookie 'session' - HttpOnly flag
✓ Cookie 'session' - SameSite flag

========================================
SMOKE TEST RESULTS
========================================
Total Tests: 21
Passed: 21
Failed: 0

✓ ALL TESTS PASSED - READY FOR PRODUCTION

Report written to: staging_smoke_report.txt
```

---

### Step 3: Review Report

```powershell
notepad staging_smoke_report.txt
```

**Look for:**
- ✅ `ALL TESTS PASSED - READY FOR PRODUCTION`
- ❌ `X TEST(S) FAILED - DO NOT PROMOTE`

**If tests fail:**
1. Review failures in report
2. Check browser console (F12) for errors
3. Check Railway logs: `railway logs`
4. Fix issues and re-deploy staging

---

### Step 4: Promote to Production

**⚠️ CRITICAL: Only run this if staging tests passed!**

```powershell
.\promote_to_prod.ps1
```

**What it does:**
- ✓ Verifies `staging_smoke_report.txt` contains "ALL TESTS PASSED"
- ✓ Creates/switches to **separate** production environment in Railway
- ✓ Prompts for **NEW** admin password (must be different from staging)
- ✓ Generates **NEW** `SECRET_KEY` (completely different from staging)
- ✓ Sets production environment variables (isolated from staging)
- ✓ Deploys to Railway production environment
- ✓ Saves production URL to `.production_url`
- ✓ Saves admin password to `.prod_admin_password.txt` (⚠️ SECURE THIS!)
- ✓ Prints comprehensive post-deployment checklist

**Environment Isolation:**
After promotion, you will have TWO separate Railway environments:
- **Staging Environment:** Uses `HLStearns2025!`, can test freely
- **Production Environment:** Uses YOUR new password, handles real users

Changes to staging **do not** affect production. Each environment has:
- Different `SECRET_KEY`
- Different `ADMIN_PASSWORD`
- Different database (isolated data)
- Different deployment history

**Interactive Prompt:**
```
[3/6] Setting production secrets...

⚠️  CRITICAL: Change admin password for production!
   Staging uses: HLStearns2025!
   Production needs a DIFFERENT password

Enter NEW admin password for production: ********
```

**Expected Output:**
```
========================================
Capstone Hub - Production Promotion
========================================

[1/6] Verifying staging tests...
✓ Staging tests passed

[2/6] Switching to production environment...
✓ Environment switched to production

[3/6] Setting production secrets...
✓ FLASK_ENV=production
✓ SECRET_KEY=<NEW-KEY> (different from staging)
✓ PORT=5000
✓ ADMIN_PASSWORD=<YOUR-PASSWORD>

⚠️  Admin password saved to: .prod_admin_password.txt

[4/6] Deploying to Railway production...
✓ Production deployment successful

[5/6] Retrieving production URL...
✓ Production URL saved to .production_url

========================================
PRODUCTION DEPLOYMENT COMPLETE
========================================

Production URL: https://your-app-production.railway.app
Admin Password: <see .prod_admin_password.txt>

[6/6] Post-deployment verification steps:

REQUIRED ACTIONS:

1. Run smoke test against production:
   python smoke_staging.py --url https://your-app-production.railway.app

2. Test admin login with NEW password

3. Add one test item to verify database works

4. Monitor production logs for 24 hours:
   railway logs
```

---

### Step 5: Verify Production

Run smoke test against production URL:

```powershell
python smoke_staging.py --url https://your-app-production.railway.app
```

**Manual verification:**
1. Open production URL in browser
2. Click lock icon 🔐
3. Enter **NEW** password (from `.prod_admin_password.txt`)
4. Verify admin badge 👑 appears
5. Click "Add Process"
6. Create test item
7. Refresh page
8. Verify item persists

---

## 📁 Generated Files

After running deployment scripts, you'll have:

```
.staging_url                    # Staging URL (auto-generated)
.production_url                 # Production URL (auto-generated)
.prod_admin_password.txt        # ⚠️ SECURE THIS FILE!
staging_smoke_report.txt        # Test results
```

**⚠️ Security Reminder:**
- Delete `.prod_admin_password.txt` after sharing password securely
- Do not commit `.staging_url` or `.production_url` to git
- Share admin password via secure channel (not email/Slack)

---

## 🔄 Re-running Tests

**Test staging again:**
```powershell
python smoke_staging.py
```

**Test production:**
```powershell
python smoke_staging.py --url https://your-production-url.railway.app
```

**Re-deploy staging without changing secrets:**
```powershell
railway up
```

**Re-deploy production:**
```powershell
railway environment production
railway up
```

---

## 🐛 Troubleshooting

### "Railway CLI not logged in"
```powershell
railway login
```

### "requests library not found"
```powershell
pip install requests
```

### "Staging tests failed"
Review `staging_smoke_report.txt` for specific failures, fix issues, re-deploy.

### "Could not retrieve staging/production URL"
```powershell
railway status
# Manually note URL and add to .staging_url or .production_url
```

### "Admin login fails in smoke test"
Check if password changed in Railway dashboard:
```powershell
railway variables list
```

### "XSS test fails"
Check browser console for CSP errors. Verify `escapeHTML()` is applied in all render functions.

### "Security headers missing"
Check `src/main.py` has `@app.after_request` decorator (lines 52-69).

---

## 📊 Success Criteria

**✅ Ready for Production if:**
- All 21 smoke tests pass on staging
- `staging_smoke_report.txt` shows "ALL TESTS PASSED"
- No console errors when browsing staging
- Admin login works with staging password
- Data persists after refresh

**❌ Do NOT promote if:**
- Any smoke test fails
- Console shows red errors
- Unauthorized POST returns 200 (should be 403)
- XSS payload executes (should be escaped)
- Security headers missing

---

## 🎯 Quick Reference - Complete Workflow

### The Exact Sequence to Run:

```powershell
# Navigate to project
cd C:\Users\kylem\capstone-hub-complete-dev-package

# STEP 1: Deploy to Staging
.\staging_deploy.ps1

# STEP 2: Run Smoke Tests (auto-runs, but can run manually)
python .\smoke_staging.py

# STEP 3: Review Test Results
notepad staging_smoke_report.txt
# Look for: "ALL TESTS PASSED - READY FOR PRODUCTION"

# STEP 4: Promote to Production (ONLY if tests passed)
.\promote_to_prod.ps1
# Script will prompt for NEW admin password

# STEP 5: Verify Production
python .\smoke_staging.py --url https://your-production-url.railway.app
```

### Environment Management:

```powershell
# Switch between environments
railway environment staging          # Work with staging
railway environment production       # Work with production

# View environment variables
railway variables --service capstone-hub

# Monitor logs
railway logs --service capstone-hub

# Check deployment status
railway status
```

### Rollback Procedures:

```powershell
# Rollback production to previous deployment
railway environment production
railway rollback <deployment-id>

# Or switch back to staging temporarily
railway environment staging
# Production remains untouched
```

---

## 📞 Support

**If deployment fails:**
1. Check Railway dashboard for error logs
2. Review `staging_smoke_report.txt` for test failures
3. Check `FINAL_PRE_PRODUCTION_REVIEW.md` for troubleshooting
4. Verify all prerequisites installed

**Common issues:**
- Railway CLI not logged in → Run `railway login`
- Python not found → Install Python 3.8+
- Smoke test fails → Review report, fix issues, re-deploy
- Admin password not working → Check Railway variables

---

**Document Version:** 1.0.0
**Last Updated:** October 3, 2025
**Based on:** FINAL_PRE_PRODUCTION_REVIEW.md
**Platform:** Windows PowerShell + Railway CLI

# Capstone Hub - Operations Checklist

**Version:** v0.36.1
**Last Updated:** 2025-10-04
**Environment:** Railway Production

---

## Pre-Deployment Checklist

### 1. Build Verification
```bash
# Run complete build verification suite
bash scripts/verify_build.sh

# Expected output:
# ✅ Tests passed
# ✅ No vulnerabilities in dependencies
# ✅ Route manifest generated
# ✅ All critical files present
```

### 2. Environment Validation
```bash
# Validate all required environment variables
python scripts/validate_env.py

# Expected output:
# [OK] ENVIRONMENT READY
```

**Critical Environment Variables:**
- `SECRET_KEY` - Flask session encryption (REQUIRED)
- `ADMIN_PASSWORD` or `ADMIN_PASSWORD_HASH` - Admin authentication (REQUIRED)
- `VIEWER_PASSWORD` or `VIEWER_PASSWORD_HASH` - Viewer authentication (optional, defaults to "CapstoneView")
- `DATABASE_URL` - Database connection (optional, defaults to SQLite)
- `LOG_LEVEL` - Logging verbosity (INFO for production)
- `FLASK_ENV` - Must be "production"
- `ENABLE_DEBUG_ROUTES` - Must be "0" or unset

**Set via Railway:**
```bash
railway variables set SECRET_KEY="your-secret-key"
railway variables set ADMIN_PASSWORD_HASH="pbkdf2:sha256:..."
railway variables set FLASK_ENV="production"
railway variables set LOG_LEVEL="INFO"
```

### 3. Security Proofs
```bash
# Verify admin guard protection
python scripts/verify_admin_guard.py

# Verify rate limiting
bash scripts/prove_rate_limit.sh

# Check output files:
cat security/build_snapshot/admin_guard_proof.txt
cat security/build_snapshot/rate_limit_proof.txt
```

### 4. Pre-Deployment Smoke Test
```bash
# Quick smoke test alias
make smoke
```

---

## Deployment Process

### Option 1: Railway CLI Deployment
```bash
# Link to project (first time only)
railway link

# Deploy
railway up

# Monitor logs
railway logs

# Check status
railway status
```

### Option 2: Git Push Deployment
```bash
# Railway auto-deploys from main branch
git push origin main
```

---

## Post-Deployment Verification

### 1. Health Check
```bash
# Check application is responding
curl https://your-app.up.railway.app/

# Check authentication endpoint
curl https://your-app.up.railway.app/api/auth/status
```

### 2. Verify Security Headers
```bash
curl -I https://your-app.up.railway.app/ | grep -E "(X-Frame-Options|Content-Security-Policy|X-Content-Type-Options)"

# Expected headers:
# X-Frame-Options: DENY
# Content-Security-Policy: default-src 'self'; ...
# X-Content-Type-Options: nosniff
```

### 3. Test Authentication Flow
- Open app in browser
- Verify login page loads
- Test admin login
- Test viewer login
- Verify role permissions work correctly

---

## Backup and Restore

### Database Backup (SQLite)
```bash
# Local backup
cp src/database/app.db backups/app.db.$(date +%Y%m%d_%H%M%S)

# Railway backup (if using Railway volumes)
railway run cp /app/src/database/app.db /backups/
```

### Environment Variables Backup
```bash
# Export current variables
railway variables > env_backup_$(date +%Y%m%d).txt

# Restore variables
cat env_backup_20251004.txt | while read line; do
    railway variables set "$line"
done
```

### Code Backup
```bash
# All code is in git - verify latest tag
git tag -l "v*" | sort -V | tail -1

# Create release archive
git archive --format=tar.gz --prefix=capstone-hub/ v0.36.1 > capstone-hub-v0.36.1.tar.gz
```

### 14-Day Backup Verification

Regular verification ensures backups are current and recoverable.

**Daily Backup Check (Automated):**
```bash
# Verify backup timestamp (should be within 24 hours)
ls -lh backups/*.db | tail -5

# Check backup age
find backups/ -name "*.db" -mtime -1 | wc -l
# Should return at least 1
```

**Weekly Backup Integrity Check:**
```bash
# Verify backup file is not corrupted
sqlite3 backups/app.db.20251004_120000 "PRAGMA integrity_check;"
# Expected output: ok

# Check backup size (should not be 0)
du -h backups/*.db | tail -5
```

**Automated Cleanup (14-Day Retention):**

Create optional cleanup cron job:
```bash
# Add to crontab for daily cleanup at 2 AM
# crontab -e
0 2 * * * python /app/scripts/cleanup_backups.py --retain 14
```

**Railway Backup Cron:**
```bash
# Schedule via Railway cron (if available)
railway cron add "0 2 * * *" "python scripts/cleanup_backups.py --retain 14"
```

**Manual Cleanup Command:**
```bash
# Clean backups older than 14 days
python scripts/cleanup_backups.py --retain 14

# Dry run to see what would be deleted
python scripts/cleanup_backups.py --retain 14 --dry-run
```

**Backup Verification Report:**
```bash
# Generate backup status report
echo "=== Backup Status Report ==="
echo "Backup directory: backups/"
echo "Total backups: $(ls -1 backups/*.db 2>/dev/null | wc -l)"
echo "Latest backup: $(ls -t backups/*.db 2>/dev/null | head -1 | xargs basename)"
echo "Latest timestamp: $(ls -t backups/*.db 2>/dev/null | head -1 | xargs stat -c %y 2>/dev/null || stat -f %Sm)"
echo "Total size: $(du -sh backups/ 2>/dev/null | cut -f1)"
echo ""
echo "Backups older than 14 days:"
find backups/ -name "*.db" -mtime +14 | wc -l
```

**Recovery Test Procedure (Monthly):**
```bash
# 1. Backup current database
cp src/database/app.db src/database/app.db.current

# 2. Restore from backup
cp backups/app.db.20251004_120000 src/database/app.db.test

# 3. Verify restored database
sqlite3 src/database/app.db.test "SELECT COUNT(*) FROM deliverables;"

# 4. Restore original
mv src/database/app.db.current src/database/app.db
rm src/database/app.db.test
```

---

## Log Management

### Log Locations

**Railway (Production):**
```bash
# View live logs
railway logs

# View specific timeframe
railway logs --since 1h
railway logs --since 2025-10-04
```

**Local Development:**
- `logs/app.log` - Application logs (10MB × 5 backups)
- `logs/error.log` - Error logs only (10MB × 5 backups)
- `logs/csp_reports.log` - CSP violation reports

### Log Rotation
- Automatic rotation at 10MB per file
- 5 backup files retained
- Older logs automatically deleted

### Log Monitoring
```bash
# Watch logs in real-time (local)
tail -f logs/app.log

# Filter for errors
grep ERROR logs/app.log

# Check for security issues
grep -i "security\|auth\|403\|401" logs/app.log
```

---

## Incident Response

### Critical Security Alert Process

1. **Identify Incident**
   - Monitor logs for anomalies
   - Check error rates in Railway dashboard
   - Review CSP violation reports

2. **Immediate Actions**
   ```bash
   # Stop the service if needed
   railway down

   # Check recent deployments
   git log --oneline -10

   # Review recent changes
   git diff HEAD~1
   ```

3. **Investigate**
   - Check `logs/error.log` for stack traces
   - Review authentication logs for unauthorized access
   - Check rate limit violations
   - Review CSP reports

4. **Mitigate**
   ```bash
   # Rollback to previous version
   git checkout v0.36.0
   railway up

   # Or redeploy current version
   railway up --force

   # Reset admin password
   railway variables set ADMIN_PASSWORD_HASH="new-hash"
   railway restart
   ```

5. **Document**
   - Record incident details in `security/INCIDENTS.md`
   - Update runbook if new procedures discovered
   - Create post-mortem if significant

---

## Rollback Procedures

### Quick Rollback
```bash
# Revert to previous tagged version
git checkout v0.36.0
railway up

# Or rollback in Railway UI
railway rollback
```

### Rollback with Verification
```bash
# Checkout previous version
git checkout v0.36.0

# Run verification
bash scripts/verify_build.sh
python scripts/validate_env.py

# Deploy
railway up

# Verify deployment
curl https://your-app.up.railway.app/
```

---

## Monitoring and Alerts

### Key Metrics to Monitor

**Application Health:**
- Response time (p50, p95, p99)
- Error rate (4xx, 5xx)
- Memory usage
- CPU usage

**Security Metrics:**
- Failed login attempts
- Rate limit violations
- CSP violations
- Authentication errors (401, 403)

**Business Metrics:**
- Active sessions
- API endpoint usage
- Data export requests

### Railway Monitoring
- Dashboard: https://railway.app/project/your-project
- Metrics tab shows CPU, memory, network
- Logs tab for real-time log viewing
- Deployments tab for history

---

## Maintenance Tasks

### Weekly
- [ ] Review error logs
- [ ] Check CSP violation reports
- [ ] Verify backup integrity
- [ ] Review Railway resource usage

### Monthly
- [ ] Run full security audit: `bash scripts/collect_audit_evidence.ps1`
- [ ] Update dependencies: `pip list --outdated`
- [ ] Review and rotate logs if needed
- [ ] Test backup restore procedure

### Quarterly
- [ ] Security dependency audit: `python -m pip_audit`
- [ ] Password rotation (admin/viewer)
- [ ] Review and update documentation
- [ ] Disaster recovery drill

---

## Emergency Contacts

**Development Team:**
- Primary: [Your Name/Email]
- Secondary: [Backup Contact]

**Railway Support:**
- Dashboard: https://railway.app/support
- Community: https://discord.gg/railway

**Security Issues:**
- Report via: [SECURITY.md](../SECURITY.md)
- Critical issues: [Emergency Contact]

---

## Common Issues and Solutions

### Issue: Application Won't Start
```bash
# Check logs for errors
railway logs | grep ERROR

# Verify environment variables
railway variables

# Restart service
railway restart
```

### Issue: Authentication Failing
```bash
# Verify admin password is set
railway variables | grep ADMIN_PASSWORD

# Test password hash generation
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YourPassword'))"

# Update password
railway variables set ADMIN_PASSWORD_HASH="new-hash"
railway restart
```

### Issue: High Memory Usage
```bash
# Check current usage
railway status

# Review log file sizes
railway run ls -lh logs/

# Restart to clear memory
railway restart
```

### Issue: CSP Violations
```bash
# Check violation reports
railway run cat logs/csp_reports.log

# Common causes:
# - Third-party scripts not in allowlist
# - Inline styles without 'unsafe-inline'
# - External images/fonts

# Update CSP in src/main.py if needed
```

---

## Quick Reference Commands

```bash
# Deploy
railway up

# View logs
railway logs

# Environment variables
railway variables
railway variables set KEY=value

# Service control
railway restart
railway down

# Status
railway status

# Local development
python src/main.py

# Run tests
pytest -v

# Build verification
bash scripts/verify_build.sh

# Smoke test
make smoke
```

---

## Documentation References

- [DEPLOYMENT.md](../DEPLOYMENT.md) - Detailed deployment guide
- [SECURITY.md](../SECURITY.md) - Security policy and disclosure
- [CHANGELOG.md](../CHANGELOG.md) - Version history
- [README.md](../README.md) - Project overview
- [security/AUDIT_INDEX.md](../security/AUDIT_INDEX.md) - Security audit documentation

---

**Document Version:** 1.0
**Maintained By:** Development Team
**Next Review:** 2025-11-04

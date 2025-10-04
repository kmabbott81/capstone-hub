# Change Control Procedures

**Project:** Capstone Hub
**Version:** v0.36.1
**Last Updated:** 2025-10-04

---

## Overview

This document defines the change control procedures for Capstone Hub, including version tagging, deployment, and rollback processes.

---

## Version Numbering Scheme

### Format: `vMAJOR.MINOR.PATCH[-SUFFIX]`

- **MAJOR**: Breaking changes or major feature releases (e.g., v1.0.0, v2.0.0)
- **MINOR**: New features, enhancements, backwards-compatible (e.g., v0.36.0, v0.37.0)
- **PATCH**: Bug fixes, security patches, minor updates (e.g., v0.36.1, v0.36.2)
- **SUFFIX**: Optional descriptor (e.g., `-phase1b`, `-sealed`, `-p1b-maint`)

### Current Version History
```
v0.36.0              - Phase 1 Security implementation
v0.36.0-audit        - Phase 1 Security audit
v0.36.0-audit-remediated - Audit gap remediation
v0.36.1-phase1b      - Phase 1b pre-production hardening
v0.36.1-sealed       - Phase 1b smoke test and seal
v0.36.1-p1b-maint    - Phase 1b maintenance patch (current)
```

---

## Change Request Process

### 1. Planning Phase

**Before making changes:**
```bash
# Check current version and branch
git status
git log --oneline -5
git tag -l "v*" | tail -5

# Create feature branch
git checkout -b feature/your-feature-name
```

### 2. Development Phase

**During development:**
- Make incremental commits with clear messages
- Run tests frequently: `pytest -v`
- Keep CHANGELOG.md updated with changes

```bash
# Regular commits
git add <files>
git commit -m "Clear description of changes"

# Run verification before merge
make smoke
```

### 3. Pre-Merge Verification

**Before merging to main:**
```bash
# Run complete verification suite
bash scripts/verify_build.sh
python scripts/validate_env.py
make smoke

# Review changes
git diff main..feature/your-feature-name

# Check for security issues
python -m pip_audit
```

### 4. Merge and Tag

**Merge to main branch:**
```bash
# Switch to main
git checkout main
git pull origin main

# Merge feature branch
git merge feature/your-feature-name

# Update CHANGELOG.md with version number and date
nano CHANGELOG.md
```

**Create version tag:**
```bash
# For minor version bump (new features)
git tag -a v0.37.0 -m "Brief description of changes"

# For patch version bump (bug fixes)
git tag -a v0.36.2 -m "Brief description of fixes"

# For maintenance patches
git tag -a v0.36.1-p2 -m "Maintenance patch description"
```

### 5. Push to Remote

```bash
# Push commits and tags
git push origin main
git push origin --tags

# Or push with follow-tags
git push --follow-tags
```

---

## Deployment Process

### Railway Automatic Deployment

Railway automatically deploys when changes are pushed to `main`:

```bash
# Push triggers automatic deployment
git push origin main

# Monitor deployment
railway logs
railway status
```

### Manual Railway Deployment

For manual control:

```bash
# Deploy specific version
git checkout v0.36.1-sealed
railway up

# Monitor
railway logs --tail

# Verify deployment
curl https://your-app.up.railway.app/
```

### Pre-Deployment Checklist

- [ ] All tests pass: `pytest -v`
- [ ] Build verification passes: `bash scripts/verify_build.sh`
- [ ] Environment validated: `python scripts/validate_env.py`
- [ ] Security audit clean: `python -m pip_audit`
- [ ] CHANGELOG.md updated
- [ ] Version tag created
- [ ] README.md version badge updated

---

## Rollback Procedures

### Quick Rollback (Emergency)

**Immediate rollback to previous version:**

```bash
# Option 1: Railway rollback command
railway rollback

# Option 2: Checkout and redeploy previous tag
git checkout v0.36.0-audit-remediated
railway up

# Verify rollback
curl https://your-app.up.railway.app/
railway logs | head -20
```

### Verified Rollback (Recommended)

**Rollback with full verification:**

```bash
# 1. Identify target version
git tag -l "v*" | tail -10

# 2. Checkout target version
git checkout v0.36.0-audit-remediated

# 3. Run verification
bash scripts/verify_build.sh
python scripts/validate_env.py

# 4. Deploy
railway up

# 5. Monitor and verify
railway logs --tail
curl -I https://your-app.up.railway.app/

# 6. Test critical functionality
python scripts/verify_admin_guard.py
bash scripts/prove_rate_limit.sh
```

### Post-Rollback Actions

After rollback:
1. Document incident in `security/INCIDENTS.md`
2. Create GitHub issue for root cause analysis
3. Update CHANGELOG.md with rollback entry
4. Notify stakeholders
5. Plan remediation

---

## Hotfix Process

For critical security issues or production bugs:

### 1. Create Hotfix Branch

```bash
# From production tag
git checkout v0.36.1-sealed
git checkout -b hotfix/critical-issue-name
```

### 2. Implement Fix

```bash
# Make minimal changes to fix issue
# Update tests
# Update CHANGELOG.md

git add <files>
git commit -m "Hotfix: brief description of fix"
```

### 3. Test Hotfix

```bash
# Run verification
pytest -v
bash scripts/verify_build.sh
make smoke
```

### 4. Deploy Hotfix

```bash
# Merge to main
git checkout main
git merge hotfix/critical-issue-name

# Create patch tag
git tag -a v0.36.1-p1 -m "Hotfix: description"

# Push
git push --follow-tags

# Verify deployment
railway logs
```

---

## Environment Variable Changes

### Adding New Environment Variable

1. **Update `.env.sample`** with new variable and documentation
2. **Update `scripts/validate_env.py`** to check for new variable
3. **Update `DEPLOYMENT.md`** with variable description
4. **Update `docs/OPS_CHECKLIST.md`** if variable affects operations

```bash
# Set in Railway
railway variables set NEW_VARIABLE="value"

# Restart service
railway restart

# Verify
railway variables | grep NEW_VARIABLE
```

### Rotating Secrets

```bash
# Generate new secret
python -c "import secrets; print(secrets.token_hex(32))"

# Update in Railway
railway variables set SECRET_KEY="new-value"

# Restart (triggers session invalidation)
railway restart

# Verify in logs
railway logs | grep "Logging configured"
```

---

## Database Schema Changes

### Safe Schema Migration

```bash
# 1. Backup current database
railway run python scripts/backup_db.py

# 2. Create migration script
# Add to src/migrations/

# 3. Test locally
python scripts/migrate_db.py --dry-run

# 4. Apply migration
python scripts/migrate_db.py --apply

# 5. Verify
python scripts/verify_schema.py
```

### Rollback Database Migration

```bash
# Restore from backup
railway run python scripts/restore_db.py --backup backups/db_20251004.db

# Or revert migration
python scripts/migrate_db.py --rollback
```

---

## Emergency Procedures

### Complete Service Shutdown

```bash
# Stop Railway service
railway down

# Or scale to zero
railway scale --replicas 0
```

### Emergency Password Reset

```bash
# Generate new admin password hash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('NewEmergencyPassword'))"

# Set in Railway
railway variables set ADMIN_PASSWORD_HASH="pbkdf2:sha256:..."

# Restart
railway restart
```

### Clear All Sessions

```bash
# Generate new SECRET_KEY (invalidates all sessions)
python -c "import secrets; print(secrets.token_hex(32))"

railway variables set SECRET_KEY="new-key"
railway restart
```

---

## Verification Commands Reference

### Pre-Deployment Verification
```bash
# Complete smoke test
make smoke

# Individual checks
bash scripts/verify_build.sh
python scripts/validate_env.py
python scripts/verify_admin_guard.py
bash scripts/prove_rate_limit.sh
python scripts/verify_headers.py
```

### Post-Deployment Verification
```bash
# Check deployment status
railway status

# View recent logs
railway logs --since 5m

# Test endpoints
curl https://your-app.up.railway.app/
curl https://your-app.up.railway.app/api/auth/status

# Verify security headers
python scripts/verify_headers.py
```

### Health Checks
```bash
# Application health
curl -f https://your-app.up.railway.app/ || echo "FAILED"

# Authentication health
curl -f https://your-app.up.railway.app/api/auth/status || echo "FAILED"

# Database health
railway run python -c "from src.models.database import db; print('OK')"
```

---

## Git Tag Management

### List All Tags
```bash
# Show all tags
git tag -l

# Show version tags only
git tag -l "v*"

# Show with dates
git tag -l "v*" --format="%(refname:short) %(creatordate:short)"
```

### Delete Tag (If Needed)
```bash
# Delete local tag
git tag -d v0.36.1-wrong

# Delete remote tag
git push origin :refs/tags/v0.36.1-wrong
```

### Tag Inspection
```bash
# Show tag details
git show v0.36.1-sealed

# Show tag message
git tag -l -n9 v0.36.1-sealed
```

---

## Release Checklist Template

Use this checklist for every release:

```markdown
## Release: v0.XX.Y

### Pre-Release
- [ ] All tests passing
- [ ] Security audit clean
- [ ] CHANGELOG.md updated
- [ ] README.md version badge updated
- [ ] Environment variables documented
- [ ] Smoke test passed

### Release
- [ ] Feature branch merged to main
- [ ] Version tag created
- [ ] Tags pushed to remote
- [ ] Railway deployment successful

### Post-Release
- [ ] Application responding
- [ ] Security headers verified
- [ ] Authentication working
- [ ] Admin/viewer roles functional
- [ ] Logs clean (no errors)
- [ ] Backup created
- [ ] Team notified

### Documentation
- [ ] CHANGELOG.md complete
- [ ] Release notes written
- [ ] Known issues documented
- [ ] Migration guide (if needed)
```

---

## Audit Trail

All changes must maintain an audit trail:

1. **Git commits** - Descriptive commit messages
2. **CHANGELOG.md** - User-facing change summary
3. **Git tags** - Version milestones
4. **Railway deployment logs** - Production deployment record
5. **security/build_snapshot/** - Verification artifacts

---

## Contact Information

**Change Control Authority:**
- Development Team Lead: [Your Name/Email]
- Security Lead: security@hlstearns.local
- Operations Contact: [Ops Email]

**Emergency Contact:**
- [Phone Number]

---

## Revision History

| Version | Date       | Changes                               | Author      |
| ------- | ---------- | ------------------------------------- | ----------- |
| 1.0     | 2025-10-04 | Initial change control procedures     | Dev Team    |

---

**Last Review Date:** 2025-10-04
**Next Review Due:** 2025-11-04
**Document Owner:** Development Team Lead

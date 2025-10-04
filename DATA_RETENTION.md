# Data Retention Policy

**Project:** Capstone Hub
**Version:** v0.36.2
**Effective Date:** 2025-10-04
**Last Review:** 2025-10-04
**Next Review Due:** 2026-01-04

---

## Overview

This document describes the data retention, backup, and deletion policies for Capstone Hub. Our approach prioritizes privacy, security, and regulatory compliance while maintaining operational integrity for academic capstone project management.

---

## Data Categories

### 1. Application Data (Primary Database)

**Location:** `src/database/app.db` (SQLite)

**Categories:**
- **Deliverables**: Project deliverables, descriptions, status, dates
- **Business Processes**: Workflow documentation and process descriptions
- **AI Technologies**: Catalog of AI tools and technologies
- **Software Tools**: Development tools and integrations
- **Research Items**: Research findings, references, citations
- **Integrations**: External service configurations (no credentials stored)

**Personal Identifiable Information (PII):**
- ❌ No names, emails, or contact information stored
- ❌ No IP addresses stored in application database
- ❌ No demographic data collected

**Retention Duration:**
- **Active Projects**: Indefinite (until project completion + 1 year)
- **Completed Projects**: 2 years post-completion
- **Archived Projects**: 5 years for academic record purposes

**Deletion Process:**
```bash
# Manual deletion via admin interface
# Or bulk deletion via script
python scripts/purge_old_data.py --older-than 5y --dry-run
python scripts/purge_old_data.py --older-than 5y --confirm
```

---

### 2. Session Data

**Location:** Server-side session storage (filesystem)

**Categories:**
- Session ID (cryptographically secure random token)
- User role (admin/viewer)
- Authentication status
- Last activity timestamp

**PII Status:**
- ❌ No usernames stored in session
- ❌ No passwords stored in session
- ✅ Session tokens only (non-reversible)

**Retention Duration:**
- **Active Sessions**: 30 minutes of inactivity
- **Expired Sessions**: Automatically purged on expiration

**Automatic Cleanup:**
- Flask session management handles automatic expiration
- No manual intervention required

---

### 3. Authentication Data

**Location:** Environment variables only (never persisted to disk)

**Categories:**
- Admin password hash (PBKDF2-SHA256)
- Viewer password hash (PBKDF2-SHA256)
- SECRET_KEY for session encryption

**PII Status:**
- ❌ No plain-text passwords stored
- ✅ Hashes only (non-reversible)

**Retention Duration:**
- Indefinite (until manually rotated)
- Recommended rotation: Every 90 days

**Deletion Process:**
```bash
# Rotate admin password
railway variables set ADMIN_PASSWORD_HASH="new-hash"

# Clear all sessions (via SECRET_KEY rotation)
railway variables set SECRET_KEY="new-key"
railway restart
```

---

### 4. Log Data

**Location:** `logs/` directory

**Categories:**

#### Application Logs (`logs/app.log`)
- HTTP request methods and paths (no query parameters)
- Response status codes
- Application startup/shutdown events
- Feature usage patterns
- Configuration changes

**Sensitive Data Handling:**
- ✅ Passwords automatically redacted via `SensitiveDataFilter`
- ✅ Tokens automatically redacted
- ✅ API keys automatically redacted
- ✅ Secrets automatically redacted

#### Error Logs (`logs/error.log`)
- Exception stack traces (sanitized)
- Error timestamps
- Affected endpoints (no parameters)

#### CSP Violation Reports (`logs/csp_reports.log`)
- Violated CSP directive
- Blocked resource URL
- Page URL where violation occurred

**PII Status:**
- ❌ No IP addresses logged in application logs
- ❌ No user identifiers logged
- ❌ No session IDs logged
- ✅ Railway infrastructure logs may contain IP addresses (see Railway section)

**Retention Duration:**
- **Active Logs**: 10MB per file (5 backups = 50MB total)
- **Automatic Rotation**: When log file reaches 10MB
- **Retention Period**: Approximately 30-90 days depending on activity
- **Manual Retention**: Older logs automatically deleted by rotation

**Deletion Process:**
```bash
# Manual log cleanup
rm logs/app.log.*
rm logs/error.log.*
rm logs/csp_reports.log.*

# Logs will be recreated automatically
```

---

### 5. Backup Data

**Location:** `backups/` directory (local) or Railway volumes (production)

**Categories:**
- Complete database snapshots
- Configuration backups (env vars, no secrets)
- Verification artifacts (test results)

**PII Status:**
- ❌ No PII in database backups (per section 1)
- ❌ No credentials in configuration backups

**Retention Duration:**
- **Active Backups**: 14 days (automated cleanup)
- **Monthly Snapshots**: 1 year (manual archive)
- **Annual Archives**: 5 years (compressed, encrypted)

**Encryption:**
- **At Rest**: SQLite database files (filesystem-level encryption via Railway)
- **In Transit**: Not applicable (local backups only)
- **Archive Encryption**: Use GPG for long-term archives

**Deletion Process:**
```bash
# Automated cleanup (14-day retention)
python scripts/cleanup_backups.py --retain 14

# Manual deletion of specific backup
rm backups/app.db.20251004_120000

# Secure deletion (overwrite)
shred -u backups/app.db.20251004_120000  # Linux
sdelete backups/app.db.20251004_120000   # Windows
```

---

### 6. Railway Infrastructure Logs

**Location:** Railway platform (external)

**Categories:**
- HTTP access logs (IP addresses, user agents)
- Deployment logs
- System metrics (CPU, memory, network)

**PII Status:**
- ✅ Contains IP addresses (Railway managed)
- ✅ Contains user agents (Railway managed)

**Retention Duration:**
- Per Railway's data retention policy (typically 30-90 days)
- Not under direct control of application

**Access:**
```bash
# View Railway logs
railway logs

# Export logs for audit
railway logs --since 24h > audit_logs_$(date +%Y%m%d).txt
```

**Deletion Process:**
- Managed by Railway (automatic purge per their policy)
- No manual deletion available

---

### 7. CI/CD Artifacts

**Location:** GitHub Actions (external)

**Categories:**
- Test results
- Security audit reports
- Build verification artifacts
- Route manifests

**PII Status:**
- ❌ No PII in CI/CD artifacts

**Retention Duration:**
- **Test Results**: 7 days (GitHub Actions default)
- **Security Audits**: 30 days
- **Build Artifacts**: 90 days

**Deletion Process:**
- Automatic per GitHub Actions retention policies
- Can be manually deleted via GitHub Actions UI

---

## Data Processing Legal Basis

**Academic Use Context:**
- **Purpose**: MBA Capstone project management and demonstration
- **Legal Basis**: Legitimate educational interest
- **Scope**: Single-user or small team academic use
- **Geographic Scope**: United States (Railway hosting)

**Not Applicable:**
- GDPR (no EU data subjects)
- CCPA (no California consumer data)
- HIPAA (no health information)
- FERPA (no student records beyond project artifacts)

**Note:** If deploying for broader institutional use, consult university counsel regarding applicability of education records regulations.

---

## Data Minimization Principles

### What We Don't Collect
- ❌ User names or email addresses
- ❌ IP addresses (except Railway infrastructure logs)
- ❌ Geolocation data
- ❌ Device fingerprints
- ❌ Cookies (except session cookie)
- ❌ Analytics or tracking data
- ❌ Third-party advertising data
- ❌ Social media integrations

### What We Minimize
- ✅ Session data (30-minute expiration)
- ✅ Logs (automatic rotation)
- ✅ Backups (14-day retention)
- ✅ Error traces (sanitized, no PII)

---

## Data Subject Rights

### Right to Access
Users can request export of their project data:
```bash
# Export all deliverables to JSON
curl https://your-app.up.railway.app/api/deliverables/export \
  -H "Authorization: Bearer <token>" \
  -o deliverables_export.json
```

### Right to Deletion
Contact: privacy@hlstearns.local

**Process:**
1. Email privacy contact with deletion request
2. Specify data category to delete (deliverables, research items, etc.)
3. Admin will execute deletion within 30 days
4. Confirmation email sent upon completion

**Manual Deletion Commands:**
```bash
# Delete specific deliverable
curl -X DELETE https://your-app.up.railway.app/api/deliverables/<id> \
  -H "X-CSRFToken: <token>"

# Bulk deletion via admin interface
# Or database-level deletion:
sqlite3 src/database/app.db "DELETE FROM deliverables WHERE id = <id>;"
```

### Right to Rectification
Contact: privacy@hlstearns.local

Users can request correction of inaccurate data. Admin will update records within 14 days.

### Right to Portability
All data is exportable via API endpoints in JSON format. See [API documentation](docs/API.md) for export endpoints.

---

## Data Security During Retention

### Encryption
- **At Rest**:
  - SQLite database files protected by filesystem permissions (600)
  - Railway volume encryption (AES-256)
  - Long-term archives encrypted with GPG

- **In Transit**:
  - HTTPS/TLS 1.2+ for all web traffic
  - Railway platform encryption for internal traffic

### Access Control
- **Database**: Read/write access requires admin authentication
- **Logs**: Read access requires Railway CLI authentication or SSH access
- **Backups**: Restricted filesystem permissions (chmod 600)

### Audit Logging
- Admin actions logged to `logs/app.log`
- Failed authentication attempts logged
- Rate limit violations logged
- Security header violations logged

---

## Data Breach Response

### Detection
- Monitor `logs/error.log` for anomalies
- Review failed authentication attempts
- Check rate limit violation patterns
- Review CSP violation reports

### Response Plan
1. **Immediate Actions** (within 1 hour):
   - Isolate affected system: `railway down`
   - Rotate all credentials
   - Clear all sessions

2. **Investigation** (within 24 hours):
   - Review logs for breach timeline
   - Identify affected data categories
   - Assess PII exposure risk

3. **Notification** (within 72 hours):
   - Contact: security@hlstearns.local
   - Document incident in `security/INCIDENTS.md`
   - Notify affected parties if PII compromised

4. **Remediation**:
   - Deploy security patches
   - Update access controls
   - Review and update security policies

See [SECURITY.md](SECURITY.md) for complete incident response procedures.

---

## Purge Schedule

### Automated Purges
| Data Category | Frequency | Retention | Automation |
|---------------|-----------|-----------|------------|
| Expired Sessions | On expiration | 30 minutes | Flask automatic |
| Rotated Logs | On 10MB | 5 backups | Python logging |
| Old Backups | Daily | 14 days | Cron script |

### Manual Purges (Annual Review)
| Data Category | Frequency | Retention | Process |
|---------------|-----------|-----------|---------|
| Completed Projects | Annually | 2 years | Admin review + deletion |
| Archived Projects | Annually | 5 years | Admin review + deletion |
| Long-term Backups | Annually | 1 year | Archive cleanup |
| CI/CD Artifacts | Quarterly | 90 days | GitHub cleanup |

### Purge Verification
```bash
# Generate data retention report
python scripts/generate_retention_report.py

# Output:
# - Total records by category
# - Oldest record dates
# - Records eligible for purge
# - Storage utilization
```

---

## Third-Party Data Processors

### Railway (Infrastructure Provider)
- **Data Processed**: HTTP logs, metrics, deployment artifacts
- **Retention**: Per Railway policy (~30-90 days)
- **Location**: United States
- **Privacy Policy**: https://railway.app/legal/privacy

### GitHub (Code Repository & CI/CD)
- **Data Processed**: Source code, test results, artifacts
- **Retention**: Indefinite (code), 7-90 days (artifacts)
- **Location**: United States
- **Privacy Policy**: https://docs.github.com/en/site-policy/privacy-policies

### CDN Providers (Bootstrap, Font CDN)
- **Data Processed**: Asset requests (IP, user agent)
- **Retention**: Per CDN policy
- **Location**: Global CDN network
- **Privacy Policy**: See respective CDN providers

**Note:** No PII is transmitted to third-party processors beyond infrastructure-level IP addresses.

---

## Compliance Monitoring

### Quarterly Review
- [ ] Review log retention and rotation
- [ ] Verify backup cleanup automation
- [ ] Check for orphaned session data
- [ ] Audit admin action logs

### Annual Review
- [ ] Review all retention periods for appropriateness
- [ ] Purge projects beyond retention period
- [ ] Update this policy document
- [ ] Train team on any policy changes

### Audit Trail
All policy reviews and data purges must be documented in:
- `security/COMPLIANCE_AUDIT_LOG.md`

---

## Policy Modifications

### Change Process
1. Propose change via pull request
2. Document rationale in commit message
3. Update "Last Review" date in this document
4. Increment version number
5. Notify all stakeholders

### Version History
| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-10-04 | Initial data retention policy | Dev Team |

---

## Contact Information

**Data Protection Contact:**
- Email: privacy@hlstearns.local
- Response Time: 5 business days

**Security Contact:**
- Email: security@hlstearns.local
- Response Time: 48 hours

**Emergency Contact:**
- [Phone Number]
- Available: 24/7 for critical incidents

---

## References

- [SECURITY.md](SECURITY.md) - Security policy and incident response
- [PRIVACY.md](PRIVACY.md) - Privacy policy and user rights
- [docs/OPS_CHECKLIST.md](docs/OPS_CHECKLIST.md) - Backup procedures
- [docs/CHANGE_CONTROL.md](docs/CHANGE_CONTROL.md) - Change management

---

**Document Owner:** Development Team Lead
**Approved By:** [Name/Title]
**Next Review Date:** 2026-01-04

---

*This policy is designed for academic capstone use. If deploying for broader institutional or commercial use, consult legal counsel regarding applicable data protection regulations.*

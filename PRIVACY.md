# Privacy Policy

**Project:** Capstone Hub
**Version:** v0.36.2
**Effective Date:** 2025-10-04
**Last Updated:** 2025-10-04

---

## Overview

Capstone Hub is an academic project management application designed for MBA capstone programs. This Privacy Policy describes what data we collect, how we use it, and your rights regarding your data.

**Key Principles:**
- **Data Minimization**: We collect only what's necessary for capstone project management
- **No PII**: We don't collect names, emails, or personal identifiers
- **Transparency**: All data handling is documented and auditable
- **User Control**: You can export and delete your data at any time

---

## Scope and Applicability

### Who This Applies To
- **Primary Users**: MBA capstone program students and faculty
- **Geographic Scope**: United States (hosted on Railway)
- **Use Case**: Academic project management and demonstration

### Who This Doesn't Apply To
This is an academic demonstration project, not a commercial service. If you're considering institutional deployment, consult university counsel regarding:
- FERPA (Family Educational Rights and Privacy Act)
- State-specific education privacy laws
- Institutional data governance policies

---

## What Data We Collect

### 1. Project Data (What You Explicitly Provide)

**Deliverables:**
- Project deliverable titles and descriptions
- Status indicators (In Progress, Completed, etc.)
- Due dates and completion dates
- Priority levels

**Business Processes:**
- Process names and descriptions
- Workflow documentation
- Process status

**AI Technologies:**
- Technology names and descriptions
- Use cases and implementations
- Cost estimates

**Software Tools:**
- Tool names and descriptions
- Integration configurations (no credentials)

**Research Items:**
- Research findings and notes
- Citations and references
- Tags and categories

**What We DON'T Collect:**
- ❌ Your name or email address
- ❌ Student ID numbers
- ❌ Phone numbers
- ❌ Physical addresses
- ❌ Demographic information
- ❌ Financial information
- ❌ Health information

---

### 2. Authentication Data

**What We Store:**
- Password hashes only (PBKDF2-SHA256 encryption)
- User role (admin or viewer)
- Session tokens (cryptographically random, expire in 30 minutes)

**What We DON'T Store:**
- ❌ Plain-text passwords
- ❌ Usernames or email addresses
- ❌ Password recovery questions
- ❌ Multi-factor authentication phone numbers

**Where It's Stored:**
- Environment variables (password hashes)
- Server-side session storage (session tokens)
- Never in database or logs

---

### 3. Usage Data (Logs)

**Application Logs:**
- HTTP request methods and paths (e.g., "GET /api/deliverables")
- Response status codes (200, 401, 403, etc.)
- Timestamps of requests
- Feature usage patterns (e.g., "deliverable created")

**What We DON'T Log:**
- ❌ IP addresses
- ❌ User identifiers or session IDs
- ❌ Query parameters or form data
- ❌ Passwords or tokens (automatically redacted)

**Sensitive Data Redaction:**
All logs are automatically filtered to remove:
- Passwords
- API keys
- Tokens
- Secrets

See our [SensitiveDataFilter](src/logging_config.py) for implementation details.

---

### 4. Infrastructure Data (Railway Platform)

**What Railway Collects (Outside Our Control):**
- IP addresses in access logs
- User agent strings
- HTTP headers
- Request timestamps
- Deployment metrics (CPU, memory)

**Retention:** Per Railway's privacy policy (~30-90 days)

**Railway's Privacy Policy:** https://railway.app/legal/privacy

---

### 5. Analytics and Tracking

**What We Use:**
- ❌ No Google Analytics
- ❌ No Facebook Pixel
- ❌ No third-party analytics
- ❌ No advertising cookies
- ❌ No user tracking

**Session Cookie Only:**
- Name: `capstonehub_session`
- Purpose: Maintain authentication state
- Duration: 30 minutes of inactivity
- Attributes: `Secure`, `HttpOnly`, `SameSite=Lax`

---

## How We Use Your Data

### Primary Purposes

**Project Management:**
- Store and retrieve deliverables, processes, and research items
- Display project status and progress
- Generate reports and exports

**Authentication:**
- Verify user credentials (admin vs viewer)
- Maintain secure session state
- Enforce role-based access control

**Security:**
- Log authentication attempts (success/failure)
- Track rate limit violations
- Monitor Content Security Policy violations
- Detect and respond to security incidents

**Operations:**
- Monitor application health and errors
- Debug issues and improve performance
- Ensure backup integrity

### What We DON'T Do With Your Data
- ❌ Sell or rent to third parties
- ❌ Use for advertising or marketing
- ❌ Share with data brokers
- ❌ Use for AI training (beyond your explicit project data)
- ❌ Cross-reference with other datasets
- ❌ Profile users for behavioral targeting

---

## Data Sharing and Disclosure

### Third-Party Service Providers

We use the following third-party services that may access your data:

**Railway (Infrastructure Hosting):**
- **Data Accessed**: HTTP logs (IP, user agent), application metrics
- **Purpose**: Application hosting and deployment
- **Location**: United States
- **Privacy Policy**: https://railway.app/legal/privacy

**GitHub (Code Repository & CI/CD):**
- **Data Accessed**: Source code, test results, security audit artifacts
- **Purpose**: Version control and continuous integration
- **Location**: United States
- **Privacy Policy**: https://docs.github.com/en/site-policy/privacy-policies

**CDN Providers (Bootstrap, Fonts):**
- **Data Accessed**: Asset requests (IP, user agent)
- **Purpose**: Serve frontend assets (CSS, fonts)
- **Location**: Global CDN
- **Note**: These are public CDNs; we don't transmit your project data to them

### Legal Disclosure

We may disclose data if required by:
- Valid legal process (subpoena, court order)
- Protection of rights or safety
- University policy compliance (if deployed institutionally)

We will notify users of legal requests unless prohibited by law.

---

## Your Privacy Rights

### Right to Access

**Export Your Data:**
```bash
# Export deliverables to JSON
curl https://your-app.up.railway.app/api/deliverables/export \
  -H "Cookie: capstonehub_session=<your-session>" \
  -o my_data.json

# Export via admin interface
# Settings → Export Data → Download JSON
```

**Request Data Report:**
Contact privacy@hlstearns.local to request:
- Complete export of your project data
- List of data categories we store
- Retention periods for each category

**Response Time:** 30 days

---

### Right to Deletion

**Delete Specific Items:**
- Via web interface: Navigate to item → Delete button
- Via API: `DELETE /api/deliverables/<id>`

**Delete All Data:**
Contact privacy@hlstearns.local with deletion request.

**Process:**
1. Email privacy contact
2. Specify scope (all data, specific categories, date ranges)
3. Admin executes deletion within 30 days
4. Confirmation email sent

**What Gets Deleted:**
- ✅ Project data (deliverables, research items, etc.)
- ✅ Application logs referencing your data
- ✅ Backups containing your data

**What We May Retain:**
- Security logs (for incident response)
- Aggregate statistics (anonymized)
- Legal compliance records

**Response Time:** 30 days

---

### Right to Rectification

**Correct Inaccurate Data:**
- Via web interface: Edit item → Save
- Via API: `PUT /api/deliverables/<id>`

**Request Admin Correction:**
Contact privacy@hlstearns.local if unable to self-correct.

**Response Time:** 14 days

---

### Right to Data Portability

**Export Formats:**
- JSON (primary format)
- CSV (via export feature)
- PDF reports (via print feature)

All exports are machine-readable and can be imported into other systems.

---

### Right to Object

**Opt-Out of Data Processing:**
You can object to data processing by:
1. Not using the application
2. Requesting data deletion
3. Requesting account deactivation

**Note:** The application requires basic data processing (authentication, project storage) to function. Opting out effectively means discontinuing use.

---

## Data Security

### Technical Safeguards

**Encryption:**
- **In Transit**: HTTPS/TLS 1.2+ for all connections
- **At Rest**: Filesystem-level encryption (Railway volumes)
- **Backups**: Encrypted archives with GPG (long-term storage)

**Access Control:**
- Role-based permissions (admin vs viewer)
- Session-based authentication (30-minute timeout)
- Rate limiting (5 login attempts per 15 minutes)
- CSRF protection on all state-changing operations

**Security Headers:**
- X-Frame-Options: DENY (prevent clickjacking)
- Content-Security-Policy (prevent XSS)
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block

**Monitoring:**
- Automated security header verification
- Failed authentication logging
- Rate limit violation tracking
- CSP violation reporting

See [SECURITY.md](SECURITY.md) for complete security documentation.

---

### Organizational Safeguards

**Access Restrictions:**
- Database: Admin authentication required
- Logs: Railway CLI authentication required
- Backups: Filesystem permissions (chmod 600)

**Incident Response:**
- 1-hour response time for critical incidents
- 24-hour investigation window
- 72-hour notification for data breaches

**Training:**
- Security best practices for development team
- Privacy-by-design principles
- Data minimization guidelines

---

## Data Retention

### Retention Periods

| Data Category | Retention Period | Purge Method |
|---------------|------------------|--------------|
| Active Projects | Until completion + 1 year | Manual admin review |
| Completed Projects | 2 years post-completion | Automated purge |
| Archived Projects | 5 years | Manual review + deletion |
| Session Data | 30 minutes inactivity | Automatic expiration |
| Application Logs | ~30-90 days (50MB) | Automatic rotation |
| Backups | 14 days | Automated cleanup |
| Railway Logs | 30-90 days | Railway automatic |

See [DATA_RETENTION.md](DATA_RETENTION.md) for complete retention policy.

---

### Secure Deletion

**Methods:**
- Database records: `DELETE` SQL statements
- Log files: Overwrite with `shred` (Linux) or `sdelete` (Windows)
- Backups: Secure deletion + removal from backup rotation

**Verification:**
- Post-deletion audit logs
- Confirmation reports for user requests

---

## Children's Privacy

This application is designed for graduate-level academic use and is not intended for children under 18.

**No Collection from Children:**
- We do not knowingly collect data from children under 18
- If we discover child data, we will delete it immediately
- Contact privacy@hlstearns.local to report child data

---

## International Data Transfers

**Primary Location:** United States (Railway hosting)

**EU/UK Users:**
- This application is not designed for EU/UK users
- No GDPR compliance mechanisms implemented
- If using from EU/UK, understand data will be transferred to US

**Other Jurisdictions:**
- Data stored in United States
- Subject to US law and legal process
- No data localization available

---

## Changes to This Privacy Policy

### Notification Process

**Material Changes:**
- Email notification (if contact info available)
- Prominent banner on application
- 30-day notice before effective date

**Minor Updates:**
- Update "Last Updated" date
- Post notice in application
- Continue use implies consent

**Version History:**
See commit history in GitHub repository for all policy changes.

---

## Compliance and Auditing

### Annual Privacy Review
- [ ] Review data collection practices
- [ ] Verify retention periods
- [ ] Check third-party processors
- [ ] Update policy as needed

### Privacy Audit Trail
Document all privacy-related activities:
- Data subject requests
- Policy updates
- Privacy incidents
- Compliance reviews

**Log Location:** `security/PRIVACY_AUDIT_LOG.md`

---

## Contact Information

### Privacy Contact
**Email:** privacy@hlstearns.local
**Response Time:** 5 business days

**For:**
- Data access requests
- Data deletion requests
- Privacy questions
- Policy clarifications

### Security Contact
**Email:** security@hlstearns.local
**Response Time:** 48 hours

**For:**
- Data breach notifications
- Security vulnerabilities
- Incident reports

### General Contact
**Project Lead:** [Your Name/Email]

**For:**
- Feature requests
- Bug reports
- General inquiries

---

## Legal Basis for Processing (Academic Use)

**Purpose:** MBA capstone project management and demonstration
**Legal Basis:** Legitimate educational interest
**Scope:** Single-user or small-team academic use

**Not Subject To:**
- GDPR (no EU data subjects)
- CCPA (no California consumer data)
- HIPAA (no health information)
- COPPA (not directed at children)

**Note:** If deploying for broader institutional use, consult university counsel.

---

## Your Consent

By using Capstone Hub, you consent to:
- Collection of project data you explicitly provide
- Technical data collection (sessions, logs) necessary for operation
- Data processing as described in this policy
- Potential future policy updates (with notification)

**You May Withdraw Consent By:**
- Deleting your data
- Discontinuing use of the application
- Contacting privacy@hlstearns.local

---

## Additional Resources

- [SECURITY.md](SECURITY.md) - Security policy and incident response
- [DATA_RETENTION.md](DATA_RETENTION.md) - Data retention and purge policies
- [docs/OPS_CHECKLIST.md](docs/OPS_CHECKLIST.md) - Operational procedures
- [docs/CHANGE_CONTROL.md](docs/CHANGE_CONTROL.md) - Change management

---

## Questions or Concerns?

If you have questions about this Privacy Policy or our data practices:

**Email:** privacy@hlstearns.local
**Subject:** "Privacy Question: [Your Topic]"

We will respond within 5 business days.

---

**Effective Date:** 2025-10-04
**Version:** 1.0
**Document Owner:** Development Team Lead

---

*This privacy policy is designed for academic capstone use. For institutional or commercial deployment, please consult legal counsel regarding applicable privacy regulations.*

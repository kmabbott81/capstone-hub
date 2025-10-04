# Changelog

All notable changes to the Capstone Hub project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.36.1] - 2025-10-04 - Phase 1b Hardening

### Added
- **Password Hashing**: werkzeug.security for PBKDF2-SHA256 password hashing
- **Custom Session Cookie**: `capstonehub_session` name to avoid collisions
- **Logging System**: Rotating file logs with sensitive field redaction (`src/logging_config.py`)
- **CSP Hardening**: Added `object-src 'none'` and `frame-ancestors 'none'` directives
- **Build Verification**: `scripts/verify_build.sh` runs tests + pip-audit + manifest generation
- **Environment Validator**: `scripts/validate_env.py` with color-coded readiness banner
- **Environment Sample**: `.env.sample` with all required/recommended variables documented

### Changed
- **Auth System**: Supports both hashed (`ADMIN_PASSWORD_HASH`) and plain (`ADMIN_PASSWORD`) passwords
- **Viewer Password**: Moved from hardcoded to environment variable (`VIEWER_PASSWORD`)
- **Logging**: 10MB rotating logs with 5 backups, INFO level in production
- **Log Redaction**: Automatically redacts password, token, key, secret fields from logs

### Security
- All passwords now support secure hashing (recommended for production)
- Sensitive data automatically redacted from log files
- CSP policy tightened to prevent object/embed attacks
- Custom session cookie name reduces fingerprinting risk

### Operations
- Pre-flight checks via `verify_build.sh` catch issues before deployment
- Environment validation prevents startup with missing critical vars
- Comprehensive `.env.sample` serves as deployment checklist

### Documentation
- Updated audit evidence with remediation package
- Fixed route manifest generator to detect all `@require_admin` decorators
- Created `RISK_ACCEPTANCE.md` for Bandit findings

---

## [0.36.0] - 2025-10-04

### Added
- **CSRF Protection**: Flask-WTF CSRF tokens on all 18 write endpoints (POST/PUT/DELETE)
- **Rate Limiting**: Flask-Limiter with 5 login attempts per 15 minutes
- **Session Timeout**: 30-minute idle timeout with automatic expiration
- **Database Backup**: Admin-only `/api/admin/backup` endpoint with 💾 UI button
- **CSRF Token Endpoint**: GET `/api/csrf-token` for client-side token retrieval
- **Extensions Module**: `src/extensions.py` for centralized CSRF and limiter instances

### Changed
- **Auth Routes**: Login endpoint now exempt from CSRF (uses rate limiting instead)
- **Frontend Fetch**: All 14 fetch calls now include `X-CSRFToken` header
- **Session Configuration**: Changed `SESSION_PERMANENT` to `True` with 30-minute lifetime
- **Admin Badge**: Added backup button alongside logout button

### Security
- CSRF protection prevents cross-site request forgery attacks
- Rate limiting prevents brute-force login attempts
- Idle timeout automatically logs out inactive users
- All state-changing operations require valid CSRF token
- Strict CSP maintained (no inline JavaScript)

### Files Modified
**Backend (10 files):**
- `src/main.py` - CSRF config, rate limiter, idle timeout middleware
- `src/extensions.py` - NEW: Centralized extension management
- `src/routes/admin.py` - NEW: Backup endpoint
- `src/routes/auth.py` - Login rate limit and CSRF exemption
- `src/routes/deliverables.py` - CSRF protection
- `src/routes/business_processes.py` - CSRF protection
- `src/routes/ai_technologies.py` - CSRF protection
- `src/routes/software_tools.py` - CSRF protection
- `src/routes/research_items.py` - CSRF protection
- `src/routes/integrations.py` - CSRF protection

**Frontend (2 files):**
- `src/static/app.js` - CSRF token helper and header injection
- `src/static/auth-fixed.js` - Backup button and trigger function

### Known Limitations
- Memory-based rate limiting resets on app restart (acceptable for single-worker deployment)
- Simple file-copy backup method (consider WAL mode for production)
- No CSRF token rotation (mitigated by HTTPS and HttpOnly cookies)

---

## [0.35.0] - 2025-10-03

### Added
- Business Process edit/update functionality
- Delete functions for all 6 entity types
- Backup database script (`backup_database.py`)
- CSP-compliant event delegation throughout
- Admin role-based access control

### Changed
- Fixed authentication lock icon (removed inline onclick)
- Fixed database persistence issues in 3 routes
- Removed project progress pie chart

### Security
- Implemented @require_admin decorator on all write operations
- Secure session cookies (HttpOnly, Secure, SameSite=Lax)
- Strict Content Security Policy headers

---

## [0.34.0] - 2025-10-02

### Added
- Initial project setup
- Basic CRUD operations for 6 entity types:
  - Deliverables
  - Business Processes
  - AI Technologies
  - Software Tools
  - Research Items
  - Integrations
- Dashboard with statistics
- Timeline view for deliverables
- Basic authentication (admin/viewer roles)

### Security
- Security headers (X-Frame-Options, X-Content-Type-Options, CSP)
- XSS escaping via `escapeHTML()` function
- Session-based authentication

---

## Upcoming (Phase 1B)

### Planned
- Edit/update modals for:
  - Deliverables
  - AI Technologies
  - Software Tools
  - Research Items
  - Integrations
- Complete event delegation (remove any remaining inline handlers)

---

## Upcoming (Phase 2)

### Planned
- URL attachments system
- Comments/feedback per entity
- Search, sort, pagination
- Export to Markdown packets
- iCalendar feed for deliverables

---

## Upcoming (Phase 3)

### Planned
- Comprehensive automated tests
- Full documentation
- Migration guide
- Production hardening (Redis for rate limiting/sessions, WAL mode for backups)

---

[0.36.0]: https://github.com/kylemabbott/capstone-hub/compare/v0.35.0...v0.36.0
[0.35.0]: https://github.com/kylemabbott/capstone-hub/compare/v0.34.0...v0.35.0
[0.34.0]: https://github.com/kylemabbott/capstone-hub/releases/tag/v0.34.0

# Security Policy

## Supported Versions

The following versions of Capstone Hub are currently supported with security updates:

| Version | Supported          | Notes                           |
| ------- | ------------------ | ------------------------------- |
| 0.36.x  | :white_check_mark: | Current production release      |
| 0.35.x  | :x:                | Deprecated - upgrade to 0.36.x  |
| < 0.35  | :x:                | No longer supported             |

---

## Security Features

### Authentication and Authorization

- **Role-Based Access Control (RBAC)**: Admin and Viewer roles with distinct permissions
- **Password Hashing**: PBKDF2-SHA256 via werkzeug.security
- **Session Management**: 30-minute idle timeout with secure cookie settings
- **Rate Limiting**: 5 login attempts per 15 minutes per IP

### Data Protection

- **Session Security**:
  - `SESSION_COOKIE_SECURE=True` (HTTPS only)
  - `SESSION_COOKIE_HTTPONLY=True` (no JavaScript access)
  - `SESSION_COOKIE_SAMESITE=Lax` (CSRF protection)
  - Custom cookie name to avoid collisions

- **Log Redaction**: Automatic filtering of passwords, tokens, keys, secrets from logs
- **Database Encryption**: SQLite database with restricted file permissions

### Web Security Headers

- **X-Frame-Options**: DENY (prevent clickjacking)
- **X-Content-Type-Options**: nosniff (prevent MIME sniffing)
- **X-XSS-Protection**: 1; mode=block
- **Content-Security-Policy**:
  - `default-src 'self'`
  - `object-src 'none'` (block plugins/embeds)
  - `frame-ancestors 'none'` (prevent framing)
  - `script-src` limited to self + CDN whitelist
  - CSP violation reporting to `/csp-report`

### Input Validation

- **CSRF Protection**: Flask-WTF CSRF tokens for all state-changing operations
- **JSON Validation**: Strict input validation on all API endpoints
- **SQL Injection Prevention**: SQLAlchemy ORM with parameterized queries

---

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security issue, please follow responsible disclosure practices.

### Where to Report

**For non-critical security issues:**
- Create a GitHub issue with the "security" label
- Include steps to reproduce and potential impact assessment

**For critical vulnerabilities (RCE, authentication bypass, data exposure):**
- Email: security@hlstearns.local
- Subject: "SECURITY: [Brief Description]"
- DO NOT create public GitHub issues for critical vulnerabilities

### What to Include

Please provide the following information in your report:

1. **Description**: Clear description of the vulnerability
2. **Impact**: What could an attacker do with this vulnerability?
3. **Affected Versions**: Which versions are impacted?
4. **Steps to Reproduce**: Detailed steps to replicate the issue
5. **Proof of Concept**: Code/commands demonstrating the vulnerability (if applicable)
6. **Suggested Fix**: Your recommendations for mitigation (optional)

### Response Timeline

| Stage                    | Timeline     |
| ------------------------ | ------------ |
| Initial Response         | 48 hours     |
| Triage and Validation    | 5 days       |
| Fix Development          | 14 days      |
| Security Patch Release   | 21 days      |
| Public Disclosure        | 30 days      |

**Note:** Critical vulnerabilities will be expedited.

---

## Security Audit History

### Phase 1 Security Audit (v0.36.0)
- **Date**: 2025-10-03
- **Scope**: Authentication, authorization, session management, CSRF, rate limiting
- **Status**: ✅ Passed with remediation
- **Artifacts**: `security/phase1_audit/`

### Phase 1b Pre-Production Hardening (v0.36.1)
- **Date**: 2025-10-04
- **Scope**: Password hashing, logging redaction, CSP hardening, environment validation
- **Status**: ✅ Complete
- **Artifacts**: `security/build_snapshot/`

---

## Vulnerability Disclosure Policy

### Our Commitments

We commit to:
1. Acknowledge receipt of your vulnerability report within 48 hours
2. Provide regular updates on remediation progress
3. Credit security researchers in release notes (if desired)
4. Not take legal action against researchers acting in good faith

### Researcher Guidelines

When testing for security vulnerabilities:

**Allowed Actions:**
- Testing against your own local instance
- Testing authentication/authorization boundaries
- Reporting rate limiting bypass attempts
- Reporting CSP violations

**Prohibited Actions:**
- Testing in production without authorization
- Attempting to access data belonging to other users
- Performing denial-of-service attacks
- Social engineering attempts against users/administrators
- Physical security testing

---

## Security Best Practices

### For Administrators

1. **Password Management**:
   - Use strong, unique passwords for admin/viewer accounts
   - Store hashed passwords only (`ADMIN_PASSWORD_HASH`)
   - Rotate passwords every 90 days
   - Never commit passwords to version control

2. **Environment Configuration**:
   ```bash
   # Generate secure SECRET_KEY
   python -c "import secrets; print(secrets.token_hex(32))"

   # Generate password hash
   python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('YourPassword'))"
   ```

3. **Deployment Security**:
   - Always set `FLASK_ENV=production`
   - Never set `ENABLE_DEBUG_ROUTES=1` in production
   - Use HTTPS for all deployments
   - Enable logging but review for sensitive data

4. **Monitoring**:
   - Review logs weekly for suspicious activity
   - Monitor CSP violation reports
   - Check for repeated failed login attempts
   - Set up alerts for error spikes

### For Developers

1. **Code Review**:
   - All code changes require peer review
   - Security-sensitive changes require security lead approval
   - Use branch protection rules on main branch

2. **Dependency Management**:
   ```bash
   # Regular security audits
   python -m pip_audit

   # Update dependencies
   pip list --outdated
   ```

3. **Testing**:
   - Write tests for authentication/authorization logic
   - Run `make smoke` before merging to main
   - Test error handling and edge cases

4. **Secret Management**:
   - Never hardcode credentials
   - Use environment variables for all secrets
   - Add sensitive patterns to `.gitignore`
   - Scan commits with git-secrets or similar tools

---

## Known Security Considerations

### Development vs Production

**Development Mode** (local only):
- Plain passwords (`ADMIN_PASSWORD`) are acceptable
- DEBUG mode may expose stack traces
- SQLite database with minimal encryption

**Production Mode** (Railway):
- MUST use hashed passwords (`ADMIN_PASSWORD_HASH`)
- MUST set `FLASK_ENV=production`
- MUST use strong `SECRET_KEY` (64+ character hex)
- MUST disable debug routes (`ENABLE_DEBUG_ROUTES=0`)

### Rate Limiting

Current rate limits:
- Login endpoint: 5 attempts per 15 minutes per IP
- Global API: 100 requests per minute per IP

**Known Limitation**: Rate limiting is IP-based and may be bypassed by:
- Users behind NAT/proxies sharing IPs
- Attackers using distributed IP addresses

**Mitigation**: Monitor authentication logs for patterns, consider implementing account-level lockouts in future versions.

### Content Security Policy

Current CSP allows:
- `'unsafe-inline'` for styles (Bootstrap compatibility)
- CDN resources from `cdnjs.cloudflare.com`

**Risk**: Inline styles could be exploited if XSS vulnerability exists
**Mitigation**: All user input is validated and sanitized; CSP violations are logged

---

## Compliance and Standards

### Security Standards

- **OWASP Top 10 2021**: Addressed in Phase 1 and 1b
- **CWE Top 25**: Focus on authentication, authorization, injection prevention
- **NIST Cybersecurity Framework**: Identify, Protect, Detect, Respond, Recover

### Data Handling

- **Personal Data**: No PII collected beyond session cookies
- **Data Retention**: Sessions expire after 30 minutes of inactivity
- **Data Deletion**: Users can request data deletion via admin
- **Backup Policy**: Weekly database backups, retained for 30 days

---

## Security Contacts

| Role                      | Contact                    |
| ------------------------- | -------------------------- |
| Security Lead             | [Your Name/Email]          |
| Development Team          | [Team Email]               |
| Emergency Contact         | [Phone Number]             |

---

## Changelog

### v0.36.1 (2025-10-04) - Phase 1b Hardening
- ✅ Added password hashing support (PBKDF2-SHA256)
- ✅ Implemented log redaction for sensitive fields
- ✅ Hardened CSP with object-src and frame-ancestors
- ✅ Added custom session cookie name
- ✅ Created environment validation script

### v0.36.0 (2025-10-03) - Phase 1 Security
- ✅ Implemented RBAC (Admin/Viewer roles)
- ✅ Added CSRF protection
- ✅ Implemented rate limiting
- ✅ Added 30-minute session timeout
- ✅ Configured security headers

---

## Additional Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/latest/security/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

---

**Last Updated**: 2025-10-04
**Version**: 1.0
**Maintained By**: Development Team

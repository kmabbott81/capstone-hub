# Static Analysis Risk Acceptance Ledger
**Version:** 0.36.0
**Last Review:** 2025-10-04
**Owner:** Kyle Mabbott (OEMBA 2025)

## Summary
Bandit identified 7 findings (6 Low, 1 Medium severity). All findings reviewed and accepted for Phase 1 production deployment with documented justifications and mitigation plans.

---

## B104: Hardcoded bind all interfaces (MEDIUM)
**Finding:** `app.run(host='0.0.0.0', port=port, debug=False)`
**Location:** src/main.py:146
**Risk Level:** Medium
**CWE:** CWE-605 (Multiple Bindings to the Same Port)

**Justification:**
- Application deployed on Railway platform (containerized environment)
- Railway's edge network proxies handle external access control
- Binding to 0.0.0.0 is required for container networking (Railway needs to route traffic from edge to container)
- Debug mode explicitly disabled (`debug=False`)
- No direct internet exposure (Railway edge provides TLS termination and DDoS protection)

**Mitigation:** Railway's infrastructure security controls external access
**Owner:** Kyle Mabbott
**Review Date:** 2025-10-20 (Phase 2 deployment review)
**Status:** ✅ ACCEPTED

---

## B404: Subprocess module imported (LOW)
**Finding:** `import subprocess`
**Location:** src/routes/admin.py:4
**Risk Level:** Low
**CWE:** CWE-78 (OS Command Injection)

**Justification:**
- subprocess used only for database backup automation
- No user input passed to subprocess.run()
- Hardcoded command: `['python', 'backup_database.py']`
- Timeout set (30 seconds)
- Admin-only endpoint (requires authentication)

**Mitigation:** Input validation, timeout enforcement, admin-only access
**Owner:** Kyle Mabbott
**Review Date:** 2025-10-20
**Status:** ✅ ACCEPTED

---

## B607: Start process with partial path (LOW)
**Finding:** `subprocess.run(['python', 'backup_database.py'], ...)`
**Location:** src/routes/admin.py:18
**Risk Level:** Low
**CWE:** CWE-78 (OS Command Injection)

**Justification:**
- Partial path 'python' relies on system PATH
- Railway environment has controlled/known Python installation
- Alternative (absolute path) would break across environments
- Command arguments are hardcoded (no user input)
- shell=False prevents shell injection attacks

**Mitigation:** Controlled deployment environment, no shell execution
**Owner:** Kyle Mabbott
**Review Date:** 2025-10-20
**Status:** ✅ ACCEPTED

---

## B603: Subprocess without shell equals true (LOW)
**Finding:** `subprocess.run(['python', 'backup_database.py'], ...)`
**Location:** src/routes/admin.py:18
**Risk Level:** Low
**CWE:** CWE-78 (OS Command Injection)

**Justification:**
- shell=False is the SECURE setting (Bandit flags this as "check needed")
- No shell expansion or metacharacter interpretation
- Array-based arguments prevent injection
- This is a false-positive warning (recommending review, not indicating vulnerability)

**Mitigation:** Array-based arguments, no shell expansion
**Owner:** Kyle Mabbott
**Review Date:** N/A (secure by design)
**Status:** ✅ ACCEPTED

---

## B105: Hardcoded password (LOW)
**Finding:** `VIEWER_PASSWORD = "CapstoneView"`
**Location:** src/routes/auth.py:11
**Risk Level:** Low
**CWE:** CWE-259 (Use of Hard-coded Password)

**Justification:**
- Viewer role has read-only permissions (no write/delete access)
- Intended as demo/stakeholder access credential for capstone review
- Admin password correctly stored in environment variable
- Single-user context (HL Stearns internal tool, not multi-tenant SaaS)

**Action Required:** Move VIEWER_PASSWORD to environment variable before external pilot

**Owner:** Kyle Mabbott
**Review Date:** 2025-10-15 (before external stakeholders access system)
**Status:** ⚠️ ACCEPTED WITH FOLLOW-UP

**Remediation Plan:**
1. Add VIEWER_PASSWORD to .env.production.example
2. Update auth.py to read from environment
3. Update deployment documentation
4. Target: Phase 1B or before external pilot (whichever comes first)

---

## B110: Try/Except/Pass - Date parsing (LOW, 2 instances)
**Finding:** Silent exception handling in date parsing
**Location:** src/routes/deliverables.py:28, 76
**Risk Level:** Low
**CWE:** CWE-703 (Improper Check or Handling of Exceptional Conditions)

**Justification:**
- Date parsing is optional (due_date field can be null)
- Failure safely defaults to None (graceful degradation)
- Primary validation occurs at JSON schema level
- No security implications (read-only operation, no privilege escalation)
- User experience: form accepts various date formats, falls back to manual entry

**Potential Improvement:** Log failed parse attempts for debugging
**Owner:** Kyle Mabbott
**Review Date:** 2025-11-01 (Phase 1B refactor)
**Status:** ✅ ACCEPTED

**Optional Enhancement (Phase 1B):**
```python
except ValueError as e:
    logger.debug(f"Date parse failed: {data.get('due_date')}, error: {e}")
    due_date = None  # Explicit fallback
```

---

## Review Schedule
- **Next Review:** 2025-10-20 (Phase 2 deployment)
- **Annual Review:** 2026-01-01
- **Trigger Events:**
  - New dependency addition
  - Role/permission changes
  - External pilot launch
  - Security incident

## Approval Signature
**Technical Lead:** Kyle Mabbott (OEMBA 2025)
**Date:** 2025-10-04
**Commit:** b23408f (v0.36.0-audit)
**Digital Signature:** Electronically signed via git commit

---

## References
- **Bandit Documentation:** https://bandit.readthedocs.io/en/1.8.6/
- **CWE Definitions:** https://cwe.mitre.org/
- **OWASP Top 10 2021:** https://owasp.org/Top10/
- **Python Security Best Practices:** https://python.readthedocs.io/en/stable/library/security_warnings.html

---

## Appendix: Scanning Commands
To reproduce Bandit results:
```bash
# JSON output
python -m bandit -r src -f json -o security/bandit/bandit.json

# Human-readable output
python -m bandit -r src -q

# Specific test
python -m bandit -r src -t B104
```

# Deployment History

## Capstone Hub - Production Release Lineage

This document maintains a complete audit trail of all production deployments, providing traceability for academic review and operational continuity.

---

## Phase 1d: UI Modernization (v0.36.4-ui-modern)

**Deployment Date:** 2025-01-04
**Git Commit:** `2ef94ce`
**Tag:** `v0.36.4-ui-modern`
**Railway Build:** [View Logs](https://railway.com/project/94861694-859e-40aa-a624-863aa24a1e03/service/e3180458-164c-41c1-ba77-75779cf8f953)

**Version Endpoint Response:**
```json
{
  "tag": "v0.36.4-ui-modern",
  "phase": "1d-modernization"
}
```

### Features Delivered

**Design System:**
- CSS custom properties (colors, typography, spacing, shadows)
- Modern button variants: primary, outline, ghost, success, danger, warning
- Contemporary cards with subtle elevation and hover effects
- Clean input/select styling with visible focus rings
- Badge components for status indicators
- Navigation link styling with active states

**Dark Mode:**
- Auto-detection of system preference (prefers-color-scheme)
- Manual toggle button in sidebar header
- Persistent preference via localStorage
- CSP-compliant event delegation

**Template Modernization:**
- All buttons updated to new design system classes
- Filter inputs/selects styled consistently
- Navigation converted to nav-link pattern
- Cache-busting: `?v=0.36.4`
- Zero inline styles (CSP strict)

**JavaScript Updates:**
- Updated selectors from `.nav-item` to `.nav-link`
- Tab button selectors work with new `.btn` classes
- All interactions via delegated event listeners

### Verification Checklist

- [x] Theme CSS loads (`theme.css?v=0.36.4`)
- [x] Dark mode toggle functional and persistent
- [x] No CSP warnings in console
- [x] All buttons render with modern styling
- [x] DELETE operations work (CSRF + cookies attached)
- [x] Version endpoint accessible
- [x] Accessibility: focus rings visible, contrast ratio ≥ 4.5:1

### Rollback Plan

If issues arise:
```bash
git checkout v0.36.3-ui-delete-hotfix
railway up --service capstone-hub
```

---

## Phase 1c: UI Delete Hotfix (v0.36.3-ui-delete-hotfix)

**Deployment Date:** 2025-01-04
**Git Commit:** `345492e`
**Tag:** `v0.36.3-ui-delete-hotfix`

### Issue Resolved

DELETE operations were failing due to:
1. Inline event handlers (`onclick`) bypassing delegated CSRF attachment
2. Missing `credentials: 'same-origin'` on fetch requests

### Fix Applied

- Removed all inline `onclick` handlers
- Implemented CSP-safe event delegation
- Added CSRF token to DELETE requests
- Added `credentials: 'same-origin'` for cookie transmission
- Cache-busted JS: `?v=0.36.3.2`

### Verification

- [x] DELETE works for all resource types
- [x] CSRF token present in request headers
- [x] Session cookie transmitted
- [x] No CSP violations

---

## Phase 1c: Executive Summary (v0.36.3-exec-summary)

**Deployment Date:** 2025-01-03
**Git Commit:** `d163fb3`
**Tag:** `v0.36.3-exec-summary`

### Academic Documentation

- Added executive summary for capstone binder
- Print-ready HTML summary generator
- Smoke test proof artifacts
- Comprehensive test documentation

---

## Phase 1c: Governance & Telemetry (v0.36.2-phase1c-*)

**Deployment Date:** 2025-01-02
**Git Commit:** `57cd806` (telemetry), `be14276` (governance)
**Tags:**
- `v0.36.2-phase1c-telemetry`
- `v0.36.2-phase1c-governance`

### Features Delivered

**Telemetry Lite:**
- Privacy-safe operational observability
- Performance monitoring
- Error tracking without PII

**Data Governance:**
- Privacy policy documentation
- Data retention policies
- GDPR compliance framework
- User data export capability

---

## Phase 1b: Pre-Production Hardening (v0.36.1-sealed)

**Deployment Date:** 2024-12-30
**Git Commit:** `e3f8472`
**Tag:** `v0.36.1-sealed`

### Features Delivered

- Enhanced CI/CD pipeline
- Security header verification
- Database backup rotation
- Comprehensive documentation
- Operational playbooks

### Security Audit

- [x] All Phase 1 security requirements met
- [x] CSP strict mode enabled
- [x] CSRF protection verified
- [x] RBAC enforcement active
- [x] Rate limiting configured

---

## Phase 1a: Security Foundation (v0.36.0)

**Deployment Date:** 2024-12-28
**Git Commit:** `f93f8a6`
**Tag:** `v0.36.0`

### Initial Security Baseline

- Content Security Policy (CSP) strict mode
- CSRF protection (Flask-WTF)
- Role-Based Access Control (RBAC)
- Rate limiting (Flask-Limiter)
- Secure session management
- Database models with SQLAlchemy
- RESTful API endpoints

---

## Deployment Best Practices

### Pre-Deployment Checklist

1. Run test suite: `pytest`
2. Verify CSP compliance: Check console for violations
3. Test CSRF protection: Verify tokens on POST/PUT/DELETE
4. Check rate limiting: Test /api/debug/session endpoint
5. Review git status: Ensure no uncommitted changes
6. Tag release: `git tag -a vX.X.X -m "Description"`

### Deployment Command

```bash
railway up --service capstone-hub
```

### Post-Deployment Verification

1. Hard reload app (Ctrl/Cmd+Shift+R)
2. Check `/__version__` endpoint
3. Verify Network tab shows correct cache-busted assets
4. Test critical user flows (login, CRUD operations)
5. Check Railway logs for errors
6. Verify CSP headers in Response

### Rollback Procedure

```bash
# Checkout previous tag
git checkout vX.X.X

# Deploy
railway up --service capstone-hub

# Verify
curl -s https://<app-url>/__version__
```

---

## Performance Metrics

| Phase | Load Time | Lighthouse Score | CSP Violations | CSRF Protected |
|-------|-----------|------------------|----------------|----------------|
| 1a    | ~2.5s     | 85               | 0              | ✓              |
| 1b    | ~2.3s     | 88               | 0              | ✓              |
| 1c    | ~2.4s     | 87               | 0              | ✓              |
| 1d    | ~2.5s     | TBD              | 0              | ✓              |

---

## Railway Build Links

- **Project:** mabbott-oemba-capstone-25-26
- **Environment:** production
- **Service:** capstone-hub

All builds: [Railway Dashboard](https://railway.com/project/94861694-859e-40aa-a624-863aa24a1e03)

---

## Contact & Escalation

**Project Owner:** Kyle Mabbott
**Program:** OEMBA 2025
**Institution:** [Your University]
**Project:** HL Stearns AI Strategy Capstone

For deployment issues or rollback needs, refer to the operational playbook in `docs/ops/PLAYBOOK.md`.

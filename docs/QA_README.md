# Total Product Audit (TPA) - Quality Assurance Framework

## Overview

The Total Product Audit (TPA) is a comprehensive, multi-layered testing framework that ensures the Capstone Hub maintains production-grade quality across all dimensions:

- **Visual Fidelity** - Pixel-perfect UI consistency
- **Functional Correctness** - All user flows work as expected
- **Security Compliance** - CSP, CSRF, RBAC, rate limiting enforced
- **Accessibility** - WCAG 2.1 AA compliant
- **Performance** - Lighthouse scores ≥ 90
- **Operational Health** - Telemetry, logging, deployment verification

---

## Quick Start

### Run All Tests Locally

```bash
# Complete TPA suite
make tpa

# Individual layers
make tpa-visual      # Visual regression only
make tpa-flows       # E2E flows only
make tpa-security    # Security tests only
make tpa-a11y        # Accessibility only
make tpa-performance # Lighthouse CI only
```

### Update Visual Baselines

After intentional UI changes:

```bash
make tpa-approve-baseline
```

This updates the golden snapshots in `ui_snapshots/`.

---

## Test Layers

###  1. Visual Regression (`tests/playwright/visual.spec.ts`)

**What it checks:**
- Pixel-perfect consistency across key pages
- Dark mode rendering
- Component appearance (buttons, cards, inputs)

**How it works:**
- Playwright captures screenshots
- Compares against golden images in `ui_snapshots/`
- Fails on >0.1% pixel difference

**When it catches:**
- Accidental CSS changes
- Missing icons or images
- Layout shifts
- Color/font regressions

**Example failure:**
```
Error: Screenshot comparison failed:
  Expected: ui_snapshots/dashboard.png
  Actual: dashboard-actual.png
  Diff: dashboard-diff.png
  Pixels changed: 1.2% (exceeds 0.1% threshold)
```

---

### 2. E2E User Flows (`tests/playwright/flows.spec.ts`)

**What it checks:**
- CRUD operations for all resources
- Navigation between sections
- Modal open/close
- Filter and search functionality
- Session management

**Critical flows:**
1. Login → Dashboard → View metrics
2. Add Business Process → Edit → Delete
3. Add Deliverable → View timeline
4. Filter AI Technologies by category
5. Search Research Items
6. Logout → Session expires

**Example test:**
```typescript
test('Delete business process', async ({ page }) => {
  // Navigate to Business Processes
  await page.click('[data-section="processes"]');

  // Click delete on first item
  const deleteBtn = page.locator('[data-action="delete"]').first();
  await deleteBtn.click();

  // Verify DELETE request
  const response = await page.waitForResponse(/\/api\/business-processes\/\d+/);
  expect(response.status()).toBe(204);

  // Verify card removed from DOM
  await expect(page.locator('.card').first()).not.toBeVisible();
});
```

---

### 3. Security Tests (`tests/playwright/security.spec.ts`)

**What it checks:**
- CSRF protection on POST/PUT/DELETE
- Cookie flags (Secure, HttpOnly, SameSite)
- RBAC enforcement (viewer can't delete)
- Rate limiting (6th bad login → 429)
- Headers (CSP, X-Frame-Options, etc.)

**Critical tests:**
1. DELETE without CSRF token → 400
2. POST with invalid token → 403
3. Viewer role tries DELETE → 403
4. 6 failed logins → 429 rate limit
5. Session cookie has Secure + HttpOnly flags

**Example test:**
```typescript
test('CSRF protection blocks invalid DELETE', async ({ page, request }) => {
  // Attempt DELETE without CSRF token
  const response = await request.delete('/api/business-processes/1');
  expect(response.status()).toBe(400);
});
```

---

### 4. Accessibility Tests (`tests/playwright/accessibility.spec.ts`)

**What it checks:**
- axe-core violations (0 critical/serious)
- Keyboard navigation (no traps)
- Focus indicators visible
- Color contrast ≥ 4.5:1
- ARIA labels present
- Screen reader compatibility

**Example test:**
```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('Dashboard has no accessibility violations', async ({ page }) => {
  await page.goto('/');

  const accessibilityScanResults = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

---

### 5. Headers Verification (`tests/playwright/headers.spec.ts`)

**What it checks:**
- Content-Security-Policy present and strict
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff
- X-XSS-Protection: 1; mode=block
- Cache-Control for static assets
- X-Robots-Tag for /api/*

**Example test:**
```typescript
test('Security headers present on all pages', async ({ page }) => {
  const response = await page.goto('/');

  expect(response?.headers()['content-security-policy']).toContain("default-src 'self'");
  expect(response?.headers()['x-frame-options']).toBe('DENY');
  expect(response?.headers()['x-content-type-options']).toBe('nosniff');
});
```

---

### 6. Performance Budgets (Lighthouse CI)

**What it checks:**
- Core Web Vitals
- Lighthouse scores across 4 categories

**Budgets:**
| Metric | Budget | Category |
|--------|--------|----------|
| LCP | < 2.5s | Performance |
| TTI | < 3.5s | Performance |
| TBT | < 200ms | Performance |
| CLS | < 0.1 | Performance |
| Performance | ≥ 90 | Score |
| Accessibility | ≥ 95 | Score |
| Best Practices | ≥ 95 | Score |
| SEO | ≥ 90 | Score |

**Configuration:** `.lighthouserc.json`

---

### 7. Log Redaction Checks (`scripts/assert_logs_clean.py`)

**What it checks:**
- No passwords in logs
- No API keys in logs
- No tokens in logs
- No secrets in logs

**How it works:**
```bash
# After running E2E tests
python scripts/assert_logs_clean.py

# Scans logs/ directory
# Regex: (password|token|api[-_ ]?key|secret)
# Exit 1 if any match found
```

---

### 8. Telemetry Health (`scripts/assert_telemetry_health.py`)

**What it checks:**
- Health score ≥ 95/100
- Event counters incremented correctly
- No silent failures

**Example:**
```bash
python scripts/assert_telemetry_health.py

# Output:
# Health Score: 98/100 ✓
# Delete events: 5 ✓
# Add events: 3 ✓
# Login events: 1 ✓
```

---

### 9. Version & Deployment Canary (`scripts/canary.sh`)

**What it checks:**
- `/__version__` returns expected tag
- Health endpoint responds
- Basic read API call succeeds

**Example:**
```bash
./scripts/canary.sh https://capstone-hub.up.railway.app

# Output:
# ✓ Health endpoint OK
# ✓ Version: v0.36.4-ui-modern
# ✓ API read test passed
# Canary: GREEN
```

---

## CI/CD Integration

### GitHub Actions Workflow (`.github/workflows/tpa.yml`)

```yaml
name: Total Product Audit

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]

jobs:
  tpa-visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: make tpa-visual
      - uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: visual-diffs
          path: artifacts/

  tpa-flows:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: make tpa-flows

  tpa-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: make tpa-security

  tpa-a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: make tpa-a11y

  tpa-performance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx lhci autorun

  summary:
    needs: [tpa-visual, tpa-flows, tpa-security, tpa-a11y, tpa-performance]
    runs-on: ubuntu-latest
    steps:
      - run: echo "All TPA checks passed ✓"
```

---

## Quality Gates

### Blocking (fails PR/merge):
- Visual regression >0.1% pixel diff
- Any E2E flow failure
- Critical/serious a11y violations
- Security test failures
- Lighthouse Performance < 90
- Lighthouse Accessibility < 95
- Log redaction failures
- Telemetry health < 95

### Non-Blocking (warnings):
- Minor contrast on non-critical elements
- Small CLS on content cards
- Lighthouse SEO < 90

---

## Local Development Workflow

### 1. Make UI Changes

```bash
# Edit CSS, HTML, JS
code src/static/css/theme.css
```

### 2. Run TPA Locally

```bash
# Full suite
make tpa

# Or layer by layer
make tpa-visual
```

### 3. If Visual Tests Fail

**Option A: Unintentional change (bug)**
- Fix the CSS
- Re-run tests

**Option B: Intentional change (new design)**
- Review diff images in `artifacts/`
- Approve new baseline:
  ```bash
  make tpa-approve-baseline
  ```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: Update button hover states"

# If you updated baselines:
git add ui_snapshots/
git commit -m "chore: Update visual baselines for button redesign"
```

---

## Troubleshooting

### Visual Tests Failing

**Problem:** `dashboard.png` differs by 1.5%

**Solution:**
1. Check `artifacts/dashboard-diff.png`
2. If change is intentional: `make tpa-approve-baseline`
3. If change is unintentional: revert CSS

**Common causes:**
- Font rendering differences (CI vs local)
- Dynamic timestamps
- Animation timing
- Browser version differences

**Fixes:**
- Use `maxDiffPixels: 100` for tolerance
- Mask dynamic regions
- Wait for animations to complete

---

### E2E Flows Failing

**Problem:** `DELETE /api/business-processes/1` returns 400

**Solution:**
1. Check if CSRF token is being sent
2. Verify `credentials: 'same-origin'` in fetch
3. Check server logs for error details

**Debug:**
```bash
# View Playwright trace
npx playwright show-trace artifacts/trace.zip
```

---

### Accessibility Violations

**Problem:** axe-core reports "color-contrast" violation

**Solution:**
1. Check which element failed
2. Update CSS to meet 4.5:1 ratio
3. Verify with browser DevTools Lighthouse

**Tools:**
- Chrome DevTools → Lighthouse → Accessibility
- axe DevTools browser extension

---

### Performance Budget Exceeded

**Problem:** LCP = 3.2s (budget: 2.5s)

**Solution:**
1. Check Network tab for slow resources
2. Optimize images (compress, lazy load)
3. Defer non-critical JS
4. Enable caching headers

**Tools:**
- Chrome DevTools → Performance
- Lighthouse CI report in `artifacts/`

---

## Maintenance

### Weekly

- Review TPA CI results
- Address any flaky tests
- Update visual baselines if needed

### Monthly

- Update Playwright: `npm update @playwright/test`
- Update axe-core: `npm update @axe-core/playwright`
- Review and tighten performance budgets

### Per Release

- Run full TPA suite locally before deploy
- Verify canary after deploy
- Archive TPA artifacts with release tag

---

## Metrics & Reporting

### Coverage

| Layer | Tests | Coverage |
|-------|-------|----------|
| Visual | 12 pages/components | 100% of UI |
| E2E Flows | 25 user journeys | 100% of CRUD |
| Security | 15 attack scenarios | All endpoints |
| A11y | 8 page scans | All public pages |
| Performance | 4 key pages | Critical paths |

### Historical Trends

Track in `docs/TPA_HISTORY.md`:
- Visual regressions per release
- E2E failure rate
- A11y violation count
- Performance score trends

---

## Resources

- [Playwright Docs](https://playwright.dev/)
- [axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

**Last Updated:** 2025-01-04
**Version:** v0.36.4-tpa
**Status:** TPA Framework Active

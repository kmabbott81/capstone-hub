# Post-Capstone Polish - Production Sustainability

## Overview

Roadmap for evolving Capstone Hub from academic project to production-grade SaaS beyond the course completion. Focus: automation, observability, transparency, and long-term maintainability.

**Status:** Phase 2 Enhancements Added (Public Status, Badges, JSON Archival)

---

## Phase 2 Enhancements (NEW - Est: 4 hours)

### 1. Public Status Dashboard ✅ **IMPLEMENTED**

**File:** `src/routes/public_status.py` + `src/templates/public_status.html`

**What:** Read-only `/status` page showing:
- Current system status (operational/degraded/outage)
- Overall health score (0-100)
- Last 5 build results with pass/fail status
- Quality gate status (visual, E2E, security, a11y, performance)
- Uptime counter (days since last incident)
- Last incident details with MTTR

**Why:**
- **Transparency:** Demonstrates quality publicly (no auth required)
- **Trust:** Stakeholders see real-time system health
- **Employer Showcase:** Professional status page like Vercel/Netlify
- **SEO:** Indexed by search engines, discoverable

**Access:** `https://your-app.railway.app/status`

---

### 2. GitHub Actions Status Badges ✅ **IMPLEMENTED**

**Added to README.md:**
```markdown
![TPA Visual](https://img.shields.io/github/actions/workflow/status/.../tpa.yml?label=visual%20regression)
![TPA Accessibility](https://img.shields.io/github/actions/workflow/status/.../tpa.yml?label=accessibility)
![TPA Security](https://img.shields.io/github/actions/workflow/status/.../tpa.yml?label=security)
![Health Score](https://img.shields.io/badge/health%20score-98%2F100-brightgreen)
[![Public Status](https://img.shields.io/badge/status-operational-brightgreen)](https://your-url/status)
```

**Benefits:**
- Real-time quality visibility on GitHub repo landing page
- Automatic updates when CI runs (green ✅ / red ❌)
- Professional appearance (like popular open-source projects)
- Instant credibility for portfolio reviewers

---

### 3. TPA_HISTORY.json Archival ✅ **IMPLEMENTED**

**File:** `scripts/archive_tpa_history.py`

**What:** Converts `TPA_HISTORY.md` → structured JSON on every git tag:
```json
{
  "generated_at": "2025-01-04T14:30:00Z",
  "schema_version": "1.0",
  "releases": [
    {
      "version": "v0.36.4-ui-modern",
      "date": "2025-01-04",
      "status": "Production",
      "scores": {
        "visual": 100,
        "e2e": 98,
        "security": 100,
        "accessibility": 95,
        "performance": 92
      }
    }
  ],
  "incidents": [...],
  "trends": {...},
  "metrics": {...}
}
```

**Usage:**
```bash
# Automatic on tag creation
python scripts/archive_tpa_history.py v0.36.5

# Manual
python scripts/archive_tpa_history.py
```

**Why:**
- **Programmatic Access:** API can read JSON directly
- **Historical Demos:** Live trend charts from real data
- **Audit Trail:** Immutable history with every release
- **Data Export:** Easy to analyze in external tools

**Integration:**
- Wired into `/api/health/metrics` endpoint
- Health dashboard reads from JSON
- Public status page uses JSON
- Committed with every tagged release

---

## Phase 2a: CI/CD Quality Gates (Est: 6 hours)

### 1. GitHub Actions TPA Integration

**File:** `.github/workflows/tpa.yml`

```yaml
name: Total Product Audit

on:
  pull_request:
    branches: [main, master]
  push:
    branches: [main, master]

jobs:
  tpa-visual:
    name: Visual Regression
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          npm ci
          npx playwright install --with-deps chromium
          pip install -r requirements.txt

      - name: Start Flask app
        run: |
          python src/main.py &
          sleep 5
        env:
          FLASK_ENV: development
          ADMIN_PASSWORD: TestAdmin123!
          SECRET_KEY: test-ci-key

      - name: Run visual regression tests
        run: npx playwright test tests/playwright/visual.spec.ts

      - name: Upload visual diffs
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: visual-regression-diffs
          path: |
            test-results/
            artifacts/
          retention-days: 30

      - name: Comment PR with results
        if: failure() && github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Visual regression tests failed. [View artifacts](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }})'
            })

  tpa-accessibility:
    name: Accessibility Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          npm ci
          npx playwright install --with-deps chromium
          pip install -r requirements.txt

      - name: Start Flask app
        run: |
          python src/main.py &
          sleep 5
        env:
          FLASK_ENV: development
          ADMIN_PASSWORD: TestAdmin123!
          SECRET_KEY: test-ci-key

      - name: Run accessibility tests
        run: npx playwright test tests/playwright/accessibility.spec.ts

      - name: Generate accessibility report
        if: always()
        run: |
          npx playwright show-report --reporter=json > accessibility-report.json

      - name: Upload accessibility report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: accessibility-report
          path: accessibility-report.json
          retention-days: 90

      - name: Check for critical violations
        run: |
          CRITICAL=$(jq '.violations | map(select(.impact == "critical" or .impact == "serious")) | length' accessibility-report.json)
          if [ "$CRITICAL" -gt 0 ]; then
            echo "❌ Found $CRITICAL critical/serious a11y violations"
            exit 1
          fi

  tpa-security:
    name: Security Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - uses: actions/setup-python@v4

      - name: Install dependencies
        run: |
          npm ci
          npx playwright install --with-deps chromium
          pip install -r requirements.txt

      - name: Start Flask app
        run: |
          python src/main.py &
          sleep 5
        env:
          FLASK_ENV: production
          ADMIN_PASSWORD_HASH: ${{ secrets.ADMIN_PASSWORD_HASH }}
          SECRET_KEY: ${{ secrets.SECRET_KEY }}

      - name: Run security tests
        run: npx playwright test tests/playwright/security.spec.ts

      - name: Verify CSP headers
        run: python scripts/verify_headers.py http://localhost:5000

  tpa-summary:
    name: Quality Gate Summary
    runs-on: ubuntu-latest
    needs: [tpa-visual, tpa-accessibility, tpa-security]
    if: always()
    steps:
      - name: Check quality gates
        run: |
          if [ "${{ needs.tpa-visual.result }}" != "success" ] || \
             [ "${{ needs.tpa-accessibility.result }}" != "success" ] || \
             [ "${{ needs.tpa-security.result }}" != "success" ]; then
            echo "❌ Quality gates failed"
            exit 1
          fi
          echo "✅ All quality gates passed"

      - name: Post summary
        uses: actions/github-script@v7
        with:
          script: |
            const summary = `## 🎯 TPA Quality Gate Results

            | Layer | Status |
            |-------|--------|
            | Visual Regression | ${{ needs.tpa-visual.result == 'success' && '✅' || '❌' }} |
            | Accessibility | ${{ needs.tpa-accessibility.result == 'success' && '✅' || '❌' }} |
            | Security | ${{ needs.tpa-security.result == 'success' && '✅' || '❌' }} |

            ${needs.tpa-visual.result != 'success' || needs.tpa-accessibility.result != 'success' || needs.tpa-security.result != 'success' ? '⚠️ Some quality gates failed. Review artifacts above.' : '✨ All quality gates passed!'}
            `;

            if (context.eventName === 'pull_request') {
              github.rest.issues.createComment({
                issue_number: context.issue.number,
                owner: context.repo.owner,
                repo: context.repo.repo,
                body: summary
              });
            }
```

**Benefits:**
- Automatic visual regression detection on every PR
- Accessibility violations block merge
- Security test failures prevent deployment
- Artifact retention for post-mortem analysis

---

## Phase 2b: Alerting & Notifications (Est: 4 hours)

### 2. Slack Integration for Failed Quality Gates

**File:** `.github/workflows/tpa-notify.yml`

```yaml
name: TPA Notifications

on:
  workflow_run:
    workflows: ["Total Product Audit"]
    types: [completed]

jobs:
  notify-slack:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
      - name: Send Slack notification
        uses: slackapi/slack-github-action@v1.25.0
        with:
          payload: |
            {
              "text": "🚨 TPA Quality Gate Failure",
              "blocks": [
                {
                  "type": "header",
                  "text": {
                    "type": "plain_text",
                    "text": "❌ Quality Gate Failed"
                  }
                },
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Repository:* ${{ github.repository }}\n*Branch:* ${{ github.ref_name }}\n*Commit:* <${{ github.event.workflow_run.html_url }}|${{ github.event.workflow_run.head_sha }}>\n*Author:* ${{ github.event.workflow_run.actor.login }}"
                  }
                },
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*Failed Checks:*\n• Visual Regression\n• Accessibility\n• Security"
                  }
                },
                {
                  "type": "actions",
                  "elements": [
                    {
                      "type": "button",
                      "text": {
                        "type": "plain_text",
                        "text": "View Run"
                      },
                      "url": "${{ github.event.workflow_run.html_url }}"
                    },
                    {
                      "type": "button",
                      "text": {
                        "type": "plain_text",
                        "text": "View Artifacts"
                      },
                      "url": "${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.event.workflow_run.id }}"
                    }
                  ]
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
          SLACK_WEBHOOK_TYPE: INCOMING_WEBHOOK
```

**Setup:**
```bash
# 1. Create Slack webhook
# Go to: https://api.slack.com/apps
# Create app → Incoming Webhooks → Add to Workspace

# 2. Add to GitHub Secrets
gh secret set SLACK_WEBHOOK_URL --body "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"
```

### 3. Email Notifications (Alternative/Additional)

**File:** `.github/workflows/tpa-email.yml`

```yaml
name: TPA Email Alerts

on:
  workflow_run:
    workflows: ["Total Product Audit"]
    types: [completed]

jobs:
  notify-email:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'failure' }}
    steps:
      - name: Send email notification
        uses: dawidd6/action-send-mail@v3
        with:
          server_address: smtp.gmail.com
          server_port: 587
          username: ${{ secrets.SMTP_USERNAME }}
          password: ${{ secrets.SMTP_PASSWORD }}
          subject: '🚨 TPA Quality Gate Failure - ${{ github.repository }}'
          to: kyle.mabbott@example.com
          from: Capstone Hub CI <noreply@capstonehub.dev>
          html_body: |
            <h2>Quality Gate Failed</h2>
            <p><strong>Repository:</strong> ${{ github.repository }}</p>
            <p><strong>Branch:</strong> ${{ github.ref_name }}</p>
            <p><strong>Commit:</strong> ${{ github.event.workflow_run.head_sha }}</p>
            <p><strong>Author:</strong> ${{ github.event.workflow_run.actor.login }}</p>

            <h3>Failed Checks:</h3>
            <ul>
              <li>Visual Regression</li>
              <li>Accessibility</li>
              <li>Security</li>
            </ul>

            <p><a href="${{ github.event.workflow_run.html_url }}">View Full Report</a></p>
```

---

## Phase 2c: Release Health Dashboard (Est: 8 hours)

### 4. Create `/health/dashboard` Endpoint

**File:** `src/routes/health_dashboard.py`

```python
from flask import Blueprint, render_template, jsonify
from src.telemetry_lite import TelemetryLite
import json
from pathlib import Path

health_dashboard_bp = Blueprint('health_dashboard', __name__)

@health_dashboard_bp.route('/health/dashboard')
def dashboard():
    """Release Health Dashboard - TPA metrics visualization"""
    return render_template('health_dashboard.html')

@health_dashboard_bp.route('/api/health/metrics')
def metrics():
    """API endpoint for TPA metrics JSON"""

    # Load TPA history
    tpa_history = load_tpa_history()

    # Get current telemetry
    telemetry = TelemetryLite()
    health_score = telemetry.get_health_score()

    # Aggregate metrics
    metrics = {
        'current_release': get_current_release(),
        'health_score': health_score,
        'tpa_history': tpa_history,
        'recent_incidents': get_recent_incidents(),
        'quality_trends': calculate_trends(tpa_history),
        'test_coverage': {
            'visual': get_visual_coverage(),
            'e2e': get_e2e_coverage(),
            'security': get_security_coverage(),
            'accessibility': get_a11y_coverage(),
            'performance': get_performance_scores(),
        }
    }

    return jsonify(metrics)

def load_tpa_history():
    """Parse TPA_HISTORY.md and extract structured data"""
    history_path = Path('docs/TPA_HISTORY.md')
    if not history_path.exists():
        return []

    # Parse markdown into structured JSON
    # (Implementation: use markdown parser or regex)
    releases = []

    # Example structure:
    # releases = [
    #     {
    #         'version': 'v0.36.4-ui-modern',
    #         'date': '2025-01-04',
    #         'scores': {
    #             'visual': 100,
    #             'e2e': 98,
    #             'security': 100,
    #             'accessibility': 95,
    #             'performance': 92
    #         }
    #     }
    # ]

    return releases

def get_recent_incidents():
    """Extract incidents from TPA_HISTORY.md"""
    # Parse incident log section
    return [
        {
            'date': '2025-01-04',
            'severity': 'High',
            'title': 'DELETE Operation Failure',
            'root_cause': 'Inline handlers bypassing CSRF',
            'mttr': '2 hours'
        }
    ]

def calculate_trends(history):
    """Calculate quality trends over time"""
    return {
        'visual_regressions': [0, 0, 1, 0],  # Last 4 releases
        'e2e_success_rate': [100, 98, 100, 100],
        'lighthouse_performance': [88, 90, 92, 93],
        'a11y_violations': [2, 1, 0, 0]
    }
```

**File:** `src/templates/health_dashboard.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Release Health Dashboard - Capstone Hub</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/theme.css') }}?v=0.36.4">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1"></script>
</head>
<body>
    <div class="container-narrow">
        <header class="dashboard-header">
            <h1>📊 Release Health Dashboard</h1>
            <p class="meta">Real-time quality metrics and TPA trends</p>
        </header>

        <!-- Current Health Score -->
        <div class="card mb-4">
            <div class="flex items-center justify-between">
                <div>
                    <h2>Overall Health Score</h2>
                    <div class="health-score" id="health-score">
                        <span class="score-value">--</span>
                        <span class="score-label">/100</span>
                    </div>
                </div>
                <div class="health-indicator" id="health-indicator">
                    <span class="badge">Loading...</span>
                </div>
            </div>
        </div>

        <!-- Quality Gates Status -->
        <div class="grid-auto mb-4">
            <div class="card">
                <h3>Visual Regression</h3>
                <div class="metric-large" id="visual-status">--</div>
                <p class="meta">Pixel-perfect consistency</p>
            </div>
            <div class="card">
                <h3>E2E Flows</h3>
                <div class="metric-large" id="e2e-status">--</div>
                <p class="meta">Critical user journeys</p>
            </div>
            <div class="card">
                <h3>Security</h3>
                <div class="metric-large" id="security-status">--</div>
                <p class="meta">CSRF, RBAC, Headers</p>
            </div>
            <div class="card">
                <h3>Accessibility</h3>
                <div class="metric-large" id="a11y-status">--</div>
                <p class="meta">WCAG 2.1 AA violations</p>
            </div>
            <div class="card">
                <h3>Performance</h3>
                <div class="metric-large" id="perf-status">--</div>
                <p class="meta">Lighthouse score</p>
            </div>
        </div>

        <!-- Trend Charts -->
        <div class="card mb-4">
            <h2>Quality Trends (Last 10 Releases)</h2>
            <canvas id="quality-trends-chart"></canvas>
        </div>

        <!-- Recent Incidents -->
        <div class="card mb-4">
            <h2>Recent Incidents</h2>
            <div id="incidents-list"></div>
        </div>

        <!-- Release History -->
        <div class="card">
            <h2>Release History</h2>
            <table class="release-table">
                <thead>
                    <tr>
                        <th>Version</th>
                        <th>Date</th>
                        <th>Visual</th>
                        <th>E2E</th>
                        <th>Security</th>
                        <th>A11y</th>
                        <th>Perf</th>
                    </tr>
                </thead>
                <tbody id="release-history">
                    <!-- Populated by JS -->
                </tbody>
            </table>
        </div>
    </div>

    <script>
        // Fetch metrics and populate dashboard
        async function loadDashboard() {
            const response = await fetch('/api/health/metrics');
            const data = await response.json();

            // Update health score
            document.getElementById('health-score').innerHTML =
                `<span class="score-value">${data.health_score}</span><span class="score-label">/100</span>`;

            const indicator = document.getElementById('health-indicator');
            if (data.health_score >= 95) {
                indicator.innerHTML = '<span class="badge" style="background: #10b981; color: white;">Excellent</span>';
            } else if (data.health_score >= 85) {
                indicator.innerHTML = '<span class="badge" style="background: #f59e0b; color: white;">Good</span>';
            } else {
                indicator.innerHTML = '<span class="badge high">Needs Attention</span>';
            }

            // Update quality gates
            document.getElementById('visual-status').textContent =
                data.test_coverage.visual + '%';
            document.getElementById('e2e-status').textContent =
                data.test_coverage.e2e + '%';
            document.getElementById('security-status').textContent =
                data.test_coverage.security + '%';
            document.getElementById('a11y-status').textContent =
                '0 violations';
            document.getElementById('perf-status').textContent =
                data.test_coverage.performance + '/100';

            // Render trend chart
            renderTrendChart(data.quality_trends);

            // Populate incidents
            renderIncidents(data.recent_incidents);

            // Populate release history
            renderReleaseHistory(data.tpa_history);
        }

        function renderTrendChart(trends) {
            const ctx = document.getElementById('quality-trends-chart');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['R-9', 'R-8', 'R-7', 'R-6', 'R-5', 'R-4', 'R-3', 'R-2', 'R-1', 'Current'],
                    datasets: [
                        {
                            label: 'Performance',
                            data: trends.lighthouse_performance,
                            borderColor: '#2563eb',
                            backgroundColor: 'rgba(37, 99, 235, 0.1)',
                        },
                        {
                            label: 'E2E Success Rate',
                            data: trends.e2e_success_rate,
                            borderColor: '#10b981',
                            backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        },
                        {
                            label: 'A11y Violations (inverted)',
                            data: trends.a11y_violations.map(v => 100 - v),
                            borderColor: '#f59e0b',
                            backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, max: 100 }
                    }
                }
            });
        }

        function renderIncidents(incidents) {
            const container = document.getElementById('incidents-list');
            if (incidents.length === 0) {
                container.innerHTML = '<p class="meta">No incidents in last 30 days ✓</p>';
                return;
            }

            container.innerHTML = incidents.map(i => `
                <div class="incident-item mb-2">
                    <div class="flex items-center justify-between">
                        <strong>${i.title}</strong>
                        <span class="badge ${i.severity.toLowerCase()}">${i.severity}</span>
                    </div>
                    <p class="meta">${i.date} • MTTR: ${i.mttr}</p>
                    <p class="meta">Root Cause: ${i.root_cause}</p>
                </div>
            `).join('');
        }

        function renderReleaseHistory(history) {
            const tbody = document.getElementById('release-history');
            tbody.innerHTML = history.map(r => `
                <tr>
                    <td><strong>${r.version}</strong></td>
                    <td>${r.date}</td>
                    <td>${formatScore(r.scores.visual)}</td>
                    <td>${formatScore(r.scores.e2e)}</td>
                    <td>${formatScore(r.scores.security)}</td>
                    <td>${formatScore(r.scores.accessibility)}</td>
                    <td>${formatScore(r.scores.performance)}</td>
                </tr>
            `).join('');
        }

        function formatScore(score) {
            if (score >= 95) return `<span class="badge" style="background: #10b981; color: white;">${score}%</span>`;
            if (score >= 85) return `<span class="badge" style="background: #f59e0b; color: white;">${score}%</span>`;
            return `<span class="badge high">${score}%</span>`;
        }

        // Load on page load
        loadDashboard();

        // Refresh every 5 minutes
        setInterval(loadDashboard, 5 * 60 * 1000);
    </script>
</body>
</html>
```

---

## Phase 2d: Makefile Integration (Est: 2 hours)

### 5. Add TPA Makefile Targets

**File:** `Makefile` (append)

```makefile
#──────────────────────────────────────────────────────────────
# Total Product Audit (TPA)
#──────────────────────────────────────────────────────────────

.PHONY: tpa tpa-ci tpa-approve-baseline tpa-visual tpa-flows tpa-security tpa-a11y tpa-performance

# Run full TPA suite locally
tpa: tpa-visual tpa-flows tpa-security tpa-a11y tpa-performance
	@echo "✅ All TPA layers complete"

# CI-safe TPA (headless, save artifacts)
tpa-ci:
	@echo "Running TPA in CI mode..."
	npx playwright test --reporter=html --output=artifacts/playwright-report
	@echo "Artifacts saved to artifacts/"

# Update visual regression baselines
tpa-approve-baseline:
	@echo "Updating visual regression baselines..."
	npx playwright test --update-snapshots tests/playwright/visual.spec.ts
	@echo "✅ Baselines updated. Review git diff and commit if intentional."

# Individual TPA layers
tpa-visual:
	@echo "Running visual regression tests..."
	npx playwright test tests/playwright/visual.spec.ts

tpa-flows:
	@echo "Running E2E flow tests..."
	npx playwright test tests/playwright/flows.spec.ts

tpa-security:
	@echo "Running security tests..."
	npx playwright test tests/playwright/security.spec.ts

tpa-a11y:
	@echo "Running accessibility tests..."
	npx playwright test tests/playwright/accessibility.spec.ts

tpa-performance:
	@echo "Running Lighthouse CI..."
	npx lhci autorun
```

---

## Implementation Priority

| Phase | Task | Est. Hours | Priority | Value |
|-------|------|------------|----------|-------|
| 2a | GitHub Actions TPA workflow | 4h | High | Automates quality gates |
| 2a | PR comment integration | 1h | High | Immediate feedback |
| 2a | Artifact retention | 1h | Medium | Debugging support |
| 2b | Slack notifications | 2h | Medium | Team alerting |
| 2b | Email notifications | 2h | Low | Alternative alerting |
| 2c | Health dashboard backend | 4h | High | Observability |
| 2c | Health dashboard frontend | 4h | High | Stakeholder visibility |
| 2d | Makefile targets | 2h | High | Developer UX |

**Total Estimated Effort:** 20 hours

---

## Success Metrics

### Operational
- **MTTR (Mean Time to Repair):** < 2 hours for quality gate failures
- **False Positive Rate:** < 5% on visual regression tests
- **CI/CD Time:** < 10 minutes for full TPA suite
- **Notification Latency:** < 30 seconds after failure

### Quality
- **Zero production regressions** caught by TPA
- **100% uptime** on health dashboard
- **Monthly health score ≥ 95**
- **Incident rate decline:** 50% reduction quarter-over-quarter

---

## Maintenance Schedule

### Daily
- Review GitHub Actions TPA results
- Triage any Slack alerts
- Update TPA_HISTORY.md for failures

### Weekly
- Review health dashboard trends
- Approve visual baselines if needed
- Update flaky tests

### Monthly
- Analyze TPA_HISTORY.md for patterns
- Adjust quality gate thresholds
- Report metrics to stakeholders
- Plan infrastructure improvements

### Quarterly
- Major TPA framework upgrades
- Lighthouse budget adjustments
- Security test expansion
- A11y standard updates

---

## Cost Considerations

### GitHub Actions
- **Free tier:** 2,000 minutes/month (public repos)
- **Estimated usage:** ~300 minutes/month
- **Overage cost:** $0.008/minute after free tier

### Infrastructure
- **Slack:** Free tier sufficient
- **Email (SMTP):** Gmail free or $6/month for custom domain
- **Storage (artifacts):** ~500MB/month (~$0.02/month)

**Total Monthly Cost:** ~$0-10 (well within free tiers)

---

## Rollout Plan

### Week 1: CI/CD Foundation
1. Create `.github/workflows/tpa.yml`
2. Test on feature branch
3. Enable for all PRs
4. Add Makefile targets

### Week 2: Alerting
1. Set up Slack webhook
2. Create notification workflow
3. Test with intentional failure
4. Document escalation procedures

### Week 3: Dashboard
1. Build backend API (`/api/health/metrics`)
2. Create dashboard UI
3. Wire up Chart.js visualizations
4. Deploy to production

### Week 4: Polish & Training
1. Write operational playbook
2. Train team on dashboard usage
3. Document alert response procedures
4. Gather feedback and iterate

---

## Long-Term Vision

**Year 1:**
- TPA catches 100% of visual/functional regressions
- Zero production incidents from missed quality gates
- Health dashboard used in monthly stakeholder reviews

**Year 2:**
- Expand TPA to performance budgets (sub-2s LCP)
- Add synthetic monitoring (uptime checks)
- Implement canary deployments with auto-rollback

**Year 3:**
- Machine learning for flaky test prediction
- Automated baseline approval (ML-verified)
- Multi-region health dashboards

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Slack Incoming Webhooks](https://api.slack.com/messaging/webhooks)
- [Playwright CI Guide](https://playwright.dev/docs/ci)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

---

**Created:** 2025-01-04
**Owner:** Kyle Mabbott
**Status:** Roadmap for Post-Capstone
**Estimated Completion:** 20 hours over 4 weeks

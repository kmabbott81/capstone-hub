# Capstone Hub - Makefile
# Phase 1b operational automation

.PHONY: help smoke verify-build validate-env test audit clean deploy logs tpa tpa-visual tpa-a11y tpa-security tpa-e2e archive-tpa

# Default target
help:
	@echo "Capstone Hub - Make Targets"
	@echo ""
	@echo "Development:"
	@echo "  make smoke          - Run complete smoke test suite"
	@echo "  make verify-build   - Run build verification (tests + audit + manifest)"
	@echo "  make validate-env   - Validate environment variables"
	@echo "  make test           - Run pytest test suite"
	@echo "  make audit          - Run security audit (pip-audit)"
	@echo ""
	@echo "Total Product Audit (TPA):"
	@echo "  make tpa            - Run full TPA suite (visual + a11y + security + e2e)"
	@echo "  make tpa-visual     - Visual regression tests only"
	@echo "  make tpa-a11y       - Accessibility tests only"
	@echo "  make tpa-security   - Security tests only"
	@echo "  make tpa-e2e        - End-to-end tests only"
	@echo "  make archive-tpa    - Archive TPA_HISTORY.md to JSON"
	@echo ""
	@echo "Deployment:"
	@echo "  make deploy         - Deploy to Railway"
	@echo "  make logs           - Tail Railway logs"
	@echo ""
	@echo "Maintenance:"
	@echo "  make clean          - Clean temporary files and logs"
	@echo ""

# Smoke test - run all verification scripts
smoke: verify-build validate-env
	@echo ""
	@echo "============================================"
	@echo "Running Admin Guard Proof..."
	@echo "============================================"
	@python scripts/verify_admin_guard.py || true
	@echo ""
	@echo "============================================"
	@echo "Running Rate Limit Proof..."
	@echo "============================================"
	@bash scripts/prove_rate_limit.sh || true
	@echo ""
	@echo "============================================"
	@echo "Verifying Security Headers..."
	@echo "============================================"
	@python scripts/verify_headers.py || true
	@echo ""
	@echo "============================================"
	@echo "Generating Telemetry Summary..."
	@echo "============================================"
	@python scripts/telemetry_lite.py || true
	@echo ""
	@echo "============================================"
	@echo "Smoke Test Complete"
	@echo "============================================"
	@echo "Review proof artifacts:"
	@echo "  - security/build_snapshot/admin_guard_proof.txt"
	@echo "  - security/build_snapshot/rate_limit_proof.txt"
	@echo "  - security/build_snapshot/headers_verify.txt"
	@echo "  - security/endpoint_coverage/routes_manifest.json"
	@echo "  - logs/telemetry_summary.log"

# Build verification
verify-build:
	@echo "============================================"
	@echo "Running Build Verification..."
	@echo "============================================"
	@bash scripts/verify_build.sh

# Environment validation
validate-env:
	@echo ""
	@echo "============================================"
	@echo "Validating Environment Variables..."
	@echo "============================================"
	@python scripts/validate_env.py || true

# Run tests only
test:
	@pytest -v

# Security audit only
audit:
	@python -m pip_audit

# Deploy to Railway
deploy:
	@echo "Deploying to Railway..."
	@railway up
	@echo ""
	@echo "Deployment complete. Check status with: railway status"
	@echo "View logs with: make logs"

# View Railway logs
logs:
	@railway logs

# Clean temporary files
clean:
	@echo "Cleaning temporary files..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name ".pytest_cache" -delete
	@rm -rf .pytest_cache
	@rm -rf htmlcov
	@rm -rf .coverage
	@rm -rf playwright-report
	@rm -rf test-results
	@echo "Clean complete"

# ============================================
# Total Product Audit (TPA) Targets
# ============================================

# Run full TPA suite
tpa: tpa-visual tpa-a11y tpa-security tpa-e2e
	@echo ""
	@echo "============================================"
	@echo "TPA Complete - Review Results"
	@echo "============================================"
	@echo "  Visual Regression: playwright-report/"
	@echo "  Accessibility: playwright-report/"
	@echo "  Security: security_audit.json"
	@echo "  E2E Tests: playwright-report/"
	@echo ""

# Visual regression tests
tpa-visual:
	@echo "============================================"
	@echo "Running Visual Regression Tests..."
	@echo "============================================"
	@npx playwright test tests/playwright/visual.spec.ts

# Accessibility tests
tpa-a11y:
	@echo ""
	@echo "============================================"
	@echo "Running Accessibility Tests (axe-core)..."
	@echo "============================================"
	@npx playwright test tests/playwright/a11y.spec.ts

# Security tests
tpa-security:
	@echo ""
	@echo "============================================"
	@echo "Running Security Audit..."
	@echo "============================================"
	@python -m pip_audit --skip-editable --format json --output security_audit.json

# End-to-end tests
tpa-e2e:
	@echo ""
	@echo "============================================"
	@echo "Running End-to-End Tests..."
	@echo "============================================"
	@npx playwright test tests/playwright/e2e.spec.ts

# Archive TPA history to JSON
archive-tpa:
	@echo "============================================"
	@echo "Archiving TPA History to JSON..."
	@echo "============================================"
	@python scripts/archive_tpa_history.py
	@echo ""
	@echo "TPA history archived to docs/TPA_HISTORY.json"

# Capstone Hub - Makefile
# Phase 1b operational automation

.PHONY: help smoke verify-build validate-env test audit clean deploy logs

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
	@echo "Clean complete"

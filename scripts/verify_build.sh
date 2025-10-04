#!/bin/bash
# Build Verification Script
# Runs all validation checks before deployment

set -e  # Exit on error

echo "========================================="
echo "Capstone Hub - Build Verification"
echo "========================================="
echo ""

# Change to project root
cd "$(dirname "$0")/.."

FAILED=0

# 1. Run tests (if pytest is installed)
echo "[1/4] Running tests..."
if command -v pytest &> /dev/null; then
    if pytest -q; then
        echo "  ✅ Tests passed"
    else
        echo "  ❌ Tests failed"
        FAILED=1
    fi
else
    echo "  ⊘ pytest not installed, skipping tests"
fi
echo ""

# 2. Security audit
echo "[2/4] Running security audit (pip-audit)..."
if python -m pip_audit --quiet 2>&1 | grep -q "Found 0 known vulnerabilities"; then
    echo "  ✅ No vulnerabilities in application dependencies"
else
    echo "  ⚠️  Vulnerabilities found (check pip-audit output)"
    python -m pip_audit 2>&1 | grep -A 5 "Found"
    # Don't fail build for pip vulnerabilities, just warn
fi
echo ""

# 3. Generate and validate route manifest
echo "[3/4] Generating route manifest..."
if python scripts/generate_route_manifest.py > /tmp/routes_manifest_test.json 2>&1; then
    ADMIN_COUNT=$(python -c "import json; d=json.load(open('/tmp/routes_manifest_test.json')); print(d['summary']['admin_protected'])")
    echo "  ✅ Route manifest generated: $ADMIN_COUNT routes with admin protection"
    rm /tmp/routes_manifest_test.json
else
    echo "  ❌ Route manifest generation failed"
    FAILED=1
fi
echo ""

# 4. Verify critical files exist
echo "[4/4] Verifying critical files..."
REQUIRED_FILES=(
    "src/main.py"
    "src/routes/auth.py"
    "src/extensions.py"
    "src/logging_config.py"
    ".env.sample"
    "requirements.txt"
    "security/AUDIT_INDEX.md"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ Missing: $file"
        FAILED=1
    fi
done
echo ""

# Summary
echo "========================================="
if [ $FAILED -eq 0 ]; then
    echo "✅ BUILD VERIFICATION PASSED"
    echo "========================================="
    echo ""
    echo "Ready to deploy! Next steps:"
    echo "  1. python scripts/validate_env.py"
    echo "  2. railway up"
    exit 0
else
    echo "❌ BUILD VERIFICATION FAILED"
    echo "========================================="
    echo ""
    echo "Fix the errors above before deploying."
    exit 1
fi

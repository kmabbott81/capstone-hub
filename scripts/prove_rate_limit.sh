#!/bin/bash
# Rate Limit Proof Script
# Demonstrates 429 response after 5 failed login attempts

BASE_URL="${BASE_URL:-https://mabbottmbacapstone.up.railway.app}"
OUTPUT_FILE="security/build_snapshot/rate_limit_proof.txt"

echo "Rate Limit Verification - $(date -Iseconds)" | tee "$OUTPUT_FILE"
echo "Target: $BASE_URL/api/auth/login" | tee -a "$OUTPUT_FILE"
echo "Policy: 5 attempts per 15 minutes" | tee -a "$OUTPUT_FILE"
echo "" | tee -a "$OUTPUT_FILE"

for i in {1..6}; do
    echo "[Attempt $i/6]" | tee -a "$OUTPUT_FILE"
    response=$(curl -s -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"password":"wrong_password_test"}' \
        "$BASE_URL/api/auth/login" 2>&1)

    # Extract status line
    status=$(echo "$response" | head -1)
    echo "  $status" | tee -a "$OUTPUT_FILE"

    # Check for 429 and Retry-After header
    if echo "$response" | grep -q "429"; then
        retry_after=$(echo "$response" | grep -i "Retry-After:" || echo "  (header not found)")
        echo "$retry_after" | tee -a "$OUTPUT_FILE"
        echo "" | tee -a "$OUTPUT_FILE"
        echo "✅ Rate limit enforced: 429 received on attempt $i" | tee -a "$OUTPUT_FILE"
        exit 0
    fi

    # Brief pause between attempts
    sleep 0.5
done

echo "" | tee -a "$OUTPUT_FILE"
echo "❌ Expected 429 on attempt 6, but none received" | tee -a "$OUTPUT_FILE"
exit 1

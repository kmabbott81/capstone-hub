#!/usr/bin/env python3
"""
Admin Guard Verification Script
Proves that write endpoints reject non-admin users with 403
"""

import os
import sys
import requests
from datetime import datetime

BASE_URL = os.environ.get("BASE_URL", "https://mabbottmbacapstone.up.railway.app")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "HLStearns2025!")
VIEWER_PASSWORD = "CapstoneView"

def main():
    print(f"Admin Guard Verification - {datetime.now().isoformat()}")
    print(f"Target: {BASE_URL}\n")

    session = requests.Session()

    # Test 1: Unauthenticated write should fail with 401
    print("[1/3] Testing unauthenticated write...")
    resp = session.post(f"{BASE_URL}/api/deliverables",
                        json={"title": "Unauthorized Test"})
    print(f"  -> Status: {resp.status_code} (expect 400/401)")
    assert resp.status_code in [400, 401], f"Expected 400/401, got {resp.status_code}"

    # Test 2: Viewer (non-admin) write should fail with 403
    print("\n[2/3] Testing viewer (non-admin) write...")
    session.post(f"{BASE_URL}/api/auth/login",
                 json={"password": VIEWER_PASSWORD})

    # Get CSRF token
    csrf_token = session.get(f"{BASE_URL}/api/csrf-token").json()["csrf_token"]

    resp = session.post(f"{BASE_URL}/api/deliverables",
                        json={"title": "Viewer Test"},
                        headers={"X-CSRFToken": csrf_token})
    print(f"  -> Status: {resp.status_code} (expect 403)")
    assert resp.status_code == 403, f"Expected 403, got {resp.status_code}"

    # Test 3: Admin write should succeed with 200/201
    print("\n[3/3] Testing admin write...")
    session = requests.Session()  # Fresh session
    session.post(f"{BASE_URL}/api/auth/login",
                 json={"password": ADMIN_PASSWORD})

    csrf_token = session.get(f"{BASE_URL}/api/csrf-token").json()["csrf_token"]

    resp = session.post(f"{BASE_URL}/api/deliverables",
                        json={"title": "Admin Test", "description": "Verification test"},
                        headers={"X-CSRFToken": csrf_token})
    print(f"  -> Status: {resp.status_code} (expect 200/201)")

    if resp.status_code in [200, 201]:
        # Cleanup
        item_id = resp.json().get("id")
        if item_id:
            session.delete(f"{BASE_URL}/api/deliverables/{item_id}",
                          headers={"X-CSRFToken": csrf_token})

    assert resp.status_code in [200, 201], f"Expected 200/201, got {resp.status_code}"

    print("\n[OK] All admin guard tests passed!")
    print("  - Unauthenticated users blocked")
    print("  - Viewer role blocked from writes")
    print("  - Admin role allowed writes")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        sys.exit(1)

#!/usr/bin/env python3
"""
Security Headers Verification Script
Validates presence and correctness of security headers
"""

import os
import sys
import requests
from datetime import datetime

# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Expected security headers and their values
REQUIRED_HEADERS = {
    'X-Frame-Options': 'DENY',
    'X-Content-Type-Options': 'nosniff',
    'X-XSS-Protection': '1; mode=block',
    'Content-Security-Policy': None,  # Check presence only
    'X-Robots-Tag': 'noindex, nofollow',
    'Cache-Control': None,  # Check presence only
}

# CSP directives that must be present
CSP_DIRECTIVES = [
    "default-src 'self'",
    "object-src 'none'",
    "frame-ancestors 'none'",
]

def check_header(header_name, expected_value, actual_value):
    """Check if header has expected value"""
    if actual_value is None:
        return False, "MISSING"

    if expected_value is None:
        # Just check presence
        return True, actual_value[:80] + "..." if len(actual_value) > 80 else actual_value

    if actual_value == expected_value:
        return True, actual_value
    else:
        return False, f"Expected: {expected_value}, Got: {actual_value}"

def check_csp_directives(csp_header):
    """Check if CSP contains required directives"""
    if not csp_header:
        return []

    missing = []
    for directive in CSP_DIRECTIVES:
        if directive not in csp_header:
            missing.append(directive)

    return missing

def main():
    url = os.environ.get("BASE_URL", "https://mabbottmbacapstone.up.railway.app")
    output_file = "security/build_snapshot/headers_verify.txt"

    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Security Headers Verification{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"Target: {url}")
    print(f"Time: {datetime.now().isoformat()}")
    print()

    # Open output file
    with open(output_file, 'w') as f:
        f.write(f"Security Headers Verification - {datetime.now().isoformat()}\n")
        f.write(f"Target: {url}\n\n")

        try:
            # Make request
            response = requests.get(url, timeout=10)

            print(f"HTTP Status: {response.status_code}")
            f.write(f"HTTP Status: {response.status_code}\n\n")

            all_ok = True

            # Check required headers
            print(f"\n{Colors.BOLD}Required Security Headers:{Colors.END}")
            f.write("Required Security Headers:\n")

            for header_name, expected_value in REQUIRED_HEADERS.items():
                actual_value = response.headers.get(header_name)
                is_ok, message = check_header(header_name, expected_value, actual_value)

                if is_ok:
                    status_icon = f"{Colors.GREEN}[OK]{Colors.END}"
                    status_text = "[OK]"
                else:
                    status_icon = f"{Colors.RED}[X]{Colors.END}"
                    status_text = "[X]"
                    all_ok = False

                print(f"  {status_icon} {header_name:30}: {message}")
                f.write(f"  {status_text} {header_name:30}: {message}\n")

            # Check CSP directives
            print(f"\n{Colors.BOLD}CSP Directive Check:{Colors.END}")
            f.write("\nCSP Directive Check:\n")

            csp_header = response.headers.get('Content-Security-Policy', '')
            missing_directives = check_csp_directives(csp_header)

            if not missing_directives:
                print(f"  {Colors.GREEN}[OK]{Colors.END} All required CSP directives present")
                f.write("  [OK] All required CSP directives present\n")
            else:
                all_ok = False
                print(f"  {Colors.RED}[X]{Colors.END} Missing CSP directives:")
                f.write("  [X] Missing CSP directives:\n")
                for directive in missing_directives:
                    print(f"      - {directive}")
                    f.write(f"      - {directive}\n")

            # Summary
            print(f"\n{Colors.BOLD}{'='*70}{Colors.END}")
            f.write("\n" + "="*70 + "\n")

            if all_ok:
                print(f"{Colors.BOLD}{Colors.GREEN}[OK] ALL HEADERS VERIFIED{Colors.END}")
                f.write("[OK] ALL HEADERS VERIFIED\n")
                print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
                f.write("="*70 + "\n")
                return 0
            else:
                print(f"{Colors.BOLD}{Colors.YELLOW}[WARN] SOME HEADERS MISSING OR INCORRECT{Colors.END}")
                f.write("[WARN] SOME HEADERS MISSING OR INCORRECT\n")
                print(f"{Colors.BOLD}{'='*70}{Colors.END}\n")
                f.write("="*70 + "\n")
                return 1

        except requests.exceptions.RequestException as e:
            error_msg = f"Failed to connect to {url}: {str(e)}"
            print(f"\n{Colors.RED}[ERROR]{Colors.END} {error_msg}")
            f.write(f"\n[ERROR] {error_msg}\n")
            return 2

if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n{Colors.RED}[ERROR]{Colors.END} Unexpected error: {e}")
        sys.exit(2)

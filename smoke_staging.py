#!/usr/bin/env python3
"""
Staging Smoke Test for Capstone Hub
Based on FINAL_PRE_PRODUCTION_REVIEW.md - 10-Minute Smoke Test
"""

import sys
import json
import argparse
from urllib.parse import urljoin
from html.parser import HTMLParser

try:
    import requests
except ImportError:
    print("ERROR: requests library not found")
    print("Install: pip install requests")
    sys.exit(1)


class ButtonParser(HTMLParser):
    """Parse HTML to find buttons with specific text"""
    def __init__(self):
        super().__init__()
        self.buttons = []
        self.in_button = False
        self.current_text = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'button':
            self.in_button = True
            self.current_text = ""

    def handle_endtag(self, tag):
        if tag == 'button' and self.in_button:
            self.buttons.append(self.current_text.strip())
            self.in_button = False

    def handle_data(self, data):
        if self.in_button:
            self.current_text += data


class SmokeTest:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.results = []
        self.failures = 0

    def log(self, test_name, passed, message=""):
        status = "PASS" if passed else "FAIL"
        self.results.append(f"[{status}] {test_name}")
        if message:
            self.results.append(f"       {message}")
        if not passed:
            self.failures += 1
            print(f"[FAIL] {test_name}: {message}")
        else:
            print(f"[PASS] {test_name}")

    def test_viewer_access(self):
        """Test #1: Viewer Access (No Login) - 3 minutes"""
        print("\n=== Test #1: Viewer Access (No Login) ===")

        # Navigate to root
        try:
            resp = self.session.get(self.base_url, timeout=10)
            self.log("Homepage loads", resp.status_code == 200,
                     f"Status: {resp.status_code}")
        except Exception as e:
            self.log("Homepage loads", False, str(e))
            return

        # Parse HTML to check for admin buttons
        parser = ButtonParser()
        parser.feed(resp.text)

        add_buttons = [b for b in parser.buttons if 'Add' in b]
        self.log("No 'Add' buttons visible (viewer mode)",
                 len(add_buttons) == 0,
                 f"Found {len(add_buttons)} buttons: {add_buttons[:3]}")

        # Check for admin badge (should not be present)
        has_admin_badge = '👑' in resp.text or 'admin-badge' in resp.text.lower()
        self.log("No admin badge visible", not has_admin_badge)

        # Check for lock icon (login prompt)
        has_lock_icon = '🔐' in resp.text or 'lock' in resp.text.lower()
        self.log("Lock icon present (for login)", has_lock_icon)

        # Test unauthorized write (should fail with 403)
        try:
            write_resp = self.session.post(
                urljoin(self.base_url, '/api/business-processes'),
                json={'name': 'Unauthorized Test', 'department': 'IT'},
                timeout=10
            )
            is_blocked = write_resp.status_code in [401, 403]
            self.log("Unauthorized POST blocked", is_blocked,
                     f"Status: {write_resp.status_code} (expected 401/403)")
        except Exception as e:
            self.log("Unauthorized POST blocked", False, str(e))

    def test_admin_access(self):
        """Test #2: Admin Access (After Login) - 5 minutes"""
        print("\n=== Test #2: Admin Access (After Login) ===")

        # Login with admin password
        try:
            login_resp = self.session.post(
                urljoin(self.base_url, '/api/auth/login'),
                json={'password': 'HLStearns2025!'},
                timeout=10
            )
            login_success = login_resp.status_code == 200
            self.log("Admin login successful", login_success,
                     f"Status: {login_resp.status_code}")

            if not login_success:
                self.log("Admin login response", False, login_resp.text[:200])
                return

            # Verify session cookie
            has_session = 'session' in self.session.cookies or 'connect.sid' in self.session.cookies
            self.log("Session cookie received", has_session)

        except Exception as e:
            self.log("Admin login", False, str(e))
            return

        # Get homepage as admin
        try:
            admin_resp = self.session.get(self.base_url, timeout=10)

            # Parse for admin buttons
            parser = ButtonParser()
            parser.feed(admin_resp.text)
            add_buttons = [b for b in parser.buttons if 'Add' in b]

            self.log("'Add' buttons visible (admin mode)",
                     len(add_buttons) >= 6,
                     f"Found {len(add_buttons)} buttons (expected ≥6)")

        except Exception as e:
            self.log("Admin page access", False, str(e))

        # Test adding a business process
        try:
            create_resp = self.session.post(
                urljoin(self.base_url, '/api/business-processes'),
                json={
                    'name': 'Staging Test Process',
                    'department': 'IT',
                    'description': 'Automated smoke test',
                    'automation_potential': 'High'
                },
                timeout=10
            )
            created = create_resp.status_code == 201
            self.log("Create Business Process", created,
                     f"Status: {create_resp.status_code}")

            if created:
                # Verify it appears in list
                get_resp = self.session.get(
                    urljoin(self.base_url, '/api/business-processes'),
                    timeout=10
                )
                processes = get_resp.json()
                found = any(p.get('name') == 'Staging Test Process' for p in processes)
                self.log("New process appears in list", found,
                         f"Total processes: {len(processes)}")
        except Exception as e:
            self.log("Create Business Process", False, str(e))

    def test_xss_protection(self):
        """Test #3: XSS Protection - 1 minute"""
        print("\n=== Test #3: XSS Protection ===")

        # Must be logged in as admin
        if 'session' not in self.session.cookies and 'connect.sid' not in self.session.cookies:
            # Try login again
            try:
                self.session.post(
                    urljoin(self.base_url, '/api/auth/login'),
                    json={'password': 'HLStearns2025!'},
                    timeout=10
                )
            except:
                pass

        # Create deliverable with XSS payload
        xss_payload = "<script>alert('XSS Attack!')</script>"
        try:
            create_resp = self.session.post(
                urljoin(self.base_url, '/api/deliverables'),
                json={
                    'title': xss_payload,
                    'phase': 'Foundation',
                    'description': 'XSS test'
                },
                timeout=10
            )

            if create_resp.status_code == 201:
                # Get deliverables and check if HTML is escaped
                get_resp = self.session.get(
                    urljoin(self.base_url, '/api/deliverables'),
                    timeout=10
                )
                deliverables = get_resp.json()
                xss_item = next((d for d in deliverables if xss_payload in d.get('title', '')), None)

                if xss_item:
                    # Get main page HTML and check rendering
                    page_resp = self.session.get(self.base_url, timeout=10)
                    html = page_resp.text

                    # Check if HTML is escaped (safe)
                    has_escaped = '&lt;script&gt;' in html or '&lt;' in html
                    has_raw_script = '<script>alert' in html

                    is_safe = has_escaped or not has_raw_script
                    self.log("XSS payload escaped", is_safe,
                             "HTML properly escaped" if is_safe else "Raw <script> tag found!")
                else:
                    self.log("XSS test item created", False, "Item not found in API response")
            else:
                self.log("XSS test deliverable creation", False,
                         f"Status: {create_resp.status_code}")

        except Exception as e:
            self.log("XSS Protection test", False, str(e))

    def test_security_headers(self):
        """Test #4: Security Headers - 1 minute"""
        print("\n=== Test #4: Security Headers ===")

        try:
            resp = requests.get(self.base_url, timeout=10)
            headers = resp.headers

            # Check required headers from FINAL_PRE_PRODUCTION_REVIEW.md
            expected_headers = {
                'X-Robots-Tag': 'noindex',
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1',
                'Content-Security-Policy': "default-src 'self'",
                'Cache-Control': 'no-store'
            }

            for header, expected_value in expected_headers.items():
                actual = headers.get(header, '')
                present = expected_value.lower() in actual.lower() if expected_value else header in headers
                self.log(f"Header: {header}", present,
                         f"Value: {actual[:50] if actual else 'MISSING'}")

            # Check session cookie flags
            cookies = resp.cookies
            if cookies:
                for cookie in cookies:
                    secure = cookie.secure
                    httponly = cookie.has_nonstandard_attr('HttpOnly') or 'httponly' in str(cookie).lower()
                    samesite = cookie.get_nonstandard_attr('SameSite') or 'lax' in str(cookie).lower()

                    self.log(f"Cookie '{cookie.name}' - Secure flag", secure)
                    self.log(f"Cookie '{cookie.name}' - HttpOnly flag", httponly)
                    self.log(f"Cookie '{cookie.name}' - SameSite flag", samesite)
            else:
                self.log("Session cookies present", False, "No cookies set")

        except Exception as e:
            self.log("Security Headers test", False, str(e))

    def run_all_tests(self):
        """Run complete smoke test suite"""
        print("========================================")
        print("Capstone Hub - Staging Smoke Test")
        print("========================================")
        print(f"Base URL: {self.base_url}")
        print("")

        self.test_viewer_access()
        self.test_admin_access()
        self.test_xss_protection()
        self.test_security_headers()

        # Generate report
        print("\n========================================")
        print("SMOKE TEST RESULTS")
        print("========================================")

        total = len(self.results)
        passed = total - self.failures

        report = [
            "========================================",
            "Capstone Hub - Staging Smoke Test Report",
            "========================================",
            f"Base URL: {self.base_url}",
            f"Total Tests: {total}",
            f"Passed: {passed}",
            f"Failed: {self.failures}",
            "",
            "TEST RESULTS:",
            "-------------"
        ] + self.results

        if self.failures == 0:
            report.append("")
            report.append("========================================")
            report.append("ALL TESTS PASSED - READY FOR PRODUCTION")
            report.append("========================================")
            report.append("")
            report.append("Next steps:")
            report.append("1. Review this report: staging_smoke_report.txt")
            report.append("2. Deploy to production: .\\promote_to_prod.ps1")
            report.append("3. Re-run smoke test against production URL")
            print("\nALL TESTS PASSED - READY FOR PRODUCTION")
        else:
            report.append("")
            report.append("========================================")
            report.append(f"{self.failures} TEST(S) FAILED - DO NOT PROMOTE")
            report.append("========================================")
            report.append("")
            report.append("Review failures above and fix issues before production.")
            print(f"\n{self.failures} TEST(S) FAILED - DO NOT PROMOTE")

        # Write report
        with open('staging_smoke_report.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"\nReport written to: staging_smoke_report.txt")

        return 0 if self.failures == 0 else 1


def main():
    parser = argparse.ArgumentParser(description='Run Capstone Hub smoke tests')
    parser.add_argument('--url', type=str, help='Base URL to test')
    args = parser.parse_args()

    # Get URL from argument or .staging_url file
    base_url = args.url
    if not base_url:
        try:
            with open('.staging_url', 'r') as f:
                base_url = f.read().strip()
        except FileNotFoundError:
            print("ERROR: No staging URL found")
            print("Either:")
            print("  1. Run staging_deploy.ps1 first (creates .staging_url)")
            print("  2. Specify URL: python smoke_staging.py --url https://your-url.com")
            sys.exit(1)

    if not base_url.startswith('http'):
        base_url = f'https://{base_url}'

    # Run tests
    tester = SmokeTest(base_url)
    exit_code = tester.run_all_tests()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()

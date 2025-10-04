#!/usr/bin/env python3
"""
Environment Variable Validation Script
Checks all required env vars and prints readiness status
"""

import os
import sys


# ANSI color codes
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


# Required environment variables
REQUIRED_VARS = [
    ('SECRET_KEY', 'Flask session encryption key', True),
]

# Recommended variables (not strictly required)
RECOMMENDED_VARS = [
    ('ADMIN_PASSWORD_HASH', 'Hashed admin password (production)'),
    ('ADMIN_PASSWORD', 'Plain admin password (development)'),
    ('VIEWER_PASSWORD_HASH', 'Hashed viewer password (production)'),
    ('VIEWER_PASSWORD', 'Plain viewer password (development)'),
    ('DATABASE_URL', 'Database connection string'),
    ('LOG_LEVEL', 'Logging verbosity'),
]

# Security checks
SECURITY_CHECKS = [
    ('ENABLE_DEBUG_ROUTES', '0', 'Debug routes must be disabled'),
    ('FLASK_ENV', 'production', 'Flask environment should be production'),
]


def check_variable(name, description, required=False):
    """Check if an environment variable is set"""
    value = os.environ.get(name)

    if value:
        # Mask sensitive values
        if any(sensitive in name.lower() for sensitive in ['password', 'secret', 'key', 'token']):
            display_value = f"{value[:8]}..." if len(value) > 8 else "[SET]"
        else:
            display_value = value

        print(f"  {Colors.GREEN}[OK]{Colors.END} {name:25} = {display_value}")
        return True
    else:
        status = f"{Colors.RED}[X]{Colors.END}" if required else f"{Colors.YELLOW}[!]{Colors.END}"
        req_label = "(REQUIRED)" if required else "(optional)"
        print(f"  {status} {name:25} {req_label} - {description}")
        return not required


def check_security(name, expected, description):
    """Check if a security-related variable has the correct value"""
    value = os.environ.get(name, '')

    if value == expected:
        print(f"  {Colors.GREEN}[OK]{Colors.END} {name:25} = {expected}")
        return True
    else:
        actual = value if value else "(not set)"
        print(f"  {Colors.YELLOW}[!]{Colors.END} {name:25} = {actual} (expected: {expected})")
        print(f"      {description}")
        return False


def main():
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}Capstone Hub - Environment Validation{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

    all_ok = True

    # Check required variables
    print(f"{Colors.BOLD}Required Variables:{Colors.END}")
    for name, desc, req in REQUIRED_VARS:
        if not check_variable(name, desc, req):
            all_ok = False
    print()

    # Check recommended variables
    print(f"{Colors.BOLD}Recommended Variables:{Colors.END}")
    has_admin = False
    has_viewer = False

    for name, desc in RECOMMENDED_VARS:
        check_variable(name, desc, False)
        if 'ADMIN_PASSWORD' in name and os.environ.get(name):
            has_admin = True
        if 'VIEWER_PASSWORD' in name and os.environ.get(name):
            has_viewer = True

    if not has_admin:
        print(f"  {Colors.RED}[X]{Colors.END} No admin password configured (HASH or PLAIN)")
        all_ok = False

    if not has_viewer:
        print(f"  {Colors.YELLOW}[!]{Colors.END} No viewer password configured (will use default)")

    print()

    # Check security settings
    print(f"{Colors.BOLD}Security Checks:{Colors.END}")
    for name, expected, desc in SECURITY_CHECKS:
        if not check_security(name, expected, desc):
            # Don't fail for security warnings, just note them
            pass
    print()

    # Print readiness banner
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    if all_ok:
        print(f"{Colors.BOLD}{Colors.GREEN}[OK] ENVIRONMENT READY{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
        print("All required environment variables are set.")
        print("You can safely start the application.")
        return 0
    else:
        print(f"{Colors.BOLD}{Colors.RED}[X] ENVIRONMENT NOT READY{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}\n")
        print("Required environment variables are missing.")
        print("Set them before starting the application:")
        print("")
        print("  # Copy sample file")
        print("  cp .env.sample .env")
        print("")
        print("  # Edit .env with your values")
        print("  nano .env")
        print("")
        print("  # Or set via Railway:")
        print("  railway variables set SECRET_KEY=...")
        print("")
        return 1


if __name__ == '__main__':
    sys.exit(main())

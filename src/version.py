"""
Capstone Hub Version Information
"""

__version__ = "0.36.0"
__release_date__ = "2025-10-04"
__release_name__ = "Phase 1 Security"

VERSION_INFO = {
    "version": __version__,
    "release_date": __release_date__,
    "release_name": __release_name__,
    "features": [
        "CSRF protection on all write endpoints",
        "Rate limiting (5 login attempts per 15 minutes)",
        "30-minute idle session timeout",
        "Admin database backup endpoint with UI",
        "CSRF token API endpoint (GET /api/csrf-token)",
        "Centralized extension management (extensions.py)",
        "All frontend fetch calls protected with CSRF tokens",
        "Strict CSP maintained (event delegation only)"
    ]
}

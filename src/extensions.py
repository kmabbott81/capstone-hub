"""
Flask extensions initialization
Centralized extension instances to avoid circular imports
"""

from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize CSRF protection
csrf = CSRFProtect()

# Initialize rate limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["2000 per day", "200 per hour"],
    storage_uri="memory://"
)

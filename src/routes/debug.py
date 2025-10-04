# staging-only debug helpers (DO NOT enable in production)
import os
import time
from functools import wraps
from flask import Blueprint, request, jsonify, session
from src.routes.auth import require_admin  # used on some routes
from src.extensions import csrf

debug_bp = Blueprint("debug", __name__)
DEBUG_KEY = os.environ.get("DEBUG_KEY", "")

def debug_guard(require_admin_role=False):
    def deco(fn):
        @wraps(fn)
        def wrapper(*a, **k):
            if os.environ.get("ENABLE_DEBUG_ROUTES") != "1":
                return jsonify({"error": "debug_disabled"}), 404
            if request.headers.get("X-Debug-Key") != DEBUG_KEY:
                return jsonify({"error": "forbidden"}), 403
            if require_admin_role:
                # reuse your server auth if requested
                if session.get("user_role") != "admin":
                    return jsonify({"error":"admin_required"}), 403
            return fn(*a, **k)
        return wrapper
    return deco

@debug_bp.route("/api/_debug/ping")
@debug_guard()
def ping():
    return jsonify({"pong": True, "ts": int(time.time())})

@debug_bp.route("/api/_debug/set_last_seen", methods=["POST"])
@debug_guard(require_admin_role=True)
@csrf.exempt
def set_last_seen():
    """Simulate idle session expiry: set last activity N seconds ago."""
    ago = int((request.json or {}).get("ago_seconds", 1900))
    session["_last_seen"] = int(time.time()) - ago
    return jsonify({"ok": True, "set_ago": ago})

@debug_bp.route("/api/_debug/force_429", methods=["POST"])
@debug_guard()
@csrf.exempt
def force_429():
    """Useful to test limiter/error handling paths in clients."""
    return jsonify({"error":"forced"}), 429

import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request, session
from datetime import timedelta, datetime
from flask_wtf.csrf import generate_csrf
from src.models.database import db
from src.models.user import User
from src.models.deliverable import Deliverable
from src.models.business_process import BusinessProcess
from src.models.ai_technology import AITechnology
from src.models.software_tool import SoftwareTool
from src.models.research_item import ResearchItem
from src.models.integration import Integration
from src.routes.user import user_bp
from src.routes.deliverables import deliverables_bp
from src.routes.business_processes import business_processes_bp
from src.routes.ai_technologies import ai_technologies_bp
from src.routes.software_tools import software_tools_bp
from src.routes.research_items import research_items_bp
from src.routes.advanced_features import advanced_features_bp
from src.routes.integrations import integrations_bp
from src.routes.auth import auth_bp
from src.routes.admin import admin_bp
from flask_cors import CORS
from src.extensions import csrf, limiter

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'HL_Stearns_Capstone_2025_Secure_Key_#$%')
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JS access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_CHECK_DEFAULT'] = False  # Manual checking via decorator
app.config['WTF_CSRF_TIME_LIMIT'] = None  # No expiration
CORS(app)

# Initialize extensions
csrf.init_app(app)
limiter.init_app(app)

app.register_blueprint(user_bp)
app.register_blueprint(deliverables_bp)
app.register_blueprint(business_processes_bp)
app.register_blueprint(ai_technologies_bp)
app.register_blueprint(software_tools_bp)
app.register_blueprint(research_items_bp)
app.register_blueprint(integrations_bp)
app.register_blueprint(advanced_features_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

# CSRF token endpoint
@app.route('/api/csrf-token', methods=['GET'])
def get_csrf_token():
    """Get CSRF token for client-side requests"""
    return jsonify({'csrf_token': generate_csrf()})

# Idle timeout middleware
@app.before_request
def enforce_idle_timeout():
    """Enforce 30-minute idle timeout"""
    if request.path.startswith('/api/'):
        now = datetime.utcnow().timestamp()
        last = session.get('_last_seen')

        if last and (now - last) > 1800:  # 30 minutes in seconds
            session.clear()
            if request.method != 'GET':
                return jsonify({'error': 'Session expired'}), 401

        session['_last_seen'] = now

# Security headers middleware
@app.after_request
def set_security_headers(response):
    response.headers['X-Robots-Tag'] = 'noindex, nofollow'
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    # CSP: Allow unsafe-inline for styles (Bootstrap), strict script-src
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "img-src 'self' data: https:; "
        "style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; "
        "script-src 'self' https://cdnjs.cloudflare.com; "
        "font-src 'self' data: https://cdnjs.cloudflare.com; "
        "connect-src 'self'"
    )
    return response

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
import hashlib
import os
from werkzeug.security import check_password_hash
from src.extensions import csrf, limiter

auth_bp = Blueprint('auth', __name__)

# Password configuration - read from environment variables
# For production, use hashed passwords. For development, plain passwords are acceptable.
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH')  # pbkdf2:sha256 hash
ADMIN_PASSWORD_PLAIN = os.getenv('ADMIN_PASSWORD')  # Fallback for development
VIEWER_PASSWORD_HASH = os.getenv('VIEWER_PASSWORD_HASH')  # pbkdf2:sha256 hash
VIEWER_PASSWORD_PLAIN = os.getenv('VIEWER_PASSWORD', 'CapstoneView')  # Fallback for development

@auth_bp.route('/api/auth/login', methods=['POST'])
@limiter.limit("5 per 15 minutes")
@csrf.exempt
def login():
    """Authenticate user with admin or viewer password"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
            
        password = data.get('password', '')

        # Check admin credentials (prefer hash, fallback to plain)
        is_admin = False
        if ADMIN_PASSWORD_HASH and check_password_hash(ADMIN_PASSWORD_HASH, password):
            is_admin = True
        elif ADMIN_PASSWORD_PLAIN and password == ADMIN_PASSWORD_PLAIN:
            is_admin = True

        if is_admin:
            session.permanent = False
            session['user_role'] = 'admin'
            session['authenticated'] = True

            return jsonify({
                'success': True,
                'role': 'admin',
                'message': 'Admin access granted',
                'permissions': {
                    'can_edit': True,
                    'can_delete': True,
                    'can_export': True,
                    'can_manage_integrations': True,
                    'can_view_analytics': True
                }
            })

        # Check viewer credentials (prefer hash, fallback to plain)
        is_viewer = False
        if VIEWER_PASSWORD_HASH and check_password_hash(VIEWER_PASSWORD_HASH, password):
            is_viewer = True
        elif VIEWER_PASSWORD_PLAIN and password == VIEWER_PASSWORD_PLAIN:
            is_viewer = True

        if is_viewer:
            session.permanent = False
            session['user_role'] = 'viewer'
            session['authenticated'] = True

            return jsonify({
                'success': True,
                'role': 'viewer',
                'message': 'Viewer access granted',
                'permissions': {
                    'can_edit': False,
                    'can_delete': False,
                    'can_export': True,
                    'can_manage_integrations': False,
                    'can_view_analytics': True
                }
            })
        
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid password'
            }), 401
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Authentication error: {str(e)}'
        }), 500

@auth_bp.route('/api/auth/logout', methods=['POST'])
def logout():
    """Log out the current user"""
    session.clear()
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@auth_bp.route('/api/auth/status', methods=['GET'])
def get_auth_status():
    """Get current authentication status"""
    try:
        if session.get('authenticated'):
            role = session.get('user_role', 'viewer')
            return jsonify({
                'authenticated': True,
                'role': role,
                'permissions': get_user_permissions(role)
            })
        else:
            return jsonify({
                'authenticated': False,
                'role': None,
                'permissions': {
                    'can_edit': False,
                    'can_delete': False,
                    'can_export': False,
                    'can_manage_integrations': False,
                    'can_view_analytics': False
                }
            })
    except Exception as e:
        return jsonify({
            'authenticated': False,
            'role': None,
            'error': str(e),
            'permissions': {
                'can_edit': False,
                'can_delete': False,
                'can_export': False,
                'can_manage_integrations': False,
                'can_view_analytics': False
            }
        })

def get_user_permissions(role):
    """Get permissions based on user role"""
    if role == 'admin':
        return {
            'can_edit': True,
            'can_delete': True,
            'can_export': True,
            'can_manage_integrations': True,
            'can_view_analytics': True
        }
    elif role == 'viewer':
        return {
            'can_edit': False,
            'can_delete': False,
            'can_export': True,
            'can_manage_integrations': False,
            'can_view_analytics': True
        }
    else:
        return {
            'can_edit': False,
            'can_delete': False,
            'can_export': False,
            'can_manage_integrations': False,
            'can_view_analytics': False
        }

def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_admin(f):
    """Decorator to require admin role"""
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': 'Authentication required'}), 401
        if session.get('user_role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@auth_bp.route('/api/auth/change-password', methods=['POST'])
@require_admin
def change_password():
    """Change admin or viewer password (admin only)"""
    data = request.get_json()
    password_type = data.get('type')  # 'admin' or 'viewer'
    new_password = data.get('new_password')
    
    if not new_password or len(new_password) < 6:
        return jsonify({
            'success': False,
            'message': 'Password must be at least 6 characters'
        }), 400
    
    # In a real implementation, you would update the password in a secure way
    # For this demo, we'll just return success
    return jsonify({
        'success': True,
        'message': f'{password_type.title()} password updated successfully',
        'note': 'Password change would be implemented in production'
    })

@auth_bp.route('/api/auth/session-info', methods=['GET'])
@require_auth
def get_session_info():
    """Get detailed session information"""
    return jsonify({
        'role': session.get('user_role'),
        'login_time': session.get('login_time'),
        'session_duration': str(datetime.now() - datetime.fromisoformat(session.get('login_time', datetime.now().isoformat()))),
        'permissions': get_user_permissions(session.get('user_role')),
        'can_change_passwords': session.get('user_role') == 'admin'
    })


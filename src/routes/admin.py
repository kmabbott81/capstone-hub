from flask import Blueprint, jsonify
from src.routes.auth import require_admin
from src.extensions import csrf
import subprocess
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/backup', methods=['POST'])
@require_admin
@csrf.protect
def trigger_backup():
    """Manually trigger database backup"""
    try:
        # Get the project root directory (3 levels up from this file)
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

        result = subprocess.run(
            ['python', 'backup_database.py'],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=project_root
        )

        if result.returncode == 0:
            return jsonify({
                'success': True,
                'message': 'Backup created successfully',
                'output': result.stdout
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Backup failed',
                'error': result.stderr
            }), 500

    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'message': 'Backup timed out after 30 seconds'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Backup error: {str(e)}'
        }), 500

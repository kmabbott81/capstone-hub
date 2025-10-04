from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.deliverable import Deliverable
from src.models.database import db
from src.routes.auth import require_admin
from src.extensions import csrf

deliverables_bp = Blueprint('deliverables', __name__)

@deliverables_bp.route('/api/deliverables', methods=['GET'])
def get_deliverables():
    """Get all deliverables"""
    deliverables = Deliverable.query.all()
    return jsonify([d.to_dict() for d in deliverables])

@deliverables_bp.route('/api/deliverables', methods=['POST'])
@require_admin
@csrf.protect
def create_deliverable():
    """Create a new deliverable"""
    data = request.get_json()

    try:
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data.get('due_date').replace('Z', '+00:00')).date()
            except:
                pass

        deliverable = Deliverable(
            title=data.get('title'),
            description=data.get('description', ''),
            phase=data.get('phase'),
            due_date=due_date,
            status=data.get('status', 'Not Started'),
            priority=data.get('priority', 'Medium'),
            completion_percentage=data.get('completion_percentage', 0)
        )

        db.session.add(deliverable)
        db.session.commit()

        return jsonify({
            'id': deliverable.id,
            'title': deliverable.title,
            'description': deliverable.description,
            'phase': deliverable.phase,
            'due_date': deliverable.due_date.isoformat() if deliverable.due_date else None,
            'status': deliverable.status,
            'priority': deliverable.priority,
            'completion_percentage': deliverable.completion_percentage,
            'created_at': deliverable.created_at.isoformat(),
            'updated_at': deliverable.updated_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@deliverables_bp.route('/api/deliverables/<int:deliverable_id>', methods=['PUT'])
@require_admin
@csrf.protect
def update_deliverable(deliverable_id):
    """Update an existing deliverable"""
    data = request.get_json()
    deliverable = Deliverable.query.get(deliverable_id)

    if not deliverable:
        return jsonify({'error': 'Deliverable not found'}), 404

    try:
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data.get('due_date').replace('Z', '+00:00')).date()
            except:
                pass

        deliverable.title = data.get('title', deliverable.title)
        deliverable.description = data.get('description', deliverable.description)
        deliverable.phase = data.get('phase', deliverable.phase)
        deliverable.due_date = due_date if due_date else deliverable.due_date
        deliverable.status = data.get('status', deliverable.status)
        deliverable.priority = data.get('priority', deliverable.priority)
        deliverable.completion_percentage = data.get('completion_percentage', deliverable.completion_percentage)
        deliverable.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify(deliverable.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@deliverables_bp.route('/api/deliverables/<int:deliverable_id>', methods=['DELETE'])
@require_admin
@csrf.protect
def delete_deliverable(deliverable_id):
    """Delete a deliverable"""
    deliverable = Deliverable.query.get(deliverable_id)

    if not deliverable:
        return jsonify({'error': 'Deliverable not found'}), 404

    try:
        db.session.delete(deliverable)
        db.session.commit()
        return jsonify({'message': 'Deliverable deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@deliverables_bp.route('/api/deliverables/phases', methods=['GET'])
def get_phases():
    """Get all available phases"""
    phases = [
        'Foundation & Planning',
        'Research & Analysis', 
        'Implementation',
        'Evaluation & Testing',
        'Final Report & Presentation'
    ]
    return jsonify(phases)


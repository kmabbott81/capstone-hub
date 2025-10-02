from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.deliverable import Deliverable
from src.models.database import db

deliverables_bp = Blueprint('deliverables', __name__)

@deliverables_bp.route('/api/deliverables', methods=['GET'])
def get_deliverables():
    """Get all deliverables"""
    deliverables = Deliverable.query.all()
    return jsonify([{
        'id': d.id,
        'title': d.title,
        'description': d.description or '',
        'phase': d.phase,
        'due_date': d.due_date.isoformat() if d.due_date else None,
        'status': d.status or 'Not Started',
        'priority': d.priority or 'Medium',
        'completion_percentage': d.completion_percentage or 0,
        'created_at': d.created_at.isoformat() if d.created_at else '',
        'updated_at': d.updated_at.isoformat() if d.updated_at else ''
    } for d in deliverables])

@deliverables_bp.route('/api/deliverables', methods=['POST'])
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
def update_deliverable(deliverable_id):
    """Update an existing deliverable"""
    data = request.get_json()
    
    for deliverable in deliverables_data:
        if deliverable['id'] == deliverable_id:
            deliverable.update({
                'title': data.get('title', deliverable['title']),
                'description': data.get('description', deliverable['description']),
                'phase': data.get('phase', deliverable['phase']),
                'due_date': data.get('due_date', deliverable['due_date']),
                'status': data.get('status', deliverable['status']),
                'priority': data.get('priority', deliverable['priority']),
                'completion_percentage': data.get('completion_percentage', deliverable['completion_percentage']),
                'updated_at': datetime.now().isoformat()
            })
            return jsonify(deliverable)
    
    return jsonify({'error': 'Deliverable not found'}), 404

@deliverables_bp.route('/api/deliverables/<int:deliverable_id>', methods=['DELETE'])
def delete_deliverable(deliverable_id):
    """Delete a deliverable"""
    global deliverables_data
    deliverables_data = [d for d in deliverables_data if d['id'] != deliverable_id]
    return jsonify({'message': 'Deliverable deleted successfully'})

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


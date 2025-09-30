from flask import Blueprint, request, jsonify
from datetime import datetime

deliverables_bp = Blueprint('deliverables', __name__)

# In-memory storage for demonstration (replace with database in production)
deliverables_data = []

@deliverables_bp.route('/api/deliverables', methods=['GET'])
def get_deliverables():
    """Get all deliverables"""
    return jsonify(deliverables_data)

@deliverables_bp.route('/api/deliverables', methods=['POST'])
def create_deliverable():
    """Create a new deliverable"""
    data = request.get_json()
    
    deliverable = {
        'id': len(deliverables_data) + 1,
        'title': data.get('title'),
        'description': data.get('description', ''),
        'phase': data.get('phase'),
        'due_date': data.get('due_date'),
        'status': data.get('status', 'Not Started'),
        'priority': data.get('priority', 'Medium'),
        'completion_percentage': data.get('completion_percentage', 0),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    deliverables_data.append(deliverable)
    return jsonify(deliverable), 201

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


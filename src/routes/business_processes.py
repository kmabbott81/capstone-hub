from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.business_process import BusinessProcess
from src.models.database import db
from src.routes.auth import require_admin
from src.extensions import csrf

business_processes_bp = Blueprint('business_processes', __name__)

@business_processes_bp.route('/api/business-processes', methods=['GET'])
def get_business_processes():
    """Get all business processes"""
    processes = BusinessProcess.query.all()
    return jsonify([p.to_dict() for p in processes])

@business_processes_bp.route('/api/business-processes', methods=['POST'])
@require_admin

def create_business_process():
    """Create a new business process"""
    data = request.get_json()

    try:
        process = BusinessProcess(
            name=data.get('name'),
            description=data.get('description', ''),
            department=data.get('department'),
            automation_potential=data.get('automation_potential', 'Medium'),
            ai_opportunity=data.get('ai_opportunity', 'Medium'),
            evaluation_status=data.get('status', 'Not Started')
        )

        db.session.add(process)
        db.session.commit()

        return jsonify({
            'id': process.id,
            'name': process.name,
            'description': process.description,
            'department': process.department,
            'automation_potential': process.automation_potential,
            'ai_opportunity': process.ai_opportunity,
            'evaluation_status': process.evaluation_status,
            'created_at': process.created_at.isoformat(),
            'updated_at': process.updated_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_processes_bp.route('/api/business-processes/<int:process_id>', methods=['PUT'])
@require_admin

def update_business_process(process_id):
    """Update an existing business process"""
    data = request.get_json()
    process = BusinessProcess.query.get(process_id)

    if not process:
        return jsonify({'error': 'Business process not found'}), 404

    try:
        process.name = data.get('name', process.name)
        process.description = data.get('description', process.description)
        process.department = data.get('department', process.department)
        process.automation_potential = data.get('automation_potential', process.automation_potential)
        process.ai_opportunity = data.get('ai_opportunity', process.ai_opportunity)
        process.evaluation_status = data.get('status', process.evaluation_status)
        process.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify(process.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_processes_bp.route('/api/business-processes/<int:process_id>', methods=['DELETE'])
@require_admin

def delete_business_process(process_id):
    """Delete a business process"""
    process = BusinessProcess.query.get(process_id)

    if not process:
        return jsonify({'error': 'Business process not found'}), 404

    try:
        db.session.delete(process)
        db.session.commit()
        return jsonify({'message': 'Business process deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@business_processes_bp.route('/api/business-processes/departments', methods=['GET'])
def get_departments():
    """Get all available departments"""
    departments = [
        'Sales',
        'Operations', 
        'Customer Service',
        'Finance',
        'IT',
        'Human Resources',
        'Marketing',
        'Procurement'
    ]
    return jsonify(departments)

@business_processes_bp.route('/api/business-processes/automation-levels', methods=['GET'])
def get_automation_levels():
    """Get automation potential levels"""
    levels = ['High', 'Medium', 'Low']
    return jsonify(levels)


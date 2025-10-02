from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.business_process import BusinessProcess
from src.models.database import db

business_processes_bp = Blueprint('business_processes', __name__)

@business_processes_bp.route('/api/business-processes', methods=['GET'])
def get_business_processes():
    """Get all business processes"""
    processes = BusinessProcess.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'description': p.description,
        'department': p.department,
        'automation_potential': p.automation_potential,
        'ai_opportunity': p.ai_opportunity,
        'evaluation_status': p.evaluation_status,
        'created_at': p.created_at.isoformat(),
        'updated_at': p.updated_at.isoformat()
    } for p in processes])

@business_processes_bp.route('/api/business-processes', methods=['POST'])
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
def update_business_process(process_id):
    """Update an existing business process"""
    data = request.get_json()
    
    for process in processes_data:
        if process['id'] == process_id:
            process.update({
                'name': data.get('name', process['name']),
                'description': data.get('description', process['description']),
                'department': data.get('department', process['department']),
                'current_state': data.get('current_state', process['current_state']),
                'automation_potential': data.get('automation_potential', process['automation_potential']),
                'priority': data.get('priority', process['priority']),
                'estimated_time_savings': data.get('estimated_time_savings', process['estimated_time_savings']),
                'estimated_cost_savings': data.get('estimated_cost_savings', process['estimated_cost_savings']),
                'complexity': data.get('complexity', process['complexity']),
                'stakeholders': data.get('stakeholders', process['stakeholders']),
                'pain_points': data.get('pain_points', process['pain_points']),
                'success_metrics': data.get('success_metrics', process['success_metrics']),
                'status': data.get('status', process['status']),
                'updated_at': datetime.now().isoformat()
            })
            return jsonify(process)
    
    return jsonify({'error': 'Business process not found'}), 404

@business_processes_bp.route('/api/business-processes/<int:process_id>', methods=['DELETE'])
def delete_business_process(process_id):
    """Delete a business process"""
    global processes_data
    processes_data = [p for p in processes_data if p['id'] != process_id]
    return jsonify({'message': 'Business process deleted successfully'})

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


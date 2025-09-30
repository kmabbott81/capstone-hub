from flask import Blueprint, request, jsonify
from datetime import datetime

business_processes_bp = Blueprint('business_processes', __name__)

# In-memory storage for demonstration (replace with database in production)
processes_data = []

@business_processes_bp.route('/api/business-processes', methods=['GET'])
def get_business_processes():
    """Get all business processes"""
    return jsonify(processes_data)

@business_processes_bp.route('/api/business-processes', methods=['POST'])
def create_business_process():
    """Create a new business process"""
    data = request.get_json()
    
    process = {
        'id': len(processes_data) + 1,
        'name': data.get('name'),
        'description': data.get('description', ''),
        'department': data.get('department'),
        'current_state': data.get('current_state', 'Manual'),
        'automation_potential': data.get('automation_potential', 'Medium'),
        'priority': data.get('priority', 'Medium'),
        'estimated_time_savings': data.get('estimated_time_savings', 0),
        'estimated_cost_savings': data.get('estimated_cost_savings', 0),
        'complexity': data.get('complexity', 'Medium'),
        'stakeholders': data.get('stakeholders', []),
        'pain_points': data.get('pain_points', []),
        'success_metrics': data.get('success_metrics', []),
        'status': data.get('status', 'Identified'),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    processes_data.append(process)
    return jsonify(process), 201

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


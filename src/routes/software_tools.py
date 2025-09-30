from flask import Blueprint, request, jsonify
from datetime import datetime

software_tools_bp = Blueprint('software_tools', __name__)

# In-memory storage for demonstration (replace with database in production)
software_tools_data = []

@software_tools_bp.route('/api/software-tools', methods=['GET'])
def get_software_tools():
    """Get all software tools"""
    return jsonify(software_tools_data)

@software_tools_bp.route('/api/software-tools', methods=['POST'])
def create_software_tool():
    """Create a new software tool"""
    data = request.get_json()
    
    tool = {
        'id': len(software_tools_data) + 1,
        'name': data.get('name'),
        'description': data.get('description', ''),
        'category': data.get('category'),
        'tool_type': data.get('tool_type'),  # Core, Optional, Integration
        'vendor': data.get('vendor', ''),
        'version': data.get('version', ''),
        'pricing_model': data.get('pricing_model', ''),
        'monthly_cost': data.get('monthly_cost', 0),
        'annual_cost': data.get('annual_cost', 0),
        'user_licenses': data.get('user_licenses', 0),
        'features': data.get('features', []),
        'integrations': data.get('integrations', []),
        'pros': data.get('pros', []),
        'cons': data.get('cons', []),
        'evaluation_status': data.get('evaluation_status', 'Not Evaluated'),
        'evaluation_score': data.get('evaluation_score', 0),
        'implementation_complexity': data.get('implementation_complexity', 'Medium'),
        'training_required': data.get('training_required', False),
        'support_quality': data.get('support_quality', 'Unknown'),
        'security_rating': data.get('security_rating', 'Unknown'),
        'scalability': data.get('scalability', 'Medium'),
        'business_impact': data.get('business_impact', 'Medium'),
        'technical_requirements': data.get('technical_requirements', []),
        'decision_status': data.get('decision_status', 'Under Review'),
        'notes': data.get('notes', ''),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    software_tools_data.append(tool)
    return jsonify(tool), 201

@software_tools_bp.route('/api/software-tools/<int:tool_id>', methods=['PUT'])
def update_software_tool(tool_id):
    """Update an existing software tool"""
    data = request.get_json()
    
    for tool in software_tools_data:
        if tool['id'] == tool_id:
            tool.update({
                'name': data.get('name', tool['name']),
                'description': data.get('description', tool['description']),
                'category': data.get('category', tool['category']),
                'tool_type': data.get('tool_type', tool['tool_type']),
                'vendor': data.get('vendor', tool['vendor']),
                'version': data.get('version', tool['version']),
                'pricing_model': data.get('pricing_model', tool['pricing_model']),
                'monthly_cost': data.get('monthly_cost', tool['monthly_cost']),
                'annual_cost': data.get('annual_cost', tool['annual_cost']),
                'user_licenses': data.get('user_licenses', tool['user_licenses']),
                'features': data.get('features', tool['features']),
                'integrations': data.get('integrations', tool['integrations']),
                'pros': data.get('pros', tool['pros']),
                'cons': data.get('cons', tool['cons']),
                'evaluation_status': data.get('evaluation_status', tool['evaluation_status']),
                'evaluation_score': data.get('evaluation_score', tool['evaluation_score']),
                'implementation_complexity': data.get('implementation_complexity', tool['implementation_complexity']),
                'training_required': data.get('training_required', tool['training_required']),
                'support_quality': data.get('support_quality', tool['support_quality']),
                'security_rating': data.get('security_rating', tool['security_rating']),
                'scalability': data.get('scalability', tool['scalability']),
                'business_impact': data.get('business_impact', tool['business_impact']),
                'technical_requirements': data.get('technical_requirements', tool['technical_requirements']),
                'decision_status': data.get('decision_status', tool['decision_status']),
                'notes': data.get('notes', tool['notes']),
                'updated_at': datetime.now().isoformat()
            })
            return jsonify(tool)
    
    return jsonify({'error': 'Software tool not found'}), 404

@software_tools_bp.route('/api/software-tools/<int:tool_id>', methods=['DELETE'])
def delete_software_tool(tool_id):
    """Delete a software tool"""
    global software_tools_data
    software_tools_data = [t for t in software_tools_data if t['id'] != tool_id]
    return jsonify({'message': 'Software tool deleted successfully'})

@software_tools_bp.route('/api/software-tools/categories', methods=['GET'])
def get_tool_categories():
    """Get all software tool categories"""
    categories = {
        'CRM': [
            'Salesforce',
            'HubSpot',
            'Microsoft Dynamics 365',
            'Pipedrive',
            'Zoho CRM'
        ],
        'ERP': [
            'NetSuite',
            'SAP',
            'Microsoft Dynamics 365',
            'QuickBooks Enterprise',
            'Sage'
        ],
        'Cloud Platform': [
            'Microsoft Azure',
            'Amazon AWS',
            'Google Cloud Platform',
            'IBM Cloud',
            'Oracle Cloud'
        ],
        'Analytics & BI': [
            'Power BI',
            'Tableau',
            'Looker',
            'Qlik Sense',
            'Google Analytics'
        ],
        'Communication': [
            'Microsoft Teams',
            'Slack',
            'Zoom',
            'Google Workspace',
            'Cisco Webex'
        ],
        'Project Management': [
            'Microsoft Project',
            'Asana',
            'Monday.com',
            'Jira',
            'Trello'
        ],
        'Document Management': [
            'SharePoint',
            'Google Drive',
            'Dropbox Business',
            'Box',
            'OneDrive'
        ],
        'Automation': [
            'Power Automate',
            'Zapier',
            'UiPath',
            'Automation Anywhere',
            'Blue Prism'
        ]
    }
    return jsonify(categories)

@software_tools_bp.route('/api/software-tools/types', methods=['GET'])
def get_tool_types():
    """Get software tool types"""
    types = ['Core', 'Optional', 'Integration']
    return jsonify(types)

@software_tools_bp.route('/api/software-tools/evaluation-criteria', methods=['GET'])
def get_evaluation_criteria():
    """Get evaluation criteria for software tools"""
    criteria = {
        'functionality': 'How well does it meet business requirements?',
        'usability': 'How easy is it to use and learn?',
        'integration': 'How well does it integrate with existing systems?',
        'scalability': 'Can it grow with the business?',
        'security': 'How secure is the platform?',
        'support': 'Quality of vendor support and documentation',
        'cost': 'Total cost of ownership including licensing and implementation',
        'reliability': 'System uptime and performance',
        'customization': 'Ability to customize to specific needs',
        'reporting': 'Quality and flexibility of reporting capabilities'
    }
    return jsonify(criteria)


from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.software_tool import SoftwareTool
from src.models.database import db
from src.routes.auth import require_admin

software_tools_bp = Blueprint('software_tools', __name__)

@software_tools_bp.route('/api/software-tools', methods=['GET'])
def get_software_tools():
    """Get all software tools"""
    tools = SoftwareTool.query.all()
    return jsonify([{
        'id': tool.id,
        'name': tool.name,
        'description': tool.description,
        'category': tool.category,
        'vendor': tool.vendor,
        'tool_type': tool.tool_type,
        'evaluation_status': tool.evaluation_status,
        'created_at': tool.created_at.isoformat(),
        'updated_at': tool.updated_at.isoformat()
    } for tool in tools])

@software_tools_bp.route('/api/software-tools', methods=['POST'])
@require_admin
def create_software_tool():
    """Create a new software tool"""
    data = request.get_json()

    try:
        tool = SoftwareTool(
            name=data.get('name'),
            description=data.get('description', ''),
            category=data.get('category'),
            tool_type=data.get('tool_type'),
            vendor=data.get('vendor', ''),
            pricing_model=data.get('pricing_model', ''),
            pricing_details=data.get('pricing_details', ''),
            features=data.get('features', ''),
            hl_stearns_fit=data.get('hl_stearns_fit', ''),
            current_usage=data.get('current_usage', ''),
            replacement_for=data.get('replacement_for', ''),
            integration_capabilities=data.get('integration_capabilities', ''),
            data_migration_complexity=data.get('data_migration_complexity', ''),
            training_requirements=data.get('training_requirements', ''),
            support_quality=data.get('support_quality', ''),
            scalability=data.get('scalability', ''),
            security_features=data.get('security_features', ''),
            mobile_support=data.get('mobile_support', False),
            cloud_based=data.get('cloud_based', True),
            on_premise_option=data.get('on_premise_option', False),
            api_quality=data.get('api_quality', ''),
            customization_level=data.get('customization_level', ''),
            evaluation_status=data.get('evaluation_status', 'Not Evaluated'),
            implementation_priority=data.get('implementation_priority', ''),
            roi_potential=data.get('roi_potential', ''),
            risk_level=data.get('risk_level', ''),
            decision_status=data.get('decision_status', ''),
            pilot_results=data.get('pilot_results', ''),
            notes=data.get('notes', '')
        )

        db.session.add(tool)
        db.session.commit()

        return jsonify({
            'id': tool.id,
            'name': tool.name,
            'description': tool.description,
            'category': tool.category,
            'vendor': tool.vendor,
            'tool_type': tool.tool_type,
            'evaluation_status': tool.evaluation_status,
            'created_at': tool.created_at.isoformat(),
            'updated_at': tool.updated_at.isoformat()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@software_tools_bp.route('/api/software-tools/<int:tool_id>', methods=['PUT'])
@require_admin
def update_software_tool(tool_id):
    """Update an existing software tool"""
    data = request.get_json()
    tool = SoftwareTool.query.get(tool_id)

    if not tool:
        return jsonify({'error': 'Software tool not found'}), 404

    try:
        tool.name = data.get('name', tool.name)
        tool.description = data.get('description', tool.description)
        tool.category = data.get('category', tool.category)
        tool.tool_type = data.get('tool_type', tool.tool_type)
        tool.vendor = data.get('vendor', tool.vendor)
        tool.pricing_model = data.get('pricing_model', tool.pricing_model)
        tool.pricing_details = data.get('pricing_details', tool.pricing_details)
        tool.features = data.get('features', tool.features)
        tool.hl_stearns_fit = data.get('hl_stearns_fit', tool.hl_stearns_fit)
        tool.current_usage = data.get('current_usage', tool.current_usage)
        tool.replacement_for = data.get('replacement_for', tool.replacement_for)
        tool.integration_capabilities = data.get('integration_capabilities', tool.integration_capabilities)
        tool.data_migration_complexity = data.get('data_migration_complexity', tool.data_migration_complexity)
        tool.training_requirements = data.get('training_requirements', tool.training_requirements)
        tool.support_quality = data.get('support_quality', tool.support_quality)
        tool.scalability = data.get('scalability', tool.scalability)
        tool.security_features = data.get('security_features', tool.security_features)
        tool.mobile_support = data.get('mobile_support', tool.mobile_support)
        tool.cloud_based = data.get('cloud_based', tool.cloud_based)
        tool.on_premise_option = data.get('on_premise_option', tool.on_premise_option)
        tool.api_quality = data.get('api_quality', tool.api_quality)
        tool.customization_level = data.get('customization_level', tool.customization_level)
        tool.evaluation_status = data.get('evaluation_status', tool.evaluation_status)
        tool.implementation_priority = data.get('implementation_priority', tool.implementation_priority)
        tool.roi_potential = data.get('roi_potential', tool.roi_potential)
        tool.risk_level = data.get('risk_level', tool.risk_level)
        tool.decision_status = data.get('decision_status', tool.decision_status)
        tool.pilot_results = data.get('pilot_results', tool.pilot_results)
        tool.notes = data.get('notes', tool.notes)
        tool.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify({
            'id': tool.id,
            'name': tool.name,
            'description': tool.description,
            'category': tool.category,
            'vendor': tool.vendor,
            'tool_type': tool.tool_type,
            'evaluation_status': tool.evaluation_status,
            'created_at': tool.created_at.isoformat(),
            'updated_at': tool.updated_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@software_tools_bp.route('/api/software-tools/<int:tool_id>', methods=['DELETE'])
@require_admin
def delete_software_tool(tool_id):
    """Delete a software tool"""
    tool = SoftwareTool.query.get(tool_id)

    if not tool:
        return jsonify({'error': 'Software tool not found'}), 404

    try:
        db.session.delete(tool)
        db.session.commit()
        return jsonify({'message': 'Software tool deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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


from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.database import db

from src.routes.auth import require_admin
integrations_bp = Blueprint('integrations', __name__)

@integrations_bp.route('/api/integrations', methods=['GET'])
def get_integrations():
    """Get all integrations"""
    integrations = Integration.query.all()
    return jsonify([{
        'id': integration.id,
        'name': integration.name,
        'platform': integration.platform,
        'integration_type': integration.integration_type,
        'purpose': integration.purpose,
        'setup_status': integration.setup_status,
        'created_at': integration.created_at.isoformat() if integration.created_at else None,
        'updated_at': integration.updated_at.isoformat() if integration.updated_at else None
    } for integration in integrations])

@integrations_bp.route('/api/integrations', methods=['POST'])
@require_admin
def create_integration():
    """Create a new integration"""
    data = request.get_json()

    try:
        integration = Integration(
            name=data.get('name'),
            platform=data.get('platform'),
            integration_type=data.get('integration_type'),
            purpose=data.get('purpose', ''),
            data_sync_direction=data.get('data_sync_direction'),
            sync_frequency=data.get('sync_frequency'),
            api_endpoint=data.get('api_endpoint'),
            authentication_method=data.get('authentication_method', ''),
            credentials_stored=data.get('credentials_stored', False),
            setup_status=data.get('setup_status', 'Not Configured'),
            sync_status=data.get('sync_status'),
            error_log=data.get('error_log'),
            data_mapping=data.get('data_mapping'),
            filters_applied=data.get('filters_applied'),
            security_considerations=data.get('security_considerations'),
            compliance_notes=data.get('compliance_notes'),
            performance_metrics=data.get('performance_metrics'),
            usage_statistics=data.get('usage_statistics'),
            configuration_notes=data.get('configuration_notes'),
            troubleshooting_guide=data.get('troubleshooting_guide')
        )

        db.session.add(integration)
        db.session.commit()

        return jsonify(integration.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@integrations_bp.route('/api/integrations/<int:integration_id>', methods=['PUT'])
@require_admin
def update_integration(integration_id):
    """Update an existing integration"""
    data = request.get_json()
    
    for integration in integrations_data:
        if integration['id'] == integration_id:
            integration.update({
                'name': data.get('name', integration['name']),
                'description': data.get('description', integration['description']),
                'platform': data.get('platform', integration['platform']),
                'integration_type': data.get('integration_type', integration['integration_type']),
                'purpose': data.get('purpose', integration['purpose']),
                'status': data.get('status', integration['status']),
                'priority': data.get('priority', integration['priority']),
                'configuration': data.get('configuration', integration['configuration']),
                'api_endpoints': data.get('api_endpoints', integration['api_endpoints']),
                'authentication_method': data.get('authentication_method', integration['authentication_method']),
                'data_sync_frequency': data.get('data_sync_frequency', integration['data_sync_frequency']),
                'data_types': data.get('data_types', integration['data_types']),
                'error_handling': data.get('error_handling', integration['error_handling']),
                'monitoring': data.get('monitoring', integration['monitoring']),
                'security_considerations': data.get('security_considerations', integration['security_considerations']),
                'testing_status': data.get('testing_status', integration['testing_status']),
                'last_sync': data.get('last_sync', integration['last_sync']),
                'sync_errors': data.get('sync_errors', integration['sync_errors']),
                'performance_metrics': data.get('performance_metrics', integration['performance_metrics']),
                'documentation_url': data.get('documentation_url', integration['documentation_url']),
                'contact_person': data.get('contact_person', integration['contact_person']),
                'implementation_date': data.get('implementation_date', integration['implementation_date']),
                'maintenance_schedule': data.get('maintenance_schedule', integration['maintenance_schedule']),
                'backup_procedures': data.get('backup_procedures', integration['backup_procedures']),
                'rollback_plan': data.get('rollback_plan', integration['rollback_plan']),
                'cost': data.get('cost', integration['cost']),
                'roi_metrics': data.get('roi_metrics', integration['roi_metrics']),
                'user_feedback': data.get('user_feedback', integration['user_feedback']),
                'notes': data.get('notes', integration['notes']),
                'updated_at': datetime.now().isoformat()
            })
            return jsonify(integration)
    
    return jsonify({'error': 'Integration not found'}), 404

@integrations_bp.route('/api/integrations/<int:integration_id>', methods=['DELETE'])
@require_admin
def delete_integration(integration_id):
    """Delete an integration"""
    global integrations_data
    integrations_data = [i for i in integrations_data if i['id'] != integration_id]
    return jsonify({'message': 'Integration deleted successfully'})

@integrations_bp.route('/api/integrations/platforms', methods=['GET'])
def get_integration_platforms():
    """Get available integration platforms"""
    platforms = {
        'Cloud Storage': [
            'Google Drive',
            'Microsoft OneDrive',
            'Dropbox',
            'Box',
            'Amazon S3'
        ],
        'Productivity Suites': [
            'Microsoft 365',
            'Google Workspace',
            'Notion',
            'Airtable',
            'Monday.com'
        ],
        'CRM Systems': [
            'Salesforce',
            'HubSpot',
            'Microsoft Dynamics 365',
            'Pipedrive',
            'Zoho CRM'
        ],
        'ERP Systems': [
            'NetSuite',
            'SAP',
            'Microsoft Dynamics 365',
            'QuickBooks',
            'Sage'
        ],
        'Communication': [
            'Microsoft Teams',
            'Slack',
            'Discord',
            'Zoom',
            'Webex'
        ],
        'Analytics': [
            'Power BI',
            'Tableau',
            'Google Analytics',
            'Looker',
            'Qlik'
        ]
    }
    return jsonify(platforms)

@integrations_bp.route('/api/integrations/types', methods=['GET'])
def get_integration_types():
    """Get integration types"""
    types = [
        'API',
        'Webhook',
        'Database Connection',
        'File Transfer',
        'Real-time Sync',
        'Batch Processing',
        'ETL Pipeline',
        'Message Queue',
        'Direct Connection',
        'Third-party Connector'
    ]
    return jsonify(types)

@integrations_bp.route('/api/integrations/authentication-methods', methods=['GET'])
def get_authentication_methods():
    """Get authentication methods"""
    methods = [
        'OAuth 2.0',
        'API Key',
        'Basic Authentication',
        'Bearer Token',
        'JWT',
        'SAML',
        'Certificate-based',
        'Custom Authentication'
    ]
    return jsonify(methods)

@integrations_bp.route('/api/integrations/sync-frequencies', methods=['GET'])
def get_sync_frequencies():
    """Get data synchronization frequencies"""
    frequencies = [
        'Real-time',
        'Every 5 minutes',
        'Every 15 minutes',
        'Every 30 minutes',
        'Hourly',
        'Every 4 hours',
        'Every 12 hours',
        'Daily',
        'Weekly',
        'Monthly',
        'On-demand'
    ]
    return jsonify(frequencies)


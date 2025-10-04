from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.database import db
from src.models.integration import Integration
from src.routes.auth import require_admin
from src.extensions import csrf

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
@csrf.protect
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
@csrf.protect
def update_integration(integration_id):
    """Update an existing integration"""
    data = request.get_json()
    integration = Integration.query.get(integration_id)

    if not integration:
        return jsonify({'error': 'Integration not found'}), 404

    try:
        integration.name = data.get('name', integration.name)
        integration.platform = data.get('platform', integration.platform)
        integration.integration_type = data.get('integration_type', integration.integration_type)
        integration.purpose = data.get('purpose', integration.purpose)
        integration.data_sync_direction = data.get('data_sync_direction', integration.data_sync_direction)
        integration.sync_frequency = data.get('sync_frequency', integration.sync_frequency)
        integration.api_endpoint = data.get('api_endpoint', integration.api_endpoint)
        integration.authentication_method = data.get('authentication_method', integration.authentication_method)
        integration.credentials_stored = data.get('credentials_stored', integration.credentials_stored)
        integration.setup_status = data.get('setup_status', integration.setup_status)
        integration.sync_status = data.get('sync_status', integration.sync_status)
        integration.error_log = data.get('error_log', integration.error_log)
        integration.data_mapping = data.get('data_mapping', integration.data_mapping)
        integration.filters_applied = data.get('filters_applied', integration.filters_applied)
        integration.security_considerations = data.get('security_considerations', integration.security_considerations)
        integration.compliance_notes = data.get('compliance_notes', integration.compliance_notes)
        integration.performance_metrics = data.get('performance_metrics', integration.performance_metrics)
        integration.usage_statistics = data.get('usage_statistics', integration.usage_statistics)
        integration.configuration_notes = data.get('configuration_notes', integration.configuration_notes)
        integration.troubleshooting_guide = data.get('troubleshooting_guide', integration.troubleshooting_guide)
        integration.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify(integration.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@integrations_bp.route('/api/integrations/<int:integration_id>', methods=['DELETE'])
@require_admin
@csrf.protect
def delete_integration(integration_id):
    """Delete an integration"""
    integration = Integration.query.get(integration_id)

    if not integration:
        return jsonify({'error': 'Integration not found'}), 404

    try:
        db.session.delete(integration)
        db.session.commit()
        return jsonify({'message': 'Integration deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

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


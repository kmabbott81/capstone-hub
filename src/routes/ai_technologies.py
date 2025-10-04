from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.ai_technology import AITechnology
from src.models.database import db
from src.routes.auth import require_admin
from src.extensions import csrf

ai_technologies_bp = Blueprint('ai_technologies', __name__)

@ai_technologies_bp.route('/api/ai-technologies', methods=['GET'])
def get_ai_technologies():
    """Get all AI technologies"""
    technologies = AITechnology.query.all()
    return jsonify([tech.to_dict() for tech in technologies])

@ai_technologies_bp.route('/api/ai-technologies', methods=['POST'])
@require_admin
@csrf.protect()
def create_ai_technology():
    """Create a new AI technology"""
    data = request.get_json()

    try:
        ai_tech = AITechnology(
            name=data.get('name'),
            description=data.get('description', ''),
            category=data.get('category'),
            subcategory=data.get('subcategory', ''),
            platform_provider=data.get('platform_provider', ''),
            pricing_model=data.get('pricing_model', ''),
            pricing_details=data.get('pricing_details', ''),
            use_cases=data.get('use_cases', ''),
            hl_stearns_applications=data.get('hl_stearns_applications', ''),
            integration_complexity=data.get('integration_complexity', 'Medium'),
            technical_requirements=data.get('technical_requirements', ''),
            data_requirements=data.get('data_requirements', ''),
            security_considerations=data.get('security_considerations', ''),
            evaluation_status=data.get('evaluation_status', 'Not Evaluated'),
            pilot_status=data.get('pilot_status', ''),
            roi_potential=data.get('roi_potential', 'Medium'),
            implementation_priority=data.get('implementation_priority', 'Medium'),
            competitive_advantage=data.get('competitive_advantage', 'Medium'),
            learning_curve=data.get('learning_curve', 'Medium'),
            vendor_support=data.get('vendor_support', 'Good'),
            api_availability=data.get('api_availability', False),
            custom_training_possible=data.get('custom_training_possible', False),
            on_premise_option=data.get('on_premise_option', False),
            compliance_ready=data.get('compliance_ready', False),
            notes=data.get('notes', '')
        )

        db.session.add(ai_tech)
        db.session.commit()

        return jsonify(ai_tech.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_technologies_bp.route('/api/ai-technologies/<int:tech_id>', methods=['PUT'])
@require_admin
@csrf.protect()
def update_ai_technology(tech_id):
    """Update an existing AI technology"""
    data = request.get_json()
    tech = AITechnology.query.get(tech_id)

    if not tech:
        return jsonify({'error': 'AI technology not found'}), 404

    try:
        tech.name = data.get('name', tech.name)
        tech.description = data.get('description', tech.description)
        tech.category = data.get('category', tech.category)
        tech.subcategory = data.get('subcategory', tech.subcategory)
        tech.platform_provider = data.get('platform_provider', tech.platform_provider)
        tech.pricing_model = data.get('pricing_model', tech.pricing_model)
        tech.pricing_details = data.get('pricing_details', tech.pricing_details)
        tech.use_cases = data.get('use_cases', tech.use_cases)
        tech.hl_stearns_applications = data.get('hl_stearns_applications', tech.hl_stearns_applications)
        tech.integration_complexity = data.get('integration_complexity', tech.integration_complexity)
        tech.technical_requirements = data.get('technical_requirements', tech.technical_requirements)
        tech.data_requirements = data.get('data_requirements', tech.data_requirements)
        tech.security_considerations = data.get('security_considerations', tech.security_considerations)
        tech.evaluation_status = data.get('evaluation_status', tech.evaluation_status)
        tech.pilot_status = data.get('pilot_status', tech.pilot_status)
        tech.roi_potential = data.get('roi_potential', tech.roi_potential)
        tech.implementation_priority = data.get('implementation_priority', tech.implementation_priority)
        tech.competitive_advantage = data.get('competitive_advantage', tech.competitive_advantage)
        tech.learning_curve = data.get('learning_curve', tech.learning_curve)
        tech.vendor_support = data.get('vendor_support', tech.vendor_support)
        tech.api_availability = data.get('api_availability', tech.api_availability)
        tech.custom_training_possible = data.get('custom_training_possible', tech.custom_training_possible)
        tech.on_premise_option = data.get('on_premise_option', tech.on_premise_option)
        tech.compliance_ready = data.get('compliance_ready', tech.compliance_ready)
        tech.notes = data.get('notes', tech.notes)
        tech.updated_at = datetime.utcnow()

        db.session.commit()
        return jsonify(tech.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_technologies_bp.route('/api/ai-technologies/<int:tech_id>', methods=['DELETE'])
@require_admin
@csrf.protect()
def delete_ai_technology(tech_id):
    """Delete an AI technology"""
    tech = AITechnology.query.get(tech_id)

    if not tech:
        return jsonify({'error': 'AI technology not found'}), 404

    try:
        db.session.delete(tech)
        db.session.commit()
        return jsonify({'message': 'AI technology deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@ai_technologies_bp.route('/api/ai-technologies/categories', methods=['GET'])
def get_ai_categories():
    """Get all AI technology categories"""
    categories = {
        'Generative AI': [
            'Text Generation',
            'Image Generation', 
            'Code Generation',
            'Audio Generation',
            'Video Generation'
        ],
        'Agentic AI': [
            'Autonomous Agents',
            'Multi-Agent Systems',
            'Decision Making Agents',
            'Task Automation Agents'
        ],
        'Embedded AI': [
            'CRM AI Features',
            'ERP AI Modules',
            'Business Intelligence AI',
            'Workflow Automation AI'
        ],
        'Predictive AI': [
            'Demand Forecasting',
            'Risk Assessment',
            'Customer Behavior Prediction',
            'Maintenance Prediction'
        ],
        'Computer Vision': [
            'Image Recognition',
            'Document Processing',
            'Quality Control',
            'Inventory Management'
        ],
        'Natural Language Processing': [
            'Chatbots',
            'Document Analysis',
            'Sentiment Analysis',
            'Language Translation'
        ],
        'Machine Learning': [
            'Classification',
            'Regression',
            'Clustering',
            'Recommendation Systems'
        ]
    }
    return jsonify(categories)

@ai_technologies_bp.route('/api/ai-technologies/providers', methods=['GET'])
def get_ai_providers():
    """Get major AI platform providers"""
    providers = [
        'OpenAI',
        'Microsoft Azure AI',
        'Google Cloud AI',
        'Amazon AWS AI',
        'IBM Watson',
        'Anthropic',
        'Hugging Face',
        'Salesforce Einstein',
        'ServiceNow AI',
        'UiPath AI',
        'Other'
    ]
    return jsonify(providers)


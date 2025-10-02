from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.ai_technology import AITechnology
from src.models.database import db

ai_technologies_bp = Blueprint('ai_technologies', __name__)

@ai_technologies_bp.route('/api/ai-technologies', methods=['GET'])
def get_ai_technologies():
    """Get all AI technologies"""
    technologies = AITechnology.query.all()
    return jsonify([tech.to_dict() for tech in technologies])

@ai_technologies_bp.route('/api/ai-technologies', methods=['POST'])
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
def update_ai_technology(tech_id):
    """Update an existing AI technology"""
    data = request.get_json()
    
    for tech in ai_tech_data:
        if tech['id'] == tech_id:
            tech.update({
                'name': data.get('name', tech['name']),
                'description': data.get('description', tech['description']),
                'category': data.get('category', tech['category']),
                'subcategory': data.get('subcategory', tech['subcategory']),
                'provider': data.get('provider', tech['provider']),
                'platform': data.get('platform', tech['platform']),
                'use_cases': data.get('use_cases', tech['use_cases']),
                'capabilities': data.get('capabilities', tech['capabilities']),
                'limitations': data.get('limitations', tech['limitations']),
                'pricing_model': data.get('pricing_model', tech['pricing_model']),
                'integration_complexity': data.get('integration_complexity', tech['integration_complexity']),
                'evaluation_status': data.get('evaluation_status', tech['evaluation_status']),
                'priority': data.get('priority', tech['priority']),
                'business_impact': data.get('business_impact', tech['business_impact']),
                'technical_requirements': data.get('technical_requirements', tech['technical_requirements']),
                'security_considerations': data.get('security_considerations', tech['security_considerations']),
                'roi_potential': data.get('roi_potential', tech['roi_potential']),
                'implementation_timeline': data.get('implementation_timeline', tech['implementation_timeline']),
                'updated_at': datetime.now().isoformat()
            })
            return jsonify(tech)
    
    return jsonify({'error': 'AI technology not found'}), 404

@ai_technologies_bp.route('/api/ai-technologies/<int:tech_id>', methods=['DELETE'])
def delete_ai_technology(tech_id):
    """Delete an AI technology"""
    global ai_tech_data
    ai_tech_data = [t for t in ai_tech_data if t['id'] != tech_id]
    return jsonify({'message': 'AI technology deleted successfully'})

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


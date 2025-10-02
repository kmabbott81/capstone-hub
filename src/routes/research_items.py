from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.research_item import ResearchItem
from src.models.database import db

research_items_bp = Blueprint('research_items', __name__)

@research_items_bp.route('/api/research-items', methods=['GET'])
def get_research_items():
    """Get all research items"""
    items = ResearchItem.query.all()
    return jsonify([{
        'id': item.id,
        'title': item.title,
        'description': item.description,
        'research_type': item.research_type,
        'research_method': item.research_method,
        'completion_status': item.completion_status,
        'quality_score': item.quality_score,
        'relevance_score': item.relevance_score,
        'credibility_score': item.credibility_score,
        'priority': item.priority,
        'created_at': item.created_at.isoformat(),
        'updated_at': item.updated_at.isoformat()
    } for item in items])

@research_items_bp.route('/api/research-items', methods=['POST'])
def create_research_item():
    """Create a new research item"""
    data = request.get_json()

    try:
        research_item = ResearchItem(
            title=data.get('title'),
            description=data.get('description', ''),
            research_type=data.get('research_type'),
            research_method=data.get('research_method', ''),
            completion_status=data.get('status', 'Not Started'),
            priority=data.get('priority', 'Medium')
        )

        db.session.add(research_item)
        db.session.commit()

        return jsonify({
            'id': research_item.id,
            'title': research_item.title,
            'description': research_item.description,
            'research_type': research_item.research_type,
            'research_method': research_item.research_method,
            'completion_status': research_item.completion_status,
            'quality_score': research_item.quality_score,
            'relevance_score': research_item.relevance_score,
            'credibility_score': research_item.credibility_score,
            'priority': research_item.priority,
            'created_at': research_item.created_at.isoformat(),
            'updated_at': research_item.updated_at.isoformat()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@research_items_bp.route('/api/research-items/<int:item_id>', methods=['PUT'])
def update_research_item(item_id):
    """Update an existing research item"""
    data = request.get_json()
    item = ResearchItem.query.get(item_id)

    if not item:
        return jsonify({'error': 'Research item not found'}), 404

    try:
        item.title = data.get('title', item.title)
        item.description = data.get('description', item.description)
        item.research_type = data.get('research_type', item.research_type)
        item.research_method = data.get('research_method', item.research_method)
        item.completion_status = data.get('status', item.completion_status)
        item.priority = data.get('priority', item.priority)
        item.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'research_type': item.research_type,
            'research_method': item.research_method,
            'completion_status': item.completion_status,
            'priority': item.priority,
            'created_at': item.created_at.isoformat(),
            'updated_at': item.updated_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@research_items_bp.route('/api/research-items/<int:item_id>', methods=['DELETE'])
def delete_research_item(item_id):
    """Delete a research item"""
    item = ResearchItem.query.get(item_id)

    if not item:
        return jsonify({'error': 'Research item not found'}), 404

    try:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Research item deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@research_items_bp.route('/api/research-items/methods', methods=['GET'])
def get_research_methods():
    """Get available research methods"""
    methods = {
        'Primary Research': [
            'Interviews',
            'Surveys',
            'Focus Groups',
            'Observations',
            'Case Studies',
            'Experiments',
            'Field Studies',
            'Ethnographic Studies'
        ],
        'Secondary Research': [
            'Literature Review',
            'Industry Reports',
            'Academic Papers',
            'Government Data',
            'Company Reports',
            'Market Research',
            'Competitive Analysis',
            'Historical Data Analysis'
        ]
    }
    return jsonify(methods)

@research_items_bp.route('/api/research-items/suggested-questions', methods=['GET'])
def get_suggested_questions():
    """Get suggested research questions by category"""
    questions = {
        'Business Process Analysis': [
            'What are the current pain points in this process?',
            'How much time does this process currently take?',
            'What are the costs associated with this process?',
            'Who are the key stakeholders involved?',
            'What tools/systems are currently used?',
            'What would success look like for this process?',
            'What are the compliance/regulatory requirements?',
            'What are the biggest bottlenecks?'
        ],
        'Technology Evaluation': [
            'What are the key features required?',
            'How does this integrate with existing systems?',
            'What is the total cost of ownership?',
            'What training would be required?',
            'What are the security implications?',
            'How scalable is this solution?',
            'What is the vendor support like?',
            'What are the implementation timelines?'
        ],
        'Stakeholder Interviews': [
            'What are your biggest challenges in your current role?',
            'How do you currently handle [specific process]?',
            'What would make your job easier?',
            'What concerns do you have about new technology?',
            'How do you measure success in your department?',
            'What training or support would you need?',
            'How do you see this impacting your workflow?',
            'What questions do you have about the proposed changes?'
        ],
        'Market Research': [
            'Who are the key competitors in this space?',
            'What are the industry trends?',
            'What are the best practices in similar companies?',
            'What are the regulatory considerations?',
            'What are the emerging technologies?',
            'What are the cost benchmarks?',
            'What are the implementation challenges?',
            'What are the success factors?'
        ]
    }
    return jsonify(questions)

@research_items_bp.route('/api/research-items/data-sources', methods=['GET'])
def get_data_sources():
    """Get suggested data sources"""
    sources = {
        'Academic': [
            'Google Scholar',
            'JSTOR',
            'IEEE Xplore',
            'ACM Digital Library',
            'ResearchGate',
            'Academia.edu',
            'PubMed',
            'SSRN'
        ],
        'Industry': [
            'Gartner',
            'Forrester',
            'IDC',
            'McKinsey Global Institute',
            'Deloitte Insights',
            'PwC Research',
            'KPMG Insights',
            'EY Insights'
        ],
        'Government': [
            'Bureau of Labor Statistics',
            'Census Bureau',
            'SEC Filings',
            'Federal Trade Commission',
            'Department of Commerce',
            'Small Business Administration',
            'NIST',
            'GAO Reports'
        ],
        'Business': [
            'Company Annual Reports',
            'Industry Association Reports',
            'Trade Publications',
            'Conference Proceedings',
            'Vendor White Papers',
            'Case Studies',
            'Press Releases',
            'Financial Reports'
        ]
    }
    return jsonify(sources)


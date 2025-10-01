from flask import Blueprint, request, jsonify
from datetime import datetime

research_items_bp = Blueprint('research_items', __name__)

# In-memory storage for demonstration (replace with database in production)
research_data = []

@research_items_bp.route('/research-items', methods=['GET'])
def get_research_items():
    """Get all research items"""
    return jsonify(research_data)

@research_items_bp.route('/research-items', methods=['POST'])
def create_research_item():
    """Create a new research item"""
    data = request.get_json()
    
    research_item = {
        'id': len(research_data) + 1,
        'title': data.get('title'),
        'description': data.get('description', ''),
        'research_type': data.get('research_type'),  # Primary, Secondary
        'research_method': data.get('research_method', ''),
        'data_source': data.get('data_source', ''),
        'participants': data.get('participants', []),
        'questions': data.get('questions', []),
        'findings': data.get('findings', ''),
        'insights': data.get('insights', []),
        'recommendations': data.get('recommendations', []),
        'status': data.get('status', 'Planned'),
        'priority': data.get('priority', 'Medium'),
        'start_date': data.get('start_date'),
        'completion_date': data.get('completion_date'),
        'estimated_hours': data.get('estimated_hours', 0),
        'actual_hours': data.get('actual_hours', 0),
        'budget': data.get('budget', 0),
        'tags': data.get('tags', []),
        'related_processes': data.get('related_processes', []),
        'related_technologies': data.get('related_technologies', []),
        'documents': data.get('documents', []),
        'links': data.get('links', []),
        'quality_score': data.get('quality_score', 0),
        'reliability_score': data.get('reliability_score', 0),
        'relevance_score': data.get('relevance_score', 0),
        'notes': data.get('notes', ''),
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat()
    }
    
    research_data.append(research_item)
    return jsonify(research_item), 201

@research_items_bp.route('/research-items/<int:item_id>', methods=['PUT'])
def update_research_item(item_id):
    """Update an existing research item"""
    data = request.get_json()
    
    for item in research_data:
        if item['id'] == item_id:
            item.update({
                'title': data.get('title', item['title']),
                'description': data.get('description', item['description']),
                'research_type': data.get('research_type', item['research_type']),
                'research_method': data.get('research_method', item['research_method']),
                'data_source': data.get('data_source', item['data_source']),
                'participants': data.get('participants', item['participants']),
                'questions': data.get('questions', item['questions']),
                'findings': data.get('findings', item['findings']),
                'insights': data.get('insights', item['insights']),
                'recommendations': data.get('recommendations', item['recommendations']),
                'status': data.get('status', item['status']),
                'priority': data.get('priority', item['priority']),
                'start_date': data.get('start_date', item['start_date']),
                'completion_date': data.get('completion_date', item['completion_date']),
                'estimated_hours': data.get('estimated_hours', item['estimated_hours']),
                'actual_hours': data.get('actual_hours', item['actual_hours']),
                'budget': data.get('budget', item['budget']),
                'tags': data.get('tags', item['tags']),
                'related_processes': data.get('related_processes', item['related_processes']),
                'related_technologies': data.get('related_technologies', item['related_technologies']),
                'documents': data.get('documents', item['documents']),
                'links': data.get('links', item['links']),
                'quality_score': data.get('quality_score', item['quality_score']),
                'reliability_score': data.get('reliability_score', item['reliability_score']),
                'relevance_score': data.get('relevance_score', item['relevance_score']),
                'notes': data.get('notes', item['notes']),
                'updated_at': datetime.now().isoformat()
            })
            return jsonify(item)
    
    return jsonify({'error': 'Research item not found'}), 404

@research_items_bp.route('/research-items/<int:item_id>', methods=['DELETE'])
def delete_research_item(item_id):
    """Delete a research item"""
    global research_data
    research_data = [r for r in research_data if r['id'] != item_id]
    return jsonify({'message': 'Research item deleted successfully'})

@research_items_bp.route('/research-items/methods', methods=['GET'])
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

@research_items_bp.route('/research-items/suggested-questions', methods=['GET'])
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

@research_items_bp.route('/research-items/data-sources', methods=['GET'])
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


from datetime import datetime
from src.models.database import db

class ResearchItem(db.Model):
    __tablename__ = 'research_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    research_type = db.Column(db.String(50), nullable=False)  # Primary, Secondary
    research_method = db.Column(db.String(100))  # Interview, Survey, Literature Review, Case Study, etc.
    category = db.Column(db.String(100))  # Industry Analysis, Technology Assessment, Competitive Analysis, etc.
    source_type = db.Column(db.String(100))  # Academic, Industry Report, Interview, Survey, etc.
    source_details = db.Column(db.Text)  # Publication, URL, Contact info, etc.
    target_audience = db.Column(db.String(200))  # Who to interview/survey
    suggested_questions = db.Column(db.Text)  # JSON string of questions
    data_collection_method = db.Column(db.String(100))  # Online, Phone, In-person, Email
    sample_size_target = db.Column(db.Integer)
    sample_size_actual = db.Column(db.Integer)
    completion_status = db.Column(db.String(50), default='Not Started')  # Not Started, In Progress, Completed
    quality_score = db.Column(db.Integer)  # 1-10 rating
    relevance_score = db.Column(db.Integer)  # 1-10 rating
    credibility_score = db.Column(db.Integer)  # 1-10 rating
    key_findings = db.Column(db.Text)
    actionable_insights = db.Column(db.Text)
    supporting_evidence = db.Column(db.Text)
    limitations = db.Column(db.Text)
    follow_up_needed = db.Column(db.Boolean, default=False)
    follow_up_actions = db.Column(db.Text)
    related_deliverables = db.Column(db.Text)  # JSON string of deliverable IDs
    storage_location = db.Column(db.String(200))  # Notion, Google Drive, etc.
    storage_url = db.Column(db.String(500))
    tags = db.Column(db.Text)  # JSON string of tags
    priority = db.Column(db.String(20), default='Medium')  # High, Medium, Low
    deadline = db.Column(db.Date)
    assigned_to = db.Column(db.String(100))
    review_status = db.Column(db.String(50))  # Not Reviewed, Under Review, Approved
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'research_type': self.research_type,
            'research_method': self.research_method,
            'category': self.category,
            'source_type': self.source_type,
            'source_details': self.source_details,
            'target_audience': self.target_audience,
            'suggested_questions': self.suggested_questions,
            'data_collection_method': self.data_collection_method,
            'sample_size_target': self.sample_size_target,
            'sample_size_actual': self.sample_size_actual,
            'completion_status': self.completion_status,
            'quality_score': self.quality_score,
            'relevance_score': self.relevance_score,
            'credibility_score': self.credibility_score,
            'key_findings': self.key_findings,
            'actionable_insights': self.actionable_insights,
            'supporting_evidence': self.supporting_evidence,
            'limitations': self.limitations,
            'follow_up_needed': self.follow_up_needed,
            'follow_up_actions': self.follow_up_actions,
            'related_deliverables': self.related_deliverables,
            'storage_location': self.storage_location,
            'storage_url': self.storage_url,
            'tags': self.tags,
            'priority': self.priority,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'assigned_to': self.assigned_to,
            'review_status': self.review_status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


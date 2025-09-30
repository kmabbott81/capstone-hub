from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class AITechnology(db.Model):
    __tablename__ = 'ai_technologies'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)  # Generative, Agentic, Embedded, Predictive, etc.
    subcategory = db.Column(db.String(100))  # LLM, Computer Vision, NLP, RPA, etc.
    platform_provider = db.Column(db.String(100))  # OpenAI, Microsoft, Google, etc.
    pricing_model = db.Column(db.String(100))  # Per token, Subscription, One-time, Free
    pricing_details = db.Column(db.Text)
    use_cases = db.Column(db.Text)  # JSON string of use cases
    hl_stearns_applications = db.Column(db.Text)  # Specific applications for HL Stearns
    integration_complexity = db.Column(db.String(20))  # Easy, Medium, Hard
    technical_requirements = db.Column(db.Text)
    data_requirements = db.Column(db.Text)
    security_considerations = db.Column(db.Text)
    evaluation_status = db.Column(db.String(50), default='Not Evaluated')  # Not Evaluated, Testing, Approved, Rejected
    pilot_status = db.Column(db.String(50))  # Not Started, Planning, In Progress, Completed
    roi_potential = db.Column(db.String(20))  # High, Medium, Low
    implementation_priority = db.Column(db.String(20))  # High, Medium, Low
    competitive_advantage = db.Column(db.String(20))  # High, Medium, Low
    learning_curve = db.Column(db.String(20))  # Easy, Medium, Steep
    vendor_support = db.Column(db.String(20))  # Excellent, Good, Fair, Poor
    api_availability = db.Column(db.Boolean, default=False)
    custom_training_possible = db.Column(db.Boolean, default=False)
    on_premise_option = db.Column(db.Boolean, default=False)
    compliance_ready = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'subcategory': self.subcategory,
            'platform_provider': self.platform_provider,
            'pricing_model': self.pricing_model,
            'pricing_details': self.pricing_details,
            'use_cases': self.use_cases,
            'hl_stearns_applications': self.hl_stearns_applications,
            'integration_complexity': self.integration_complexity,
            'technical_requirements': self.technical_requirements,
            'data_requirements': self.data_requirements,
            'security_considerations': self.security_considerations,
            'evaluation_status': self.evaluation_status,
            'pilot_status': self.pilot_status,
            'roi_potential': self.roi_potential,
            'implementation_priority': self.implementation_priority,
            'competitive_advantage': self.competitive_advantage,
            'learning_curve': self.learning_curve,
            'vendor_support': self.vendor_support,
            'api_availability': self.api_availability,
            'custom_training_possible': self.custom_training_possible,
            'on_premise_option': self.on_premise_option,
            'compliance_ready': self.compliance_ready,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


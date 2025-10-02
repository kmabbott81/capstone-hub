from src.models.database import db
from datetime import datetime


class SoftwareTool(db.Model):
    __tablename__ = 'software_tools'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)  # CRM, ERP, Cloud, Analytics, etc.
    tool_type = db.Column(db.String(50))  # Core, Optional, Integration, Utility
    vendor = db.Column(db.String(100))
    pricing_model = db.Column(db.String(100))  # Per user, Per month, One-time, Freemium
    pricing_details = db.Column(db.Text)
    features = db.Column(db.Text)  # JSON string of key features
    hl_stearns_fit = db.Column(db.String(20))  # Excellent, Good, Fair, Poor
    current_usage = db.Column(db.String(50))  # Currently Used, Previously Used, Never Used
    replacement_for = db.Column(db.String(200))  # What current tool this would replace
    integration_capabilities = db.Column(db.Text)
    data_migration_complexity = db.Column(db.String(20))  # Easy, Medium, Hard
    training_requirements = db.Column(db.Text)
    support_quality = db.Column(db.String(20))  # Excellent, Good, Fair, Poor
    scalability = db.Column(db.String(20))  # High, Medium, Low
    security_features = db.Column(db.Text)
    mobile_support = db.Column(db.Boolean, default=False)
    cloud_based = db.Column(db.Boolean, default=True)
    on_premise_option = db.Column(db.Boolean, default=False)
    api_quality = db.Column(db.String(20))  # Excellent, Good, Fair, Poor, None
    customization_level = db.Column(db.String(20))  # High, Medium, Low
    evaluation_status = db.Column(db.String(50), default='Not Evaluated')  # Not Evaluated, Evaluating, Approved, Rejected
    implementation_priority = db.Column(db.String(20))  # High, Medium, Low
    roi_potential = db.Column(db.String(20))  # High, Medium, Low
    risk_level = db.Column(db.String(20))  # High, Medium, Low
    decision_status = db.Column(db.String(50))  # Pending, Approved, Rejected, Deferred
    pilot_results = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'tool_type': self.tool_type,
            'vendor': self.vendor,
            'pricing_model': self.pricing_model,
            'pricing_details': self.pricing_details,
            'features': self.features,
            'hl_stearns_fit': self.hl_stearns_fit,
            'current_usage': self.current_usage,
            'replacement_for': self.replacement_for,
            'integration_capabilities': self.integration_capabilities,
            'data_migration_complexity': self.data_migration_complexity,
            'training_requirements': self.training_requirements,
            'support_quality': self.support_quality,
            'scalability': self.scalability,
            'security_features': self.security_features,
            'mobile_support': self.mobile_support,
            'cloud_based': self.cloud_based,
            'on_premise_option': self.on_premise_option,
            'api_quality': self.api_quality,
            'customization_level': self.customization_level,
            'evaluation_status': self.evaluation_status,
            'implementation_priority': self.implementation_priority,
            'roi_potential': self.roi_potential,
            'risk_level': self.risk_level,
            'decision_status': self.decision_status,
            'pilot_results': self.pilot_results,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


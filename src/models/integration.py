from src.models.database import db
from datetime import datetime


class Integration(db.Model):
    __tablename__ = 'integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    platform = db.Column(db.String(100), nullable=False)  # Notion, Microsoft, Google, etc.
    integration_type = db.Column(db.String(100))  # API, Webhook, Export/Import, etc.
    purpose = db.Column(db.Text)  # What this integration accomplishes
    data_sync_direction = db.Column(db.String(50))  # Bidirectional, To Platform, From Platform
    sync_frequency = db.Column(db.String(50))  # Real-time, Hourly, Daily, Manual
    api_endpoint = db.Column(db.String(500))
    authentication_method = db.Column(db.String(100))  # OAuth, API Key, Basic Auth
    credentials_stored = db.Column(db.Boolean, default=False)
    setup_status = db.Column(db.String(50), default='Not Configured')  # Not Configured, In Progress, Active, Error
    last_sync = db.Column(db.DateTime)
    sync_status = db.Column(db.String(50))  # Success, Failed, Partial
    error_log = db.Column(db.Text)
    data_mapping = db.Column(db.Text)  # JSON string of field mappings
    filters_applied = db.Column(db.Text)  # JSON string of sync filters
    security_considerations = db.Column(db.Text)
    compliance_notes = db.Column(db.Text)
    performance_metrics = db.Column(db.Text)  # JSON string of performance data
    usage_statistics = db.Column(db.Text)  # JSON string of usage stats
    configuration_notes = db.Column(db.Text)
    troubleshooting_guide = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'platform': self.platform,
            'integration_type': self.integration_type,
            'purpose': self.purpose,
            'data_sync_direction': self.data_sync_direction,
            'sync_frequency': self.sync_frequency,
            'api_endpoint': self.api_endpoint,
            'authentication_method': self.authentication_method,
            'credentials_stored': self.credentials_stored,
            'setup_status': self.setup_status,
            'last_sync': self.last_sync.isoformat() if self.last_sync else None,
            'sync_status': self.sync_status,
            'error_log': self.error_log,
            'data_mapping': self.data_mapping,
            'filters_applied': self.filters_applied,
            'security_considerations': self.security_considerations,
            'compliance_notes': self.compliance_notes,
            'performance_metrics': self.performance_metrics,
            'usage_statistics': self.usage_statistics,
            'configuration_notes': self.configuration_notes,
            'troubleshooting_guide': self.troubleshooting_guide,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


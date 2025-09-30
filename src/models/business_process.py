from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class BusinessProcess(db.Model):
    __tablename__ = 'business_processes'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    department = db.Column(db.String(100))  # Sales, Operations, Customer Service, Finance, etc.
    process_type = db.Column(db.String(100))  # Core, Support, Management
    current_system = db.Column(db.String(100))  # Podio, QuickBooks, Manual, etc.
    pain_points = db.Column(db.Text)
    automation_potential = db.Column(db.String(20))  # High, Medium, Low
    ai_opportunity = db.Column(db.String(20))  # High, Medium, Low, None
    complexity_score = db.Column(db.Integer)  # 1-10 scale
    frequency = db.Column(db.String(50))  # Daily, Weekly, Monthly, Quarterly
    stakeholders = db.Column(db.Text)  # JSON string of stakeholder roles
    current_time_hours = db.Column(db.Float)  # Hours per execution
    target_time_hours = db.Column(db.Float)  # Target hours after optimization
    cost_impact = db.Column(db.String(20))  # High, Medium, Low
    customer_impact = db.Column(db.String(20))  # High, Medium, Low
    evaluation_status = db.Column(db.String(50), default='Not Started')  # Not Started, In Progress, Evaluated, Implemented
    priority_score = db.Column(db.Integer)  # 1-100 calculated score
    implementation_difficulty = db.Column(db.String(20))  # Easy, Medium, Hard
    roi_potential = db.Column(db.String(20))  # High, Medium, Low
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'department': self.department,
            'process_type': self.process_type,
            'current_system': self.current_system,
            'pain_points': self.pain_points,
            'automation_potential': self.automation_potential,
            'ai_opportunity': self.ai_opportunity,
            'complexity_score': self.complexity_score,
            'frequency': self.frequency,
            'stakeholders': self.stakeholders,
            'current_time_hours': self.current_time_hours,
            'target_time_hours': self.target_time_hours,
            'cost_impact': self.cost_impact,
            'customer_impact': self.customer_impact,
            'evaluation_status': self.evaluation_status,
            'priority_score': self.priority_score,
            'implementation_difficulty': self.implementation_difficulty,
            'roi_potential': self.roi_potential,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


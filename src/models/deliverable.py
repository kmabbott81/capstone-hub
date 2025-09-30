from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Deliverable(db.Model):
    __tablename__ = 'deliverables'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    phase = db.Column(db.String(100), nullable=False)
    week_number = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(50), default='Not Started')  # Not Started, In Progress, Completed, Overdue
    priority = db.Column(db.String(20), default='Medium')  # High, Medium, Low
    category = db.Column(db.String(100))  # Research, Analysis, Documentation, Presentation
    estimated_hours = db.Column(db.Integer)
    actual_hours = db.Column(db.Integer)
    completion_percentage = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text)
    dependencies = db.Column(db.Text)  # JSON string of dependent deliverable IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'phase': self.phase,
            'week_number': self.week_number,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'priority': self.priority,
            'category': self.category,
            'estimated_hours': self.estimated_hours,
            'actual_hours': self.actual_hours,
            'completion_percentage': self.completion_percentage,
            'notes': self.notes,
            'dependencies': self.dependencies,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


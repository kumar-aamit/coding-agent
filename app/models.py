from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class DowntimeTicket(Base):
    __tablename__ = 'downtime_tickets'
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, nullable=False)
    line_area = Column(String, nullable=False)
    stop_reason_category = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Enum('low', 'medium', 'high', 'critical'), nullable=False, default='medium')
    operator_name = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    status = Column(Enum('open', 'in_progress', 'resolved'), nullable=False, default='open')
    resolution_notes = Column(Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'machine_id': self.machine_id,
            'line_area': self.line_area,
            'stop_reason_category': self.stop_reason_category,
            'description': self.description,
            'severity': self.severity,
            'operator_name': self.operator_name,
            'timestamp': self.timestamp,
            'status': self.status,
            'resolution_notes': self.resolution_notes
        }
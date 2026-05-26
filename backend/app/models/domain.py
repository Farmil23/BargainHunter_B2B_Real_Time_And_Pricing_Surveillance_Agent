from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.sql import func
from backend.app.db.session import Base

class SurveillanceTask(Base):
    __tablename__ = "surveillance_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    target_url = Column(String(512), index=True)
    target_component = Column(String(255))
    status = Column(String(50), default="pending")  # pending, running, completed, failed
    result_data = Column(Text, nullable=True)  # JSON string of the result
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

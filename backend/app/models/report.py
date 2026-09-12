import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("interview_sessions.id"), nullable=False)
    overall_score = Column(Integer, nullable=False) # e.g. 8 (out of 10)
    overall_performance = Column(String, nullable=False) # "Excellent", "Good", "Average", "Needs Improvement"
    time_taken_mins = Column(Integer, nullable=False, default=15)
    topics_covered = Column(JSON, default=list) # e.g. ["System Design", "Databases", "APIs", "Backend Development", "Problem Solving"]
    key_insights = Column(JSON, default=list) # list of text insight points
    summary = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="report")

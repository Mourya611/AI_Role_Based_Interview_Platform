import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size_bytes = Column(String, nullable=True)
    raw_text = Column(Text, nullable=False)
    candidate_name = Column(String, nullable=True)
    parsed_skills = Column(JSON, nullable=True, default=list)
    parsed_technologies = Column(JSON, nullable=True, default=list)
    parsed_projects = Column(JSON, nullable=True, default=list)
    ml_ai_experience = Column(JSON, nullable=True, default=list)
    genai_rag_experience = Column(JSON, nullable=True, default=list)
    cloud_ml_deployment_experience = Column(JSON, nullable=True, default=list)
    domain_exposure = Column(JSON, nullable=True, default=list)
    summary = Column(Text, nullable=True)
    candidate_profile = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="resumes")
    interviews = relationship("InterviewSession", back_populates="resume")

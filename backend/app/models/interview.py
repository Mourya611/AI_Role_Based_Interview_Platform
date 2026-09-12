import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    resume_id = Column(String, ForeignKey("resumes.id"), nullable=True)
    target_role = Column(String, nullable=False) # e.g. "Backend Engineer"
    status = Column(String, nullable=False, default="in_progress") # "in_progress", "completed", "cancelled"
    current_difficulty = Column(String, nullable=False, default="Medium") # "Easy", "Medium", "Hard"
    current_question_number = Column(Integer, default=1)
    total_questions = Column(Integer, default=5)
    requested_question_count = Column(Integer, default=5)
    candidate_profile = Column(JSON, nullable=True)
    blueprint = Column(JSON, nullable=True)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="interviews")
    resume = relationship("Resume", back_populates="interviews")
    questions = relationship("Question", back_populates="session", cascade="all, delete-orphan", order_by="Question.question_number")
    answers = relationship("Answer", back_populates="session", cascade="all, delete-orphan")
    report = relationship("Report", back_populates="session", uselist=False, cascade="all, delete-orphan")

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Answer(Base):
    __tablename__ = "answers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("interview_sessions.id"), nullable=False)
    question_id = Column(String, ForeignKey("questions.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    selected_option = Column(String, nullable=True) # for MCQ option selected e.g. "A", "B", "C", "D" or full text
    score = Column(Integer, nullable=False) # 1 - 10
    rating = Column(String, nullable=False) # "Excellent", "Good Answer", "Average", "Needs Improvement"
    feedback = Column(Text, nullable=False)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    concepts_detected = Column(JSON, default=list)
    recommended_next_difficulty = Column(String, default="Medium")
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="answers")
    question = relationship("Question", back_populates="answer")

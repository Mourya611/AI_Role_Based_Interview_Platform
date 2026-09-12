import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String, ForeignKey("interview_sessions.id"), nullable=False)
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    topic = Column(String, nullable=False) # e.g. "Model Architecture", "Vector Search"
    subtopic = Column(String, nullable=True)
    concept = Column(String, nullable=True)
    difficulty = Column(String, nullable=False, default="Medium")
    question_type = Column(String, nullable=False, default="descriptive") # 'mcq', 'short_answer', 'descriptive', 'scenario'
    options = Column(JSON, nullable=True) # list of 4 options for MCQ
    correct_answer = Column(Text, nullable=True) # for MCQ or expected key answer
    explanation = Column(Text, nullable=True) # explanation for answer
    question_hash = Column(String, nullable=True) # normalized hash for L1 deduplication
    question_embedding = Column(JSON, nullable=True) # vector embedding for L2 deduplication
    resume_evidence = Column(Text, nullable=True) # evidence from candidate profile
    retrieved_context = Column(JSON, nullable=True) # list of retrieved RAG chunks + metadata
    source_metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("InterviewSession", back_populates="questions")
    answer = relationship("Answer", back_populates="question", uselist=False, cascade="all, delete-orphan")

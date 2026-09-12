from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class QuestionType(str, Enum):
    MCQ = "mcq"
    SHORT_ANSWER = "short_answer"
    DESCRIPTIVE = "descriptive"
    SCENARIO = "scenario"

class QuestionClientResponse(BaseModel):
    id: str
    session_id: str
    question_number: int
    question_text: str
    topic: str
    subtopic: Optional[str] = None
    concept: Optional[str] = None
    difficulty: str
    question_type: str = "descriptive"
    options: Optional[List[str]] = None # Only provided if question_type == 'mcq'
    total_questions: Optional[int] = None
    retrieved_context: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True

# Alias for backwards compatibility
QuestionResponse = QuestionClientResponse

class QuestionDetailResponse(BaseModel):
    id: str
    session_id: str
    question_number: int
    question_text: str
    topic: str
    subtopic: Optional[str] = None
    concept: Optional[str] = None
    difficulty: str
    question_type: str = "descriptive"
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    resume_evidence: Optional[str] = None
    retrieved_context: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True

class QuestionGenerationSchema(BaseModel):
    question_text: str = Field(..., description="Clear and concise question text")
    question_type: str = Field(..., description="One of: mcq, short_answer, descriptive, scenario")
    topic: str = Field(..., description="Primary topic strictly matching target role domain")
    subtopic: Optional[str] = Field(None, description="Specific subtopic within domain")
    concept: Optional[str] = Field(None, description="Target technical concept tested")
    difficulty: str = Field("Medium", description="Easy, Medium, or Hard")
    options: Optional[List[str]] = Field(None, description="List of exactly 4 choices if mcq, null otherwise")
    correct_answer: Optional[str] = Field(None, description="Correct option text if mcq, or concise ideal answer")
    explanation: Optional[str] = Field(None, description="Technical rationale for the correct answer")
    resume_evidence: Optional[str] = Field(None, description="Direct tie-in to candidate's verified skills/projects")
    context_reasoning: Optional[str] = Field("Grounded in candidate resume and role RAG context", description="Reasoning")


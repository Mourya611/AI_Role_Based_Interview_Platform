from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class SubmitAnswerRequest(BaseModel):
    question_id: str
    answer_text: str
    selected_option: Optional[str] = None # For MCQ questions e.g. "A", "B", "C", "D" or option text

class AnswerEvaluationSchema(BaseModel):
    score: int = Field(..., description="Score out of 10")
    rating: str = Field(..., description="Rating string: Excellent, Good Answer, Average, or Needs Improvement")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    feedback: str = Field(..., description="Concise feedback on the answer")
    concepts_detected: List[str] = Field(default_factory=list)
    recommended_difficulty: str = Field(default="Medium", description="Easy, Medium, or Hard")

class AnswerResponse(BaseModel):
    id: str
    session_id: str
    question_id: str
    answer_text: str
    selected_option: Optional[str] = None
    score: int
    rating: str
    feedback: str
    strengths: List[str]
    weaknesses: List[str]
    concepts_detected: List[str]
    created_at: datetime

    class Config:
        from_attributes = True

class SubmitAnswerResponse(BaseModel):
    evaluation: AnswerResponse
    next_question: Optional[Any] = None
    is_completed: bool = False

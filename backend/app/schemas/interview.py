from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class CreateInterviewRequest(BaseModel):
    resume_id: str
    target_role: str # e.g., "AI/ML Engineer"
    total_questions: int = Field(5, description="Number of questions: 5, 7, 12, or 15")

    @field_validator("total_questions")
    @classmethod
    def validate_question_count(cls, v: int) -> int:
        if v not in [5, 7, 12, 15]:
            raise ValueError("total_questions must be one of 5, 7, 12, or 15")
        return v

class InterviewSessionResponse(BaseModel):
    id: str
    target_role: str
    status: str
    current_difficulty: str
    current_question_number: int
    total_questions: int
    requested_question_count: Optional[int] = 5
    started_at: datetime
    completed_at: Optional[datetime] = None
    resume_id: Optional[str] = None
    candidate_profile: Optional[Dict[str, Any]] = None
    blueprint: Optional[List[Dict[str, Any]]] = None

    class Config:
        from_attributes = True


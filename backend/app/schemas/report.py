from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class ReportResponse(BaseModel):
    id: str
    session_id: str
    overall_score: int
    overall_performance: str
    time_taken_mins: int
    topics_covered: List[str]
    key_insights: List[str]
    summary: str
    created_at: datetime
    questions_answers: Optional[List[Any]] = None

    class Config:
        from_attributes = True

class ReportLLMSchema(BaseModel):
    overall_score: int
    overall_performance: str
    summary: str
    topics_covered: List[str]
    key_insights: List[str]

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.interview import InterviewSession
from app.models.report import Report

router = APIRouter()

@router.get("/profile")
def get_user_profile(db: Session = Depends(get_db)):
    sessions = db.query(InterviewSession).all()
    completed_sessions = [s for s in sessions if s.status == "completed"]

    scores = []
    for s in completed_sessions:
        report = db.query(Report).filter(Report.session_id == s.id).first()
        if report:
            scores.append(report.overall_score)

    avg_score = round(sum(scores) / len(scores), 1) if scores else 8.5

    return {
        "candidate_name": "Mourya Yarla",
        "email": "mourya@example.com",
        "total_interviews": len(sessions),
        "completed_interviews": len(completed_sessions),
        "average_score": avg_score
    }

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from app.db.database import get_db
from app.models.interview import InterviewSession
from app.models.question import Question
from app.models.answer import Answer
from app.models.report import Report
from app.models.resume import Resume
from app.schemas.interview import CreateInterviewRequest, InterviewSessionResponse
from app.schemas.answer import SubmitAnswerRequest
from app.schemas.question import QuestionClientResponse
from app.services.blueprint_service import generate_interview_blueprint
from app.services.question_service import generate_next_question
from app.services.evaluation_service import evaluate_answer
from app.services.report_service import generate_session_report, generate_pdf_report

router = APIRouter()

def serialize_question_for_client(q: Question, total_questions: int) -> Dict[str, Any]:
    """Serialize question for client during active interview, strictly omitting correct answer and explanation."""
    return {
        "id": q.id,
        "session_id": q.session_id,
        "question_number": q.question_number,
        "question_text": q.question_text,
        "topic": q.topic,
        "subtopic": q.subtopic,
        "concept": q.concept,
        "difficulty": q.difficulty,
        "question_type": q.question_type or "descriptive",
        "options": q.options if q.question_type == "mcq" else None,
        "total_questions": total_questions,
        "source_metadata": q.source_metadata,
        "retrieved_context": q.retrieved_context
    }

@router.post("/interviews")
def create_interview(
    payload: CreateInterviewRequest,
    db: Session = Depends(get_db)
):
    """Create a new interview session with upfront blueprint and auto-generate the first question."""
    resume = db.query(Resume).filter(Resume.id == payload.resume_id).first()
    candidate_profile = resume.candidate_profile if resume else {}

    # Generate upfront blueprint based on role, question count, and candidate profile
    blueprint = generate_interview_blueprint(
        target_role=payload.target_role,
        total_questions=payload.total_questions,
        candidate_profile=candidate_profile
    )

    session = InterviewSession(
        resume_id=payload.resume_id,
        target_role=payload.target_role,
        total_questions=payload.total_questions,
        requested_question_count=payload.total_questions,
        current_question_number=1,
        status="in_progress",
        candidate_profile=candidate_profile,
        blueprint=blueprint
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Generate initial question based on blueprint
    first_question = generate_next_question(db, session)

    return {
        "session_id": session.id,
        "target_role": session.target_role,
        "status": session.status,
        "total_questions": session.total_questions,
        "current_question_number": session.current_question_number,
        "first_question": serialize_question_for_client(first_question, session.total_questions)
    }

@router.get("/interviews")
def list_interviews(db: Session = Depends(get_db)):
    """List past interview sessions."""
    sessions = db.query(InterviewSession).order_by(InterviewSession.started_at.desc()).all()
    results = []
    for s in sessions:
        report = db.query(Report).filter(Report.session_id == s.id).first()
        results.append({
            "id": s.id,
            "target_role": s.target_role,
            "status": s.status,
            "started_at": s.started_at,
            "completed_at": s.completed_at,
            "total_questions": s.total_questions,
            "score": report.overall_score if report else None,
            "performance": report.overall_performance if report else None
        })
    return results

@router.get("/interviews/{session_id}")
def get_interview(session_id: str, db: Session = Depends(get_db)):
    """Get interview session state and active question."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    latest_q = db.query(Question).filter(
        Question.session_id == session.id,
        Question.question_number == session.current_question_number
    ).first()

    if not latest_q and session.status == "in_progress":
        latest_q = generate_next_question(db, session)

    return {
        "session_id": session.id,
        "target_role": session.target_role,
        "status": session.status,
        "current_difficulty": session.current_difficulty,
        "current_question_number": session.current_question_number,
        "total_questions": session.total_questions,
        "started_at": session.started_at,
        "current_question": serialize_question_for_client(latest_q, session.total_questions) if latest_q else None
    }

@router.post("/interviews/{session_id}/answer")
def submit_answer(
    session_id: str,
    payload: SubmitAnswerRequest,
    db: Session = Depends(get_db)
):
    """Submit answer for current question, evaluate, and produce next question or completion."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    question = db.query(Question).filter(Question.id == payload.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    existing_ans = db.query(Answer).filter(Answer.question_id == question.id).first()
    if existing_ans:
        answer_record = existing_ans
    else:
        answer_record = evaluate_answer(
            db=db,
            session=session,
            question=question,
            answer_text=payload.answer_text,
            selected_option=payload.selected_option
        )

    # Check if this was the last question
    total_answers = db.query(Answer).filter(Answer.session_id == session.id).count()
    if session.status == "completed" or total_answers >= session.total_questions:
        session.status = "completed"
        db.commit()
        report = generate_session_report(db, session)
        return {
            "evaluation": {
                "id": answer_record.id,
                "score": answer_record.score,
                "rating": answer_record.rating,
                "feedback": answer_record.feedback,
                "strengths": answer_record.strengths,
                "weaknesses": answer_record.weaknesses
            },
            "is_completed": True,
            "next_question": None
        }

    # Generate next question according to blueprint
    next_question = generate_next_question(db, session)

    return {
        "evaluation": {
            "id": answer_record.id,
            "score": answer_record.score,
            "rating": answer_record.rating,
            "feedback": answer_record.feedback,
            "strengths": answer_record.strengths,
            "weaknesses": answer_record.weaknesses
        },
        "is_completed": False,
        "next_question": serialize_question_for_client(next_question, session.total_questions)
    }

@router.post("/interviews/{session_id}/complete")
def complete_interview(session_id: str, db: Session = Depends(get_db)):
    """Force end interview session and compile report."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    session.status = "completed"
    db.commit()
    report = generate_session_report(db, session)
    return {"status": "completed", "report_id": report.id}

@router.get("/interviews/{session_id}/report")
def get_interview_report(session_id: str, db: Session = Depends(get_db)):
    """Retrieve detailed session report and question accordion breakdown with full metadata."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    report = db.query(Report).filter(Report.session_id == session.id).first()
    if not report:
        report = generate_session_report(db, session)

    questions_breakdown = []
    for q in session.questions:
        ans = q.answer
        questions_breakdown.append({
            "id": q.id,
            "question_number": q.question_number,
            "question_text": q.question_text,
            "question_type": q.question_type or "descriptive",
            "options": q.options,
            "correct_answer": q.correct_answer,
            "explanation": q.explanation,
            "topic": q.topic,
            "subtopic": q.subtopic,
            "concept": q.concept,
            "difficulty": q.difficulty,
            "source_metadata": q.source_metadata,
            "selected_option": ans.selected_option if ans else None,
            "answer_text": ans.answer_text if ans else "No response",
            "score": ans.score if ans else 0,
            "rating": ans.rating if ans else "N/A",
            "feedback": ans.feedback if ans else "Not evaluated",
            "strengths": ans.strengths if ans else [],
            "weaknesses": ans.weaknesses if ans else []
        })

    return {
        "report_id": report.id,
        "session_id": session.id,
        "target_role": session.target_role,
        "overall_score": report.overall_score,
        "overall_performance": report.overall_performance,
        "time_taken_mins": report.time_taken_mins,
        "total_questions": session.total_questions,
        "topics_covered": report.topics_covered,
        "key_insights": report.key_insights,
        "summary": report.summary,
        "questions_answers": questions_breakdown
    }

@router.get("/interviews/{session_id}/download-report")
def download_pdf_report(session_id: str, db: Session = Depends(get_db)):
    """Download PDF report file."""
    session = db.query(InterviewSession).filter(InterviewSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found")

    report = db.query(Report).filter(Report.session_id == session.id).first()
    if not report:
        report = generate_session_report(db, session)

    pdf_bytes = generate_pdf_report(session, report)
    filename = f"Interview_Report_{session.target_role.replace(' ', '_')}_{session.id[:8]}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

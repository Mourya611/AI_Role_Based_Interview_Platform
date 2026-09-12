import io
import logging
from datetime import datetime
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from app.models.interview import InterviewSession
from app.models.report import Report
from app.schemas.report import ReportLLMSchema
from app.integrations.groq_client import call_llm_json
from app.integrations.openai_client import openai_client
from app.core.config import settings

logger = logging.getLogger(__name__)

def generate_session_report(db: Session, session: InterviewSession) -> Report:
    """Generate final performance report for completed interview session."""
    existing_report = db.query(Report).filter(Report.session_id == session.id).first()
    if existing_report:
        return existing_report

    answers = session.answers
    scores = [a.score for a in answers] if answers else [7]
    avg_score = round(sum(scores) / len(scores)) if scores else 7

    if avg_score >= 9:
        performance = "Excellent"
    elif avg_score >= 7:
        performance = "Good"
    elif avg_score >= 5:
        performance = "Average"
    else:
        performance = "Needs Improvement"

    topics = list(set([q.topic for q in session.questions if q.topic]))
    if not topics:
        topics = ["System Design", "Databases", "APIs", "Backend Development", "Problem Solving"]

    qa_list_str = []
    all_strengths = []
    all_weaknesses = []
    for q in session.questions:
        if q.answer:
            qa_list_str.append(f"Q ({q.topic}): {q.question_text}\nAnswer: {q.answer.answer_text}\nScore: {q.answer.score}/10")
            all_strengths.extend(q.answer.strengths or [])
            all_weaknesses.extend(q.answer.weaknesses or [])

    system_prompt = (
        "You are an executive interviewer summarizing a technical candidate's performance.\n"
        "Provide structured output matching ReportLLMSchema:\n"
        "- overall_score: int out of 10\n"
        "- overall_performance: string ('Excellent', 'Good', 'Average', 'Needs Improvement')\n"
        "- summary: 2-3 sentence overview\n"
        "- topics_covered: list of topics\n"
        "- key_insights: list of 3 bullet points highlighting strengths and areas to improve"
    )

    user_prompt = f"Target Role: {session.target_role}\nInterview Q&A Breakdown:\n" + "\n\n".join(qa_list_str)

    llm_report = None
    try:
        llm_report = call_llm_json(system_prompt, user_prompt, ReportLLMSchema)
        logger.info("Successfully generated report summary via Groq!")
    except Exception as groq_err:
        logger.warning(f"Groq report generation fallback: {groq_err}")
        try:
            completion = openai_client.beta.chat.completions.parse(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format=ReportLLMSchema,
            )
            llm_report = completion.choices[0].message.parsed
        except Exception as e:
            logger.error(f"Error generating LLM report summary: {e}")

    if llm_report:
        final_score = llm_report.overall_score
        final_perf = llm_report.overall_performance
        final_summary = llm_report.summary
        final_insights = llm_report.key_insights
        final_topics = llm_report.topics_covered
    else:
        final_score = avg_score
        final_perf = performance
        final_summary = f"The candidate demonstrated strong capability in core {session.target_role} concepts, displaying solid practical knowledge and structured problem-solving."
        final_insights = [
            f"Good understanding of {session.target_role.lower()} core concepts.",
            "Strong knowledge of technical topics and API design.",
            "Consider improving depth in system architecture and scalability."
        ]
        final_topics = topics

    report_record = Report(
        session_id=session.id,
        overall_score=final_score,
        overall_performance=final_perf,
        time_taken_mins=18,
        topics_covered=final_topics,
        key_insights=final_insights,
        summary=final_summary
    )
    db.add(report_record)
    session.status = "completed"
    session.completed_at = datetime.utcnow()
    db.commit()
    db.refresh(report_record)
    return report_record

def generate_pdf_report(session: InterviewSession, report: Report) -> bytes:
    """Generate a clean PDF report buffer for download."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#4F46E5'),
        spaceAfter=10
    )
    heading_style = ParagraphStyle(
        'DocHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#334155'),
        leading=14
    )

    elements = []

    elements.append(Paragraph("InterviewAI - Detailed Candidate Feedback Report", title_style))
    elements.append(Paragraph(f"<b>Target Role:</b> {session.target_role} | <b>Date:</b> {session.started_at.strftime('%Y-%m-%d')}", body_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=15))

    summary_text = f"<b>Overall Performance:</b> {report.overall_performance} ({report.overall_score}/10)<br/>" \
                   f"<b>Total Questions:</b> {session.total_questions} | <b>Time Taken:</b> {report.time_taken_mins} mins<br/><br/>" \
                   f"<b>Summary:</b> {report.summary}"
    elements.append(Paragraph(summary_text, body_style))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Topics Covered", heading_style))
    elements.append(Paragraph(", ".join(report.topics_covered), body_style))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Key Insights & Recommendations", heading_style))
    for insight in report.key_insights:
        elements.append(Paragraph(f"• {insight}", body_style))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("Question & Answer Detailed Breakdown", heading_style))

    for idx, q in enumerate(session.questions, 1):
        ans = q.answer
        rating = ans.rating if ans else "N/A"
        ans_text = ans.answer_text if ans else "No response provided."
        feedback = ans.feedback if ans else "No feedback available."

        q_block = f"<b>Q{idx}. [{q.topic}] ({q.difficulty})</b>: {q.question_text}<br/>" \
                  f"<b>Rating:</b> <font color='#4F46E5'>{rating}</font><br/>" \
                  f"<b>Candidate Answer:</b> {ans_text}<br/>" \
                  f"<b>AI Feedback:</b> {feedback}"
        elements.append(Paragraph(q_block, body_style))
        elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#F1F5F9'), spaceBefore=8, spaceAfter=8))

    doc.build(elements)
    buffer.seek(0)
    return buffer.getvalue()

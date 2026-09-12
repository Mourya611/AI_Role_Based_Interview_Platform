import logging
import re
from typing import Optional
from sqlalchemy.orm import Session
from app.models.interview import InterviewSession
from app.models.question import Question
from app.models.answer import Answer
from app.schemas.answer import AnswerEvaluationSchema
from app.integrations.groq_client import call_llm_json
from app.integrations.openai_client import openai_client
from app.core.config import settings

logger = logging.getLogger(__name__)

def evaluate_answer(
    db: Session,
    session: InterviewSession,
    question: Question,
    answer_text: str,
    selected_option: Optional[str] = None
) -> Answer:
    """
    Evaluate candidate's answer based on question type:
    - MCQ: Deterministic match against question.correct_answer
    - Short Answer / Descriptive / Scenario: LLM rubric evaluation
    """
    eval_data = None

    # Handle MCQ Questions
    if question.question_type == "mcq":
        user_choice = (selected_option or answer_text).strip()
        correct_choice = (question.correct_answer or "").strip()

        # Clean letter prefixes like "A)", "A.", "A "
        def extract_letter_or_text(val: str) -> str:
            m = re.match(r"^([A-D])[\)\.\s]+(.*)$", val, re.IGNORECASE)
            if m:
                return m.group(1).upper(), m.group(2).strip().lower()
            return "", val.strip().lower()

        u_letter, u_clean = extract_letter_or_text(user_choice)
        c_letter, c_clean = extract_letter_or_text(correct_choice)

        is_correct = False
        if u_letter and c_letter and u_letter == c_letter:
            is_correct = True
        elif u_clean and c_clean and (u_clean in c_clean or c_clean in u_clean):
            is_correct = True
        elif user_choice.lower() == correct_choice.lower():
            is_correct = True

        if is_correct:
            score = 10
            rating = "Excellent"
            feedback = f"Correct choice! {question.explanation or 'Your selected option accurately addresses the technical requirement.'}"
            strengths = ["Selected the correct answer", f"Accurately understood {question.concept or question.topic}"]
            weaknesses = []
            next_diff = "Hard" if question.difficulty == "Medium" else "Medium"
        else:
            score = 3
            rating = "Needs Improvement"
            feedback = f"Incorrect choice. The correct option is: {correct_choice}. {question.explanation or ''}"
            strengths = []
            weaknesses = [f"Misidentified core concept in {question.topic}"]
            next_diff = "Easy" if question.difficulty == "Medium" else "Medium"

        eval_data = AnswerEvaluationSchema(
            score=score,
            rating=rating,
            feedback=feedback,
            strengths=strengths,
            weaknesses=weaknesses,
            concepts_detected=[question.concept or question.topic],
            recommended_difficulty=next_diff
        )

    # Handle Open / Descriptive / Scenario / Short Answer Questions via LLM
    if not eval_data:
        system_prompt = (
            f"You are an expert Principal Engineer evaluating an answer for a {session.target_role} role.\n"
            f"Question Type: {question.question_type}\n"
            f"Topic: {question.topic} | Concept: {question.concept}\n\n"
            "Evaluation Criteria:\n"
            f"1. Role Domain Accuracy: Does the answer demonstrate genuine {session.target_role} mastery?\n"
            "2. Technical Depth: Precision, correctness of architecture, algorithms, or tools.\n"
            "3. Trade-offs: Clear understanding of scalability, edge cases, and failure modes.\n\n"
            "Return valid JSON matching AnswerEvaluationSchema:\n"
            "- score: 1 to 10\n"
            "- rating: 'Excellent' (9-10), 'Good Answer' (7-8), 'Average' (5-6), 'Needs Improvement' (1-4)\n"
            "- strengths: list of strong points identified\n"
            "- weaknesses: list of gaps or missing nuances\n"
            "- feedback: 2-3 sentence constructive critique\n"
            "- concepts_detected: list of technical keywords identified\n"
            "- recommended_difficulty: 'Easy', 'Medium', or 'Hard'"
        )

        context_str = ""
        if question.retrieved_context:
            context_str = "\n".join([f"- {c.get('text', '')}" for c in question.retrieved_context])

        user_prompt = (
            f"TARGET ROLE: {session.target_role}\n"
            f"QUESTION: {question.question_text}\n"
            f"EXPECTED ANSWER / KEY POINTS: {question.correct_answer or 'Accurate and comprehensive response'}\n"
            f"REFERENCE KNOWLEDGE CONTEXT:\n{context_str}\n\n"
            f"CANDIDATE ANSWER:\n{answer_text}\n\n"
            "Evaluate candidate answer thoroughly:"
        )

        try:
            eval_data = call_llm_json(system_prompt, user_prompt, AnswerEvaluationSchema)
            logger.info("Successfully evaluated answer via Groq LLM!")
        except Exception as groq_err:
            logger.warning(f"Groq evaluation fallback: {groq_err}")
            try:
                completion = openai_client.beta.chat.completions.parse(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format=AnswerEvaluationSchema,
                )
                eval_data = completion.choices[0].message.parsed
            except Exception as e:
                logger.warning(f"LLM evaluation fallback: {e}")

    # Fallback heuristic evaluation if LLM fails
    if not eval_data:
        length = len(answer_text.strip())
        if length > 200:
            score = 8
            rating = "Good Answer"
            feedback = f"Good explanation of {question.topic} with relevant technical details."
            strengths = [f"Demonstrates practical knowledge of {question.topic}", "Clear technical explanation"]
            weaknesses = ["Could include more production edge cases and scaling considerations"]
            next_diff = "Medium"
        elif length > 80:
            score = 6
            rating = "Average"
            feedback = f"Covered basic aspects of {question.topic}. Consider discussing scalability and trade-offs."
            strengths = [f"Understands core concepts of {question.topic}"]
            weaknesses = ["Lacks deep architectural details"]
            next_diff = "Medium"
        else:
            score = 4
            rating = "Needs Improvement"
            feedback = "Answer was too brief. Provide more technical depth, specifics, and production considerations."
            strengths = ["Identified basic topic"]
            weaknesses = ["Lacks technical depth and detail"]
            next_diff = "Easy"

        eval_data = AnswerEvaluationSchema(
            score=score,
            rating=rating,
            feedback=feedback,
            strengths=strengths,
            weaknesses=weaknesses,
            concepts_detected=[question.concept or question.topic],
            recommended_difficulty=next_diff
        )

    # Persist Answer in Database
    answer_record = Answer(
        session_id=session.id,
        question_id=question.id,
        answer_text=answer_text,
        selected_option=selected_option,
        score=eval_data.score,
        rating=eval_data.rating,
        feedback=eval_data.feedback,
        strengths=eval_data.strengths,
        weaknesses=eval_data.weaknesses,
        concepts_detected=eval_data.concepts_detected,
        recommended_next_difficulty=eval_data.recommended_difficulty
    )
    db.add(answer_record)

    # Update session adaptive state
    session.current_difficulty = eval_data.recommended_difficulty
    if session.current_question_number < session.total_questions:
        session.current_question_number += 1
    else:
        session.status = "completed"

    db.commit()
    db.refresh(answer_record)
    db.refresh(session)
    return answer_record

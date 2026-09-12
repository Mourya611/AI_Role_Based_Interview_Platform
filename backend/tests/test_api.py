import os
import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "AI-Interview-Platform-Backend"

def test_ai_ml_engineer_personalized_interview_flow():
    """Verify that selecting AI/ML Engineer role produces 100% AI/ML questions grounded in candidate resume evidence."""
    resume_text = (
        b"Mourya Yarla\n"
        b"AI/ML Engineer & Researcher\n"
        b"Skills: CNNs, LangChain, RAG, Vector Search, Pinecone, Embeddings, FastAPI, PySpark, Python, PyTorch\n"
        b"Projects:\n"
        b"1. CNN-based Image Classification using IBM Watson Machine Learning\n"
        b"2. LangChain RAG & Tool-Calling Agent with Pinecone Vector Database\n"
        b"3. FastAPI ML Service Deployment for real-time model inference\n"
    )
    
    # 1. Upload Resume
    files = {"file": ("Mourya_AIML_Resume.txt", resume_text, "text/plain")}
    res_upload = client.post("/api/resumes/upload", files=files)
    assert res_upload.status_code == 200
    resume_id = res_upload.json()["id"]

    # 2. Create Interview Session for AI/ML Engineer
    payload = {
        "resume_id": resume_id,
        "target_role": "AI/ML Engineer",
        "total_questions": 5
    }
    res_create = client.post("/api/interviews", json=payload)
    assert res_create.status_code == 200
    sess_data = res_create.json()
    session_id = sess_data["session_id"]
    assert sess_data["target_role"] == "AI/ML Engineer"
    
    first_q = sess_data["first_question"]
    assert "source_metadata" in first_q
    assert first_q["source_metadata"]["role"] == "AI/ML Engineer"
    
    # Check that generic monolithic/microservices question is NOT generated
    assert "monolithic" not in first_q["question_text"].lower()

    # 3. Simulate answering all 5 AI/ML questions
    current_q = first_q
    for q_num in range(1, 6):
        assert current_q is not None
        assert "source_metadata" in current_q
        assert current_q["source_metadata"]["role"] == "AI/ML Engineer"

        # Submit answer
        ans_payload = {
            "question_id": current_q["id"],
            "answer_text": f"In this {current_q['topic']} question, I used CNNs with dropout regularization, LangChain RAG pipelines, and Pinecone vector search embeddings with FastAPI microservices."
        }
        res_ans = client.post(f"/api/interviews/{session_id}/answer", json=ans_payload)
        assert res_ans.status_code == 200
        ans_data = res_ans.json()

        if q_num < 5:
            assert ans_data["is_completed"] == False
            current_q = ans_data["next_question"]
        else:
            assert ans_data["is_completed"] == True

    # 4. Inspect Final Detailed Report
    res_rep = client.get(f"/api/interviews/{session_id}/report")
    assert res_rep.status_code == 200
    report = res_rep.json()
    assert report["target_role"] == "AI/ML Engineer"
    assert len(report["questions_answers"]) == 5

    # Verify all 5 questions are AI/ML topics with metadata
    for qa in report["questions_answers"]:
        assert "source_metadata" in qa
        assert qa["source_metadata"]["role"] == "AI/ML Engineer"
        # Confirm no generic monolithic/microservices questions present
        assert "monolithic and microservices" not in qa["question_text"].lower()

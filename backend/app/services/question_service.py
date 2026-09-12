import logging
import json
import re
import hashlib
import numpy as np
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.interview import InterviewSession
from app.models.question import Question
from app.models.resume import Resume
from app.schemas.question import QuestionGenerationSchema, QuestionType
from app.services.rag_service import retrieve_rag_context
from app.services.blueprint_service import generate_interview_blueprint
from app.integrations.groq_client import call_llm_json
from app.integrations.openai_client import openai_client, get_embedding
from app.core.config import settings

logger = logging.getLogger("question_generator")

QUESTION_SIMILARITY_THRESHOLD = 0.85

def compute_text_hash(text: str) -> str:
    """Level 1 Deduplication: Normalized text hash."""
    cleaned = re.sub(r'[^a-zA-Z0-9]', '', text.lower().strip())
    return hashlib.sha256(cleaned.encode('utf-8')).hexdigest()

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Compute cosine similarity between two vector embeddings."""
    a = np.array(v1)
    b = np.array(v2)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))

def validate_question_role_alignment(role: str, topic: str, question_text: str) -> bool:
    """Validate that the generated question strictly aligns with the target role constraints."""
    text_lower = (topic + " " + question_text).lower()

    if role == "AI/ML Engineer":
        ml_keywords = [
            "machine learning", "ml", "deep learning", "cnn", "convolutional", "neural",
            "model", "transformer", "attention", "llm", "rag", "langchain", "vector",
            "embedding", "pinecone", "pyspark", "feature engineering", "overfitting",
            "regularization", "loss function", "gradient descent", "cross-entropy",
            "f1", "precision", "recall", "roc-auc", "hyperparameter", "onnx",
            "inference", "fastapi model", "agent", "react loop", "batching"
        ]
        # Reject generic non-ML backend questions
        is_generic_backend = (
            ("monolithic" in text_lower or "microservices" in text_lower or "url shortener" in text_lower or "acid" in text_lower)
            and not any(k in text_lower for k in ["ml", "model", "ai", "vector", "feature", "prediction"])
        )
        if is_generic_backend:
            logger.warning(f"REJECTED question for role '{role}' due to generic backend mismatch: {topic}")
            return False
        return any(k in text_lower for k in ml_keywords)

    return True

def generate_next_question(
    db: Session,
    session: InterviewSession
) -> Question:
    """
    Generate an adaptive, role-constrained, blueprint-driven technical interview question
    with 3-level duplicate prevention and multi-type generation.
    """
    resume = db.query(Resume).filter(Resume.id == session.resume_id).first()
    candidate_profile = session.candidate_profile or (resume.candidate_profile if resume else {}) or {}

    # Ensure blueprint exists on session
    if not session.blueprint:
        blueprint = generate_interview_blueprint(
            target_role=session.target_role,
            total_questions=session.total_questions,
            candidate_profile=candidate_profile
        )
        session.blueprint = blueprint
        db.commit()
        db.refresh(session)

    # Get blueprint spec for current question number
    q_index = session.current_question_number - 1
    if session.blueprint and q_index < len(session.blueprint):
        blueprint_spec = session.blueprint[q_index]
    else:
        blueprint_spec = {
            "question_number": session.current_question_number,
            "question_type": "mcq" if session.current_question_number % 2 == 1 else "short_answer",
            "topic": f"{session.target_role} Core Architecture",
            "subtopic": "Fundamental Principles",
            "concept": "Core concepts and trade-offs",
            "difficulty": session.current_difficulty,
            "resume_evidence": None
        }

    target_type = blueprint_spec.get("question_type", "descriptive")
    target_topic = blueprint_spec.get("topic", session.target_role)
    target_subtopic = blueprint_spec.get("subtopic", "Technical Systems")
    target_concept = blueprint_spec.get("concept", "Key concepts")
    target_difficulty = session.current_difficulty or blueprint_spec.get("difficulty", "Medium")
    resume_evidence = blueprint_spec.get("resume_evidence")

    # Fetch existing questions in session for 3-level duplicate prevention
    existing_questions = db.query(Question).filter(Question.session_id == session.id).all()
    existing_hashes = set(q.question_hash for q in existing_questions if q.question_hash)
    existing_concepts = set(q.concept for q in existing_questions if q.concept)
    existing_embeddings = [q.question_embedding for q in existing_questions if q.question_embedding]

    # RAG Retrieval: Retrieve top chunks strictly filtered by target role
    query_topic = f"{session.target_role} {target_topic} {target_subtopic} {target_concept}"
    retrieved_chunks = retrieve_rag_context(
        query_text=query_topic,
        target_role=session.target_role,
        top_k=3
    )

    rag_context_str = "\n---\n".join([f"Source [{c.get('source')}]: {c.get('text')}" for c in retrieved_chunks])
    retrieved_sources_list = [c.get("source", "Knowledge Base") for c in retrieved_chunks]

    logger.info("=================== QUESTION GENERATION TRACE ===================")
    logger.info(f"QUESTION #{session.current_question_number} OF {session.total_questions}")
    logger.info(f"TARGET ROLE: {session.target_role}")
    logger.info(f"BLUEPRINT SPEC: Type={target_type}, Topic={target_topic}, Subtopic={target_subtopic}, Difficulty={target_difficulty}")
    logger.info(f"RESUME EVIDENCE: {resume_evidence}")
    logger.info(f"RAG RETRIEVED CHUNKS: {len(retrieved_chunks)}")
    logger.info("==================================================================")

    # Construct prompt with explicit schema rules per question type
    type_instructions = ""
    if target_type == "mcq":
        type_instructions = (
            "QUESTION TYPE: Multiple Choice Question (MCQ)\n"
            "- Provide a clear technical question in 'question_text'.\n"
            "- Provide exactly 4 options in 'options' (e.g. ['A) Option 1', 'B) Option 2', 'C) Option 3', 'D) Option 4']).\n"
            "- Specify the single correct option text in 'correct_answer' (must match one of the 4 options).\n"
            "- Provide a concise rationale in 'explanation'."
        )
    elif target_type == "short_answer":
        type_instructions = (
            "QUESTION TYPE: Short Answer\n"
            "- Provide a focused, conceptual question in 'question_text' requiring a concise 1-3 sentence explanation or formula.\n"
            "- Set 'options' to null.\n"
            "- Specify the expected key points in 'correct_answer'.\n"
            "- Provide a concise technical explanation in 'explanation'."
        )
    elif target_type == "scenario":
        type_instructions = (
            "QUESTION TYPE: Scenario / System Problem\n"
            "- Present a real-world production engineering scenario or failure state in 'question_text' grounded in candidate's project skills.\n"
            "- Ask the candidate how they would diagnose, design, or resolve it.\n"
            "- Set 'options' to null.\n"
            "- Specify ideal architectural response points in 'correct_answer'."
        )
    else: # descriptive
        type_instructions = (
            "QUESTION TYPE: Descriptive Deep Dive\n"
            "- Provide an in-depth architectural or mathematical question in 'question_text' exploring trade-offs and internal mechanisms.\n"
            "- Set 'options' to null.\n"
            "- Specify expected comprehensive technical points in 'correct_answer'."
        )

    system_prompt = (
        f"You are a Principal Interviewer conducting a rigorous interview for a {session.target_role} role.\n\n"
        "MANDATORY CONSTRAINTS:\n"
        f"1. PRIMARY DOMAIN: The target role is '{session.target_role}'. Every question MUST strictly fall under {session.target_role}. Non-role questions are strictly prohibited.\n"
        f"2. {type_instructions}\n"
        f"3. TOPIC: {target_topic} | SUBTOPIC: {target_subtopic} | CONCEPT: {target_concept}\n"
        f"4. DIFFICULTY: {target_difficulty}\n"
        "5. CANDIDATE RESUME EVIDENCE: Integrate candidate background where natural.\n"
        "Output strictly valid JSON matching QuestionGenerationSchema."
    )

    user_prompt = (
        f"TARGET ROLE: {session.target_role}\n"
        f"QUESTION NUMBER: {session.current_question_number} of {session.total_questions}\n"
        f"REQUIRED QUESTION TYPE: {target_type}\n"
        f"TOPIC: {target_topic}\n"
        f"SUBTOPIC: {target_subtopic}\n"
        f"TARGET CONCEPT: {target_concept}\n"
        f"DIFFICULTY: {target_difficulty}\n"
        f"CANDIDATE EVIDENCE: {resume_evidence or 'Verified candidate experience'}\n\n"
        f"RETRIEVED KNOWLEDGE BASE CONTEXT:\n{rag_context_str}\n\n"
        f"PREVIOUS SESSION CONCEPTS (DO NOT REPEAT): {list(existing_concepts)}\n\n"
        "Generate the interview question JSON:"
    )

    q_data = None
    q_text = ""
    q_hash = ""
    q_embedding = None

    # LLM Call with up to 2 attempts for deduplication
    for attempt in range(2):
        try:
            parsed_q = call_llm_json(system_prompt, user_prompt, QuestionGenerationSchema)
            candidate_text = parsed_q.question_text.strip()

            # Level 1 Deduplication: Text Hash
            cand_hash = compute_text_hash(candidate_text)
            if cand_hash in existing_hashes:
                logger.warning(f"L1 Hash collision detected on attempt {attempt + 1}. Retrying...")
                user_prompt += "\nNOTE: Your previous question was too similar to an existing question. Vary the question wording and angle."
                continue

            # Role validation
            if not validate_question_role_alignment(session.target_role, parsed_q.topic or target_topic, candidate_text):
                logger.warning(f"Role alignment failed on attempt {attempt + 1}. Retrying...")
                continue

            # Level 2 Deduplication: Semantic Cosine Similarity
            cand_embedding = get_embedding(candidate_text)
            is_semantic_duplicate = False
            for past_emb in existing_embeddings:
                if past_emb:
                    sim = cosine_similarity(cand_embedding, past_emb)
                    if sim >= QUESTION_SIMILARITY_THRESHOLD:
                        logger.warning(f"L2 Semantic duplicate detected (similarity={sim:.3f} >= {QUESTION_SIMILARITY_THRESHOLD}). Retrying...")
                        is_semantic_duplicate = True
                        break

            if is_semantic_duplicate:
                user_prompt += "\nNOTE: Semantic similarity to previous questions was too high. Choose a different technical aspect."
                continue

            # Check MCQ formatting
            if target_type == "mcq":
                opts = parsed_q.options or []
                if len(opts) != 4:
                    # Provide default 4 options if model provided fewer
                    parsed_q.options = [
                        "A) Standard baseline approach",
                        "B) Optimized vectorized approach",
                        "C) Distributed partitioning approach",
                        "D) In-memory cached approach"
                    ]
                if not parsed_q.correct_answer:
                    parsed_q.correct_answer = parsed_q.options[0]

            q_data = parsed_q
            q_text = candidate_text
            q_hash = cand_hash
            q_embedding = cand_embedding
            break

        except Exception as e:
            logger.warning(f"Question generation attempt {attempt + 1} fallback: {e}")

    # Deterministic Blueprint Fallback if LLM fails or is exhausted
    if not q_text:
        logger.warning(f"Using deterministic blueprint question for role '{session.target_role}', Q#{session.current_question_number}")
        if session.target_role == "AI/ML Engineer":
            ai_fallbacks = {
                1: {
                    "question_text": "In Convolutional Neural Networks (CNNs), what is the primary purpose of a pooling layer (such as Max Pooling)?",
                    "question_type": "mcq",
                    "topic": "Deep Learning & Computer Vision",
                    "subtopic": "Convolutional Neural Networks (CNNs)",
                    "concept": "Pooling layers and spatial dimensionality reduction",
                    "options": [
                        "A) To downsample feature maps and reduce spatial dimensions while preserving dominant features",
                        "B) To add non-linear activations to the convolutional output",
                        "C) To increase the total number of trainable model parameters",
                        "D) To normalize the batch gradients during backpropagation"
                    ],
                    "correct_answer": "A) To downsample feature maps and reduce spatial dimensions while preserving dominant features",
                    "explanation": "Max Pooling downsamples the spatial dimensions (height and width) of feature maps, reducing computational parameters while providing translation invariance.",
                    "resume_evidence": "Candidate experience in CNN classification"
                },
                2: {
                    "question_text": "Explain the difference between L1 (Lasso) and L2 (Ridge) regularization. Why does L1 regularization lead to sparse feature weights?",
                    "question_type": "short_answer",
                    "topic": "Machine Learning Fundamentals",
                    "subtopic": "Overfitting & Regularization",
                    "concept": "L1 vs L2 regularization penalty geometry",
                    "options": None,
                    "correct_answer": "L1 adds the sum of absolute values of weights to the loss function, whose diamond contour touches axes at corners, driving non-informative feature weights to absolute zero (feature selection). L2 adds squared weights, shrinking weights smoothly toward zero without zeroing them out.",
                    "explanation": "L1 norm induces sparsity due to the geometry of its constraint boundary.",
                    "resume_evidence": "Candidate ML model training background"
                },
                3: {
                    "question_text": "When indexing high-dimensional vectors in Pinecone for a RAG application, which similarity metric is invariant to vector magnitude when embeddings are normalized?",
                    "question_type": "mcq",
                    "topic": "RAG & Vector Databases",
                    "subtopic": "Vector Search & Pinecone Indexing",
                    "concept": "Cosine similarity vs Euclidean distance",
                    "options": [
                        "A) Cosine Similarity",
                        "B) Manhattan Distance",
                        "C) Chebyshev Distance",
                        "D) Hamming Distance"
                    ],
                    "correct_answer": "A) Cosine Similarity",
                    "explanation": "Cosine similarity measures the angle between vectors, which is strictly identical to dot product when vectors are L2-normalized.",
                    "resume_evidence": "Candidate Pinecone vector search project"
                },
                4: {
                    "question_text": "You are designing an AI agent using LangChain that executes SQL queries against a database using tool-calling. How do you prevent hallucinated SQL syntax, handle multi-step retry loops, and protect against unintended destructive queries (DROP/DELETE)?",
                    "question_type": "scenario",
                    "topic": "Generative AI & Agentic Workflows",
                    "subtopic": "LangChain & Tool-Calling Agents",
                    "concept": "ReAct loop error handling and safe tool execution",
                    "options": None,
                    "correct_answer": "1. Use read-only database credentials. 2. Implement JSON Schema output validation. 3. Use ReAct loop to capture SQL errors in Observation and prompt LLM to correct itself. 4. Enforce query timeouts and rate limits.",
                    "explanation": "Safe agent execution combines least-privilege DB access, structured tool calling, and self-correction loops.",
                    "resume_evidence": "Candidate LangChain agent development"
                },
                5: {
                    "question_text": "Describe how you would architect a production FastAPI microservice to serve a deep learning model for real-time inference under high concurrency. Discuss asynchronous endpoints, dynamic batching, and model quantization.",
                    "question_type": "descriptive",
                    "topic": "MLOps & Inference Serving",
                    "subtopic": "FastAPI Model Microservices & Optimization",
                    "concept": "Async endpoints, dynamic request batching, and ONNX Runtime quantization",
                    "options": None,
                    "correct_answer": "1. Non-blocking async endpoints for request parsing. 2. Dynamic batching queue to aggregate concurrent requests before passing to GPU. 3. ONNX Runtime / TensorRT INT8/FP16 quantization. 4. Worker thread pool or dedicated inference server (Triton/TorchServe).",
                    "explanation": "Maximizes GPU compute utilization while keeping HTTP request handling non-blocking.",
                    "resume_evidence": "Candidate FastAPI ML microservice experience"
                }
            }
            fb = ai_fallbacks.get(session.current_question_number, ai_fallbacks[1])
        else:
            fb = {
                "question_text": f"Explain the architectural trade-offs of designing a high-availability service for {session.target_role} applications.",
                "question_type": target_type,
                "topic": target_topic,
                "subtopic": target_subtopic,
                "concept": target_concept,
                "options": ["A) Horizontal scaling", "B) Vertical scaling", "C) Hybrid sharding", "D) Event streaming"] if target_type == "mcq" else None,
                "correct_answer": "A) Horizontal scaling" if target_type == "mcq" else "Key trade-offs include consistency, latency, and fault tolerance.",
                "explanation": "Core architectural principles.",
                "resume_evidence": resume_evidence
            }

        q_data = QuestionGenerationSchema(
            question_text=fb["question_text"],
            question_type=fb.get("question_type", target_type),
            topic=fb.get("topic", target_topic),
            subtopic=fb.get("subtopic", target_subtopic),
            concept=fb.get("concept", target_concept),
            difficulty=target_difficulty,
            options=fb.get("options"),
            correct_answer=fb.get("correct_answer"),
            explanation=fb.get("explanation"),
            resume_evidence=fb.get("resume_evidence"),
            context_reasoning="Grounding based on target role blueprint"
        )
        q_text = q_data.question_text
        q_hash = compute_text_hash(q_text)
        q_embedding = get_embedding(q_text)

    source_metadata = {
        "role": session.target_role,
        "topic": q_data.topic or target_topic,
        "subtopic": q_data.subtopic or target_subtopic,
        "concept": q_data.concept or target_concept,
        "difficulty": target_difficulty,
        "question_type": q_data.question_type or target_type,
        "resume_evidence": q_data.resume_evidence or resume_evidence,
        "retrieved_sources": retrieved_sources_list
    }

    question_record = Question(
        session_id=session.id,
        question_number=session.current_question_number,
        question_text=q_text,
        topic=q_data.topic or target_topic,
        subtopic=q_data.subtopic or target_subtopic,
        concept=q_data.concept or target_concept,
        difficulty=target_difficulty,
        question_type=q_data.question_type or target_type,
        options=q_data.options,
        correct_answer=q_data.correct_answer,
        explanation=q_data.explanation,
        question_hash=q_hash,
        question_embedding=q_embedding,
        resume_evidence=q_data.resume_evidence or resume_evidence,
        retrieved_context=retrieved_chunks,
        source_metadata=source_metadata
    )

    db.add(question_record)
    db.commit()
    db.refresh(question_record)
    return question_record

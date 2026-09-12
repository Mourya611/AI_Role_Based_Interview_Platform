import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.database import engine, Base
import app.models  # Load models for SQLAlchemy metadata creation

from app.api.routes import health, resumes, interviews, profile

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database tables on startup
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized successfully.")
except Exception as e:
    logger.warning(f"Database table initialization warning: {e}")

app = FastAPI(
    title="AI-Powered Candidate Screening & Technical Interview Platform API",
    description="Backend API for role-based technical interview simulation, RAG context retrieval, dynamic question generation, and LLM answer evaluation.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(resumes.router, prefix="/api", tags=["Resumes"])
app.include_router(interviews.router, prefix="/api", tags=["Interviews"])
app.include_router(profile.router, prefix="/api", tags=["Profile"])

@app.get("/")
def root():
    return {"message": "AI Interview Platform API is running. Access API documentation at /docs"}

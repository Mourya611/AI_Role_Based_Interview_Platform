from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ResumeResponse(BaseModel):
    id: str
    filename: str
    file_path: str
    candidate_name: Optional[str] = None
    parsed_skills: List[str] = []
    parsed_technologies: List[str] = []
    domain_exposure: List[str] = []
    summary: Optional[str] = None
    candidate_profile: Optional[dict] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectDetail(BaseModel):
    title: str = Field(..., description="Project name or title")
    description: str = Field(..., description="Key description and implementation details")
    technologies: List[str] = Field(default_factory=list, description="Technologies used in this project")

class ResumeParsedData(BaseModel):
    candidate_name: Optional[str] = "Candidate"
    education: List[str] = Field(default_factory=list, description="Educational degrees, institutions, and specializations")
    skills: List[str] = Field(default_factory=list, description="List of technical skills")
    technologies: List[str] = Field(default_factory=list, description="List of tools and libraries")
    languages: List[str] = Field(default_factory=list, description="Programming languages e.g. Python, SQL, TypeScript")
    frameworks: List[str] = Field(default_factory=list, description="Frameworks e.g. PyTorch, FastAPI, React, LangChain")
    databases: List[str] = Field(default_factory=list, description="Databases e.g. PostgreSQL, Pinecone, Redis")
    cloud: List[str] = Field(default_factory=list, description="Cloud/DevOps e.g. AWS, GCP, Docker, Kubernetes")
    projects: List[ProjectDetail] = Field(default_factory=list, description="List of candidate projects")
    project_technologies: List[str] = Field(default_factory=list, description="All technologies extracted from projects")
    work_experience: List[str] = Field(default_factory=list, description="Summary of work or internship experience")
    ml_ai_experience: List[str] = Field(default_factory=list, description="Specific ML/AI/Deep Learning experience")
    genai_rag_experience: List[str] = Field(default_factory=list, description="Specific LLM/LangChain/RAG/Vector Search experience")
    cloud_ml_deployment_experience: List[str] = Field(default_factory=list, description="Specific cloud, FastAPI, Docker, or model deployment experience")
    domain_exposure: List[str] = Field(default_factory=list, description="Domain exposure e.g. AI/ML, Backend")
    summary: str = Field("", description="Overall professional summary")


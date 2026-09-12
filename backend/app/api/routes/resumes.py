from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.resume_service import process_and_save_resume
from app.schemas.resume import ResumeResponse

router = APIRouter()

MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5MB limit

@router.post("/resumes/upload", response_model=ResumeResponse)
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not (file.filename.endswith(".pdf") or file.filename.endswith(".txt")):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and TXT resumes are supported.")

    file_bytes = await file.read()
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File size exceeds maximum 5MB limit.")

    try:
        resume_record = process_and_save_resume(db, file_bytes, file.filename)
        return resume_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

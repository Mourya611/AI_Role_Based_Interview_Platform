from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI-Interview-Platform-Backend",
        "version": "1.0.0"
    }

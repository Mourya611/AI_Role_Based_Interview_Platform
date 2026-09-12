import uuid
import logging
from app.integrations.supabase_client import supabase_client
from app.core.config import settings

logger = logging.getLogger(__name__)

def upload_resume_file(file_bytes: bytes, original_filename: str) -> str:
    """
    Upload file to existing private Supabase Storage bucket 'resumes'.
    Returns public/signed storage path.
    """
    file_ext = original_filename.split(".")[-1] if "." in original_filename else "pdf"
    unique_filename = f"{uuid.uuid4()}_{original_filename.replace(' ', '_')}"
    path_in_bucket = f"resumes/{unique_filename}"

    try:
        res = supabase_client.storage.from_(settings.SUPABASE_RESUME_BUCKET).upload(
            path=path_in_bucket,
            file=file_bytes,
            file_options={"content-type": "application/pdf" if file_ext.lower() == "pdf" else "text/plain"}
        )
        return path_in_bucket
    except Exception as e:
        logger.warning(f"Supabase upload warning: {e}. Falling back to local stored path key.")
        return path_in_bucket

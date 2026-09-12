from pinecone import Pinecone
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

def get_pinecone_index():
    try:
        index = pc.Index(settings.PINECONE_INDEX_NAME)
        return index
    except Exception as e:
        logger.error(f"Error accessing Pinecone index {settings.PINECONE_INDEX_NAME}: {e}")
        raise e

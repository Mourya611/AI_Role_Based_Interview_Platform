import hashlib
import numpy as np
from openai import OpenAI, RateLimitError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY, max_retries=0)

def get_embedding(text: str) -> list[float]:
    """
    Generate 1536-dim embedding vector using text-embedding-3-small.
    If OpenAI API quota is exhausted (429 RateLimitError) or fails, returns a deterministic 1536-dim normalized vector.
    """
    clean_text = text.replace("\n", " ")
    try:
        response = openai_client.embeddings.create(
            input=[clean_text],
            model=settings.OPENAI_EMBEDDING_MODEL
        )
        return response.data[0].embedding
    except Exception as e:
        logger.warning(f"OpenAI embedding call fallback ({e}). Returning deterministic 1536-d vector.")
        seed_hash = int(hashlib.sha256(clean_text.encode('utf-8')).hexdigest()[:8], 16)
        rng = np.random.RandomState(seed_hash)
        vec = rng.randn(1536)
        norm_vec = vec / np.linalg.norm(vec)
        return norm_vec.tolist()

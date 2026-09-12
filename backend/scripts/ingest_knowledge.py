import os
import sys
import glob
import fitz # PyMuPDF
import logging

# Add parent directory to sys.path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.integrations.openai_client import get_embedding
from app.integrations.pinecone_client import get_pinecone_index
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ingest_knowledge")

ROLE_MAP = {
    "backend": "Backend Engineer",
    "ai_ml": "AI/ML Engineer",
    "full_stack": "Full Stack Developer",
    "data_engineering": "Data Engineer",
    "dsa": "Software Engineer",
    "cloud": "Cloud Engineer"
}

def chunk_text(text: str, max_chars: int = 800, overlap: int = 150) -> list[str]:
    """Split long text into overlapping chunks."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if len(current_chunk) + len(p) <= max_chars:
            current_chunk += ("\n\n" if current_chunk else "") + p
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = p

    if current_chunk:
        chunks.append(current_chunk)
    return chunks

def ingest_knowledge_base():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "knowledge_base"))
    logger.info(f"Scanning knowledge base path: {base_dir}")

    index = get_pinecone_index()
    vectors_to_upsert = []

    for folder_name, role_name in ROLE_MAP.items():
        folder_path = os.path.join(base_dir, folder_name)
        if not os.path.exists(folder_path):
            continue

        files = glob.glob(os.path.join(folder_path, "*.*"))
        for file_path in files:
            filename = os.path.basename(file_path)
            logger.info(f"Processing knowledge document: {filename} ({role_name})")

            raw_text = ""
            if file_path.endswith(".pdf"):
                doc = fitz.open(file_path)
                for page in doc:
                    raw_text += page.get_text() + "\n"
                doc.close()
            else:
                with open(file_path, "r", encoding="utf-8") as f:
                    raw_text = f.read()

            chunks = chunk_text(raw_text)
            for idx, chunk in enumerate(chunks):
                chunk_id = f"{folder_name}_{filename}_{idx}"
                embedding = get_embedding(f"Role: {role_name}\nContent: {chunk}")
                vectors_to_upsert.append({
                    "id": chunk_id,
                    "values": embedding,
                    "metadata": {
                        "source": filename,
                        "role": role_name,
                        "topic": filename.replace("_", " ").replace(".md", "").replace(".pdf", "").title(),
                        "text": chunk
                    }
                })

    if vectors_to_upsert:
        logger.info(f"Upserting {len(vectors_to_upsert)} knowledge vectors into Pinecone index '{settings.PINECONE_INDEX_NAME}'...")
        # Batch upsert (100 at a time)
        batch_size = 100
        for i in range(0, len(vectors_to_upsert), batch_size):
            batch = vectors_to_upsert[i:i + batch_size]
            index.upsert(vectors=batch)
        logger.info("Knowledge base ingestion completed successfully!")
    else:
        logger.warning("No knowledge base documents found to ingest.")

if __name__ == "__main__":
    ingest_knowledge_base()

import logging
from typing import List, Dict, Any
from app.integrations.openai_client import get_embedding
from app.integrations.pinecone_client import get_pinecone_index

logger = logging.getLogger(__name__)

def retrieve_rag_context(
    query_text: str,
    target_role: str,
    top_k: int = 4
) -> List[Dict[str, Any]]:
    """
    Construct embedding for query_text and retrieve top_k relevant context chunks
    from the Pinecone index 'ai-interview-knowledge' with strict role filtering.
    """
    try:
        query_vector = get_embedding(f"Role: {target_role}. Technical topic: {query_text}")
        index = get_pinecone_index()

        # Query pinecone index with strict role filter
        query_response = index.query(
            vector=query_vector,
            top_k=top_k,
            filter={"role": target_role},
            include_metadata=True
        )

        matches = query_response.get("matches", [])
        if not matches:
            # Try query without strict filter but prioritize role in post-filter
            query_response = index.query(
                vector=query_vector,
                top_k=top_k * 2,
                include_metadata=True
            )
            raw_matches = query_response.get("matches", [])
            matches = [m for m in raw_matches if m.get("metadata", {}).get("role") == target_role] or raw_matches[:top_k]

        results = []
        for match in matches:
            metadata = match.get("metadata", {})
            results.append({
                "score": match.get("score"),
                "text": metadata.get("text", metadata.get("chunk", "")),
                "topic": metadata.get("topic", "Technical Architecture"),
                "role": metadata.get("role", target_role),
                "source": metadata.get("source", "Knowledge Base")
            })

        if results:
            return results
    except Exception as e:
        logger.warning(f"RAG retrieval fallback triggered due to: {e}")

    # Fallback domain-specific RAG contexts strictly segregated by role
    role_fallbacks = {
        "AI/ML Engineer": [
            {"text": "Convolutional Neural Networks (CNNs) utilize learnable kernel convolutions and spatial max-pooling to extract translation-invariant visual feature representations from image inputs.", "topic": "Computer Vision & CNNs", "role": "AI/ML Engineer", "source": "Deep Learning Guide"},
            {"text": "Retrieval-Augmented Generation (RAG) pairs dense vector similarity search (Pinecone/HNSW) with LLMs to provide grounded context, preventing hallucination during query synthesis.", "topic": "RAG & Vector Search", "role": "AI/ML Engineer", "source": "GenAI Architectures"},
            {"text": "Overfitting occurs when high variance models memorize training noise; mitigate with Dropout, L1/L2 weight decay, and k-fold cross validation.", "topic": "Model Optimization & Regularization", "role": "AI/ML Engineer", "source": "ML Handbook"},
            {"text": "Serving ML models with FastAPI requires non-blocking asynchronous request handling, dynamic request batching, and ONNX Runtime/TensorRT model quantization.", "topic": "MLOps & Model Serving", "role": "AI/ML Engineer", "source": "Production ML"}
        ],
        "Backend Engineer": [
            {"text": "Monolithic architectures bundle components together; microservices decouple into independent services via REST/gRPC for horizontal scaling and fault isolation.", "topic": "System Design", "role": "Backend Engineer", "source": "System Design Primer"},
            {"text": "B-Tree database indexes maintain sorted pointers to reduce search complexity from O(N) to O(log N). Composite indexes must satisfy the leftmost prefix rule.", "topic": "Databases & Indexing", "role": "Backend Engineer", "source": "Database Internals"},
            {"text": "Distributed transactions require two-phase commit (2PC) or Saga patterns with compensating actions to ensure eventual consistency across decoupled microservices.", "topic": "Distributed Systems", "role": "Backend Engineer", "source": "Enterprise Patterns"}
        ],
        "Full Stack Developer": [
            {"text": "Server-Side Rendering (SSR) compiles React components on the server for faster First Contentful Paint and SEO, while Client-Side Rendering (CSR) hydrates DOM for dynamic interaction.", "topic": "Frontend Architecture", "role": "Full Stack Developer", "source": "Modern Web Architecture"},
            {"text": "State management requires memoization (useMemo, useCallback) and co-location to avoid cascading React re-renders across deep component trees.", "topic": "React State Management", "role": "Full Stack Developer", "source": "React Internals"}
        ],
        "Data Engineer": [
            {"text": "Batch processing with Apache Spark handles high-throughput ETL over historical data, whereas real-time streaming with Kafka/Flink processes event-driven streams with sub-second latency.", "topic": "Data Pipelines", "role": "Data Engineer", "source": "Streaming Systems"},
            {"text": "Parquet columnar storage and partition pruning drastically decrease I/O scan costs in OLAP analytical warehouses.", "topic": "Data Warehousing", "role": "Data Engineer", "source": "Big Data Storage"}
        ],
        "Cloud Engineer": [
            {"text": "Docker containers virtualize OS kernel user-space for rapid deployment, whereas Kubernetes orchestrates pod scheduling, service discovery, and rolling zero-downtime updates.", "topic": "Containerization & K8s", "role": "Cloud Engineer", "source": "Cloud Native"},
            {"text": "Infrastructure as Code (IaC) with Terraform allows declarative provisioning of VPCs, IAM security policies, and auto-scaling target groups.", "topic": "Cloud Infrastructure", "role": "Cloud Engineer", "source": "AWS Well-Architected"}
        ],
        "Software Engineer": [
            {"text": "Algorithm complexity bounds time and space growth: Hash maps provide O(1) average lookup, Binary Search provides O(log N), and Merge Sort provides O(N log N).", "topic": "Algorithms & Complexity", "role": "Software Engineer", "source": "DSA Fundamentals"},
            {"text": "SOLID principles guide clean OOP design: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.", "topic": "Object-Oriented Design", "role": "Software Engineer", "source": "Clean Architecture"}
        ]
    }
    return role_fallbacks.get(target_role, role_fallbacks.get("AI/ML Engineer", []))


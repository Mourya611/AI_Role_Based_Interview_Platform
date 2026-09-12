import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

ROLE_TOPIC_CATALOGS = {
    "AI/ML Engineer": [
        {
            "topic": "Deep Learning and Computer Vision",
            "subtopic": "Convolutional Neural Networks (CNNs)",
            "concept": "Kernel convolution, feature maps, pooling layers, and spatial invariance",
            "default_type": "mcq"
        },
        {
            "topic": "Machine Learning Fundamentals",
            "subtopic": "Overfitting and Regularization",
            "concept": "Bias-variance trade-off, L1/L2 weight penalties, dropout, and early stopping",
            "default_type": "short_answer"
        },
        {
            "topic": "RAG and Vector Databases",
            "subtopic": "Vector Search and Pinecone Indexing",
            "concept": "Dense embeddings, cosine similarity vs Euclidean distance, and HNSW approximate nearest neighbors",
            "default_type": "mcq"
        },
        {
            "topic": "Generative AI and Agentic Workflows",
            "subtopic": "LangChain and Tool-Calling Agents",
            "concept": "ReAct loop (Reasoning + Acting), function calling schemas, and hallucination mitigation",
            "default_type": "scenario"
        },
        {
            "topic": "MLOps and Inference Serving",
            "subtopic": "FastAPI Model Microservices and Optimization",
            "concept": "Asynchronous model serving, dynamic batching, GPU/CPU latency optimization, and ONNX quantization",
            "default_type": "descriptive"
        },
        {
            "topic": "Loss Functions and Optimization",
            "subtopic": "Gradient Descent and Optimizers",
            "concept": "Cross-entropy loss vs MSE, Adam optimizer momentum and adaptive learning rates",
            "default_type": "mcq"
        },
        {
            "topic": "Model Evaluation and Performance Metrics",
            "subtopic": "Classification Metrics under Class Imbalance",
            "concept": "Precision, Recall, F1-Score, ROC-AUC, and confusion matrix interpretation",
            "default_type": "short_answer"
        },
        {
            "topic": "Transformers and Attention Mechanisms",
            "subtopic": "Self-Attention and Transformer Architecture",
            "concept": "Multi-head self-attention Q, K, V matrix projections and positional encodings",
            "default_type": "descriptive"
        },
        {
            "topic": "Data Preprocessing and Feature Engineering",
            "subtopic": "Data Scaling and Embedding Normalization",
            "concept": "Min-max scaling, Z-score standardization, and unit-vector embedding normalization",
            "default_type": "short_answer"
        },
        {
            "topic": "RAG Architecture and Chunking",
            "subtopic": "Context Retrieval and Reranking",
            "concept": "Semantic chunking with token overlap, contextual compression, and cross-encoder reranking",
            "default_type": "scenario"
        },
        {
            "topic": "Computer Vision Transfer Learning",
            "subtopic": "Fine-tuning Pretrained Backbones",
            "concept": "ResNet/EfficientNet feature extraction, freezing early convolutional layers, and classifier head fine-tuning",
            "default_type": "descriptive"
        },
        {
            "topic": "ML System Design",
            "subtopic": "Real-Time Fraud and Anomaly Detection Pipeline",
            "concept": "Feature store architecture, streaming feature ingestion, low-latency scoring, and model drift monitoring",
            "default_type": "scenario"
        },
        {
            "topic": "Hyperparameter Tuning",
            "subtopic": "Optimization Strategies",
            "concept": "Grid search vs Random search vs Bayesian optimization (Tree-structured Parzen Estimator)",
            "default_type": "mcq"
        },
        {
            "topic": "Prompt Engineering and LLM Guardrails",
            "subtopic": "Safety and Structured Output Enforcement",
            "concept": "Few-shot in-context learning, chain-of-thought, and Pydantic/JSON schema constraint decoding",
            "default_type": "short_answer"
        },
        {
            "topic": "Distributed ML Training",
            "subtopic": "Data Parallelism vs Model Parallelism",
            "concept": "PyTorch DDP (DistributedDataParallel) all-reduce gradient synchronization vs tensor slicing",
            "default_type": "descriptive"
        }
    ],
    "Backend Engineer": [
        {
            "topic": "System Architecture",
            "subtopic": "Monolithic vs Microservices",
            "concept": "Service decomposition, fault isolation, and API gateway routing",
            "default_type": "mcq"
        },
        {
            "topic": "Databases and Indexing",
            "subtopic": "B-Tree Indexes and Query Optimization",
            "concept": "B-Tree logarithmic search, composite index leftmost prefix rule, and EXPLAIN ANALYZE",
            "default_type": "short_answer"
        },
        {
            "topic": "API Design",
            "subtopic": "REST vs GraphQL Trade-offs",
            "concept": "Statelessness, over-fetching/under-fetching, and HTTP caching",
            "default_type": "mcq"
        },
        {
            "topic": "Concurrency and Performance",
            "subtopic": "Asynchronous I/O and Event Loops",
            "concept": "Non-blocking I/O, coroutines, thread pools, and race condition prevention",
            "default_type": "short_answer"
        },
        {
            "topic": "Distributed Systems",
            "subtopic": "High-Throughput Rate Limiter and Cache Design",
            "concept": "Distributed token bucket, Redis caching, database sharding, and eventual consistency",
            "default_type": "scenario"
        },
        {
            "topic": "Data Consistency and Transactions",
            "subtopic": "ACID and Distributed Saga Pattern",
            "concept": "Two-phase commits vs choreographed/orchestrated Sagas with compensating transactions",
            "default_type": "descriptive"
        },
        {
            "topic": "Security and Authentication",
            "subtopic": "JWT, OAuth2 and Session Security",
            "concept": "Stateless JWT signing, refresh token rotation, and CSRF/XSS mitigations",
            "default_type": "short_answer"
        }
    ],
    "Full Stack Developer": [
        {
            "topic": "Frontend Architecture",
            "subtopic": "Server-Side Rendering (SSR) vs CSR",
            "concept": "FCP/LCP metrics, hydration, and Next.js SSR vs static rendering",
            "default_type": "mcq"
        },
        {
            "topic": "React State Management",
            "subtopic": "Re-rendering Optimization",
            "concept": "useMemo, useCallback, React.memo, and state co-location",
            "default_type": "short_answer"
        },
        {
            "topic": "Full Stack API Integration",
            "subtopic": "Client-Server Data Synchronization",
            "concept": "Optimistic UI updates, cache invalidation with SWR/React Query, and error boundaries",
            "default_type": "scenario"
        },
        {
            "topic": "Full Stack Security",
            "subtopic": "XSS, CSRF, and CORS Configuration",
            "concept": "Same-origin policy, httpOnly cookies, Content Security Policy, and CORS headers",
            "default_type": "mcq"
        },
        {
            "topic": "Database Modeling and ORM",
            "subtopic": "Relational Data Modeling and N+1 Queries",
            "concept": "Foreign keys, eager loading (joinedload), indexing foreign keys, and migration strategies",
            "default_type": "descriptive"
        }
    ],
    "Data Engineer": [
        {
            "topic": "Data Processing Paradigms",
            "subtopic": "Batch vs Stream Processing",
            "concept": "Throughput vs latency trade-offs, Spark batching vs Kafka/Flink streaming",
            "default_type": "mcq"
        },
        {
            "topic": "Big Data Computation",
            "subtopic": "PySpark RDDs and DataFrames",
            "concept": "Transformations vs Actions, Catalyst optimizer, wide vs narrow dependencies, and data shuffling",
            "default_type": "short_answer"
        },
        {
            "topic": "Data Lakehouse Architecture",
            "subtopic": "Parquet and Partitioning Strategies",
            "concept": "Columnar storage compression, dictionary encoding, and partition pruning",
            "default_type": "mcq"
        },
        {
            "topic": "Pipeline Orchestration",
            "subtopic": "DAG Scheduling and Backfilling",
            "concept": "Airflow DAG task dependencies, idempotent runs, retries, and data quality SLA checks",
            "default_type": "scenario"
        },
        {
            "topic": "Data Warehousing",
            "subtopic": "Star Schema vs Snowflake Schema",
            "concept": "Fact tables, slowly changing dimensions (SCD Type 2), and analytical aggregation performance",
            "default_type": "descriptive"
        }
    ],
    "Cloud Engineer": [
        {
            "topic": "Containerization Fundamentals",
            "subtopic": "Docker Kernels vs Hypervisors",
            "concept": "cgroups, namespaces, image layer caching, and lightweight container virtualization",
            "default_type": "mcq"
        },
        {
            "topic": "Kubernetes Orchestration",
            "subtopic": "Pods, Deployments, and Services",
            "concept": "ReplicaSets, rolling updates, ClusterIP vs NodePort vs LoadBalancer, and readiness probes",
            "default_type": "short_answer"
        },
        {
            "topic": "Infrastructure as Code",
            "subtopic": "Terraform State and Idempotency",
            "concept": "Declarative syntax, state locking in S3/DynamoDB, and plan/apply lifecycle",
            "default_type": "mcq"
        },
        {
            "topic": "Cloud Networking and High Availability",
            "subtopic": "Multi-AZ VPC Architecture",
            "concept": "Public/private subnets, NAT gateways, Route Tables, and Application Load Balancers",
            "default_type": "scenario"
        },
        {
            "topic": "Cloud Security and Governance",
            "subtopic": "IAM Least Privilege and Secret Management",
            "concept": "Role-based access control, temporary STS credentials, KMS encryption, and Secret Manager rotation",
            "default_type": "descriptive"
        }
    ],
    "Software Engineer": [
        {
            "topic": "Algorithms and Complexity",
            "subtopic": "Time and Space Complexity Analysis",
            "concept": "Big-O notation, logarithmic vs linearithmic bounds, and amortized complexity",
            "default_type": "mcq"
        },
        {
            "topic": "Data Structures",
            "subtopic": "Hash Maps and Collision Resolution",
            "concept": "Hash function distribution, separate chaining, open addressing, and load factor resizing",
            "default_type": "short_answer"
        },
        {
            "topic": "Object-Oriented Design",
            "subtopic": "SOLID Principles",
            "concept": "Single responsibility, Liskov substitution, interface segregation, and dependency inversion",
            "default_type": "mcq"
        },
        {
            "topic": "Software Architecture",
            "subtopic": "Design Patterns",
            "concept": "Factory, Observer, Strategy, and Singleton trade-offs in real-world applications",
            "default_type": "scenario"
        },
        {
            "topic": "Testing and Code Quality",
            "subtopic": "Unit, Integration, and Regression Testing",
            "concept": "Mocking vs stubbing, test-driven development, code coverage metrics, and flaky test mitigation",
            "default_type": "descriptive"
        }
    ]
}

def generate_interview_blueprint(
    target_role: str,
    total_questions: int,
    candidate_profile: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Generate an upfront blueprint enforcing question count, question type distribution,
    topic diversity, and candidate profile grounding strictly within the target role domain.
    """
    catalog = ROLE_TOPIC_CATALOGS.get(target_role, ROLE_TOPIC_CATALOGS.get("AI/ML Engineer"))
    
    # Define type distributions according to question count
    type_sequences = {
        5: ["mcq", "short_answer", "mcq", "scenario", "descriptive"],
        7: ["mcq", "short_answer", "mcq", "short_answer", "scenario", "descriptive", "descriptive"],
        12: ["mcq", "short_answer", "mcq", "short_answer", "mcq", "scenario", "descriptive", "mcq", "short_answer", "scenario", "scenario", "descriptive"],
        15: ["mcq", "short_answer", "mcq", "short_answer", "mcq", "scenario", "descriptive", "mcq", "short_answer", "scenario", "descriptive", "mcq", "short_answer", "scenario", "descriptive"]
    }

    distribution = type_sequences.get(total_questions)
    if not distribution:
        distribution = (["mcq", "short_answer", "scenario", "descriptive"] * 5)[:total_questions]

    # Map candidate profile projects and skills
    resume_skills = candidate_profile.get("skills", []) if candidate_profile else []
    resume_projects = candidate_profile.get("projects", []) if candidate_profile else []
    ml_exp = candidate_profile.get("ml_ai_experience", []) if candidate_profile else []
    genai_exp = candidate_profile.get("genai_rag_experience", []) if candidate_profile else []
    
    blueprint = []
    for i in range(total_questions):
        catalog_item = catalog[i % len(catalog)]
        q_type = distribution[i]
        q_num = i + 1
        
        # Difficulty progression
        if q_num == 1:
            diff = "Easy"
        elif q_num <= total_questions // 2:
            diff = "Medium"
        elif q_num == total_questions:
            diff = "Hard"
        else:
            diff = "Medium"

        # Tie in candidate profile evidence
        evidence = None
        if target_role == "AI/ML Engineer":
            if "CNN" in catalog_item["subtopic"] and (ml_exp or any("cnn" in str(p).lower() for p in resume_projects)):
                evidence = "Candidate experience with CNN image classification and Watson ML"
            elif "Vector" in catalog_item["subtopic"] and (genai_exp or "Pinecone" in resume_skills):
                evidence = "Candidate project utilizing Pinecone vector database and embeddings"
            elif "LangChain" in catalog_item["subtopic"] and (genai_exp or "LangChain" in resume_skills):
                evidence = "Candidate experience with LangChain tool-calling agents and RAG"
            elif "FastAPI" in catalog_item["subtopic"] and "FastAPI" in resume_skills:
                evidence = "Candidate background in FastAPI ML microservice development"
            elif resume_skills:
                evidence = f"Candidate skills in {resume_skills[i % len(resume_skills)]}"
        else:
            if resume_skills:
                evidence = f"Candidate background in {resume_skills[i % len(resume_skills)]}"

        blueprint.append({
            "question_number": q_num,
            "question_type": q_type,
            "topic": catalog_item["topic"],
            "subtopic": catalog_item["subtopic"],
            "concept": catalog_item["concept"],
            "difficulty": diff,
            "resume_evidence": evidence
        })

    logger.info(f"Generated blueprint of {len(blueprint)} questions for role {target_role}")
    return blueprint

# Machine Learning & Deep Learning Core Concepts

## Overfitting, Bias-Variance Trade-off, and Regularization
High bias leads to underfitting where a model is too simple to capture underlying patterns. High variance leads to overfitting where a model memorizes training noise and fails to generalize to unseen test data.
Regularization techniques control model complexity:
- L1 Regularization (Lasso) adds absolute coefficient weights penalty, driving uninformative feature weights to absolute zero (feature selection).
- L2 Regularization (Ridge) adds squared coefficient weights penalty, shrinking weights smoothly toward zero.
- Dropout randomly deactivates neuron activations during deep neural network training to prevent co-adaptation.
- Cross-validation (K-Fold) ensures robust out-of-sample performance evaluation.

## Convolutional Neural Networks (CNNs) & Computer Vision
CNN architectures specialize in grid-structured data like images.
- Convolutional Layers apply learnable spatial filters (kernels) to produce feature maps capturing edges, textures, and semantic shapes.
- Pooling Layers (Max Pooling / Average Pooling) downsample spatial dimensions, providing translation invariance and reducing compute.
- Activation Functions (ReLU, GELU) introduce non-linearities.
- Transfer Learning & Pretrained backbones (ResNet, EfficientNet) utilize features learned from large datasets to solve target classification tasks efficiently with fine-tuning.

## Vector Search, Embeddings, and Vector Databases (Pinecone)
Vector embeddings convert unstructured data (text, images) into dense high-dimensional vectors (e.g. 1536 dimensions) where semantic similarity corresponds to geometric proximity.
- Similarity Metrics: Cosine similarity measures angle between normalized vectors (dot product of unit vectors). Euclidean distance measures absolute spatial distance.
- Approximate Nearest Neighbor (ANN) Algorithms: Hierarchical Navigable Small World (HNSW) and Inverted File with Product Quantization (IVF-PQ) allow sub-millisecond similarity search across millions of vectors without exhaustive linear scans.
- Pinecone Indexing: Managed vector database providing serverless vector search, metadata filtering (e.g. role, topic), and hybrid search capabilities.

## Retrieval-Augmented Generation (RAG) & Chunking Strategies
RAG couples parametric memory (LLM weights) with non-parametric external knowledge bases to eliminate hallucinations and provide up-to-date domain answers.
- Chunking: Splitting documents into semantic chunks (e.g. 500-1000 characters with 10-20% overlap) prevents contextual fragmentation while fitting token budgets.
- Retrieval Pipeline: Embed user prompt -> ANN vector query against Pinecone -> Retrieve top-K relevant chunks -> Inject chunks into prompt as grounded context -> Synthesize grounded response.
- Advanced RAG: Query expansion, contextual compression, and cross-encoder re-ranking optimize precision and relevance before generation.

## Agentic AI, LangChain, and Tool Calling
AI Agents utilize LLMs as reasoning engines to iteratively plan, execute tools, observe outputs, and synthesize final responses.
- ReAct Pattern (Reason + Act): Prompts LLMs to generate Thought, Action, Action Input, and Observation loops.
- Tool Calling: Structured schema definitions (JSON Schema) enabling LLMs to invoke external APIs, database lookups, and Python code executors deterministically.
- LangChain Orchestration: Chains prompt templates, LLMs, output parsers, memory components, and vector retrievers into unified workflows.

## Loss Functions & Optimization
- Cross-Entropy Loss evaluates probabilistic classification outputs against one-hot encoded ground truth.
- Mean Squared Error (MSE) measures variance in regression tasks.
- Optimization Algorithms: Adam (Adaptive Moment Estimation) combines momentum and RMSprop for adaptive per-parameter learning rates, outperforming standard stochastic gradient descent (SGD) in sparse and non-convex deep learning landscapes.

## Model Evaluation Metrics
- Precision = TP / (TP + FP): Proportion of predicted positives that are truly positive (critical for spam detection, false-positive sensitivity).
- Recall = TP / (TP + FN): Proportion of actual positives correctly identified (critical for medical diagnosis, defect detection).
- F1 Score = 2 * (Precision * Recall) / (Precision + Recall): Harmonic mean balancing precision and recall under imbalanced class distributions.
- ROC-AUC: Area under the receiver operating characteristic curve evaluating true positive rate vs false positive rate across all decision thresholds.

## MLOps, FastAPI Serving, and Inference Optimization
Serving machine learning models in production requires balancing latency, throughput, and resource utilization.
- Asynchronous FastAPI microservices allow non-blocking request handling and health monitoring endpoints.
- Dynamic Batching groups incoming concurrent inference requests to maximize GPU/CPU tensor throughput.
- Quantization (FP16, INT8) and ONNX Runtime conversion compress model size and accelerate inference with negligible loss in accuracy.


# AI-Powered Role-Based Candidate Screening & Technical Interview Platform

A production-ready, full-stack AI platform that simulates structured technical interviews with dynamic question generation based on candidate resumes, target job roles, RAG (Retrieval-Augmented Generation) context from indexed knowledge bases, and adaptive response evaluation.

![InterviewAI Dashboard](docs/images/dashboard.png)

---

## 📸 Platform Showcase

### 1. Interactive Dashboard
Landing page matching the visual source of truth with quick-start actions, feature tags, and performance statistics.
![Dashboard Overview](docs/images/dashboard.png)

### 2. Step 1: Resume Upload & Candidate Profiling
Drag-and-drop or file selector supporting PDF and TXT documents up to 5MB. Automatic extraction of candidate technical experience, ML/AI projects, frameworks, and deployment background.
![Resume Upload](docs/images/upload_resume.png)

### 3. Step 2: Role Selection & Question Count Picker
Interactive selection across 6 engineering roles (*AI/ML Engineer, Backend Engineer, Full Stack Developer, Data Engineer, Software Engineer, Cloud Engineer*) with dynamic question count configuration (`5`, `7`, `12`, or `15` questions).
![Role and Question Count Selection](docs/images/role_and_question_selection.png)

### 4. Step 3: RAG Retrieval & Blueprint Synthesis
Real-time orchestration retrieving 1536-dimensional Pinecone vector chunks and constructing an upfront interview blueprint across mixed question types (MCQ, Short Answer, Scenario, Descriptive).
![RAG Context Generation](docs/images/rag_generation_loading.png)

### 5. Candidate Profile & Metrics Tracking
Comprehensive candidate profile overview with interview history, average competency score, and tracked domain performance.
![Candidate Profile](docs/images/candidate_profile.png)

---

## 💡 Sample Interview Outputs & Adaptive Evaluation

### Sample 1: Multiple Choice Question (MCQ) - Deep Learning & Vision
> **Question 1 of 15** · `Deep Learning and Computer Vision` · `Easy`
>
> **Question:** In a typical CNN architecture for image classification, which operation primarily provides translation (spatial) invariance?
> - **A)** Convolution with stride 1
> - **B)** Max pooling *(Selected)*
> - **C)** Batch normalization
> - **D)** Fully connected layer
>
> **Evaluation Result:**
> - **Score:** `10/10` | **Rating:** `Excellent`
> - **Feedback:** Correct choice! Pooling layers (especially max pooling) downsample feature maps, reducing sensitivity to small translations in the input image and thus providing spatial invariance.
> - **Adaptive Next Difficulty:** `Medium`

### Sample 2: Short Answer - Machine Learning Fundamentals
> **Question 2 of 15** · `Machine Learning Fundamentals` · `Medium`
>
> **Question:** Briefly describe how L2 regularization and dropout each mitigate overfitting, and state one practical way to apply early stopping during model training.
>
> **Candidate Answer:** L2 regularization adds a squared weight penalty to the loss function that shrinks non-zero weights smoothly towards zero, preventing individual features from dominating. Dropout randomly zeroes out neuron activations during training passes to prevent co-adaptation. Early stopping monitors validation set loss after each epoch and stops training when performance ceases to improve.
>
> **Evaluation Result:**
> - **Score:** `9/10` | **Rating:** `Excellent`
> - **Feedback:** Comprehensive explanation clearly differentiating weight decay penalties from activation dropout, with accurate validation-loss monitoring criteria.
> - **Key Strengths:** Accurate distinction of regularization mechanisms; practical early stopping rule.

### Sample 3: Multiple Choice Question (MCQ) - RAG & Vector Search
> **Question 3 of 15** · `RAG and Vector Databases` · `Medium`
>
> **Question:** When indexing dense vector embeddings in Pinecone for a RAG pipeline, which similarity metric is invariant to vector magnitude when embeddings are unit-normalized?
> - **A)** Cosine Similarity *(Selected)*
> - **B)** Manhattan Distance
> - **C)** Chebyshev Distance
> - **D)** Hamming Distance
>
> **Evaluation Result:**
> - **Score:** `10/10` | **Rating:** `Excellent`
> - **Feedback:** Correct! Cosine similarity measures the angle between vectors, which is strictly identical to dot product when vectors are L2-normalized.

---

## 🌟 Visual Source of Truth

The user interface matches the reference design structure, spacing, color palette (`#4F46E5` primary purple, crisp light `#F8FAFC` background, rounded cards), progress indicators, live interview screen with timer, completed summary, and detailed accordion feedback.

---

## 🏗️ System Architecture

```
                               ┌────────────────────────────────────────┐
                               │    Next.js 14+ Frontend (TypeScript)   │
                               │    Tailwind CSS, Lucide React Icons    │
                               └───────────────────┬────────────────────┘
                                                   │ REST API Calls
                                                   ▼
                               ┌────────────────────────────────────────┐
                               │         FastAPI Python Backend         │
                               │  Pydantic V2, SQLAlchemy 2.0 Async, CORS│
                               └───────┬───────────┬───────────┬────────┘
                                       │           │           │
               ┌───────────────────────┘           │           └───────────────────────┐
               ▼                                   ▼                                   ▼
        ┌──────────────┐                 ┌───────────────────┐               ┌───────────────────┐
        │  PostgreSQL  │                 │  Supabase Storage │               │    OpenAI API     │
        │ (Supabase DB)│                 │ (resumes bucket)  │               │  (OPENAI_MODEL &  │
        └──────────────┘                 └───────────────────┘               │ 1536d Embeddings) │
                                                                             └─────────┬─────────┘
                                                                                       │
                                                                                       ▼
                                                                             ┌───────────────────┐
                                                                             │   Pinecone Index  │
                                                                             │(ai-interview-knwld│
                                                                             └───────────────────┘
```

---

## 🚀 Core User Flow

```
HOME / DASHBOARD
      ↓
NEW INTERVIEW WIZARD
      ↓
UPLOAD RESUME (PDF/TXT -> PyMuPDF -> Supabase Storage)
      ↓
SELECT TARGET ROLE (Backend, AI/ML, Full Stack, Data, Software, Cloud)
      ↓
RAG CONTEXT CONSTRUCTION (Pinecone 1536-d Vector Search)
      ↓
LIVE TECHNICAL INTERVIEW (Dynamic Questions + Real-time Timer)
      ↓
SUBMIT ANSWER
      ↓
AI EVALUATION & ADAPTIVE DIFFICULTY ADJUSTMENT
      ↓
INTERVIEW COMPLETED SUMMARY
      ↓
DETAILED FEEDBACK ACCORDION & DOWNLOADABLE PDF REPORT
```

---

## 🛠️ Tech Stack

- **Frontend:** Next.js 14+ (App Router), TypeScript, Tailwind CSS, Lucide React
- **Backend:** Python 3.13, FastAPI, Pydantic V2, SQLAlchemy 2.0, ReportLab (PDF generation)
- **AI Engine:** OpenAI API (`OPENAI_MODEL` configurable, default: `gpt-4o-mini`), OpenAI `text-embedding-3-small` (1536 dimensions)
- **Vector Database (RAG):** Pinecone (Index: `ai-interview-knowledge`, 1536 dimensions, Cosine similarity)
- **Database:** PostgreSQL (Supabase Hosted)
- **File Storage:** Supabase Storage (Private bucket `resumes`)
- **PDF Processing:** PyMuPDF (`fitz`)

---

## 📁 Repository Folder Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes/
│   │   │       ├── health.py
│   │   │       ├── resumes.py
│   │   │       ├── interviews.py
│   │   │       └── profile.py
│   │   ├── core/
│   │   │   └── config.py
│   │   ├── db/
│   │   │   └── database.py
│   │   ├── integrations/
│   │   │   ├── openai_client.py
│   │   │   ├── pinecone_client.py
│   │   │   └── supabase_client.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── interview.py
│   │   │   ├── question.py
│   │   │   ├── answer.py
│   │   │   └── report.py
│   │   ├── schemas/
│   │   │   ├── resume.py
│   │   │   ├── interview.py
│   │   │   ├── question.py
│   │   │   ├── answer.py
│   │   │   └── report.py
│   │   ├── services/
│   │   │   ├── resume_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── question_service.py
│   │   │   ├── evaluation_service.py
│   │   │   ├── report_service.py
│   │   │   └── storage_service.py
│   │   └── main.py
│   ├── knowledge_base/
│   │   ├── backend/
│   │   ├── ai_ml/
│   │   ├── full_stack/
│   │   ├── data_engineering/
│   │   ├── dsa/
│   │   └── cloud/
│   ├── scripts/
│   │   └── ingest_knowledge.py
│   ├── tests/
│   │   └── test_api.py
│   ├── .env
│   ├── .env.example
│   └── requirements.txt
│
└── frontend/
    ├── app/
    │   ├── page.tsx (Dashboard)
    │   ├── new-interview/page.tsx (Resume Upload & Role Selection Wizard)
    │   ├── interview/[sessionId]/page.tsx (Live Technical Interview)
    │   ├── results/[sessionId]/page.tsx (Interview Completed Summary)
    │   ├── interviews/[sessionId]/page.tsx (Detailed Feedback & PDF Download)
    │   ├── interviews/page.tsx (My Interviews History)
    │   ├── profile/page.tsx (Candidate Profile)
    │   └── settings/page.tsx (Platform Preferences)
    ├── components/
    │   └── layout/Sidebar.tsx
    ├── lib/
    │   └── api.ts
    ├── .env.local
    └── .env.example
```

---

## ⚙️ Environment Variables Setup

### Backend `.env` (`backend/.env`)
```env
OPENAI_API_KEY=sk-proj-...
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small

PINECONE_API_KEY=pcsk_...
PINECONE_INDEX_NAME=ai-interview-knowledge

DATABASE_URL=postgresql://postgres:password@db.qrjplinrrmtiqalozmsn.supabase.co:5432/postgres

SUPABASE_URL=https://qrjplinrrmtiqalozmsn.supabase.co
SUPABASE_SERVICE_ROLE_KEY=sb_secret_...
SUPABASE_RESUME_BUCKET=resumes
```

### Frontend `.env.local` (`frontend/.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

> [!IMPORTANT]
> **Security Guarantee:** Sensitive credentials (`OPENAI_API_KEY`, `PINECONE_API_KEY`, `DATABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`) are kept exclusively on the FastAPI backend and are never transmitted to browser bundles.

---

## ⚡ Local Development Setup

### 1. Backend Setup & Ingestion

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run Knowledge Base Ingestion Script to seed Pinecone vector index
python scripts/ingest_knowledge.py

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

FastAPI server runs at `http://localhost:8000`. API documentation available at `http://localhost:8000/docs`.

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Run Next.js development server
npm run dev
```

Open `http://localhost:3000` in your web browser.

---

## 🧪 Running Tests

```bash
cd backend
pytest -v
```

---

## 🌐 Deployment Guides

### 1. Backend Deployment on Render (Web Service)

#### Option A: 1-Click Blueprint with `render.yaml`
1. Push your code to your GitHub repository: `https://github.com/Mourya611/AI_Role_Based_Interview_Platform.git`.
2. In the [Render Dashboard](https://dashboard.render.com/), click **New +** -> **Blueprint**.
3. Connect your repository. Render will automatically detect `render.yaml` and configure the service.
4. Fill in your secret environment variables (`GROQ_API_KEY`, `OPENAI_API_KEY`, `PINECONE_API_KEY`, `DATABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`).
5. Click **Apply** to deploy.

#### Option B: Manual Web Service Setup
1. In Render, select **New +** -> **Web Service**.
2. Connect your GitHub repository.
3. Configure the following settings:
   - **Name:** `ai-interview-backend`
   - **Region:** Any (e.g., Oregon or Frankfurt)
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. In the **Environment Variables** section, add:
   - `GROQ_API_KEY`: Your Groq API key
   - `GROQ_MODEL`: `openai/gpt-oss-120b`
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `OPENAI_MODEL`: `gpt-4o-mini`
   - `OPENAI_EMBEDDING_MODEL`: `text-embedding-3-small`
   - `PINECONE_API_KEY`: Your Pinecone API key
   - `PINECONE_INDEX_NAME`: `ai-interview-knowledge`
   - `DATABASE_URL`: Your Supabase PostgreSQL connection string
   - `SUPABASE_URL`: `https://<project-ref>.supabase.co`
   - `SUPABASE_SERVICE_ROLE_KEY`: Your Supabase service role key
   - `SUPABASE_RESUME_BUCKET`: `resumes`
5. Click **Create Web Service**.
6. Copy your deployed Render backend URL (e.g., `https://ai-interview-backend.onrender.com`).

---

### 2. Frontend Deployment on Vercel

1. In the [Vercel Dashboard](https://vercel.com/dashboard), click **Add New...** -> **Project**.
2. Import your GitHub repository: `https://github.com/Mourya611/AI_Role_Based_Interview_Platform`.
3. In the project configuration:
   - **Framework Preset:** `Next.js`
   - **Root Directory:** Click **Edit** and choose `frontend`.
   - **Build Command:** `npm run build` (or leave default)
   - **Output Directory:** `.next` (default)
4. In the **Environment Variables** section, add:
   - `NEXT_PUBLIC_API_URL`: Your deployed Render backend URL (e.g., `https://ai-interview-backend.onrender.com` without trailing slash).
5. Click **Deploy**.
6. Vercel will build and deploy your application to a production URL (e.g., `https://ai-role-based-interview-platform.vercel.app`).


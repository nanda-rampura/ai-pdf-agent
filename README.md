
# 🚀 AI PDF Agent (Production-Style RAG System)

![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-orange)
![VectorDB](https://img.shields.io/badge/VectorDB-ChromaDB-purple)

---

## 🧠 Overview

AI PDF Agent is a **Retrieval-Augmented Generation (RAG)** system that allows users to upload PDF documents and ask intelligent questions over them.

It uses:
- OpenAI embeddings for semantic understanding
- ChromaDB for vector similarity search
- GPT-4o-mini for response generation
- FastAPI for backend APIs

---

## ⚙️ System Architecture

```
PDF Upload
   ↓
Text Extraction (PyPDF2)
   ↓
Chunking (RecursiveCharacterTextSplitter)
   ↓
Embeddings (OpenAI)
   ↓
Vector DB (ChromaDB)
   ↓
Similarity Search
   ↓
Filtering + Ranking
   ↓
Context Compression
   ↓
LLM (GPT-4o-mini)
   ↓
Final Answer
```

---

## ✨ Features

- 📄 PDF upload via API
- ✂️ Intelligent text chunking (overlap-aware)
- 🧠 OpenAI embeddings (semantic search)
- 🔍 ChromaDB vector similarity search
- 📊 Score-based filtering & ranking
- 🧩 Context compression for LLM efficiency
- 🤖 GPT-4o-mini responses grounded in context
- 📈 Request-level logging with timing metrics
- ⚡ FastAPI production-ready structure

---

## 🏗️ Project Structure

```
app/
├── main.py                 # FastAPI app + logging middleware
├── api/
│   └── routes.py          # API endpoints
├── services/
│   ├── ai_service.py      # LLM integration
│   ├── embedding_service.py
│   ├── vector_db.py       # ChromaDB logic
│   └── pdf_service.py
└── core/
    ├── config.py
    └── request_context.py
```

---

## 📡 API Endpoints

### 📄 Upload PDF
```http
POST /upload-pdf/
```

### 🤖 Ask Question
```http
GET /ask-pdf/?question=your_question
```

---

## 🔍 Retrieval Pipeline (Key Innovation)

### 1. Retrieval
- Semantic search using embeddings + ChromaDB

### 2. Filtering
- Removes low relevance chunks using threshold (e.g., 0.65)

### 3. Ranking
- Sorts chunks by similarity score

### 4. Context Formatting
- Structured chunk labeling improves LLM reasoning

### 5. LLM Grounding
- Strict prompt prevents hallucinations

### 6. Observability
- Request ID logging
- Step-by-step timing breakdown

---

## 🧰 Tech Stack

- Python 3.11+
- FastAPI
- OpenAI API (GPT-4o-mini)
- ChromaDB (in-memory vector DB)
- LangChain (text splitting + embeddings)
- PyPDF2
- NumPy

---

## 🚀 Run Locally

```bash
git clone <repo-url>
cd ai-pdf-agent

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

---

## 🌐 API Docs

```
http://127.0.0.1:8000/docs
```

---

## ☁️ Deployment

- Deployable on Render
- Uses in-memory ChromaDB (no persistent storage required)
- Stateless API design

---

## 📈 Future Improvements

- Persistent vector DB (Redis / Chroma persistent / Pinecone)
- Multi-document chat memory
- Streaming responses
- React frontend UI
- Hybrid search (BM25 + vector)
- Reranking model (cross-encoder)

---

## 👨‍💻 Author

Built as part of an AI engineering learning journey focused on production-grade RAG systems.

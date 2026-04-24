# AI PDF Agent 🚀

An AI-powered Retrieval-Augmented Generation (RAG) system built with FastAPI and OpenAI that allows users to upload PDFs and ask semantic questions over their content.

---

## System Overview

This project implements a production-style **RAG (Retrieval-Augmented Generation) pipeline**:


The system enables intelligent question answering over PDF documents using vector-based retrieval.

---

## ⚙️ Features

- 📄 Upload PDF documents via API
- ✂️ Intelligent text chunking (RecursiveCharacterTextSplitter)
- 🧠 OpenAI embeddings for semantic representation
- 🔍 Cosine similarity-based document retrieval
- 🤖 Context-aware LLM responses using GPT-4o-mini
- ⚡ FastAPI backend (production-style modular architecture)

---

## 📌 AI Pipeline Evolution

This project was built step-by-step to simulate a real-world AI system:

- 📄 **PDF Upload API** → Ingests documents via FastAPI
- ✂️ **Chunking Layer** → Splits large documents into semantic chunks
- 🧠 **Embedding Layer** → Converts text into vector representations
- 🔍 **Similarity Search Layer** → Finds most relevant chunks using cosine similarity
- 🤖 **LLM Layer** → Generates final answer using retrieved context

---

## 🏗️ Project Structure

ai-pdf-agent/
├── app/
│ ├── main.py # FastAPI entry point
│ ├── api/
│ │ └── routes.py # API routes (upload, ask)
│ ├── services/
│ │ ├── ai_service.py # LLM logic (OpenAI calls)
│ │ ├── embedding_service.py # Chunking + embeddings + similarity
│ │ └── pdf_service.py # PDF extraction logic
│ └── core/
│ └── config.py # Environment variables & config
├── requirements.txt
├── .env
├── .gitignore
└── README.md

## 🧰 Tech Stack

- Python 3.9+
- FastAPI
- OpenAI API (GPT-4o-mini)
- LangChain (Text splitting + embeddings)
- PyPDF2
- NumPy

---

## 📡 API Endpoints

### 📄 Upload PDF

```http
POST /upload-pdf/

## API Endpoints

### Upload PDF

```
POST /upload-pdf/
```

### Ask AI

```
GET /ask-ai/
```

### Ask PDF

```
GET /ask-pdf/
```

## Setup

### 1. Clone Repository

```
git clone <your-repo-url>
cd ai-pdf-agent
```

### 2. Create Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Run Server

```
uvicorn app.main:app --reload
```

## API Docs

Open in browser:

```
http://127.0.0.1:8000/docs
```

## Future Improvements

* Chunking large PDFs
* Vector database integration
* LangChain integration
* Chat memory
* Frontend UI

---

## Author

Built as part of AI Engineering learning journey.

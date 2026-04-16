# AI PDF Agent

An AI-powered PDF assistant built with FastAPI and OpenAI that allows users to upload PDFs and ask questions.

## Features

* Upload PDF files
* Extract text from PDFs
* Ask AI questions
* Chat with uploaded PDF
* FastAPI backend
* OpenAI integration

## Project Structure

```
ai-pdf-agent/
├── app/
│   ├── main.py
│   ├── api/
│   └── services/
├── requirements.txt
├── README.md
└── .gitignore
```

## Tech Stack

* Python
* FastAPI
* OpenAI
* PyPDF2

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

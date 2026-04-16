from fastapi import FastAPI, UploadFile, File
import PyPDF2
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
import numpy as np

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# Initialize FastAPI app
app = FastAPI()

pdf_chunks = []
embeddings = OpenAIEmbeddings()
pdf_embeddings = []

@app.get("/")
def home():
    return {"message": "AI PDF Agent is running 🚀"}

@app.get("/ask-pdf/")
def ask_pdf(question: str):

    question_embedding = embeddings.embed_query(question)

    similarities = [
        cosine_similarity(question_embedding, emb)
        for emb in pdf_embeddings
    ]

    top_indices = np.argsort(similarities)[-3:]
    print("Top indices:", top_indices)

    context = "\n".join([pdf_chunks[i] for i in top_indices])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer using context"},
            {"role": "user", "content": f"{context}\n\nQuestion: {question}"}
        ]
    )

    return {"answer": response.choices[0].message.content}

@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    global pdf_chunks, pdf_embeddings

    content = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(content)

    reader = PyPDF2.PdfReader("temp.pdf")
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    pdf_chunks = split_text_into_chunks(text)

    # Create embeddings
    pdf_embeddings = embeddings.embed_documents(pdf_chunks)

    return {
        "filename": file.filename,
        "total_chunks": len(pdf_chunks)
    }

def split_text_into_chunks(text: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)
    return chunks

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


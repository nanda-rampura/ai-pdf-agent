from fastapi import APIRouter, UploadFile, File
import numpy as np
from app.services.ai_service import ask_llm
from app.services.embedding_service import (
    split_text,
    get_embeddings,
    cosine_similarity
)

router = APIRouter()

pdf_chunks = []
pdf_embeddings = []

embeddings = get_embeddings()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):

    global pdf_chunks, pdf_embeddings

    content = await file.read()

    with open("temp.pdf", "wb") as f:
        f.write(content)

    import PyPDF2
    reader = PyPDF2.PdfReader("temp.pdf")

    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    pdf_chunks = split_text(text)
    pdf_embeddings = embeddings.embed_documents(pdf_chunks)

    return {"chunks": len(pdf_chunks)}


@router.get("/ask-pdf/")
def ask_pdf(question: str):

    if not pdf_chunks:
        return {"error": "Upload PDF first"}

    q_emb = embeddings.embed_query(question)

    similarities = [
        cosine_similarity(q_emb, emb)
        for emb in pdf_embeddings
    ]

    top_indices = np.argsort(similarities)[-3:]

    context = "\n".join([pdf_chunks[i] for i in top_indices])

    answer = ask_llm(context, question)

    return {"answer": answer}
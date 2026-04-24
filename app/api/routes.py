from fastapi import APIRouter, UploadFile, File
from app.services.ai_service import ask_llm
from app.services.embedding_service import (
    split_text,
    get_embeddings,
)
import uuid
from app.services.vector_db import add_documents, search

router = APIRouter()

embeddings = get_embeddings()

@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):

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
    doc_id = str(uuid.uuid4())  # unique per upload
    ids = [f"{doc_id}_{i}" for i in range(len(pdf_chunks))]
    add_documents(pdf_chunks, pdf_embeddings, ids)
    return {
        "chunks": len(pdf_chunks),
        "message": "Stored in vector DB successfully"
    }


@router.get("/ask-pdf/")
def ask_pdf(question: str):
    q_emb = embeddings.embed_query(question)

    top_chunks = search(q_emb, top_k=3)
    
    if not top_chunks:
        return {"error": "No data found. Upload PDF first."}
    
    # Step 3: Build context
    context = "\n".join(top_chunks)

    # Step 4: Ask LLM
    answer = ask_llm(context, question)

    return {"answer": answer}
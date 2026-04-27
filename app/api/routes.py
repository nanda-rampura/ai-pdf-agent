import logging
import uuid
import time

from fastapi import APIRouter, UploadFile, File

from app.core.request_context import get_request_id
from app.services.ai_service import ask_llm
from app.services.embedding_service import split_text, get_embeddings
from app.services.vector_db import add_documents, search

router = APIRouter()

# Logger
logger = logging.getLogger(__name__)
embeddings = get_embeddings()


# -----------------------------
# Request-aware logging helper
# -----------------------------
def log(msg: str):
    rid = get_request_id() or "no-request"
    logger.info(f"[req={rid}] {msg}")


@router.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    log(f"Received file upload: {file.filename}")
    start_total = time.time()

    try:
        content = await file.read()
        log(f"File size: {len(content)} bytes")

        with open("temp.pdf", "wb") as f:
            f.write(content)

        import PyPDF2

        # ---------------- PDF parsing ----------------
        t0 = time.time()
        reader = PyPDF2.PdfReader("temp.pdf")

        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text() or ""
            text += page_text
            log(f"Extracted text from page {i}")

        log(f"PDF parsing took {time.time() - t0:.2f}s")
        log(f"Total extracted text length: {len(text)}")

        # ---------------- Chunking ----------------
        t1 = time.time()
        pdf_chunks = split_text(text)
        log(f"Split into {len(pdf_chunks)} chunks")
        log(f"Chunking took {time.time() - t1:.2f}s")

        # ---------------- Embeddings ----------------
        t2 = time.time()
        pdf_embeddings = embeddings.embed_documents(pdf_chunks)
        log("Embeddings generated successfully")
        log(f"Embedding generation took {time.time() - t2:.2f}s")

        # ---------------- Vector DB ----------------
        t3 = time.time()
        doc_id = str(uuid.uuid4())
        ids = [f"{doc_id}_{i}" for i in range(len(pdf_chunks))]

        add_documents(pdf_chunks, pdf_embeddings, ids, doc_id)

        log(f"Stored {len(pdf_chunks)} chunks in vector DB with doc_id={doc_id}")
        log(f"Vector DB insert took {time.time() - t3:.2f}s")

        log(f"Total upload time: {time.time() - start_total:.2f}s")

        return {
            "chunks": len(pdf_chunks),
            "message": "Stored in vector DB successfully"
        }

    except Exception as e:
        logger.error(f"[req={get_request_id()}] Error in upload_pdf", exc_info=True)
        return {"error": str(e)}


@router.get("/ask-pdf/")
def ask_pdf(question: str):
    log(f"Received question: {question}")
    start_total = time.time()

    try:
        # ---------------- Query embedding ----------------
        t0 = time.time()
        q_emb = embeddings.embed_query(question)
        log("Query embedding generated")
        log(f"Query embedding took {time.time() - t0:.2f}s")

        # ---------------- Vector search ----------------
        t1 = time.time()
        top_chunks = search(q_emb, top_k=3)
        log(f"Retrieved {len(top_chunks)} chunks from vector DB")
        log(f"Vector search took {time.time() - t1:.2f}s")

        if not top_chunks:
            log("No chunks found in vector DB")
            return {"error": "No data found. Upload PDF first."}

        context = "\n".join(top_chunks)
        log(f"Context length: {len(context)}")

        # ---------------- LLM call ----------------
        t2 = time.time()
        answer = ask_llm(context, question)
        log("LLM response generated successfully")
        log(f"LLM call took {time.time() - t2:.2f}s")

        log(f"Total query time: {time.time() - start_total:.2f}s")

        return {"answer": answer}

    except Exception as e:
        logger.error(f"[req={get_request_id()}] Error in ask_pdf", exc_info=True)
        return {"error": str(e)}
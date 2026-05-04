import logging
import uuid
import time

from fastapi import APIRouter, UploadFile, File
from app.services.vector_db import collection
from app.core.request_context import get_request_id
from app.services.ai_service import ask_llm
from app.services.embedding_service import split_text, get_embeddings
from app.services.vector_db import add_documents, search
from app.services.embedding_service import embed_documents_with_cache

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
            text += f"\n\n--- Page {i+1} ---\n\n"
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
        pdf_embeddings = embed_documents_with_cache(embeddings, pdf_chunks)
        log("Embeddings generated successfully")
        log(f"Embedding cache hit improved performance")
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
                "doc_id": doc_id,
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
        # ---------------- Query preprocessing ----------------
        is_summary = "summary" in question.lower()

        # Improve query for summarization
        if is_summary:
            question = "Summarize the entire document in a structured way including skills, experience, education, and key highlights."

        # ---------------- Query embedding ----------------
        t0 = time.time()
        q_emb = embeddings.embed_query(question)
        log(f"Query embedding took {time.time() - t0:.2f}s")

        # ---------------- Vector search ----------------
        t1 = time.time()
        documents, distances = search(q_emb, top_k=5)

        log(f"Retrieved {len(documents)} raw chunks")
        log(f"Vector search took {time.time() - t1:.2f}s")

        # ---------------- Safety check ----------------
        if not documents:
            log("No chunks returned from vector DB")
            return {
                "answer": "No data found. Please upload a PDF first."
            }

        # ---------------- Ranking (NO FILTERING) ----------------
        scored_chunks = []

        for doc, dist in zip(documents, distances):
            if not isinstance(dist, (int, float)):
                continue
            scored_chunks.append((doc, dist))

        # lower distance = better match
        scored_chunks.sort(key=lambda x: x[1])

        # ---------------- Adaptive chunk selection ----------------
        if is_summary:
            # summary → broader context
            top_chunks = [chunk for chunk, _ in scored_chunks[:8]]
        else:
            # normal Q&A → precise context
            top_chunks = [chunk for chunk, _ in scored_chunks[:4]]

        log(f"Top chunks selected: {len(top_chunks)}")

        # ---------------- Context compression ----------------
        context = "\n\n".join(
            f"[Chunk {i+1}] {chunk}"
            for i, chunk in enumerate(top_chunks)
        )

        log(f"Context length: {len(context)}")

        # ---------------- LLM call ----------------
        t2 = time.time()
        answer = ask_llm(context, question)
        log(f"LLM call took {time.time() - t2:.2f}s")

        log(f"Total query time: {time.time() - start_total:.2f}s")

        return {
            "answer": answer,
            "chunks_used": len(top_chunks)
        }

    except Exception as e:
        logger.error("Error in ask_pdf", exc_info=True)
        return {"error": str(e)}
    
@router.get("/documents")
def list_documents():
    try:
        results = collection.get()
        metadatas = results.get("metadatas", [])

        doc_ids = list({
            meta["doc_id"]
            for meta in metadatas
            if meta and "doc_id" in meta
        })

        return {"documents": doc_ids}

    except Exception:
        logger.error("Error listing documents", exc_info=True)
        return {"documents": []}

@router.delete("/documents/{doc_id}")
def delete_document(doc_id: str):
    result = collection.get(where={"doc_id": doc_id})

    if not result.get("ids"):
        return {"message": "not found"}

    collection.delete(where={"doc_id": doc_id})
    return {"message": "deleted"}
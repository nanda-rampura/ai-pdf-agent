import logging
import chromadb
import os

logger = logging.getLogger(__name__)

DB_PATH = os.getenv("CHROMA_DB_PATH", "./chroma_db")
os.makedirs(DB_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=DB_PATH)
logger.info("ChromaDB persistent client initialized")
collection = client.get_or_create_collection(
    name="pdf_chunks",
    embedding_function=None   
)
logger.info("ChromaDB collection 'pdf_chunks' ready")


def add_documents(chunks, embeddings, ids, doc_id):
    if not chunks:
        logger.warning("No chunks provided to add_documents")
        return

    try:
        collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=[{"doc_id": doc_id, "chunk_index": i} for i in range(len(chunks))]
    )
        logger.info(f"Added {len(chunks)} documents to vector DB")

    except Exception as e:
        logger.error("Error adding documents to vector DB", exc_info=True)
        raise

def search(query_embedding, top_k=5):
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        documents = results.get("documents", [])
        distances = results.get("distances", [])

        # ALWAYS flatten safely
        documents = documents[0] if documents else []
        distances = distances[0] if distances else []

        # FINAL SAFETY CHECK
        if not isinstance(documents, list):
            documents = []

        if not isinstance(distances, list):
            distances = []

        logger.info(f"Search returned {len(documents)} results")

        return documents, distances   # 👈 IMPORTANT CHANGE

    except Exception:
        logger.error("Error during vector DB search", exc_info=True)
        return [], []
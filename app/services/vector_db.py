import logging
import chromadb

logger = logging.getLogger(__name__)

# In-memory client (safe for Render)
client = chromadb.Client()
logger.info("ChromaDB in-memory client initialized")

collection = client.get_or_create_collection(
    name="pdf_chunks"
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
        metadatas=[{"doc_id": doc_id} for _ in chunks]
    )
        logger.info(f"Added {len(chunks)} documents to vector DB")

    except Exception as e:
        logger.error("Error adding documents to vector DB", exc_info=True)
        raise


def search(query_embedding, top_k=3):
    try:
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        docs = results.get("documents", [[]])[0]
        logger.info(f"Search returned {len(docs)} results (top_k={top_k})")

        return docs

    except Exception as e:
        logger.error("Error during vector DB search", exc_info=True)
        return []
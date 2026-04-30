import logging
import numpy as np
import hashlib
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.config import OPENAI_API_KEY

logger = logging.getLogger(__name__)

# -----------------------------
# Simple in-memory cache
# -----------------------------
embedding_cache = {}


def get_hash(text: str) -> str:
    """Create stable hash for caching embeddings."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


# -----------------------------
# Embeddings client
# -----------------------------
def get_embeddings():
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY is missing")
        raise ValueError("Missing OpenAI API key")

    logger.info("Initializing OpenAI Embeddings client")
    return OpenAIEmbeddings(api_key=OPENAI_API_KEY)


# -----------------------------
# Chunking (improved)
# -----------------------------
def split_text(text: str):
    if not text:
        logger.warning("Received empty text for splitting")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    chunks = splitter.split_text(text)
    logger.info(f"Text split into {len(chunks)} chunks")

    return chunks


# -----------------------------
# Cached embedding generator (NEW)
# -----------------------------
def embed_documents_with_cache(embeddings_model, chunks: list[str]):
    """
    Embeds documents with caching to avoid recomputation.
    """
    if not chunks:
        return []

    final_embeddings = []
    uncached_chunks = []
    uncached_indexes = []

    # Step 1: check cache
    for i, chunk in enumerate(chunks):
        h = get_hash(chunk)

        if h in embedding_cache:
            final_embeddings.append(embedding_cache[h])
        else:
            final_embeddings.append(None)
            uncached_chunks.append(chunk)
            uncached_indexes.append(i)

    # Step 2: compute missing embeddings in batch
    if uncached_chunks:
        logger.info(f"Generating embeddings for {len(uncached_chunks)} new chunks")

        new_embeddings = embeddings_model.embed_documents(uncached_chunks)

        for idx, emb, chunk in zip(uncached_indexes, new_embeddings, uncached_chunks):
            final_embeddings[idx] = emb
            embedding_cache[get_hash(chunk)] = emb

    logger.info("Embedding generation (with cache) completed")
    return final_embeddings

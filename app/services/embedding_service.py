import logging
import numpy as np
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.core.config import OPENAI_API_KEY

logger = logging.getLogger(__name__)


def get_embeddings():
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY is missing")
        raise ValueError("Missing OpenAI API key")

    logger.info("Initializing OpenAI Embeddings client")
    return OpenAIEmbeddings(api_key=OPENAI_API_KEY)


def split_text(text: str):
    if not text:
        logger.warning("Received empty text for splitting")
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)
    logger.info(f"Text split into {len(chunks)} chunks")

    return chunks


def cosine_similarity(a, b):
    denom = np.linalg.norm(a) * np.linalg.norm(b)

    if denom == 0:
        logger.warning("Zero vector encountered in cosine similarity")
        return 0

    return np.dot(a, b) / denom
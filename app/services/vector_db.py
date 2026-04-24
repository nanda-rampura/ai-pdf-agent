import chromadb

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="pdf_chunks"
)


def add_documents(chunks, embeddings, ids):
    collection.add(
    documents=chunks,
    embeddings=embeddings,
    ids=ids,
    metadatas=[{"doc_id": "xyz"} for _ in chunks]
)

def search(query_embedding, top_k=3):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]
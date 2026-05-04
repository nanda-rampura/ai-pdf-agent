print("TEST STARTED")

from app.services.vector_db import add_documents, search

print("IMPORTS OK")

chunks = ["hello", "world", "test"]
embeddings = [[0.1, 0.2, 0.3]] * 3
ids = ["1", "2", "3"]

print("ADDING DOCS")
add_documents(chunks, embeddings, ids, "test_doc")

print("SEARCHING")
docs, dist = search([0.1, 0.2, 0.3])

print("RESULTS:", docs, dist)
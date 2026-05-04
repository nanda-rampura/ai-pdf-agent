import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.vector_db import collection


@pytest.fixture
def client():
    return TestClient(app)


def seed_document(doc_id="test-doc-123"):
    collection.add(
        documents=["This is a test chunk"],
        embeddings=[[0.1] * 1536],
        ids=[f"{doc_id}_0"],
        metadatas=[{"doc_id": doc_id}]
    )
    return doc_id


def test_delete_document_success(client):
    doc_id = seed_document()

    before = collection.get(where={"doc_id": {"$eq": doc_id}})
    assert len(before.get("ids", [])) > 0

    response = client.delete(f"/documents/{doc_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "deleted"

    after = collection.get(where={"doc_id": {"$eq": doc_id}})
    assert len(after.get("ids", [])) == 0


def test_delete_document_not_found(client):
    doc_id = "non-existent-doc-999"

    response = client.delete(f"/documents/{doc_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "not found"
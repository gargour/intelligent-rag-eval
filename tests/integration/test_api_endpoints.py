from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_list_documents_empty_or_ok():
    response = client.get("/documents/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
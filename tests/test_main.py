from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_list_payload():
    response = client.post("/payloads", json={"id": 1, "content": "hello"})
    assert response.status_code == 200
    assert response.json()["content"] == "hello"

    response = client.get("/payloads")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == 1

def test_get_payload():
    client.post("/payloads", json={"id": 2, "content": "world"})
    response = client.get("/payloads/2")
    assert response.status_code == 200
    assert response.json()["content"] == "world"

def test_get_nonexistent_payload():
    response = client.get("/payloads/999")
    assert response.status_code == 200
    assert "error" in response.json()

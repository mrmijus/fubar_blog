from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"message": "HEALTH OK"}

from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from main import app
from service import AuthServiceInterface, AuthService, get_auth_service


class MockAuthService(AuthServiceInterface):
    def authenticate_user(self, email: str, password: str) -> bool:
        return True


client = TestClient(app)

def override_dependency():
    return MockAuthService()


app.dependency_overrides[get_auth_service] = override_dependency


def test_login():
    payload = {"email": "test@example.com", "password": "password"}
    response = client.post("/v1/login", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}


def test_root_endpoint():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"message": "HEALTH OK"}


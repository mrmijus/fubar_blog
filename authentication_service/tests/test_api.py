from fastapi.testclient import TestClient
from main import app
from service import AuthServiceInterface, AuthService, get_auth_service


class MockAuthService(AuthServiceInterface):
    def authenticate_user(self, email: str, password: str) -> bool:
        if email == "test@example.com" and password == "password":
            return True
        return False


client = TestClient(app)


def override_dependency():
    """Override the get_auth_service dependency with a mock instance of AuthServiceInterface"""
    return MockAuthService()


app.dependency_overrides[get_auth_service] = override_dependency


def test_login_successful():
    payload = {"email": "test@example.com", "password": "password"}
    response = client.post("/v1/login", json=payload)
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}


def test_login_unsuccessful():
    payload = {"email": "invalid@mail.com", "password": "password"}
    response = client.post("/v1/login", json=payload)
    assert response.status_code == 401
    assert response.json() == {"message": "Incorrect email or password"}


def test_root_endpoint():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"message": "HEALTH OK"}

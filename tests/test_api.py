import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200

def test_register_endpoint_exists():
    response = client.post(
        "/api/users/register",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code in [200, 400, 422, 500]

def test_login_endpoint_exists():
    response = client.post(
        "/api/users/login",
        json={"email": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code in [200, 401, 422, 500]

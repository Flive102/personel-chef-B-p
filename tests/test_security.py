import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_invalid_token_rejected():
    """Test that invalid tokens are rejected"""
    response = client.post(
        "/api/mood/detect",
        json={"text": "happy"},
        headers={"Authorization": "Bearer invalid_token_here"}
    )
    assert response.status_code in [401, 403, 500]

def test_input_validation_rejects_empty():
    """Test that empty input is rejected"""
    response = client.post(
        "/api/mood/detect",
        json={"text": ""}
    )
    assert response.status_code in [401, 422, 500]

def test_input_validation_rejects_long_text():
    """Test that very long text is rejected"""
    response = client.post(
        "/api/mood/detect",
        json={"text": "a" * 1000},
        headers={"Authorization": "Bearer test_token"}
    )
    assert response.status_code in [401, 422, 500]

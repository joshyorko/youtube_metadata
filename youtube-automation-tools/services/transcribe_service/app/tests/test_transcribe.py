import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def token():
    response = client.post("/auth/token", data={"username": "johndoe", "password": "secret"})
    return response.json()["access_token"]

def test_transcribe_endpoint_with_valid_token(token):
    response = client.post("/transcribe", headers={"Authorization": f"Bearer {token}"}, files={"file": ("test.mp3", b"dummy content")})
    assert response.status_code == 200
    assert "segments" in response.json()
    assert "info" in response.json()

def test_transcribe_endpoint_without_token():
    response = client.post("/transcribe", files={"file": ("test.mp3", b"dummy content")})
    assert response.status_code == 401

def test_transcribe_endpoint_with_invalid_token():
    response = client.post("/transcribe", headers={"Authorization": "Bearer invalidtoken"}, files={"file": ("test.mp3", b"dummy content")})
    assert response.status_code == 401

def test_transcribe_endpoint_with_expired_token(monkeypatch):
    def mock_decode_token(token, secret, algorithms):
        raise jwt.ExpiredSignatureError
    monkeypatch.setattr(jwt, "decode", mock_decode_token)
    response = client.post("/transcribe", headers={"Authorization": "Bearer expiredtoken"}, files={"file": ("test.mp3", b"dummy content")})
    assert response.status_code == 401

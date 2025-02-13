import os
import pytest
from fastapi.testclient import TestClient
from jose import jwt
from main import app
from auth import SECRET_KEY, ALGORITHM

client = TestClient(app)

@pytest.fixture
def token():
    response = client.post("/auth/token", data={"username": "johndoe", "password": "secret"})
    return response.json()["access_token"]

def test_token_generation():
    response = client.post("/auth/token", data={"username": "johndoe", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_token_verification(token):
    response = client.get("/transcribe", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200

def test_invalid_token():
    response = client.get("/transcribe", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401

def test_expired_token(monkeypatch):
    def mock_decode_token(token, secret, algorithms):
        raise jwt.ExpiredSignatureError
    monkeypatch.setattr(jwt, "decode", mock_decode_token)
    response = client.get("/transcribe", headers={"Authorization": "Bearer expiredtoken"})
    assert response.status_code == 401

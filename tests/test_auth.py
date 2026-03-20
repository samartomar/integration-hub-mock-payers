"""Auth required tests."""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_no_auth_required():
    """Health endpoint does not require auth."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_health_head_matches_get():
    """HEAD on /health and /healthz is allowed like GET (empty body per HTTP)."""
    for path in ("/health", "/healthz"):
        r_head = client.head(path)
        r_get = client.get(path)
        assert r_head.status_code == 200
        assert r_get.status_code == 200
        assert r_head.content == b""
        assert r_get.json()["status"] == "ok"


def test_api_requires_bearer_token():
    """API endpoints require Bearer token."""
    r = client.post("/api/get-verify-member-eligibility", json={})
    assert r.status_code == 401
    data = r.json()
    assert data["success"] is False
    assert data["error"]["code"] == "AUTH_401"


def test_api_rejects_empty_bearer_token():
    """API rejects empty Bearer token."""
    r = client.post(
        "/api/get-verify-member-eligibility",
        json={"memberIdWithPrefix": "MEM001", "date": "2025-01-15"},
        headers={"Authorization": "Bearer "},
    )
    assert r.status_code == 401


def test_api_rejects_missing_authorization_header():
    """API rejects missing Authorization header."""
    r = client.post(
        "/api/get-verify-member-eligibility",
        json={"memberIdWithPrefix": "MEM001", "date": "2025-01-15"},
    )
    assert r.status_code == 401


def test_api_accepts_valid_bearer_token():
    """API accepts any non-empty Bearer token."""
    r = client.post(
        "/api/get-verify-member-eligibility",
        json={"memberIdWithPrefix": "LH001-MEM001", "date": "2025-01-15"},
        headers={"Authorization": "Bearer any-non-empty-token"},
    )
    assert r.status_code == 200

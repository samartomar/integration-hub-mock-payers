"""Eligibility route tests."""
import pytest

AUTH_HEADERS = {"Authorization": "Bearer mock-token"}


def test_get_verify_member_eligibility_happy_path(client):
    """Happy path: active member."""
    r = client.post(
        "/api/get-verify-member-eligibility",
        json={"memberIdWithPrefix": "LH001-MEM001", "date": "2025-01-15"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    data = r.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ACTIVE"
    assert data["data"]["memberIdWithPrefix"] == "LH001-MEM001"
    assert "meta" in data
    assert "270/271" in data["meta"]["x12TransactionIntent"]


def test_get_verify_member_eligibility_member_not_found(client):
    """Member not found returns 404."""
    r = client.post(
        "/api/get-verify-member-eligibility",
        json={"memberIdWithPrefix": "MEM999", "date": "2025-01-15"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "MEMBER_404"


def test_get_service_benefits_happy_path(client):
    """Happy path: service benefits."""
    r = client.post(
        "/api/get-service-benefits",
        json={"memberIdWithPrefix": "LH001-MEM001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["success"] is True


def test_get_member_accumulators_happy_path(client):
    """Happy path: accumulators."""
    r = client.post(
        "/api/get-member-accumulators",
        json={"memberIdWithPrefix": "LH001-MEM001", "date": "2025-06-01"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert "accumulators" in r.json()["data"]


def test_get_cob_inquiry_happy_path(client):
    """Happy path: COB inquiry."""
    r = client.post(
        "/api/get-cob-inquiry",
        json={"memberIdWithPrefix": "LH001-MEM001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "PRIMARY"


def test_get_referral_requirement_happy_path(client):
    """Happy path: referral requirement."""
    r = client.post(
        "/api/get-referral-requirement",
        json={"memberIdWithPrefix": "LH001-MEM001", "procedureCode": "99213"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert "data" in r.json()

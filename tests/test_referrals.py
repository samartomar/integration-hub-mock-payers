"""Referral route tests (get-referral-requirement is in eligibility)."""
AUTH_HEADERS = {"Authorization": "Bearer mock-token"}


def test_get_referral_requirement_member_not_found(client):
    """Member not found for referral requirement."""
    r = client.post(
        "/api/get-referral-requirement",
        json={"memberIdWithPrefix": "MEM999", "procedureCode": "99213"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 404

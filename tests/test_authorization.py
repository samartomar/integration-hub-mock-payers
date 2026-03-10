"""Prior authorization route tests."""
AUTH_HEADERS = {"Authorization": "Bearer mock-token"}


def test_get_prior_auth_requirement_happy_path(client):
    """Happy path: prior auth requirement."""
    r = client.post(
        "/api/get-prior-auth-requirement",
        json={"memberIdWithPrefix": "LH001-MEM001", "procedureCode": "99285"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["success"] is True


def test_get_prior_auth_requirement_member_not_found(client):
    """Member not found."""
    r = client.post(
        "/api/get-prior-auth-requirement",
        json={"memberIdWithPrefix": "MEM999", "procedureCode": "99285"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 404


def test_submit_prior_auth_request_happy_path(client):
    """Happy path: submit prior auth."""
    r = client.post(
        "/api/submit-prior-auth-request",
        json={
            "memberIdWithPrefix": "LH001-MEM001",
            "providerNpi": "1234567890",
            "procedureCode": "99285",
            "diagnosisCode": "R07.9",
            "serviceDate": "2025-01-15",
        },
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert "authorizationId" in r.json()["data"]


def test_get_prior_auth_status_happy_path(client):
    """Happy path: get prior auth status."""
    r = client.post(
        "/api/get-prior-auth-status",
        json={"authorizationId": "AUTH001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "APPROVED"


def test_get_prior_auth_status_not_found(client):
    """Prior auth not found."""
    r = client.post(
        "/api/get-prior-auth-status",
        json={"authorizationId": "AUTH999"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "AUTHZ_404"


def test_get_prior_auth_pend_status(client):
    """Pend status for pended auth."""
    r = client.post(
        "/api/get-prior-auth-pend-status",
        json={"authorizationId": "AUTH003"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "PENDED"


def test_upload_supporting_document(client):
    """Upload document reference."""
    r = client.post(
        "/api/upload-supporting-document-reference",
        json={
            "authorizationId": "AUTH001",
            "documentUrl": "https://example.com/doc.pdf",
            "documentType": "CLINICAL_NOTE",
        },
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200

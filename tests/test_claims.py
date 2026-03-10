"""Claims route tests."""
AUTH_HEADERS = {"Authorization": "Bearer mock-token"}


def test_submit_claim_happy_path(client):
    """Happy path: submit claim."""
    r = client.post(
        "/api/submit-claim",
        json={
            "memberIdWithPrefix": "LH001-MEM001",
            "providerNpi": "1234567890",
            "facilityId": "FAC001",
            "serviceDate": "2025-01-15",
            "diagnosisCode": "J06.9",
            "procedureCode": "99285",
            "placeOfService": "21",
            "billedAmount": 450.00,
        },
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert "claimId" in r.json()["data"]


def test_get_claim_acknowledgment_happy_path(client):
    """Happy path: claim acknowledgment."""
    r = client.post(
        "/api/get-claim-acknowledgment",
        json={"claimId": "CLM001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["data"]["ackStatus"] == "ACCEPTED"


def test_get_claim_acknowledgment_not_found(client):
    """Claim not found."""
    r = client.post(
        "/api/get-claim-acknowledgment",
        json={"claimId": "CLM999"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 404


def test_get_claim_status_happy_path(client):
    """Happy path: claim status."""
    r = client.post(
        "/api/get-claim-status",
        json={"claimId": "CLM001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "PAID"


def test_get_claim_denial_details(client):
    """Denial details for denied claim."""
    r = client.post(
        "/api/get-claim-denial-details",
        json={"claimId": "CLM003"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["data"]["denialCode"] == "CO_97"


def test_get_eob_by_claim_id(client):
    """Get EOB by claim ID."""
    r = client.post(
        "/api/get-eob",
        json={"claimId": "CLM001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["data"]["claimId"] == "CLM001"


def test_get_eob_by_member(client):
    """Get EOB by member."""
    r = client.post(
        "/api/get-eob",
        json={"memberIdWithPrefix": "LH001-MEM001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert "eobs" in r.json()["data"]


def test_get_remittance_happy_path(client):
    """Happy path: remittance."""
    r = client.post(
        "/api/get-remittance",
        json={"claimId": "CLM001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200


def test_submit_corrected_claim(client):
    """Submit corrected claim."""
    r = client.post(
        "/api/submit-corrected-claim",
        json={
            "originalClaimId": "CLM001",
            "memberIdWithPrefix": "LH001-MEM001",
            "providerNpi": "1234567890",
            "facilityId": "FAC001",
            "serviceDate": "2025-01-15",
            "diagnosisCode": "J06.9",
            "procedureCode": "99285",
            "placeOfService": "21",
            "billedAmount": 450.00,
        },
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200


def test_get_eob_validation_error(client):
    """Get EOB requires claimId or memberIdWithPrefix."""
    r = client.post(
        "/api/get-eob",
        json={},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 400
    assert r.json()["error"]["code"] == "VALIDATION_400"


def test_get_medical_records_request_status(client):
    """Medical records request status."""
    r = client.post(
        "/api/get-medical-records-request-status",
        json={"requestId": "REC001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["data"]["status"] == "COMPLETED"

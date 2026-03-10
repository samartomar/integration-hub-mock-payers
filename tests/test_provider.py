"""Provider/network route tests."""
AUTH_HEADERS = {"Authorization": "Bearer mock-token"}


def test_get_provider_contract_status_happy_path(client):
    """Happy path: provider contract status."""
    r = client.post(
        "/api/get-provider-contract-status",
        json={"providerNpi": "1234567890", "memberIdWithPrefix": "LH001-MEM001"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    assert r.json()["data"]["networkStatus"] == "IN_NETWORK"


def test_get_provider_contract_status_provider_not_found(client):
    """Provider not found."""
    r = client.post(
        "/api/get-provider-contract-status",
        json={"providerNpi": "9999999999"},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "PROVIDER_404"


def test_get_network_directory_happy_path(client):
    """Happy path: network directory."""
    r = client.post(
        "/api/get-network-directory",
        json={},
        headers=AUTH_HEADERS,
    )
    assert r.status_code == 200
    data = r.json()
    assert "practitionerRoles" in data["data"]
    assert "organizations" in data["data"]

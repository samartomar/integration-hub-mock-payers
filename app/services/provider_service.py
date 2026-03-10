"""Provider/network service. FHIR Plan-Net."""
from app.services.fixture_loader import (
    get_member_by_id,
    get_provider_by_npi,
    load_fixture,
)


def get_provider_contract_status(
    provider_npi: str,
    member_id_with_prefix: str | None,
    tax_id: str | None,
) -> tuple[dict | None, str]:
    """Return provider contract/network status. None if provider not found."""
    provider = get_provider_by_npi(provider_npi)
    if not provider:
        return None, "provider_not_found"
    if member_id_with_prefix:
        member = get_member_by_id(member_id_with_prefix)
        if not member:
            return None, "member_not_found"
    return {
        "providerNpi": provider_npi,
        "taxId": provider.get("taxId"),
        "name": f"{provider.get('firstName', '')} {provider.get('lastName', '')}".strip(),
        "specialty": provider.get("specialty"),
        "networkStatus": provider.get("networkStatus"),
        "deliveryMethod": "EDI",
    }, "happy_path"


def get_network_directory(
    tax_id: str | None,
    network_id: str | None,
    specialty: str | None,
    zip_code: str | None,
    limit: int,
) -> tuple[dict, str]:
    """Return network directory (providers, facilities). Always returns data."""
    providers = load_fixture("providers")
    facilities = load_fixture("facilities")
    if tax_id:
        providers = [p for p in providers if p.get("taxId") == tax_id]
    if specialty:
        providers = [p for p in providers if p.get("specialty") == specialty]
    providers = providers[:limit]
    return {
        "practitionerRoles": [
            {
                "providerNpi": p.get("providerNpi"),
                "taxId": p.get("taxId"),
                "name": f"{p.get('firstName', '')} {p.get('lastName', '')}".strip(),
                "specialty": p.get("specialty"),
                "networkStatus": p.get("networkStatus"),
            }
            for p in providers
        ],
        "organizations": [
            {
                "facilityId": f.get("facilityId"),
                "name": f.get("name"),
                "npi": f.get("npi"),
                "placeOfService": f.get("placeOfService"),
                "address": f"{f.get('address')}, {f.get('city')}, {f.get('state')} {f.get('zip')}",
            }
            for f in facilities
        ],
    }, "happy_path"

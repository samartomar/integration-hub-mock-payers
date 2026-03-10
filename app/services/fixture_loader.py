"""Load JSON fixtures from app/fixtures."""
import json
from pathlib import Path

FIXTURES_DIR = Path(__file__).resolve().parent.parent / "fixtures"
_fixture_cache: dict[str, list | dict] = {}


def load_fixture(name: str) -> list | dict:
    """Load a fixture by name (e.g., 'members', 'claims')."""
    if name in _fixture_cache:
        return _fixture_cache[name]
    path = FIXTURES_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(f"Fixture not found: {name}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    _fixture_cache[name] = data
    return data


def get_member_by_id(member_id_with_prefix: str) -> dict | None:
    """Find member by memberIdWithPrefix."""
    members = load_fixture("members")
    for m in members:
        if m.get("memberIdWithPrefix") == member_id_with_prefix:
            return m
    return None


def get_provider_by_npi(provider_npi: str) -> dict | None:
    """Find provider by NPI."""
    providers = load_fixture("providers")
    for p in providers:
        if p.get("providerNpi") == provider_npi:
            return p
    return None


def get_claim_by_id(claim_id: str) -> dict | None:
    """Find claim by claimId."""
    claims = load_fixture("claims")
    for c in claims:
        if c.get("claimId") == claim_id:
            return c
    return None


def get_authorization_by_id(auth_id: str) -> dict | None:
    """Find prior auth by authorizationId."""
    auths = load_fixture("authorizations")
    for a in auths:
        if a.get("authorizationId") == auth_id:
            return a
    return None


def get_referral_by_id(referral_id: str) -> dict | None:
    """Find referral by referralId."""
    referrals = load_fixture("referrals")
    for r in referrals:
        if r.get("referralId") == referral_id:
            return r
    return None


def get_remittance_by_claim_id(claim_id: str) -> dict | None:
    """Find remittance by claimId."""
    remittances = load_fixture("remittances")
    for r in remittances:
        if r.get("claimId") == claim_id:
            return r
    return None


def get_records_request_by_id(request_id: str) -> dict | None:
    """Find records request by requestId."""
    requests = load_fixture("records_requests")
    for r in requests:
        if r.get("requestId") == request_id:
            return r
    return None


def get_coverage_by_plan_id(plan_id: str) -> dict | None:
    """Find coverage by planId."""
    coverages = load_fixture("coverages")
    for c in coverages:
        if c.get("planId") == plan_id:
            return c
    return None

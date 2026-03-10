"""Eligibility service. X12 270/271, FHIR CoverageEligibilityRequest/Response."""
from app.services.fixture_loader import (
    get_coverage_by_plan_id,
    get_member_by_id,
    load_fixture,
)


def get_verify_member_eligibility(member_id_with_prefix: str, date: str) -> tuple[dict | None, str]:
    """Return eligibility data or None if not found. Scenario name as second value."""
    member = get_member_by_id(member_id_with_prefix)
    if not member:
        return None, "member_not_found"
    if member.get("status") == "INACTIVE":
        return {
            "memberIdWithPrefix": member_id_with_prefix,
            "name": f"{member.get('firstName', '')} {member.get('lastName', '')}".strip(),
            "dob": member.get("dob"),
            "status": "INACTIVE",
            "planId": member.get("planId"),
            "effectiveDate": None,
            "terminationDate": "2024-12-31",
        }, "inactive"
    coverage = get_coverage_by_plan_id(member.get("planId", "")) or {}
    return {
        "memberIdWithPrefix": member_id_with_prefix,
        "name": f"{member.get('firstName', '')} {member.get('lastName', '')}".strip(),
        "dob": member.get("dob"),
        "status": "ACTIVE",
        "planId": member.get("planId"),
        "planName": coverage.get("planName"),
        "coverageType": coverage.get("coverageType"),
        "effectiveDate": coverage.get("effectiveDate"),
        "terminationDate": coverage.get("terminationDate"),
    }, "happy_path"


def get_service_benefits(
    member_id_with_prefix: str,
    service_type_code: str | None,
    procedure_code: str | None,
    date: str | None,
) -> tuple[dict | None, str]:
    """Return service benefits or None if member not found."""
    member = get_member_by_id(member_id_with_prefix)
    if not member:
        return None, "member_not_found"
    coverage = get_coverage_by_plan_id(member.get("planId", "")) or {}
    return {
        "memberIdWithPrefix": member_id_with_prefix,
        "planName": coverage.get("planName"),
        "serviceTypeCode": service_type_code or "30",
        "procedureCode": procedure_code or "99213",
        "benefitAmount": 100.00,
        "copayAmount": 25.00,
        "coinsurancePercent": 20,
        "asOfDate": date or "2025-01-15",
    }, "happy_path"


def get_member_accumulators(member_id_with_prefix: str, date: str) -> tuple[dict | None, str]:
    """Return accumulators or None if member not found."""
    member = get_member_by_id(member_id_with_prefix)
    if not member:
        return None, "member_not_found"
    plan_year = date[:4] if date else "2025"
    return {
        "memberIdWithPrefix": member_id_with_prefix,
        "accumulators": [
            {"accumulatorType": "DEDUCTIBLE", "accumulatorValue": 500, "planYear": plan_year},
            {"accumulatorType": "OUT_OF_POCKET", "accumulatorValue": 200, "planYear": plan_year},
        ],
    }, "happy_path"


def get_cob_inquiry(member_id_with_prefix: str, service_date: str | None) -> tuple[dict | None, str]:
    """Return COB status or None if member not found."""
    member = get_member_by_id(member_id_with_prefix)
    if not member:
        return None, "member_not_found"
    return {
        "memberIdWithPrefix": member_id_with_prefix,
        "name": f"{member.get('firstName', '')} {member.get('lastName', '')}".strip(),
        "dob": member.get("dob"),
        "claimNumber": "CLM-123456",
        "dateOfService": service_date or "2025-01-15",
        "status": "PRIMARY",
    }, "happy_path"


def get_referral_requirement(
    member_id_with_prefix: str,
    procedure_code: str,
    place_of_service: str | None,
) -> tuple[dict | None, str]:
    """Return referral requirements or None if member not found."""
    member = get_member_by_id(member_id_with_prefix)
    if not member:
        return None, "member_not_found"
    return {
        "memberIdWithPrefix": member_id_with_prefix,
        "procedureCode": procedure_code,
        "placeOfService": place_of_service or "11",
        "referralRequired": procedure_code in ("99285", "29881", "93306", "70551"),
        "requirements": [
            {"type": "REFERRAL", "description": "Specialist referral required for this procedure"},
        ] if procedure_code in ("99285", "29881", "93306", "70551") else [],
    }, "happy_path"

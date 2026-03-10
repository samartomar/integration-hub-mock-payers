"""Prior authorization service. X12 278, FHIR Claim/ClaimResponse, Da Vinci PAS/CRD."""
import uuid
from app.services.fixture_loader import get_authorization_by_id, get_member_by_id, get_provider_by_npi


def get_prior_auth_requirement(
    member_id_with_prefix: str,
    procedure_code: str,
    place_of_service: str | None,
) -> tuple[dict | None, str]:
    """Return prior auth requirements or None if member not found."""
    member = get_member_by_id(member_id_with_prefix)
    if not member:
        return None, "member_not_found"
    required = procedure_code in ("99285", "29881", "93306", "70551")
    return {
        "memberIdWithPrefix": member_id_with_prefix,
        "procedureCode": procedure_code,
        "placeOfService": place_of_service or "21",
        "priorAuthRequired": required,
        "requirements": [
            {"type": "PRIOR_AUTH", "description": "Prior authorization required for this procedure"},
        ] if required else [],
    }, "happy_path"


def submit_prior_auth_request(
    member_id_with_prefix: str,
    provider_npi: str,
    procedure_code: str,
    diagnosis_code: str,
    service_date: str,
    place_of_service: str | None,
    facility_id: str | None,
) -> tuple[dict | None, str]:
    """Submit prior auth; return new authorizationId or None if member/provider not found."""
    member = get_member_by_id(member_id_with_prefix)
    if not member:
        return None, "member_not_found"
    provider = get_provider_by_npi(provider_npi)
    if not provider:
        return None, "provider_not_found"
    auth_id = f"AUTH-NEW-{uuid.uuid4().hex[:8].upper()}"
    return {
        "authorizationId": auth_id,
        "memberIdWithPrefix": member_id_with_prefix,
        "providerNpi": provider_npi,
        "procedureCode": procedure_code,
        "diagnosisCode": diagnosis_code,
        "serviceDate": service_date,
        "status": "PENDING",
        "message": "Prior authorization request submitted successfully",
    }, "happy_path"


def get_prior_auth_status(authorization_id: str) -> tuple[dict | None, str]:
    """Return prior auth status or None if not found."""
    auth = get_authorization_by_id(authorization_id)
    if not auth:
        return None, "authz_not_found"
    return {
        "authorizationId": authorization_id,
        "memberIdWithPrefix": auth.get("memberIdWithPrefix"),
        "providerNpi": auth.get("providerNpi"),
        "procedureCode": auth.get("procedureCode"),
        "serviceDate": auth.get("serviceDate"),
        "status": auth.get("status"),
        "effectiveDate": auth.get("effectiveDate"),
        "expirationDate": auth.get("expirationDate"),
        "unitsApproved": auth.get("unitsApproved"),
        "denialReason": auth.get("denialReason"),
    }, "happy_path"


def get_prior_auth_pend_status(authorization_id: str) -> tuple[dict | None, str]:
    """Return pend status details or None if not found."""
    auth = get_authorization_by_id(authorization_id)
    if not auth:
        return None, "authz_not_found"
    return {
        "authorizationId": authorization_id,
        "status": auth.get("status"),
        "pendReason": auth.get("pendReason"),
        "estimatedCompletionDate": auth.get("estimatedCompletionDate"),
        "message": auth.get("pendReason") or "Review in progress",
    }, "happy_path"


def upload_supporting_document(
    authorization_id: str | None,
    claim_id: str | None,
    document_url: str,
    document_type: str,
    description: str | None,
) -> tuple[dict | None, str]:
    """Upload document reference. If authorizationId provided, validate it exists."""
    if authorization_id:
        auth = get_authorization_by_id(authorization_id)
        if not auth:
            return None, "authz_not_found"
    return {
        "documentReferenceId": f"DOC-{uuid.uuid4().hex[:8].upper()}",
        "authorizationId": authorization_id,
        "claimId": claim_id,
        "documentUrl": document_url,
        "documentType": document_type,
        "description": description,
        "status": "RECEIVED",
    }, "happy_path"

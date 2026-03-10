"""Claims service. X12 837/276/277/835, FHIR Claim/ClaimResponse/ExplanationOfBenefit."""
import uuid
from app.services.fixture_loader import (
    get_claim_by_id,
    get_member_by_id,
    get_provider_by_npi,
    get_records_request_by_id,
    get_remittance_by_claim_id,
    load_fixture,
)


def submit_claim(
    member_id_with_prefix: str,
    provider_npi: str,
    facility_id: str,
    service_date: str,
    diagnosis_code: str,
    procedure_code: str,
    place_of_service: str,
    billed_amount: float,
) -> tuple[dict | None, str]:
    """Submit claim; return new claimId or None if validation fails."""
    member = get_member_by_id(member_id_with_prefix)
    if not member:
        return None, "member_not_found"
    provider = get_provider_by_npi(provider_npi)
    if not provider:
        return None, "provider_not_found"
    claim_id = f"CLM-{uuid.uuid4().hex[:8].upper()}"
    return {
        "claimId": claim_id,
        "memberIdWithPrefix": member_id_with_prefix,
        "providerNpi": provider_npi,
        "facilityId": facility_id,
        "serviceDate": service_date,
        "status": "ACCEPTED",
        "ackStatus": "ACCEPTED",
        "message": "Claim submitted successfully",
    }, "happy_path"


def get_claim_acknowledgment(claim_id: str) -> tuple[dict | None, str]:
    """Return claim acknowledgment or None if not found."""
    claim = get_claim_by_id(claim_id)
    if not claim:
        return None, "claim_not_found"
    return {
        "claimId": claim_id,
        "ackStatus": claim.get("ackStatus", "ACCEPTED"),
        "submissionDate": claim.get("submissionDate"),
        "message": "Claim accepted for processing" if claim.get("ackStatus") == "ACCEPTED" else "Claim rejected",
    }, "happy_path"


def get_claim_status(claim_id: str) -> tuple[dict | None, str]:
    """Return claim status or None if not found."""
    claim = get_claim_by_id(claim_id)
    if not claim:
        return None, "claim_not_found"
    return {
        "claimId": claim_id,
        "memberIdWithPrefix": claim.get("memberIdWithPrefix"),
        "status": claim.get("status"),
        "ackStatus": claim.get("ackStatus"),
        "serviceDate": claim.get("serviceDate"),
        "submissionDate": claim.get("submissionDate"),
        "billedAmount": claim.get("billedAmount"),
        "paidAmount": claim.get("paidAmount"),
    }, "happy_path"


def get_claim_denial_details(claim_id: str) -> tuple[dict | None, str]:
    """Return denial details or None if not found. For non-denied claims return empty details."""
    claim = get_claim_by_id(claim_id)
    if not claim:
        return None, "claim_not_found"
    return {
        "claimId": claim_id,
        "status": claim.get("status"),
        "denialCode": claim.get("denialCode"),
        "denialReason": claim.get("denialReason"),
        "adjustmentCodes": [{"code": "CO_97", "description": claim.get("denialReason", "N/A")}] if claim.get("denialCode") else [],
    }, "happy_path"


def get_eob(
    claim_id: str | None,
    member_id_with_prefix: str | None,
    service_date_from: str | None,
    service_date_to: str | None,
) -> tuple[dict | None, str]:
    """Return EOB by claimId or member. None if not found."""
    if claim_id:
        claim = get_claim_by_id(claim_id)
        if not claim:
            return None, "claim_not_found"
        rem = get_remittance_by_claim_id(claim_id)
        return {
            "claimId": claim_id,
            "memberIdWithPrefix": claim.get("memberIdWithPrefix"),
            "serviceDate": claim.get("serviceDate"),
            "procedureCode": claim.get("procedureCode"),
            "diagnosisCode": claim.get("diagnosisCode"),
            "billedAmount": claim.get("billedAmount"),
            "paidAmount": claim.get("paidAmount", 0),
            "patientResponsibility": (claim.get("billedAmount", 0) or 0) - (claim.get("paidAmount") or 0),
            "paymentDate": rem.get("paymentDate") if rem else None,
        }, "happy_path"
    if member_id_with_prefix:
        claims_data = load_fixture("claims")
        claims = [c for c in claims_data if c.get("memberIdWithPrefix") == member_id_with_prefix]
        eobs = []
        for c in claims[:5]:
            rem = get_remittance_by_claim_id(c.get("claimId", ""))
            eobs.append({
                "claimId": c.get("claimId"),
                "serviceDate": c.get("serviceDate"),
                "procedureCode": c.get("procedureCode"),
                "billedAmount": c.get("billedAmount"),
                "paidAmount": c.get("paidAmount"),
                "paymentDate": rem.get("paymentDate") if rem else None,
            })
        return {"memberIdWithPrefix": member_id_with_prefix, "eobs": eobs}, "happy_path"
    return None, "validation_error"


def get_remittance(claim_id: str) -> tuple[dict | None, str]:
    """Return remittance by claimId or None if not found."""
    claim = get_claim_by_id(claim_id)
    if not claim:
        return None, "claim_not_found"
    rem = get_remittance_by_claim_id(claim_id)
    if not rem:
        return {
            "claimId": claim_id,
            "memberIdWithPrefix": claim.get("memberIdWithPrefix"),
            "status": claim.get("status"),
            "paymentAmount": claim.get("paidAmount"),
            "message": "No payment record yet; claim may be in process",
        }, "happy_path"
    return {
        "claimId": claim_id,
        "remittanceId": rem.get("remittanceId"),
        "memberIdWithPrefix": rem.get("memberIdWithPrefix"),
        "paymentAmount": rem.get("paymentAmount"),
        "paymentDate": rem.get("paymentDate"),
        "checkNumber": rem.get("checkNumber"),
        "status": rem.get("status"),
        "adjustmentCodes": rem.get("adjustmentCodes", []),
    }, "happy_path"


def submit_corrected_claim(
    original_claim_id: str,
    member_id_with_prefix: str,
    provider_npi: str,
    facility_id: str,
    service_date: str,
    diagnosis_code: str,
    procedure_code: str,
    place_of_service: str,
    billed_amount: float,
    correction_type: str,
) -> tuple[dict | None, str]:
    """Submit corrected claim. Validate original exists."""
    orig = get_claim_by_id(original_claim_id)
    if not orig:
        return None, "claim_not_found"
    member = get_member_by_id(member_id_with_prefix)
    if not member:
        return None, "member_not_found"
    claim_id = f"CLM-CORR-{uuid.uuid4().hex[:8].upper()}"
    return {
        "claimId": claim_id,
        "originalClaimId": original_claim_id,
        "correctionType": correction_type,
        "status": "ACCEPTED",
        "message": "Corrected claim submitted successfully",
    }, "happy_path"


def get_medical_records_request_status(request_id: str) -> tuple[dict | None, str]:
    """Return medical records request status or None if not found."""
    rec = get_records_request_by_id(request_id)
    if not rec:
        return None, "record_request_not_found"
    return {
        "requestId": request_id,
        "memberIdWithPrefix": rec.get("memberIdWithPrefix"),
        "claimId": rec.get("claimId"),
        "status": rec.get("status"),
        "requestedDate": rec.get("requestedDate"),
        "completedDate": rec.get("completedDate"),
        "estimatedCompletionDate": rec.get("estimatedCompletionDate"),
        "notes": rec.get("notes"),
    }, "happy_path"

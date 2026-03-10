"""Claims routes. X12 837/276/277/835, FHIR Claim/ClaimResponse/ExplanationOfBenefit."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.core.auth import require_bearer
from app.core.errors import ErrorCode
from app.models.claims import (
    GetClaimAcknowledgmentRequest,
    GetClaimDenialDetailsRequest,
    GetClaimStatusRequest,
    GetEobRequest,
    GetMedicalRecordsRequestStatusRequest,
    GetRemittanceRequest,
    SubmitClaimRequest,
    SubmitCorrectedClaimRequest,
)
from app.routes.response_helpers import error_response, success_response
from app.services import claims_service

router = APIRouter(prefix="/api", tags=["Claims"])


def to_json(resp):
    return resp.model_dump(by_alias=True, exclude_none=True)


@router.post(
    "/submit-claim",
    summary="Submit claim",
    description="X12 837, FHIR Claim. Submit professional or institutional claim.",
)
async def submit_claim(
    request: Request,
    body: SubmitClaimRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = claims_service.submit_claim(
        body.member_id_with_prefix,
        body.provider_npi,
        body.facility_id,
        body.service_date,
        body.diagnosis_code,
        body.procedure_code,
        body.place_of_service,
        body.billed_amount,
    )
    if data is None:
        code = ErrorCode.MEMBER_404 if scenario == "member_not_found" else ErrorCode.PROVIDER_404
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "submit-claim",
                    "Member or provider not found",
                    code,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "submit-claim",
            "Claim submitted",
            data,
            scenario,
        )
    )


@router.post(
    "/get-claim-acknowledgment",
    summary="Get claim acknowledgment",
    description="X12 277. Retrieve claim submission acknowledgment.",
)
async def get_claim_acknowledgment(
    request: Request,
    body: GetClaimAcknowledgmentRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = claims_service.get_claim_acknowledgment(body.claim_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-claim-acknowledgment",
                    "Claim not found",
                    ErrorCode.CLAIM_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-claim-acknowledgment",
            "Claim acknowledgment retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/get-claim-status",
    summary="Get claim status",
    description="X12 276/277, FHIR ClaimResponse. Retrieve claim adjudication status.",
)
async def get_claim_status(
    request: Request,
    body: GetClaimStatusRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = claims_service.get_claim_status(body.claim_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-claim-status",
                    "Claim not found",
                    ErrorCode.CLAIM_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-claim-status",
            "Claim status retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/get-claim-denial-details",
    summary="Get claim denial details",
    description="X12 277, FHIR ClaimResponse. Retrieve denial reason and adjustment details.",
)
async def get_claim_denial_details(
    request: Request,
    body: GetClaimDenialDetailsRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = claims_service.get_claim_denial_details(body.claim_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-claim-denial-details",
                    "Claim not found",
                    ErrorCode.CLAIM_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-claim-denial-details",
            "Denial details retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/get-eob",
    summary="Get Explanation of Benefits",
    description="X12 835, FHIR ExplanationOfBenefit. Retrieve EOB.",
)
async def get_eob(
    request: Request,
    body: GetEobRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = claims_service.get_eob(
        body.claim_id,
        body.member_id_with_prefix,
        body.service_date_from,
        body.service_date_to,
    )
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-eob",
                    "Claim not found or validation error",
                    ErrorCode.CLAIM_404 if scenario == "claim_not_found" else ErrorCode.VALIDATION_400,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-eob",
            "EOB retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/get-remittance",
    summary="Get remittance advice",
    description="X12 835. Retrieve remittance/payment details.",
)
async def get_remittance(
    request: Request,
    body: GetRemittanceRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = claims_service.get_remittance(body.claim_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-remittance",
                    "Claim not found",
                    ErrorCode.CLAIM_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-remittance",
            "Remittance retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/submit-corrected-claim",
    summary="Submit corrected claim",
    description="X12 837 replacement, FHIR Claim. Submit corrected or replacement claim.",
)
async def submit_corrected_claim(
    request: Request,
    body: SubmitCorrectedClaimRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = claims_service.submit_corrected_claim(
        body.original_claim_id,
        body.member_id_with_prefix,
        body.provider_npi,
        body.facility_id,
        body.service_date,
        body.diagnosis_code,
        body.procedure_code,
        body.place_of_service,
        body.billed_amount,
        body.correction_type,
    )
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "submit-corrected-claim",
                    "Original claim not found",
                    ErrorCode.CLAIM_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "submit-corrected-claim",
            "Corrected claim submitted",
            data,
            scenario,
        )
    )


@router.post(
    "/get-medical-records-request-status",
    summary="Get medical records request status",
    description="X12 277/275, FHIR DocumentReference. Status of medical records request.",
)
async def get_medical_records_request_status(
    request: Request,
    body: GetMedicalRecordsRequestStatusRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = claims_service.get_medical_records_request_status(body.request_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-medical-records-request-status",
                    "Records request not found",
                    ErrorCode.RECORD_REQUEST_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-medical-records-request-status",
            "Records request status retrieved",
            data,
            scenario,
        )
    )

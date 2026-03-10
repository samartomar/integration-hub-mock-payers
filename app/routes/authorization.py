"""Prior authorization routes. X12 278, FHIR Claim/ClaimResponse, Da Vinci PAS/CRD."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.core.auth import require_bearer
from app.core.errors import ErrorCode
from app.models.authorization import (
    GetPriorAuthPendStatusRequest,
    GetPriorAuthRequirementRequest,
    GetPriorAuthStatusRequest,
    SubmitPriorAuthRequest,
    UploadSupportingDocumentRequest,
)
from app.routes.response_helpers import error_response, success_response
from app.services import authorization_service

router = APIRouter(prefix="/api", tags=["Prior Authorization"])


def to_json(resp):
    return resp.model_dump(by_alias=True, exclude_none=True)


@router.post(
    "/get-prior-auth-requirement",
    summary="Get prior auth requirements",
    description="X12 278, Da Vinci CRD. Discover prior authorization requirements.",
)
async def get_prior_auth_requirement(
    request: Request,
    body: GetPriorAuthRequirementRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = authorization_service.get_prior_auth_requirement(
        body.member_id_with_prefix,
        body.procedure_code,
        body.place_of_service,
    )
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-prior-auth-requirement",
                    "Member not found",
                    ErrorCode.MEMBER_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-prior-auth-requirement",
            "Prior auth requirements retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/submit-prior-auth-request",
    summary="Submit prior auth request",
    description="X12 278, Da Vinci PAS. Submit prior authorization request.",
)
async def submit_prior_auth_request(
    request: Request,
    body: SubmitPriorAuthRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = authorization_service.submit_prior_auth_request(
        body.member_id_with_prefix,
        body.provider_npi,
        body.procedure_code,
        body.diagnosis_code,
        body.service_date,
        body.place_of_service,
        body.facility_id,
    )
    if data is None:
        code = ErrorCode.MEMBER_404 if scenario == "member_not_found" else ErrorCode.PROVIDER_404
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "submit-prior-auth-request",
                    "Member or provider not found",
                    code,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "submit-prior-auth-request",
            "Prior auth request submitted",
            data,
            scenario,
        )
    )


@router.post(
    "/get-prior-auth-status",
    summary="Get prior auth status",
    description="X12 278, FHIR ClaimResponse. Retrieve prior auth status.",
)
async def get_prior_auth_status(
    request: Request,
    body: GetPriorAuthStatusRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = authorization_service.get_prior_auth_status(body.authorization_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-prior-auth-status",
                    "Prior authorization not found",
                    ErrorCode.AUTHZ_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-prior-auth-status",
            "Prior auth status retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/get-prior-auth-pend-status",
    summary="Get prior auth pend status",
    description="X12 278 pend follow-up, FHIR ClaimResponse. Pending review details.",
)
async def get_prior_auth_pend_status(
    request: Request,
    body: GetPriorAuthPendStatusRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = authorization_service.get_prior_auth_pend_status(body.authorization_id)
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-prior-auth-pend-status",
                    "Prior authorization not found",
                    ErrorCode.AUTHZ_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-prior-auth-pend-status",
            "Pend status retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/upload-supporting-document-reference",
    summary="Upload supporting document reference",
    description="X12 275, FHIR DocumentReference. Upload reference to supporting documentation.",
)
async def upload_supporting_document_reference(
    request: Request,
    body: UploadSupportingDocumentRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = authorization_service.upload_supporting_document(
        body.authorization_id,
        body.claim_id,
        body.document_url,
        body.document_type,
        body.description,
    )
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "upload-supporting-document-reference",
                    "Prior authorization not found",
                    ErrorCode.AUTHZ_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "upload-supporting-document-reference",
            "Document reference received",
            data,
            scenario,
        )
    )

"""Eligibility routes. X12 270/271, FHIR CoverageEligibilityRequest/Response."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.core.auth import require_bearer
from app.core.errors import ErrorCode
from app.models.eligibility import (
    GetCobInquiryRequest,
    GetMemberAccumulatorsRequest,
    GetReferralRequirementRequest,
    GetServiceBenefitsRequest,
    GetVerifyMemberEligibilityRequest,
)
from app.routes.response_helpers import error_response, success_response
from app.services import eligibility_service

router = APIRouter(prefix="/api", tags=["Eligibility"])


def to_json(resp):
    """Serialize response with camelCase aliases."""
    return resp.model_dump(by_alias=True, exclude_none=True)


@router.post(
    "/get-verify-member-eligibility",
    summary="Verify member eligibility",
    description="X12 270/271, FHIR CoverageEligibilityRequest/Response. Verify member eligibility for a given date.",
    responses={
        200: {"description": "Eligibility verified", "content": {"application/json": {"example": {"success": True, "data": {"memberIdWithPrefix": "LH001-MEM001", "status": "ACTIVE"}}}}},
        404: {"description": "Member not found"},
    },
)
async def get_verify_member_eligibility(
    request: Request,
    body: GetVerifyMemberEligibilityRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = eligibility_service.get_verify_member_eligibility(
        body.member_id_with_prefix, body.date
    )
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-verify-member-eligibility",
                    "Member not found",
                    ErrorCode.MEMBER_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-verify-member-eligibility",
            "Eligibility verified",
            data,
            scenario,
        )
    )


@router.post(
    "/get-service-benefits",
    summary="Get service-level benefits",
    description="X12 270/271, FHIR CoverageEligibilityRequest/Response. Retrieve service-level benefit information.",
)
async def get_service_benefits(
    request: Request,
    body: GetServiceBenefitsRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = eligibility_service.get_service_benefits(
        body.member_id_with_prefix,
        body.service_type_code,
        body.procedure_code,
        body.date,
    )
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-service-benefits",
                    "Member not found",
                    ErrorCode.MEMBER_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-service-benefits",
            "Service benefits retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/get-member-accumulators",
    summary="Get member accumulators",
    description="X12 270/271 benefit balances, FHIR CoverageEligibilityResponse. Deductible, OOP, etc.",
)
async def get_member_accumulators(
    request: Request,
    body: GetMemberAccumulatorsRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = eligibility_service.get_member_accumulators(
        body.member_id_with_prefix, body.date
    )
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-member-accumulators",
                    "Member not found",
                    ErrorCode.MEMBER_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-member-accumulators",
            "Accumulators retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/get-cob-inquiry",
    summary="Coordination of benefits inquiry",
    description="X12 270/271 COB, FHIR CoverageEligibilityResponse. Primary/secondary determination.",
)
async def get_cob_inquiry(
    request: Request,
    body: GetCobInquiryRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = eligibility_service.get_cob_inquiry(
        body.member_id_with_prefix, body.service_date
    )
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-cob-inquiry",
                    "Member not found",
                    ErrorCode.MEMBER_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-cob-inquiry",
            "COB inquiry completed",
            data,
            scenario,
        )
    )


@router.post(
    "/get-referral-requirement",
    summary="Get referral requirements",
    description="X12 270/271, FHIR CRD. Discover referral requirements for a service.",
)
async def get_referral_requirement(
    request: Request,
    body: GetReferralRequirementRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = eligibility_service.get_referral_requirement(
        body.member_id_with_prefix,
        body.procedure_code,
        body.place_of_service,
    )
    if data is None:
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-referral-requirement",
                    "Member not found",
                    ErrorCode.MEMBER_404,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-referral-requirement",
            "Referral requirements retrieved",
            data,
            scenario,
        )
    )

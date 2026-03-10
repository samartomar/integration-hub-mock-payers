"""Provider/network routes. FHIR Plan-Net."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from app.core.auth import require_bearer
from app.core.errors import ErrorCode
from app.models.provider import GetNetworkDirectoryRequest, GetProviderContractStatusRequest
from app.routes.response_helpers import error_response, success_response
from app.services import provider_service

router = APIRouter(prefix="/api", tags=["Provider / Network"])


def to_json(resp):
    return resp.model_dump(by_alias=True, exclude_none=True)


@router.post(
    "/get-provider-contract-status",
    summary="Get provider contract status",
    description="FHIR Plan-Net OrganizationAffiliation/PractitionerRole. Check provider network participation.",
)
async def get_provider_contract_status(
    request: Request,
    body: GetProviderContractStatusRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = provider_service.get_provider_contract_status(
        body.provider_npi,
        body.member_id_with_prefix,
        body.tax_id,
    )
    if data is None:
        code = ErrorCode.PROVIDER_404 if scenario == "provider_not_found" else ErrorCode.MEMBER_404
        return JSONResponse(
            status_code=404,
            content=to_json(
                error_response(
                    "get-provider-contract-status",
                    "Provider or member not found",
                    code,
                    scenario,
                )
            ),
        )
    return to_json(
        success_response(
            "get-provider-contract-status",
            "Provider contract status retrieved",
            data,
            scenario,
        )
    )


@router.post(
    "/get-network-directory",
    summary="Get network directory",
    description="FHIR Plan-Net. PractitionerRole, Organization, Location. Retrieve network directory.",
)
async def get_network_directory(
    request: Request,
    body: GetNetworkDirectoryRequest,
    _token: str = Depends(require_bearer),
):
    data, scenario = provider_service.get_network_directory(
        body.tax_id,
        body.network_id,
        body.specialty,
        body.zip_code,
        body.limit,
    )
    return to_json(
        success_response(
            "get-network-directory",
            "Network directory retrieved",
            data,
            scenario,
        )
    )

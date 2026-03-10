"""Response wrapper for success and error responses."""
from typing import Any

from pydantic import BaseModel, Field

from app.core.errors import ErrorCode


class ResponseMeta(BaseModel):
    """Standards crosswalk metadata in every response."""

    x12_transaction_intent: str = Field(
        ...,
        description="Closest X12 transaction (e.g., 270/271, 276/277)",
        examples=["270/271"],
        alias="x12TransactionIntent",
    )
    fhir_alignment: list[str] = Field(
        default_factory=list,
        description="FHIR resources this API aligns to",
        examples=[["CoverageEligibilityRequest", "CoverageEligibilityResponse"]],
        alias="fhirAlignment",
    )
    davinci_alignment: list[str] = Field(
        default_factory=list,
        description="Da Vinci IG alignment if applicable",
        examples=[["CRD"]],
        alias="davinciAlignment",
    )
    mock_scenario: str = Field(
        ...,
        description="Fixture scenario that produced this response",
        examples=["happy_path", "member_not_found"],
        alias="mockScenario",
    )

    model_config = {"populate_by_name": True}


class SuccessResponse(BaseModel):
    """Standard success response wrapper."""

    success: bool = True
    message: str = Field(..., description="Human-readable message")
    trace_id: str = Field(..., description="Request trace ID", alias="traceId")
    meta: ResponseMeta
    data: dict[str, Any] | list[Any] | None = Field(default=None)

    model_config = {"populate_by_name": True, "json_schema_extra": {"example": {"success": True}}}


class ErrorDetail(BaseModel):
    """Error detail object."""

    code: str
    details: dict[str, Any] | None = None


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""

    success: bool = False
    message: str = Field(..., description="Human-readable error message")
    trace_id: str = Field(..., description="Request trace ID", alias="traceId")
    meta: ResponseMeta
    error: ErrorDetail

    model_config = {"populate_by_name": True}

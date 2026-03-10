"""Eligibility request/response models. X12 270/271, FHIR CoverageEligibilityRequest/Response."""
from pydantic import BaseModel, Field


# ---- Get Verify Member Eligibility ----
class GetVerifyMemberEligibilityRequest(BaseModel):
    """Request for member eligibility verification. X12 270, FHIR CoverageEligibilityRequest."""

    member_id_with_prefix: str = Field(
        ...,
        description="Member ID with optional prefix",
        examples=["LH001-MEM001"],
        alias="memberIdWithPrefix",
    )
    date: str = Field(
        ...,
        description="Eligibility date (YYYY-MM-DD)",
        examples=["2025-01-15"],
    )

    model_config = {"populate_by_name": True}


# ---- Get Service Benefits ----
class GetServiceBenefitsRequest(BaseModel):
    """Request for service-level benefits. X12 270/271."""

    member_id_with_prefix: str = Field(
        ...,
        alias="memberIdWithPrefix",
        examples=["LH001-MEM001"],
    )
    service_type_code: str | None = Field(
        default=None,
        alias="serviceTypeCode",
        examples=["30"],
    )
    procedure_code: str | None = Field(
        default=None,
        alias="procedureCode",
        examples=["99213"],
    )
    date: str | None = Field(default=None, examples=["2025-01-15"])

    model_config = {"populate_by_name": True}


# ---- Get Member Accumulators ----
class GetMemberAccumulatorsRequest(BaseModel):
    """Request for benefit accumulators. X12 270/271 benefit balances."""

    member_id_with_prefix: str = Field(
        ...,
        alias="memberIdWithPrefix",
        examples=["LH001-MEM001"],
    )
    date: str = Field(
        ...,
        description="As-of date for accumulator values",
        examples=["2025-06-01"],
    )

    model_config = {"populate_by_name": True}


# ---- Get COB Inquiry ----
class GetCobInquiryRequest(BaseModel):
    """Coordination of benefits inquiry. X12 270/271 COB."""

    member_id_with_prefix: str = Field(
        ...,
        alias="memberIdWithPrefix",
        examples=["LH001-MEM001"],
    )
    service_date: str | None = Field(
        default=None,
        alias="serviceDate",
        examples=["2025-01-15"],
    )

    model_config = {"populate_by_name": True}


# ---- Get Referral Requirement ----
class GetReferralRequirementRequest(BaseModel):
    """Referral requirement discovery. X12 270/271, FHIR CRD."""

    member_id_with_prefix: str = Field(
        ...,
        alias="memberIdWithPrefix",
        examples=["LH001-MEM001"],
    )
    procedure_code: str = Field(
        ...,
        alias="procedureCode",
        examples=["99213"],
    )
    place_of_service: str | None = Field(
        default=None,
        alias="placeOfService",
        examples=["11"],
    )

    model_config = {"populate_by_name": True}

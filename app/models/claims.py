"""Claims models. X12 837/276/277/835, FHIR Claim/ClaimResponse/ExplanationOfBenefit."""
from pydantic import BaseModel, Field, model_validator


# ---- Submit Claim ----
class SubmitClaimRequest(BaseModel):
    """Claim submission. X12 837, FHIR Claim."""

    member_id_with_prefix: str = Field(
        ...,
        alias="memberIdWithPrefix",
        examples=["LH001-MEM001"],
    )
    provider_npi: str = Field(
        ...,
        alias="providerNpi",
        examples=["1234567890"],
    )
    facility_id: str = Field(
        ...,
        alias="facilityId",
        examples=["FAC001"],
    )
    service_date: str = Field(
        ...,
        alias="serviceDate",
        examples=["2025-01-15"],
    )
    diagnosis_code: str = Field(
        ...,
        alias="diagnosisCode",
        examples=["J06.9"],
    )
    procedure_code: str = Field(
        ...,
        alias="procedureCode",
        examples=["99285"],
    )
    place_of_service: str = Field(
        ...,
        alias="placeOfService",
        examples=["21"],
    )
    billed_amount: float = Field(
        ...,
        alias="billedAmount",
        examples=[450.00],
    )

    model_config = {"populate_by_name": True}


# ---- Get Claim Acknowledgment ----
class GetClaimAcknowledgmentRequest(BaseModel):
    """Claim acknowledgment lookup. X12 277."""

    claim_id: str = Field(
        ...,
        alias="claimId",
        examples=["CLM001"],
    )

    model_config = {"populate_by_name": True}


# ---- Get Claim Status ----
class GetClaimStatusRequest(BaseModel):
    """Claim status lookup. X12 276/277."""

    claim_id: str = Field(
        ...,
        alias="claimId",
        examples=["CLM001"],
    )

    model_config = {"populate_by_name": True}


# ---- Get Claim Denial Details ----
class GetClaimDenialDetailsRequest(BaseModel):
    """Claim denial details. X12 277 adjudication."""

    claim_id: str = Field(
        ...,
        alias="claimId",
        examples=["CLM003"],
    )

    model_config = {"populate_by_name": True}


# ---- Get EOB ----
class GetEobRequest(BaseModel):
    """Explanation of Benefits request. X12 835, FHIR ExplanationOfBenefit."""

    claim_id: str | None = Field(default=None, alias="claimId")
    member_id_with_prefix: str | None = Field(default=None, alias="memberIdWithPrefix")
    service_date_from: str | None = Field(default=None, alias="serviceDateFrom")
    service_date_to: str | None = Field(default=None, alias="serviceDateTo")

    model_config = {"populate_by_name": True}

    @model_validator(mode="after")
    def require_claim_or_member(self):
        if not self.claim_id and not self.member_id_with_prefix:
            raise ValueError("Either claimId or memberIdWithPrefix is required")
        return self


# ---- Get Remittance ----
class GetRemittanceRequest(BaseModel):
    """Remittance advice request. X12 835."""

    claim_id: str = Field(
        ...,
        alias="claimId",
        examples=["CLM001"],
    )

    model_config = {"populate_by_name": True}


# ---- Submit Corrected Claim ----
class SubmitCorrectedClaimRequest(BaseModel):
    """Corrected claim submission. X12 837 replacement."""

    original_claim_id: str = Field(
        ...,
        alias="originalClaimId",
        examples=["CLM001"],
    )
    member_id_with_prefix: str = Field(
        ...,
        alias="memberIdWithPrefix",
        examples=["LH001-MEM001"],
    )
    provider_npi: str = Field(
        ...,
        alias="providerNpi",
        examples=["1234567890"],
    )
    facility_id: str = Field(
        ...,
        alias="facilityId",
        examples=["FAC001"],
    )
    service_date: str = Field(
        ...,
        alias="serviceDate",
        examples=["2025-01-15"],
    )
    diagnosis_code: str = Field(
        ...,
        alias="diagnosisCode",
        examples=["J06.9"],
    )
    procedure_code: str = Field(
        ...,
        alias="procedureCode",
        examples=["99285"],
    )
    place_of_service: str = Field(
        ...,
        alias="placeOfService",
        examples=["21"],
    )
    billed_amount: float = Field(
        ...,
        alias="billedAmount",
        examples=[450.00],
    )
    correction_type: str = Field(
        default="REPLACEMENT",
        alias="correctionType",
        examples=["REPLACEMENT"],
    )

    model_config = {"populate_by_name": True}


# ---- Get Medical Records Request Status ----
class GetMedicalRecordsRequestStatusRequest(BaseModel):
    """Medical records request status. X12 277/275, FHIR DocumentReference."""

    request_id: str = Field(
        ...,
        alias="requestId",
        examples=["REC001"],
    )

    model_config = {"populate_by_name": True}

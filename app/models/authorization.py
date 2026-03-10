"""Prior authorization models. X12 278, FHIR Claim/ClaimResponse, Da Vinci PAS/CRD."""
from pydantic import BaseModel, Field, model_validator


# ---- Get Prior Auth Requirement ----
class GetPriorAuthRequirementRequest(BaseModel):
    """Prior auth requirement discovery. X12 278, Da Vinci CRD."""

    member_id_with_prefix: str = Field(
        ...,
        alias="memberIdWithPrefix",
        examples=["LH001-MEM001"],
    )
    procedure_code: str = Field(
        ...,
        alias="procedureCode",
        examples=["99285"],
    )
    place_of_service: str | None = Field(
        default=None,
        alias="placeOfService",
        examples=["21"],
    )

    model_config = {"populate_by_name": True}


# ---- Submit Prior Auth Request ----
class SubmitPriorAuthRequest(BaseModel):
    """Prior auth submission. X12 278, Da Vinci PAS Claim."""

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
    procedure_code: str = Field(
        ...,
        alias="procedureCode",
        examples=["99285"],
    )
    diagnosis_code: str = Field(
        ...,
        alias="diagnosisCode",
        examples=["R07.9"],
    )
    service_date: str = Field(
        ...,
        alias="serviceDate",
        examples=["2025-01-15"],
    )
    place_of_service: str | None = Field(
        default=None,
        alias="placeOfService",
        examples=["21"],
    )
    facility_id: str | None = Field(default=None, alias="facilityId")

    model_config = {"populate_by_name": True}


# ---- Get Prior Auth Status ----
class GetPriorAuthStatusRequest(BaseModel):
    """Prior auth status lookup. X12 278, FHIR ClaimResponse."""

    authorization_id: str = Field(
        ...,
        alias="authorizationId",
        examples=["AUTH001"],
    )

    model_config = {"populate_by_name": True}


# ---- Get Prior Auth Pend Status ----
class GetPriorAuthPendStatusRequest(BaseModel):
    """Prior auth pend details. X12 278 pend follow-up."""

    authorization_id: str = Field(
        ...,
        alias="authorizationId",
        examples=["AUTH003"],
    )

    model_config = {"populate_by_name": True}


# ---- Upload Supporting Document Reference ----
class UploadSupportingDocumentRequest(BaseModel):
    """Supporting document reference. X12 275, FHIR DocumentReference."""

    authorization_id: str | None = Field(default=None, alias="authorizationId")
    claim_id: str | None = Field(default=None, alias="claimId")
    document_url: str = Field(
        ...,
        alias="documentUrl",
        examples=["https://example.com/doc.pdf"],
    )
    document_type: str = Field(
        ...,
        alias="documentType",
        examples=["CLINICAL_NOTE"],
    )
    description: str | None = Field(default=None)

    model_config = {"populate_by_name": True}

    @model_validator(mode="after")
    def require_auth_or_claim(self):
        if not self.authorization_id and not self.claim_id:
            raise ValueError("Either authorizationId or claimId is required")
        return self

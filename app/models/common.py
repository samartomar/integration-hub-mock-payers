"""Shared models and identifiers."""
from pydantic import BaseModel, Field


class MemberIdentifier(BaseModel):
    """Member identifier with optional prefix (e.g., LH001-MEM001)."""

    member_id_with_prefix: str = Field(
        ...,
        description="Member ID, optionally prefixed by payer/vendor (e.g., LH001-MEM001)",
        examples=["LH001-MEM001"],
        alias="memberIdWithPrefix",
    )

    model_config = {"populate_by_name": True}


class ProviderIdentifier(BaseModel):
    """Provider NPI identifier."""

    provider_npi: str = Field(
        ...,
        description="National Provider Identifier (10 digits)",
        examples=["1234567890"],
        alias="providerNpi",
        min_length=10,
        max_length=10,
    )

    model_config = {"populate_by_name": True}


class ClaimIdentifier(BaseModel):
    """Claim identifier."""

    claim_id: str = Field(
        ...,
        description="Unique claim identifier",
        examples=["CLM001"],
        alias="claimId",
    )

    model_config = {"populate_by_name": True}


class AuthorizationIdentifier(BaseModel):
    """Prior authorization identifier."""

    authorization_id: str = Field(
        ...,
        description="Prior authorization request ID",
        examples=["AUTH001"],
        alias="authorizationId",
    )

    model_config = {"populate_by_name": True}


class ReferralIdentifier(BaseModel):
    """Referral identifier."""

    referral_id: str = Field(
        ...,
        description="Referral ID",
        examples=["REF001"],
        alias="referralId",
    )

    model_config = {"populate_by_name": True}

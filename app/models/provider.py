"""Provider/network models. FHIR Plan-Net PractitionerRole, Organization, Location."""
from pydantic import BaseModel, Field


# ---- Get Provider Contract Status ----
class GetProviderContractStatusRequest(BaseModel):
    """Provider contract/network status. Plan-Net OrganizationAffiliation/PractitionerRole."""

    provider_npi: str = Field(
        ...,
        alias="providerNpi",
        examples=["1234567890"],
    )
    member_id_with_prefix: str | None = Field(
        default=None,
        alias="memberIdWithPrefix",
        examples=["LH001-MEM001"],
    )
    tax_id: str | None = Field(default=None, alias="taxId")

    model_config = {"populate_by_name": True}


# ---- Get Network Directory ----
class GetNetworkDirectoryRequest(BaseModel):
    """Network directory search. Plan-Net PractitionerRole, Organization, Location."""

    tax_id: str | None = Field(default=None, alias="taxId")
    network_id: str | None = Field(default=None, alias="networkId")
    specialty: str | None = Field(default=None)
    zip_code: str | None = Field(default=None, alias="zipCode")
    limit: int = Field(default=50, ge=1, le=200)

    model_config = {"populate_by_name": True}

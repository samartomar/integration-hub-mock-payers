"""Standards metadata model for response meta."""
from pydantic import BaseModel, Field


class StandardsMeta(BaseModel):
    """Standards crosswalk metadata for API responses."""

    x12_transaction_intent: str = Field(
        ...,
        description="Closest X12 transaction",
        examples=["270/271"],
    )
    fhir_alignment: list[str] = Field(
        default_factory=list,
        description="FHIR resource alignment",
    )
    davinci_alignment: list[str] = Field(
        default_factory=list,
        description="Da Vinci IG alignment",
    )
    mock_scenario: str = Field(
        ...,
        description="Fixture scenario used",
        examples=["happy_path"],
    )

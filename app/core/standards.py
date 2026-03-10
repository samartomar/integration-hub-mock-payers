"""Standards mapping constants for routes."""
from typing import Any

STANDARDS_BY_ROUTE: dict[str, dict[str, Any]] = {
    "get-verify-member-eligibility": {
        "x12": "270/271",
        "fhir": ["CoverageEligibilityRequest", "CoverageEligibilityResponse"],
        "davinci": [],
    },
    "get-service-benefits": {
        "x12": "270/271",
        "fhir": ["CoverageEligibilityRequest", "CoverageEligibilityResponse"],
        "davinci": [],
    },
    "get-member-accumulators": {
        "x12": "270/271 (benefit balances)",
        "fhir": ["CoverageEligibilityResponse"],
        "davinci": [],
    },
    "get-cob-inquiry": {
        "x12": "270/271 (COB)",
        "fhir": ["CoverageEligibilityResponse"],
        "davinci": [],
    },
    "get-referral-requirement": {
        "x12": "270/271",
        "fhir": ["CoverageEligibilityResponse"],
        "davinci": ["CRD"],
    },
    "get-prior-auth-requirement": {
        "x12": "278",
        "fhir": ["CoverageEligibilityResponse", "ServiceRequest"],
        "davinci": ["CRD"],
    },
    "submit-prior-auth-request": {
        "x12": "278",
        "fhir": ["Claim", "ClaimResponse"],
        "davinci": ["PAS"],
    },
    "get-prior-auth-status": {
        "x12": "278",
        "fhir": ["ClaimResponse"],
        "davinci": ["PAS"],
    },
    "get-prior-auth-pend-status": {
        "x12": "278",
        "fhir": ["ClaimResponse"],
        "davinci": ["PAS"],
    },
    "upload-supporting-document-reference": {
        "x12": "275",
        "fhir": ["DocumentReference"],
        "davinci": [],
    },
    "submit-claim": {
        "x12": "837",
        "fhir": ["Claim"],
        "davinci": [],
    },
    "get-claim-acknowledgment": {
        "x12": "277",
        "fhir": ["ClaimResponse (simplified)"],
        "davinci": [],
    },
    "get-claim-status": {
        "x12": "276/277",
        "fhir": ["ClaimResponse"],
        "davinci": [],
    },
    "get-claim-denial-details": {
        "x12": "277",
        "fhir": ["ClaimResponse"],
        "davinci": [],
    },
    "get-eob": {
        "x12": "835",
        "fhir": ["ExplanationOfBenefit"],
        "davinci": [],
    },
    "get-remittance": {
        "x12": "835",
        "fhir": ["ExplanationOfBenefit (simplified)"],
        "davinci": [],
    },
    "submit-corrected-claim": {
        "x12": "837",
        "fhir": ["Claim"],
        "davinci": [],
    },
    "get-medical-records-request-status": {
        "x12": "277/275",
        "fhir": ["DocumentReference", "Task"],
        "davinci": [],
    },
    "get-provider-contract-status": {
        "x12": "N/A (business convenience)",
        "fhir": ["OrganizationAffiliation", "PractitionerRole"],
        "davinci": ["Plan-Net"],
    },
    "get-network-directory": {
        "x12": "N/A",
        "fhir": ["PractitionerRole", "Organization", "Location", "OrganizationAffiliation"],
        "davinci": ["Plan-Net"],
    },
}

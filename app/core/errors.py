"""Standard error codes for the mock API."""
from enum import Enum


class ErrorCode(str, Enum):
    """Standard error codes."""

    AUTH_401 = "AUTH_401"
    VALIDATION_400 = "VALIDATION_400"
    MEMBER_404 = "MEMBER_404"
    CLAIM_404 = "CLAIM_404"
    AUTHZ_404 = "AUTHZ_404"
    PROVIDER_404 = "PROVIDER_404"
    REFERRAL_404 = "REFERRAL_404"
    BUSINESS_409 = "BUSINESS_409"
    SYSTEM_500 = "SYSTEM_500"
    RECORD_REQUEST_404 = "RECORD_REQUEST_404"

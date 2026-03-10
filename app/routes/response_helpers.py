"""Helpers for building standardized API responses."""
from app.core.errors import ErrorCode
from app.core.response import ErrorDetail, ErrorResponse, ResponseMeta, SuccessResponse
from app.core.standards import STANDARDS_BY_ROUTE
from app.core.trace import generate_trace_id


def build_meta(route_key: str, scenario: str) -> ResponseMeta:
    """Build ResponseMeta from route key and scenario."""
    s = STANDARDS_BY_ROUTE.get(route_key, {})
    return ResponseMeta(
        x12_transaction_intent=s.get("x12", "N/A"),
        fhir_alignment=s.get("fhir", []),
        davinci_alignment=s.get("davinci", []),
        mock_scenario=scenario,
    )


def success_response(
    route_key: str,
    message: str,
    data: dict | list | None,
    scenario: str = "happy_path",
) -> SuccessResponse:
    """Build success response."""
    trace_id = generate_trace_id()
    meta = build_meta(route_key, scenario)
    return SuccessResponse(
        success=True,
        message=message,
        trace_id=trace_id,
        meta=meta,
        data=data,
    )


def error_response(
    route_key: str,
    message: str,
    error_code: ErrorCode,
    scenario: str,
    details: dict | None = None,
) -> ErrorResponse:
    """Build error response."""
    trace_id = generate_trace_id()
    meta = build_meta(route_key, scenario)
    return ErrorResponse(
        success=False,
        message=message,
        trace_id=trace_id,
        meta=meta,
        error=ErrorDetail(code=error_code.value, details=details),
    )

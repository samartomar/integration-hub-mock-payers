"""Healthcare standards-aligned mock API. FastAPI entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.core.response import ErrorDetail, ErrorResponse, ResponseMeta
from app.core.standards import STANDARDS_BY_ROUTE
from app.core.trace import generate_trace_id
from app.routes import authorization, claims, eligibility, provider

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """App lifespan events."""
    yield


app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(eligibility.router)
app.include_router(authorization.router)
app.include_router(claims.router)
app.include_router(provider.router)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Return standardized error for HTTP exceptions (e.g., 401)."""
    trace_id = generate_trace_id()
    meta = ResponseMeta(
        x12_transaction_intent="N/A",
        fhir_alignment=[],
        davinci_alignment=[],
        mock_scenario="auth_required" if exc.status_code == 401 else "error",
    )
    code = "AUTH_401" if exc.status_code == 401 else "SYSTEM_500"
    err = ErrorResponse(
        success=False,
        message=exc.detail if isinstance(exc.detail, str) else "An error occurred",
        trace_id=trace_id,
        meta=meta,
        error=ErrorDetail(code=code, details=None),
    )
    return JSONResponse(status_code=exc.status_code, content=err.model_dump(by_alias=True, exclude_none=True))


def _serialize_validation_errors(errors: list) -> list:
    """Convert validation errors to JSON-serializable format."""
    result = []
    for e in errors:
        item = {"loc": e.get("loc"), "msg": e.get("msg"), "type": e.get("type")}
        if "ctx" in e and e["ctx"]:
            item["ctx"] = {k: str(v) for k, v in e["ctx"].items()}
        result.append(item)
    return result


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Return standardized error for validation failures."""
    trace_id = generate_trace_id()
    meta = ResponseMeta(
        x12_transaction_intent="N/A",
        fhir_alignment=[],
        davinci_alignment=[],
        mock_scenario="validation_error",
    )
    err = ErrorResponse(
        success=False,
        message="Validation error",
        trace_id=trace_id,
        meta=meta,
        error=ErrorDetail(code="VALIDATION_400", details={"errors": _serialize_validation_errors(exc.errors())}),
    )
    return JSONResponse(status_code=400, content=err.model_dump(by_alias=True, exclude_none=True))


@app.get("/health", tags=["Health"])
async def health(request: Request):
    """Health check. No auth required."""
    return {
        "status": "ok",
        "message": "Healthcare Mock API is running",
        "version": settings.api_version,
    }

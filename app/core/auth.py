"""Bearer token authentication: JWT validation (Auth0) or mock mode."""
import jwt
from jwt import PyJWKClient
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings

security = HTTPBearer(auto_error=False)

_jwks_client: PyJWKClient | None = None


def _get_jwks_client() -> PyJWKClient:
    """Get PyJWKClient for Auth0 JWKS. Cached."""
    global _jwks_client
    settings = get_settings()
    if not settings.auth0_issuer:
        raise ValueError("AUTH0_ISSUER not configured")
    if _jwks_client is None:
        jwks_uri = f"{settings.auth0_issuer.rstrip('/')}/.well-known/jwks.json"
        _jwks_client = PyJWKClient(jwks_uri)
    return _jwks_client


def _validate_jwt(token: str) -> dict:
    """Validate JWT and return payload. Raises on invalid."""
    settings = get_settings()
    jwks_client = _get_jwks_client()
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=settings.auth0_audience or None,
        issuer=settings.auth0_issuer.rstrip("/") if settings.auth0_issuer else None,
        options={
            "verify_exp": True,
            "verify_aud": bool(settings.auth0_audience),
            "verify_iss": bool(settings.auth0_issuer),
        },
    )
    # Scope check: token must have at least one required scope
    scopes = payload.get("scope", "")
    if isinstance(scopes, str):
        token_scopes = set(s.strip() for s in scopes.split() if s.strip())
    else:
        token_scopes = set(scopes) if scopes else set()
    required = set(settings.required_scopes)
    if required and not token_scopes.intersection(required):
        raise ValueError(f"Missing required scope. Has: {token_scopes}, need one of: {required}")
    # Partner code check (if configured)
    if settings.partner_code:
        claim_value = payload.get("partner_code") or payload.get("https://gosam.info/partner_code")
        if claim_value and claim_value != settings.partner_code:
            raise ValueError(f"Partner code mismatch: expected {settings.partner_code}")
    return payload


async def require_bearer(request: Request) -> str:
    """
    Validate Bearer token. When AUTH0_ISSUER is set, validates JWT via JWKS.
    Otherwise mock mode: any non-empty token accepted.
    """
    creds: HTTPAuthorizationCredentials | None = await security(request)
    if not creds or not creds.credentials or not creds.credentials.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header with Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = creds.credentials.strip()
    settings = get_settings()
    if settings.jwt_enabled:
        try:
            _validate_jwt(token)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
        except ValueError as e:
            raise HTTPException(status_code=403, detail=str(e))
    return token

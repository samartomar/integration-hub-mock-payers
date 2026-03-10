"""Simple bearer token authentication for mock API."""
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer(auto_error=False)


async def require_bearer(request: Request) -> str:
    """
    Validate Bearer token. In mock mode, any non-empty token is accepted.
    Missing or invalid header raises AUTH_401.
    """
    creds: HTTPAuthorizationCredentials | None = await security(request)
    if not creds or not creds.credentials or not creds.credentials.strip():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header with Bearer token required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return creds.credentials.strip()

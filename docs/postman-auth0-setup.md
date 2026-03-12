# Postman + Auth0 Token Setup

The collection automatically fetches a JWT from Auth0 before each request when Auth0 variables are set.

## Two environment files (LH001 and LH030)

1. **Import** the collection and both environments:
   - `postman/fastapi-healthcare-mock.postman_collection.json`
   - `postman/lh001.postman_environment.json`
   - `postman/lh030.postman_environment.json`

2. **Select** an environment from the environment dropdown (top-right): **LH001** or **LH030**.

3. **Edit** the selected environment ( Environments → LH001 or LH030 → Edit) and set:
   - `auth0ClientId` — Your M2M app Client ID
   - `auth0ClientSecret` — Your M2M app Client Secret

4. **Save** — the Pre-request Script will call Auth0 and set `bearerToken` before each API request.

| Environment | baseUrl | Auth0 domain |
|-------------|---------|--------------|
| LH001 | https://lh001.api.onrender.com | gosam.us.auth0.com |
| LH030 | https://lh030.api.onrender.com | dev-4tuxv42k7o4csoig.us.auth0.com |

## Fallback: collection variables only

Without an environment selected, the script reads `auth0TokenUrl`, `auth0ClientId`, `auth0ClientSecret`, `auth0Audience` from collection variables (right-click collection → Edit → Variables). Set those and the same token fetch will run.

## Local mock mode (no Auth0)

Leave `auth0TokenUrl` empty and set `bearerToken` to `mock-token-12345` (or any non-empty string). The script will not run.

## Token caching

The script caches the token for ~55 minutes to limit Auth0 calls. To force a refresh, clear the `bearerToken` variable in your environment (or collection) and run the request again.

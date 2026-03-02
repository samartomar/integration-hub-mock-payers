import { auth } from "express-oauth2-jwt-bearer";
import {
  applyVendorMap,
  extractLhcode,
  parseVendorClaimsFromEnv,
  parseVendorMapFromEnv,
  resolveVendorIdentity
} from "./auth/vendorIdentity.js";

const issuer = process.env.JWT_ISSUER || process.env.AUTH0_ISSUER;
const audience = process.env.JWT_AUDIENCE || process.env.AUTH0_AUDIENCE;
const vendorClaim = process.env.VENDOR_CLAIM || "https://gosam.info/vendor_code";
const configuredVendorClaims = parseVendorClaimsFromEnv();
const vendorMap = parseVendorMapFromEnv();

if (!issuer || !audience) {
  console.warn(
    "[mock-payers] JWT_ISSUER/JWT_AUDIENCE (or AUTH0_ISSUER/AUTH0_AUDIENCE) not set. JWT auth will fail."
  );
}

export const requireAuth = auth({
  issuerBaseURL: issuer,
  audience,
  tokenSigningAlg: "RS256"
});

export function attachVendorCode(req, res, next) {
  try {
    const claims = req.auth?.payload || req.auth || {};
    const { vendorValue, inferredLhcode } = resolveVendorIdentity(
      claims,
      configuredVendorClaims
    );

    const existingVendorCode = String(
      claims.vendor_code || claims[vendorClaim] || ""
    ).trim();
    const existingLhcode = String(claims.lhcode || "").trim();
    const unresolvedVendorCode = existingVendorCode || vendorValue;
    const resolvedVendorCode = applyVendorMap(unresolvedVendorCode, vendorMap);
    const mappedLhcode = extractLhcode(resolvedVendorCode);
    const resolvedLhcode =
      existingLhcode || inferredLhcode || mappedLhcode || resolvedVendorCode;

    if (!resolvedVendorCode) {
      return res.status(403).json({
        error: "FORBIDDEN",
        message: `Missing vendor identity in claims (${configuredVendorClaims.join(",")})`
      });
    }

    // Attach normalized identity to request auth context to mirror Python authorizer output.
    req.auth.vendorCode = resolvedVendorCode;
    req.auth.lhcode = resolvedLhcode;
    req.auth.vendor_code = resolvedVendorCode;
    req.vendorCode = resolvedVendorCode;

    // For JWT-authenticated requests, source vendor must come from token, not body.
    if (req.body && typeof req.body === "object") {
      const bodySourceVendor = req.body.sourceVendor || req.body.sourceVendorCode;
      if (
        bodySourceVendor &&
        String(bodySourceVendor).trim() !== resolvedVendorCode
      ) {
        console.warn(
          `[mock-payers] source vendor conflict: body=${bodySourceVendor}, jwt=${resolvedVendorCode}. Using JWT vendor.`
        );
      }

      req.body.sourceVendor = resolvedVendorCode;
      req.body.sourceVendorCode = resolvedVendorCode;
    }

    return next();
  } catch (err) {
    console.error("[mock-payers] attachVendorCode error:", err);
    return res.status(500).json({
      error: "INTERNAL_ERROR",
      message: "Unable to derive vendor code from token"
    });
  }
}

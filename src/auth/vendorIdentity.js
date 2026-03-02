const DEFAULT_VENDOR_CLAIMS = "lhcode,name,sub,entityId";
const LHCODE_REGEX = /\b(LH\d{3})\b/i;
const FALLBACK_CANDIDATES = [
  "lhcode",
  "vendor_code",
  "preferred_username",
  "email",
  "name",
  "sub"
];

function normalizeClaimList(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function firstNonEmptyClaim(claims, claimKeys) {
  for (const claimKey of claimKeys) {
    const raw = claims?.[claimKey];
    if (raw === undefined || raw === null) {
      continue;
    }
    const value = String(raw).trim();
    if (value) {
      return value;
    }
  }
  return "";
}

export function parseVendorClaimsFromEnv() {
  if (process.env.IDP_VENDOR_CLAIMS) {
    return normalizeClaimList(process.env.IDP_VENDOR_CLAIMS);
  }

  if (process.env.IDP_VENDOR_CLAIM) {
    return normalizeClaimList(process.env.IDP_VENDOR_CLAIM);
  }

  return normalizeClaimList(DEFAULT_VENDOR_CLAIMS);
}

export function extractLhcode(value) {
  const input = String(value || "");
  const match = input.match(LHCODE_REGEX);
  return match ? match[1].toUpperCase() : "";
}

export function resolveVendorIdentity(claims, vendorClaims) {
  const keys = vendorClaims?.length ? vendorClaims : parseVendorClaimsFromEnv();

  let vendorValue = firstNonEmptyClaim(claims, keys);
  let inferredLhcode = extractLhcode(vendorValue);

  if (!vendorValue || !inferredLhcode) {
    for (const candidateKey of FALLBACK_CANDIDATES) {
      const candidate = firstNonEmptyClaim(claims, [candidateKey]);
      if (!candidate) {
        continue;
      }

      if (!vendorValue) {
        vendorValue = candidate;
      }

      if (!inferredLhcode) {
        inferredLhcode = extractLhcode(candidate);
      }

      if (vendorValue && inferredLhcode) {
        break;
      }
    }
  }

  return {
    vendorValue,
    inferredLhcode
  };
}

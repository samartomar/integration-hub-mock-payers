import test from "node:test";
import assert from "node:assert/strict";
import {
  parseVendorClaimsFromEnv,
  resolveVendorIdentity
} from "../src/auth/vendorIdentity.js";

test("claim resolution uses configured order", () => {
  const original = process.env.IDP_VENDOR_CLAIMS;
  process.env.IDP_VENDOR_CLAIMS = "entityId,name,sub";

  const vendorClaims = parseVendorClaimsFromEnv();
  const claims = {
    entityId: "LH046",
    name: "LH001 Name Value",
    sub: "user|LH023"
  };

  const { vendorValue, inferredLhcode } = resolveVendorIdentity(
    claims,
    vendorClaims
  );

  assert.equal(vendorValue, "LH046");
  assert.equal(inferredLhcode, "LH046");

  if (original === undefined) {
    delete process.env.IDP_VENDOR_CLAIMS;
  } else {
    process.env.IDP_VENDOR_CLAIMS = original;
  }
});

test("fallback from sub containing LH001 infers lhcode", () => {
  const claims = {
    sub: "00u10lebyojPKzS4D698|LH001|partner"
  };

  const { vendorValue, inferredLhcode } = resolveVendorIdentity(claims, [
    "lhcode",
    "name",
    "entityId"
  ]);

  assert.equal(vendorValue, "00u10lebyojPKzS4D698|LH001|partner");
  assert.equal(inferredLhcode, "LH001");
});

test("fallback uses email/name/sub path when primary claims missing", () => {
  const claims = {
    email: "partner@partners.com",
    name: "Provider for LH030 test",
    sub: "auth0|abc"
  };

  const { vendorValue, inferredLhcode } = resolveVendorIdentity(claims, [
    "lhcode",
    "entityId"
  ]);

  assert.equal(vendorValue, "partner@partners.com");
  assert.equal(inferredLhcode, "LH030");
});

test("JWT vendor overrides conflicting body sourceVendor", async () => {
  process.env.JWT_ISSUER = "https://gosam.us.auth0.com/";
  process.env.JWT_AUDIENCE = "urn:integrationhub:api";
  process.env.IDP_VENDOR_CLAIMS = "lhcode,name,sub,entityId";
  process.env.VENDOR_CLAIM = "https://gosam.info/vendor_code";

  const { attachVendorCode } = await import(`../src/auth.js?t=${Date.now()}`);

  const req = {
    auth: {
      vendor_code: "LH002",
      sub: "partner|LH002"
    },
    body: {
      sourceVendor: "LH999",
      sourceVendorCode: "LH998"
    }
  };

  let nextCalled = false;
  const res = {
    status() {
      return this;
    },
    json() {
      return this;
    }
  };

  attachVendorCode(req, res, () => {
    nextCalled = true;
  });

  assert.equal(nextCalled, true);
  assert.equal(req.auth.vendorCode, "LH002");
  assert.equal(req.auth.lhcode, "LH002");
  assert.equal(req.body.sourceVendor, "LH002");
  assert.equal(req.body.sourceVendorCode, "LH002");
});

test("JWT vendor map remaps subject-derived identity to lhcode", async () => {
  process.env.JWT_ISSUER = "https://integrator-8163795.okta.com/oauth2/default";
  process.env.JWT_AUDIENCE = "api://default";
  process.env.IDP_VENDOR_CLAIMS = "lhcode,name,sub,entityId";
  process.env.JWT_VENDOR_MAP =
    "02.partner@partners.com:LH002,01.partner@partners.com:LH001";

  const { attachVendorCode } = await import(`../src/auth.js?t=${Date.now()}`);

  const req = {
    auth: {
      payload: {
        sub: "02.partner@partners.com"
      }
    },
    body: {}
  };

  let nextCalled = false;
  const res = {
    status() {
      return this;
    },
    json() {
      return this;
    }
  };

  attachVendorCode(req, res, () => {
    nextCalled = true;
  });

  assert.equal(nextCalled, true);
  assert.equal(req.auth.vendorCode, "LH002");
  assert.equal(req.auth.vendor_code, "LH002");
  assert.equal(req.auth.lhcode, "LH002");
});

test("auth bypass injects synthetic JWT identity", async () => {
  process.env.AUTH_BYPASS_ENABLED = "true";
  process.env.AUTH_BYPASS_VENDOR_CODE = "LH023";
  process.env.AUTH_BYPASS_SUBJECT = "bypass|LH023";
  process.env.VENDOR_CLAIM = "https://gosam.info/vendor_code";

  const { maybeBypassAuth } = await import(`../src/auth.js?t=${Date.now()}`);

  const req = {};
  let nextCalled = false;
  maybeBypassAuth(req, {}, () => {
    nextCalled = true;
  });

  assert.equal(nextCalled, true);
  assert.equal(req.auth.payload.vendor_code, "LH023");
  assert.equal(req.auth.payload.lhcode, "LH023");
  assert.equal(req.auth.payload.sub, "bypass|LH023");
  assert.equal(req.auth.payload["https://gosam.info/vendor_code"], "LH023");
});

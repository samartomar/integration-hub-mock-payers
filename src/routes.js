import express from "express";
import {
  getCobInquiryResponse,
  getProviderContractStatusResponse,
  getVerifyMemberEligibilityResponse,
  isKnownVendor
} from "./mockData.js";

const router = express.Router();

router.get("/health", (req, res) => {
  return res.json({
    status: "ok",
    message: "Mock payer API is running",
    vendorCode: req.vendorCode || null
  });
});

router.get("/api/whoami", (req, res) => {
  return res.json({
    vendorCode: req.auth?.vendorCode || null,
    vendor_code: req.auth?.vendor_code || null,
    lhcode: req.auth?.lhcode || null,
    subject: req.auth?.sub || null
  });
});

router.post("/api/get-cob-inquiry", (req, res) => {
  const vendorCode = req.vendorCode;
  if (!isKnownVendor(vendorCode)) {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: `Vendor ${vendorCode} is not allowed for GET_COB_INQUIRY`
    });
  }

  const { memberIdWithPrefix } = req.body || {};
  if (!memberIdWithPrefix || typeof memberIdWithPrefix !== "string") {
    return res.status(400).json({
      error: "VALIDATION_ERROR",
      message: "memberIdWithPrefix (string) is required"
    });
  }

  return res.json(getCobInquiryResponse(vendorCode, memberIdWithPrefix));
});

router.post("/api/get-verify-member-eligibility", (req, res) => {
  const vendorCode = req.vendorCode;
  if (!isKnownVendor(vendorCode)) {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: `Vendor ${vendorCode} is not allowed for GET_VERIFY_MEMBER_ELIGIBILITY`
    });
  }

  const { memberIdWithPrefix, date } = req.body || {};
  if (!memberIdWithPrefix || !date) {
    return res.status(400).json({
      error: "VALIDATION_ERROR",
      message: "memberIdWithPrefix and date are required"
    });
  }

  return res.json(
    getVerifyMemberEligibilityResponse(vendorCode, memberIdWithPrefix, date)
  );
});

router.post("/api/get-provider-contract-status", (req, res) => {
  const vendorCode = req.vendorCode;
  if (!isKnownVendor(vendorCode)) {
    return res.status(403).json({
      error: "FORBIDDEN",
      message: `Vendor ${vendorCode} is not allowed for GET_PROVIDER_CONTRACT_STATUS`
    });
  }

  const { memberIdWithPrefix } = req.body || {};
  if (!memberIdWithPrefix || typeof memberIdWithPrefix !== "string") {
    return res.status(400).json({
      error: "VALIDATION_ERROR",
      message: "memberIdWithPrefix (string) is required"
    });
  }

  return res.json(
    getProviderContractStatusResponse(vendorCode, memberIdWithPrefix)
  );
});

export default router;

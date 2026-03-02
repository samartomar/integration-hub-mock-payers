const KNOWN_VENDORS = ["LH001", "LH002", "LH023", "LH030", "LH046"];

export function getCobInquiryResponse(vendorCode, memberIdWithPrefix) {
  return {
    memberIdWithPrefix,
    name: `${vendorCode} Member`,
    dob: "1985-01-15",
    claimNumber: "CLM-123456",
    dateOfService: "2026-02-01",
    status: "PRIMARY"
  };
}

export function getVerifyMemberEligibilityResponse(
  vendorCode,
  memberIdWithPrefix,
  date
) {
  return {
    memberIdWithPrefix,
    name: `${vendorCode} Member`,
    dob: "1985-01-15",
    claimNumber: "CLM-987654",
    dateOfService: date,
    status: "ACTIVE"
  };
}

export function getProviderContractStatusResponse(vendorCode, memberIdWithPrefix) {
  return {
    memberIdWithPrefix,
    name: `${vendorCode} Provider`,
    dob: "1979-07-03",
    kpi: "4.7",
    taxId: "12-3456789",
    deliveryMethod: "EDI",
    claimNumber: "CLM-555999",
    dateOfService: "2026-01-20",
    status: "IN_NETWORK"
  };
}

export function isKnownVendor(vendorCode) {
  return KNOWN_VENDORS.includes(vendorCode);
}

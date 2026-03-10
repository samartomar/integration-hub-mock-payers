# Mock API Scenarios

Deterministic fixture-backed scenarios for the healthcare mock API platform.

---

## Scenario Naming Convention

- `happy_path` — successful response
- `member_not_found` — member does not exist
- `claim_not_found` — claim does not exist
- `authz_not_found` — prior auth does not exist
- `provider_not_found` — provider not in fixture
- `referral_not_found` — referral does not exist
- `validation_error` — invalid input
- `inactive` — member/coverage inactive
- `denied` — prior auth or claim denied
- `pended` — prior auth or claim pending
- `approved` — prior auth approved
- `rejected` — claim rejected
- `in_process` — claim in adjudication
- `paid` — claim paid

---

## Eligibility Scenarios

### get-verify-member-eligibility

| Scenario | Endpoint | Fixture IDs | Outcome |
|----------|----------|-------------|---------|
| happy_path | POST /api/get-verify-member-eligibility | memberIdWithPrefix: `MEM001`, date: `2025-01-15` | Active |
| member_not_found | Same | memberIdWithPrefix: `MEM999` | MEMBER_404 |
| inactive | Same | memberIdWithPrefix: `MEM003` | Inactive |
| validation_error | Same | Missing memberIdWithPrefix | VALIDATION_400 |

### get-service-benefits

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | memberIdWithPrefix: `MEM001`, serviceTypeCode: `30` | Benefits returned |
| member_not_found | memberIdWithPrefix: `MEM999` | MEMBER_404 |

### get-member-accumulators

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | memberIdWithPrefix: `MEM001`, date: `2025-06-01` | Accumulators |
| member_not_found | memberIdWithPrefix: `MEM999` | MEMBER_404 |

### get-cob-inquiry

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | memberIdWithPrefix: `MEM001` | PRIMARY/SECONDARY |
| member_not_found | memberIdWithPrefix: `MEM999` | MEMBER_404 |

### get-referral-requirement

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | memberIdWithPrefix: `MEM001`, procedureCode: `99213` | Requirements |
| member_not_found | memberIdWithPrefix: `MEM999` | MEMBER_404 |

---

## Prior Authorization Scenarios

### get-prior-auth-requirement

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | memberIdWithPrefix: `MEM001`, procedureCode: `99285` | Requirements |
| member_not_found | memberIdWithPrefix: `MEM999` | MEMBER_404 |

### submit-prior-auth-request

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | memberIdWithPrefix: `MEM001`, providerNpi: `1234567890`, procedureCode: `99285` | authorizationId returned |
| validation_error | Missing required fields | VALIDATION_400 |
| member_not_found | memberIdWithPrefix: `MEM999` | MEMBER_404 |

### get-prior-auth-status

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | authorizationId: `AUTH001` | Approved |
| authz_not_found | authorizationId: `AUTH999` | AUTHZ_404 |
| pended | authorizationId: `AUTH003` | Pended |

### get-prior-auth-pend-status

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | authorizationId: `AUTH003` | Pend details |
| authz_not_found | authorizationId: `AUTH999` | AUTHZ_404 |

### upload-supporting-document-reference

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | authorizationId: `AUTH001`, documentUrl, documentType | Doc reference saved |
| authz_not_found | authorizationId: `AUTH999` | AUTHZ_404 |

---

## Claims Scenarios

### submit-claim

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | Valid claim payload | claimId returned |
| validation_error | Invalid/missing fields | VALIDATION_400 |

### get-claim-acknowledgment

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | claimId: `CLM001` | Accepted |
| claim_not_found | claimId: `CLM999` | CLAIM_404 |
| rejected | claimId: `CLM002` | Rejected |

### get-claim-status

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | claimId: `CLM001` | In process / Paid |
| claim_not_found | claimId: `CLM999` | CLAIM_404 |

### get-claim-denial-details

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | claimId: `CLM003` (denied) | Denial codes |
| claim_not_found | claimId: `CLM999` | CLAIM_404 |

### get-eob

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | claimId: `CLM001` or memberIdWithPrefix: `MEM001` | EOB |
| claim_not_found | claimId: `CLM999` | CLAIM_404 |

### get-remittance

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | claimId: `CLM001` | Remittance |
| claim_not_found | claimId: `CLM999` | CLAIM_404 |

### submit-corrected-claim

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | originalClaimId: `CLM001`, correction payload | New claimId |
| claim_not_found | originalClaimId: `CLM999` | CLAIM_404 |

### get-medical-records-request-status

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | requestId: `REC001` | Status |
| not_found | requestId: `REC999` | Error |

---

## Provider Scenarios

### get-provider-contract-status

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | providerNpi: `1234567890`, memberIdWithPrefix: `MEM001` | IN_NETWORK |
| provider_not_found | providerNpi: `9999999999` | PROVIDER_404 |
| member_not_found | memberIdWithPrefix: `MEM999` | MEMBER_404 |

### get-network-directory

| Scenario | Fixture IDs | Outcome |
|----------|-------------|---------|
| happy_path | Optional: taxId, networkId | Providers, locations, organizations |
| empty | taxId with no matches | Empty list |

---

## Seeded Fixture ID Reference

| Fixture | Sample IDs |
|---------|------------|
| Members | MEM001, MEM002, MEM003, ... MEM010+ |
| Providers | 1234567890, 9876543210, ... |
| Facilities | FAC001, FAC002, ... FAC006 |
| Claims | CLM001, CLM002, ... CLM012 |
| Authorizations | AUTH001, AUTH002, ... AUTH008 |
| Referrals | REF001, REF002, ... REF005 |
| Remittances | REM001, REM002, ... REM006 |
| Records requests | REC001, REC002, ... REC005 |

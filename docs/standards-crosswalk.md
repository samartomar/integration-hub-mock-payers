# Standards Crosswalk: Mock API to X12 / FHIR / Da Vinci

This document maps each business route to relevant healthcare standards. The mock platform uses standards-shaped JSON abstractions rather than full EDI/HL7 conformance.

---

## 1. POST /api/get-verify-member-eligibility

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Verify member eligibility for a given date |
| **X12** | 270 (Eligibility Request) / 271 (Eligibility Response) |
| **FHIR** | CoverageEligibilityRequest / CoverageEligibilityResponse |
| **Da Vinci** | CRD ( Coverage Requirements Discovery) — eligibility subset |
| **Simplification notes** | Simplified benefit structure; no full 271 loops; JSON abstraction of inquiry/response |

---

## 2. POST /api/get-service-benefits

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve service-level benefit information |
| **X12** | 270/271 — benefit inquiry/response |
| **FHIR** | CoverageEligibilityRequest / CoverageEligibilityResponse (benefit details) |
| **Da Vinci** | CRD benefit discovery |
| **Simplification notes** | Focus on service type and benefit amounts; no full EB segment mapping |

---

## 3. POST /api/get-member-accumulators

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve deductible, OOP, and other benefit balances |
| **X12** | 270/271 conceptual benefit balances |
| **FHIR** | CoverageEligibilityResponse benefit balances / financial resources |
| **Da Vinci** | CRD financial responsibility |
| **Simplification notes** | Accumulator types as simplified benefit balance view |

---

## 4. POST /api/get-cob-inquiry

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Coordination of benefits inquiry — primary/secondary determination |
| **X12** | Eligibility/benefit inquiry concepts; COB also relates to claim coordination |
| **FHIR** | CoverageEligibilityResponse extensions / simplified coverage coordination view |
| **Da Vinci** | — |
| **Simplification notes** | Simplified COB status; full COB rules out of scope |

---

## 5. POST /api/get-referral-requirement

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Discover referral requirements for a service |
| **X12** | 270/271 benefit/referral requirement intent |
| **FHIR** | CoverageEligibilityResponse / CRD-aligned requirement discovery |
| **Da Vinci** | CRD requirement discovery for referrals |
| **Simplification notes** | Requirement list; no full CRD Questionnaire/Response |

---

## 6. POST /api/get-prior-auth-requirement

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Discover prior authorization requirements before submission |
| **X12** | 278 inquiry intent |
| **FHIR** | Da Vinci CRD-aligned requirement discovery response |
| **Da Vinci** | CRD (Coverage Requirements Discovery) |
| **Simplification notes** | Requirement list; no full CRD capability exchange |

---

## 7. POST /api/submit-prior-auth-request

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Submit prior authorization request for review |
| **X12** | 278 request for review and response |
| **FHIR** | PAS-aligned Claim for preauthorization use |
| **Da Vinci** | PAS (Prior Authorization Support) |
| **Simplification notes** | Claim-like payload; no full PAS workflow/Questionnaire |

---

## 8. POST /api/get-prior-auth-status

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve current prior authorization status |
| **X12** | 278 response / review status intent |
| **FHIR** | ClaimResponse |
| **Da Vinci** | PAS |
| **Simplification notes** | Status-oriented view; no full ClaimResponse resource |

---

## 9. POST /api/get-prior-auth-pend-status

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve pending/under-review prior auth details |
| **X12** | 278 pend / review follow-up intent |
| **FHIR** | ClaimResponse plus Task-like pending details |
| **Da Vinci** | PAS |
| **Simplification notes** | Pend reason codes and estimated completion |

---

## 10. POST /api/upload-supporting-document-reference

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Upload reference to supporting documentation for claims/auth |
| **X12** | 275 attachment/supporting info intent |
| **FHIR** | DocumentReference |
| **Da Vinci** | CDex-style document exchange concepts (docs only) |
| **Simplification notes** | Metadata reference; no binary payload handling |

---

## 11. POST /api/submit-claim

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Submit professional or institutional claim |
| **X12** | 837 professional/institutional simplified claim intent |
| **FHIR** | Claim |
| **Da Vinci** | — |
| **Simplification notes** | Claim-like payload; no full 837 segment mapping |

---

## 12. POST /api/get-claim-acknowledgment

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve claim submission acknowledgment |
| **X12** | 277 claim acknowledgment |
| **FHIR** | Simplified acknowledgment model — non-core convenience API |
| **Da Vinci** | — |
| **Simplification notes** | Accept/reject status; not a core FHIR resource |

---

## 13. POST /api/get-claim-status

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve claim adjudication status |
| **X12** | 276/277 |
| **FHIR** | ClaimResponse status-oriented view |
| **Da Vinci** | — |
| **Simplification notes** | Status, dates; no full 277 segment mapping |

---

## 14. POST /api/get-claim-denial-details

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve denial reason and adjustment details |
| **X12** | 277 / adjudication intent |
| **FHIR** | ClaimResponse (adjudication, error) |
| **Da Vinci** | — |
| **Simplification notes** | Denial codes, adjustment codes; simplified adjudication |

---

## 15. POST /api/get-eob

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve Explanation of Benefits |
| **X12** | 835 payment/advice and EOB concepts |
| **FHIR** | ExplanationOfBenefit |
| **Da Vinci** | — |
| **Simplification notes** | EOB-shaped structure; no full 835 PLB/N1 loops |

---

## 16. POST /api/get-remittance

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve remittance advice / payment details |
| **X12** | 835 |
| **FHIR** | Simplified remittance view with optional EOB linkage |
| **Da Vinci** | — |
| **Simplification notes** | Payment details; optional EOB reference |

---

## 17. POST /api/submit-corrected-claim

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Submit corrected or replacement claim |
| **X12** | 837 corrected/replacement claim intent |
| **FHIR** | Claim with replacement/correction indicators |
| **Da Vinci** | — |
| **Simplification notes** | Original claim reference; correction type |

---

## 18. POST /api/get-medical-records-request-status

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Status of medical records / documentation request |
| **X12** | 277 additional info + 275 supporting documentation |
| **FHIR** | DocumentReference / Task-style simplified status |
| **Da Vinci** | CDex relevance (docs) |
| **Simplification notes** | Status, dates; no full CDex workflow |

---

## 19. POST /api/get-provider-contract-status

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Check provider network/contract participation |
| **X12** | No single canonical provider-contract transaction |
| **FHIR** | Plan-Net: OrganizationAffiliation, PractitionerRole, network participation |
| **Da Vinci** | PDex Plan-Net |
| **Simplification notes** | Business convenience API; Plan-Net aligned abstraction |

---

## 20. POST /api/get-network-directory

| Dimension | Mapping |
|-----------|---------|
| **Business purpose** | Retrieve network directory (providers, locations, organizations) |
| **X12** | None |
| **FHIR** | Plan-Net: PractitionerRole, Organization, Location, OrganizationAffiliation |
| **Da Vinci** | PDex Plan-Net |
| **Simplification notes** | Directory search; no full Plan-Net $match |

---

## Future Path to Stricter Compliance

1. **X12**: Integrate licensed 270/271/276/277/278/837/835 implementation guides; map JSON to EDI segments.
2. **FHIR**: Adopt full CoverageEligibilityRequest/Response, Claim, ClaimResponse, EOB resources; expose FHIR REST endpoints.
3. **Da Vinci**: Implement full CRD, PAS, Plan-Net capability statements and operations.

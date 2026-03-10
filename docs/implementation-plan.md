# Implementation Plan: Healthcare Standards-Aligned Mock API Platform

## Purpose

Build a production-style FastAPI mock API platform for U.S. healthcare administrative workflows, explicitly aligned with X12, HL7 FHIR, and Da Vinci implementation guides. The platform serves as a credible demonstration for payer/provider integration patterns and adoption readiness.

## Design Philosophy

- **Dual-surface design**: Business-friendly routes under `/api/` with standards mapping documented in meta and docs
- **Fixture-backed determinism**: No random generation; consistent seeded scenarios
- **Standards-aware, not standards-compliant**: Clear crosswalk to X12/FHIR/Da Vinci without fabricating full EDI
- **Credible to healthcare architects**: Realistic fields, outcomes, and documentation

## Phases

### Phase 1: Documentation (Complete First)

1. `implementation-plan.md` (this document)
2. `standards-crosswalk.md` — per-endpoint X12/FHIR/Da Vinci mapping
3. `mock-api-scenarios.md` — scenario names, fixture IDs, supported outcomes

### Phase 2: Project Skeleton

- `app/main.py` — FastAPI app, CORS, route mounting
- `app/core/` — config, auth, errors, response wrapper, trace, standards
- Directory structure for routes, models, services, fixtures

### Phase 3: Core Utilities

- Config (env, settings)
- Auth: Bearer validator (any non-empty token accepted)
- Errors: Standard codes (AUTH_401, VALIDATION_400, MEMBER_404, etc.)
- Response wrapper: success/error with meta (x12TransactionIntent, fhirAlignment, davinciAlignment, mockScenario)
- Trace: TRACE-xxx IDs
- Standards: Route metadata constants

### Phase 4: Fixtures

- members.json (≥10)
- coverages.json
- providers.json (≥8)
- facilities.json (≥6)
- claims.json (≥12)
- authorizations.json (≥8)
- referrals.json (≥5)
- remittances.json (≥6)
- records_requests.json (≥5)

All IDs must line up; outcomes: active, inactive, approved, pended, denied, accepted, rejected, in process, paid, not found, validation error.

### Phase 5: Models

- Pydantic models for all requests/responses
- Field descriptions, examples
- Standards metadata
- Shared identifiers (memberIdWithPrefix, providerNpi, claimId, etc.)

### Phase 6: Services and Routes

- Services: eligibility, authorization, claims, provider, referral
- Thin routes that delegate to services
- Fixture lookup, scenario resolution
- All 20 required routes implemented

### Phase 7: OpenAPI and Tests

- OpenAPI summary, description, examples per route
- pytest + TestClient
- Auth required, happy path, failure path for each route
- Broader coverage for key endpoints

### Phase 8: Finalization

- Run full test suite
- Fix failures
- Architecture doc
- README update

## Execution Checklist

- [x] Create implementation-plan.md
- [ ] Create standards-crosswalk.md
- [ ] Create mock-api-scenarios.md
- [ ] Build project skeleton
- [ ] Build core utilities
- [ ] Create fixtures
- [ ] Implement models
- [ ] Implement services
- [ ] Implement routes
- [ ] Add OpenAPI examples
- [ ] Add tests
- [ ] Run test suite
- [ ] Create architecture.md
- [ ] Update README
- [ ] Final summary

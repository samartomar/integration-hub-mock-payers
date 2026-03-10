# Architecture: Healthcare Mock API Platform

## Design Rationale

### Dual-Surface API Design

The platform exposes **business-friendly routes** under `/api/` rather than raw FHIR or X12 endpoints. This design was chosen because:

1. **Integration simplicity**: Payers, providers, and integration hubs expect pragmatic REST APIs with clear business semantics.
2. **Standards mapping without conformance burden**: Each route documents X12, FHIR, and Da Vinci alignment in `meta` and in `docs/standards-crosswalk.md` without requiring full EDI/HL7 conformance.
3. **Credibility**: Healthcare architects can see explicit crosswalks (e.g., "X12 270/271, FHIR CoverageEligibilityRequest/Response") and evaluate adoption readiness.

### Why Full X12 Conformance Is Out of Scope

- X12 implementation guides (270/271, 276/277, 278, 837, 835) are typically **licensed** and not freely available in the repository.
- Fabricating full EDI loops/segments without source specifications would be incorrect and misleading.
- The mock uses **standards-shaped JSON abstractions** labeled with the closest X12 transaction, FHIR resource, and business intent—appropriate for demos and integration testing.

### Fixture Strategy

- **Deterministic**: No random generation. All scenarios are seeded in `app/fixtures/`.
- **Consistent**: IDs (memberIdWithPrefix, claimId, providerNpi, etc.) line up across endpoints.
- **Outcome variety**: Fixtures include active, inactive, approved, pended, denied, accepted, rejected, in process, paid, not found, validation error.
- **Internal consistency**: Coverage, claims, providers, remittances, and authorizations reference each other correctly.

### Service Layer Pattern

- **Thin routes**: Routes validate input, call the service, and format response/error.
- **Fat services**: `app/services/` contain all fixture lookup and scenario logic.
- **No inline mocks**: Mock data lives in `app/fixtures/`; routes and services do not embed large dictionaries.

### How to Extend the Platform

1. **Add a scenario**: Add fixture data in the appropriate JSON file; update service logic to resolve the scenario; document in `docs/mock-api-scenarios.md`.
2. **Add a route**: Create request/response models in `app/models/`; implement service in `app/services/`; add route in `app/routes/`; add standards mapping in `app/core/standards.py` and `docs/standards-crosswalk.md`.
3. **Add a standards mapping**: Update `STANDARDS_BY_ROUTE` in `app/core/standards.py`; add a section in `docs/standards-crosswalk.md`.

-- Seed rows for mock payer outbound endpoints (single Render service).
-- Update the two values in params before running:
--   base_url        -> deployed URL, e.g. https://integration-hub-mock-payers.onrender.com
--   auth_profile_id -> UUID of JWT auth profile used by outbound calls

WITH params AS (
  SELECT
    'https://integration-hub-mock-payers.onrender.com'::text AS base_url,
    '00000000-0000-0000-0000-000000000000'::uuid AS auth_profile_id
)
INSERT INTO control_plane.vendor_endpoints
  (source_vendor_code, operation_code, flow_direction, url, auth_profile_id, is_active)
SELECT
  seed.source_vendor_code,
  seed.operation_code,
  'OUTBOUND',
  p.base_url || seed.path_suffix,
  p.auth_profile_id,
  TRUE
FROM (
  VALUES
    ('LH001', 'GET_COB_INQUIRY', '/api/get-cob-inquiry'),
    ('LH001', 'GET_VERIFY_MEMBER_ELIGIBILITY', '/api/get-verify-member-eligibility'),
    ('LH001', 'GET_PROVIDER_CONTRACT_STATUS', '/api/get-provider-contract-status'),
    ('LH002', 'GET_COB_INQUIRY', '/api/get-cob-inquiry'),
    ('LH002', 'GET_VERIFY_MEMBER_ELIGIBILITY', '/api/get-verify-member-eligibility'),
    ('LH002', 'GET_PROVIDER_CONTRACT_STATUS', '/api/get-provider-contract-status'),
    ('LH023', 'GET_COB_INQUIRY', '/api/get-cob-inquiry'),
    ('LH023', 'GET_VERIFY_MEMBER_ELIGIBILITY', '/api/get-verify-member-eligibility'),
    ('LH023', 'GET_PROVIDER_CONTRACT_STATUS', '/api/get-provider-contract-status'),
    ('LH030', 'GET_COB_INQUIRY', '/api/get-cob-inquiry'),
    ('LH030', 'GET_VERIFY_MEMBER_ELIGIBILITY', '/api/get-verify-member-eligibility'),
    ('LH030', 'GET_PROVIDER_CONTRACT_STATUS', '/api/get-provider-contract-status'),
    ('LH046', 'GET_COB_INQUIRY', '/api/get-cob-inquiry'),
    ('LH046', 'GET_VERIFY_MEMBER_ELIGIBILITY', '/api/get-verify-member-eligibility'),
    ('LH046', 'GET_PROVIDER_CONTRACT_STATUS', '/api/get-provider-contract-status')
) AS seed(source_vendor_code, operation_code, path_suffix)
CROSS JOIN params p;

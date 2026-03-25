#!/usr/bin/env bash
# Example: create SIP digest on Exotel vSIP trunk (Integration 1 — outbound).
# Copy to .env or export vars locally. Do not commit real credentials.
# If passwords contain quotes or backslashes, escape them or use a secrets manager.

set -euo pipefail

: "${API_KEY:?}"
: "${API_TOKEN:?}"
: "${SUBDOMAIN:?}"
: "${ACCOUNT_SID:?}"
: "${TRUNK_SID:?}"
: "${SIP_USER:?}"
: "${SIP_PASS:?}"

curl -s -X POST \
  "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d "$(printf '%s' "{\"user_name\":\"${SIP_USER}\",\"password\":\"${SIP_PASS}\",\"friendly_name\":\"eleven_labs\"}")"

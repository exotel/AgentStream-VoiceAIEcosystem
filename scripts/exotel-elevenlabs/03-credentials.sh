#!/usr/bin/env bash
# Create SIP digest on trunk. MUST match ElevenLabs phone import (EXOTEL_SIP_USERNAME / EXOTEL_SIP_PASSWORD).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"
load_env

require_vars EXOTEL_API_KEY EXOTEL_API_TOKEN EXOTEL_SUBDOMAIN EXOTEL_ACCOUNT_SID EXOTEL_TRUNK_SID \
  EXOTEL_SIP_USERNAME EXOTEL_SIP_PASSWORD

BODY=$(jq -n \
  --arg u "${EXOTEL_SIP_USERNAME}" \
  --arg p "${EXOTEL_SIP_PASSWORD}" \
  --arg fn "${EXOTEL_SIP_FRIENDLY_NAME:-eleven_labs}" \
  '{user_name: $u, password: $p, friendly_name: $fn}')

RESP=$(curl -sS -X POST "$(exotel_base)/trunks/${EXOTEL_TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d "${BODY}")

echo "${RESP}" | jq . 2>/dev/null || echo "${RESP}"

#!/usr/bin/env bash
# Map Exophone (DID) to trunk. Requires EXOTEL_TRUNK_SID and EXOTEL_PHONE_NUMBER (E.164).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"
load_env

require_vars EXOTEL_API_KEY EXOTEL_API_TOKEN EXOTEL_SUBDOMAIN EXOTEL_ACCOUNT_SID EXOTEL_TRUNK_SID EXOTEL_PHONE_NUMBER

BODY=$(jq -n --arg pn "${EXOTEL_PHONE_NUMBER}" '{phone_number: $pn}')

RESP=$(curl -sS -X POST "$(exotel_base)/trunks/${EXOTEL_TRUNK_SID}/phone-numbers" \
  -H "Content-Type: application/json" \
  -d "${BODY}")

echo "${RESP}" | jq . 2>/dev/null || echo "${RESP}"

PNID=$(echo "${RESP}" | jq -r '.. | .id? // empty' | head -1)
if [[ -n "${PNID}" && "${PNID}" != "null" ]]; then
  echo "" >&2
  echo "Optional — add to .env if you need mode updates: EXOTEL_TRUNK_PHONE_NUMBER_ID=${PNID}" >&2
fi

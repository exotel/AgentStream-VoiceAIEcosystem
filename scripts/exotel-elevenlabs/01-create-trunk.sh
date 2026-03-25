#!/usr/bin/env bash
# Create Exotel vSIP trunk. Prints JSON response; save trunk_sid into EXOTEL_TRUNK_SID in .env
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"
load_env

require_vars EXOTEL_API_KEY EXOTEL_API_TOKEN EXOTEL_SUBDOMAIN EXOTEL_ACCOUNT_SID

BODY=$(jq -n \
  --arg name "${EXOTEL_TRUNK_NAME:-ElevenLabs_Trunk}" \
  --arg domain "${EXOTEL_ACCOUNT_SID}.pstn.exotel.com" \
  '{trunk_name: $name, nso_code: "ANY-ANY", domain_name: $domain}')

RESP=$(curl -sS -X POST "$(exotel_base)/trunks" \
  -H "Content-Type: application/json" \
  -d "${BODY}")

echo "${RESP}" | jq . 2>/dev/null || echo "${RESP}"

SID=$(echo "${RESP}" | jq -r '.response.trunk_sid // .trunk_sid // .TrunkSid // empty' 2>/dev/null | head -1)
if [[ -n "${SID}" && "${SID}" != "null" ]]; then
  echo "" >&2
  echo "Add to your .env: EXOTEL_TRUNK_SID=${SID}" >&2
fi

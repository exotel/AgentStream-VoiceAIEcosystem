#!/usr/bin/env bash
# Add ElevenLabs SIP FQDN as destination URI on the SAME trunk (inbound path to ElevenLabs).
# Default: sip.rtc.elevenlabs.io:5060;transport=tcp
# India residency (optional): set ELEVENLABS_SIP_DESTINATION in .env
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"
load_env

require_vars EXOTEL_API_KEY EXOTEL_API_TOKEN EXOTEL_SUBDOMAIN EXOTEL_ACCOUNT_SID EXOTEL_TRUNK_SID

DEST="${ELEVENLABS_SIP_DESTINATION:-sip.rtc.elevenlabs.io:5060;transport=tcp}"

BODY=$(jq -n --arg d "${DEST}" '{destinations: [{destination: $d}]}')

RESP=$(curl -sS -X POST "$(exotel_base)/trunks/${EXOTEL_TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d "${BODY}")

echo "Using destination: ${DEST}" >&2
echo "${RESP}" | jq . 2>/dev/null || echo "${RESP}"

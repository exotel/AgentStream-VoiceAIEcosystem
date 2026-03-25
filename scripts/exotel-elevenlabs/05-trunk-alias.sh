#!/usr/bin/env bash
# Set outbound CLI (trunk_external_alias) to your Exophone — use after mapping DID.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "${SCRIPT_DIR}/lib.sh"
load_env

require_vars EXOTEL_API_KEY EXOTEL_API_TOKEN EXOTEL_SUBDOMAIN EXOTEL_ACCOUNT_SID EXOTEL_TRUNK_SID EXOTEL_PHONE_NUMBER

BODY=$(jq -n --arg exo "${EXOTEL_PHONE_NUMBER}" \
  '{settings: [{name: "trunk_external_alias", value: $exo}]}')

RESP=$(curl -sS -X POST "$(exotel_base)/trunks/${EXOTEL_TRUNK_SID}/settings" \
  -H "Content-Type: application/json" \
  -d "${BODY}")

echo "${RESP}" | jq . 2>/dev/null || echo "${RESP}"

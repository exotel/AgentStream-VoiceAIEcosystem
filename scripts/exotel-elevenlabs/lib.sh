#!/usr/bin/env bash
# Shared helpers for Exotel vSIP + ElevenLabs scripts.
# shellcheck disable=SC1091

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

load_env() {
  if [[ -f "${REPO_ROOT}/.env" ]]; then
    # shellcheck source=/dev/null
    set -a && source "${REPO_ROOT}/.env" && set +a
  fi
}

require_vars() {
  local missing=()
  for name in "$@"; do
    if [[ -z "${!name:-}" ]]; then
      missing+=("$name")
    fi
  done
  if [[ ${#missing[@]} -gt 0 ]]; then
    echo "Missing required env: ${missing[*]}" >&2
    echo "Copy .env.example to .env and fill values." >&2
    exit 1
  fi
}

exotel_base() {
  echo "https://${EXOTEL_API_KEY}:${EXOTEL_API_TOKEN}@${EXOTEL_SUBDOMAIN}/v2/accounts/${EXOTEL_ACCOUNT_SID}"
}

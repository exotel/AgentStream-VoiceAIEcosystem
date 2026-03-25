#!/usr/bin/env bash
# Run the LiveKit outbound caller agent (dev mode).
# Requires: venv created with Python 3.10+, deps installed, .env.local configured.

set -e
cd "$(dirname "$0")"

if [[ ! -d venv ]]; then
  echo "Creating venv with Python 3.10+..."
  if command -v python3.11 &>/dev/null; then
    python3.11 -m venv venv
  elif command -v python3.12 &>/dev/null; then
    python3.12 -m venv venv
  else
    python3 -m venv venv
  fi
  ./venv/bin/pip install -r requirements.txt
  echo "Venv ready. Edit .env.local with your credentials, then run: ./run.sh"
  exit 0
fi

if [[ ! -f .env.local ]]; then
  cp .env.example .env.local
  echo "Created .env.local from .env.example. Edit it with your LiveKit/OpenAI/Deepgram/SIP credentials."
  exit 1
fi

exec ./venv/bin/python3 agent.py dev "$@"

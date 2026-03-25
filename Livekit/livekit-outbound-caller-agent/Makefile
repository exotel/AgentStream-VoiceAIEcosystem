# LiveKit outbound caller agent
# Usage:
#   make install          # create venv and install dependencies
#   make call             # call default number (set PHONE in .env.local or use PHONE=)
#   make call PHONE=+919876543210

PYTHON ?= python3
VENV   := venv
BIN    := $(VENV)/bin
PIP    := $(BIN)/pip
PY     := $(BIN)/python3

.PHONY: install call help

help:
	@echo "Targets:"
	@echo "  make install              Create venv and install dependencies"
	@echo "  make call PHONE=<number>  Place outbound call (e.g. PHONE=+919876543210)"
	@echo ""
	@echo "Ensure .env.local has LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, SIP_OUTBOUND_TRUNK_ID"

install: $(BIN)/python3
$(BIN)/python3: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

call: install
	@if [ -z "$(PHONE)" ]; then \
		echo "Usage: make call PHONE=+<number>"; \
		echo "Example: make call PHONE=+917696016726"; \
		exit 1; \
	fi
	$(PY) call_phone.py "$(PHONE)"

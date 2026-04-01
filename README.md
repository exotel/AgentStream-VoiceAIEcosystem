# AgentStream — Voice AI Ecosystem

Practical integration guides and reference snippets for connecting **Exotel telephony (SIP trunking / Voice Streaming)** with popular Voice AI platforms (e.g., ElevenLabs, LiveKit, Retell, Bolna, Pipecat, Ultravox, Vapi, Smallest AI, Vocallabs, Rapida AI, NLPearl).

## What’s in this repo

- **Support guides**: `docs/support/` — step-by-step setup for Exotel ↔ provider integrations.
- **Shared Exotel trunk API snippets**: `docs/support/_exotel-trunk-api-snippets.md` — reusable curl templates (create trunk, map DID, credentials, allowlist, destination URI).
- **Provider “connector” docs / quickstarts**: `<provider>/integrations/exotel-vsip/` — implementation and runbooks for each provider’s flow.
- **WebRTC app setup**: `docs/integrations/webrtc-application-setup.md` — WebRTC application wiring notes.

## Quickstart

1. Copy `.env.example` → `.env` and fill in values locally.
2. Pick your provider guide from `docs/support/README.md`.
3. Follow the **Outbound** / **Inbound** flow steps in the chosen support article.

## Security

- **Do not commit secrets**: keep real credentials in `.env` (ignored by git).
- **Use placeholders in docs**: examples should stay as `API_KEY`, `API_TOKEN`, `SIP_PASS`, etc.


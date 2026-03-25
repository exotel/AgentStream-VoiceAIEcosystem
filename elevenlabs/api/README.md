# ElevenLabs — API approach

Use this track to get started **via the API** (keys, SDK, and minimal examples).

## Prerequisites

- ElevenLabs account
- API key from **Profile → API keys** (or the developer section in the app)

## Suggested steps

1. **Create or copy an API key** in the ElevenLabs dashboard (store it securely; never commit keys).
2. **Set environment variables** — e.g. `ELEVENLABS_API_KEY` (see project root `.env.example` if present).
3. **Pick an integration**:
   - REST: `https://api.elevenlabs.io` with `xi-api-key` header
   - Official SDKs where available for your language
   - **Agents + Exotel — SIP trunk:** [`integrations/exotel-vsip/QUICKSTART.md`](../integrations/exotel-vsip/QUICKSTART.md) · [Voice AI Connector](../integrations/exotel-vsip/elevenlabs-voice-ai-connector.md)
   - **Agents + Exotel — WebSocket bridge:** [`integrations/exotel-wss/README.md`](../integrations/exotel-wss/README.md) (Exotel pattern: [Agent-Stream](https://github.com/exotel/Agent-Stream); ElevenLabs: ConvAI WebSocket + [signed URL](https://elevenlabs.io/docs/conversational-ai/api-reference/conversations/get-signed-url))
4. **Smoke test**: list voices or run a short text-to-speech request.
5. **Iterate**: voice ID, model ID, and streaming vs. non-streaming as needed.

## Notes

- Keep keys in `.env` (gitignored) or a secrets manager.
- Add small example scripts or `curl` snippets in this folder as you build them.

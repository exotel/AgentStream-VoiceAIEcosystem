# ElevenLabs

This area covers two ways to work with [ElevenLabs](https://elevenlabs.io/):

| Track | Folder | Purpose |
|--------|--------|---------|
| **API** | [`api/`](./api/) | Programmatic setup: API keys, SDKs, and first calls (TTS, voices, etc.). |
| **Dashboard** | [`dashboard/`](./dashboard/) | Manual setup in the ElevenLabs web UI: account, voices, projects, and settings. |

## Integrations (Exotel + ElevenLabs)

**Two approaches:** [integrations/README.md](./integrations/README.md) — **SIP trunk** vs **WebSocket (Voicebot + bridge)**.

| Integration | Path |
|-------------|------|
| **SIP trunk (vSIP)** — native ElevenLabs SIP | [`integrations/exotel-vsip/`](./integrations/exotel-vsip/) — [Quickstart](./integrations/exotel-vsip/QUICKSTART.md) · [Voice AI Connector](./integrations/exotel-vsip/elevenlabs-voice-ai-connector.md) |
| **WSS** — Exotel Voicebot → your bridge → ElevenLabs ConvAI WS | [`integrations/exotel-wss/`](./integrations/exotel-wss/) (see [Agent-Stream](https://github.com/exotel/Agent-Stream) for Exotel streaming reference) |

Start with whichever fits your workflow; you can combine both (e.g. configure voices in the dashboard, then call them from code via the API).

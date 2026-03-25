# Exotel Voicebot (WSS) + ElevenLabs Conversational AI

This track is the **WebSocket / streaming** approach: Exotel’s **Voicebot Applet** opens a **`wss://`** connection to **your** server; your server bridges audio and signalling to **ElevenLabs** over the **Conversational AI WebSocket** API.

It is **not** the same as [SIP trunk integration](../exotel-vsip/) (no vSIP trunk to `sip.rtc.elevenlabs.io` here).

---

## Reference: Exotel side (voice streaming)

Exotel publishes **[Agent-Stream](https://github.com/exotel/Agent-Stream)** — a sample Python bot that accepts Exotel’s **WebSocket streaming** and forwards to **OpenAI Realtime API**.

Use it as the **Exotel integration reference** (not the AI vendor):

| Topic | Agent-Stream / Exotel pattern |
|-------|--------------------------------|
| **URL** | Public `wss://your-host/...` (e.g. ngrok or VPS) — Voicebot Applet points here |
| **Sample rate** | Often **24 kHz** for quality (see sample repo `config` / README) |
| **Audio** | Raw PCM / streaming chunks as documented in the Voicebot product |
| **Bidirectional** | Enabled for real-time speech |

Clone and read: [github.com/exotel/Agent-Stream](https://github.com/exotel/Agent-Stream) (`main.py`, `core/`, `README`).

---

## ElevenLabs side (what to integrate instead of OpenAI)

Replace the OpenAI Realtime client with **ElevenLabs Conversational AI** over WebSocket:

| Step | ElevenLabs resource |
|------|---------------------|
| **Auth for private agents** | Get a **signed URL** — [`GET /v1/convai/conversation/get-signed-url`](https://elevenlabs.io/docs/conversational-ai/api-reference/conversations/get-signed-url) with `agent_id` and `xi-api-key` |
| **Connect** | WebSocket to the returned `signed_url`, or public agent patterns per docs |
| **Protocol** | [Agent WebSockets API reference](https://elevenlabs.io/docs/agents-platform/api-reference/agents-platform/websocket) (message types, audio streaming) |
| **SDKs** | Official clients may wrap WebSocket (check [ElevenLabs docs](https://elevenlabs.io/docs) for your stack — e.g. React / JS libraries under Agents) |

**Base idea:** your bridge calls ElevenLabs with the **server-side API key**, obtains a **signed URL**, opens **`wss://`** to ConvAI, then **maps** Exotel’s incoming/outgoing audio frames to ElevenLabs’ message format (and back).

---

## Architecture (bridge required)

```text
Caller → PSTN → Exotel → Voicebot Applet → wss://YOUR_BRIDGE
                                              │
                    ┌─────────────────────────┴─────────────────────────┐
                    │  Your service (replace Agent-Stream OpenAI      │
                    │  with ElevenLabs ConvAI WebSocket client)         │
                    └─────────────────────────┬─────────────────────────┘
                                              ▼
                    wss://api.elevenlabs.io/.../convai/conversation?...
                    (signed URL from get-signed-url)
```

There is **no** official “paste ElevenLabs URL into Exotel Voicebot” flow—**you** implement the bridge (same role Agent-Stream plays for OpenAI).

---

## When to choose WSS vs SIP

| Prefer **SIP** ([exotel-vsip](../exotel-vsip/)) | Prefer **WSS** (this page) |
|-----------------------------------------------|-----------------------------|
| You want ElevenLabs-managed SIP + phone import | You must keep Voicebot / existing streaming apps |
| PSTN path should avoid your media server | You need custom logic before audio hits the model |
| Ops happy with trunk + ACL / FQDN | You already run a WS service like Agent-Stream |

---

## Security

- Keep **`xi-api-key`** on the **bridge server** only; use **signed URLs** for the browser or untrusted clients per ElevenLabs docs.
- Use **`wss://`** everywhere in production; terminate TLS correctly.

---

## See also

- [SIP trunk Voice AI Connector](../exotel-vsip/elevenlabs-voice-ai-connector.md)
- [ElevenLabs SIP trunking (telephony)](https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking)
- [Exotel dynamic SIP trunking](https://docs.exotel.com/dynamic-sip-trunking/overview)

# Voice AI Ecosystem: ElevenLabs Voice AI Connector (Exotel vSIP)

Connect **[Exotel](https://exotel.com/) vSIP** (Alpha) to **[ElevenLabs](https://elevenlabs.io/) Conversational AI** over **SIP** (not WebSocket). This is the **SIP trunk** arm of the Exotel + ElevenLabs story; the **WebSocket / Voicebot** arm is documented in [`../exotel-wss/`](../exotel-wss/README.md). Overview: [`../README.md`](../README.md).

This pack is part of the Voice AI Ecosystem documentation in [`elevenlabs/README.md`](../../README.md).

| Doc | Use when |
|-----|----------|
| [**QUICKSTART.md**](./QUICKSTART.md) | Short path to a first **outbound** test call (digest pattern). |
| [**elevenlabs-voice-ai-connector.md**](./elevenlabs-voice-ai-connector.md) | You need the **full reference**: both integration patterns, troubleshooting, API queries, and links. |

## Integration patterns (summary)

| Pattern | Direction | Auth | Typical use |
|---------|-----------|------|-------------|
| **Integration 1 — Outbound** | ElevenLabs → Exotel → PSTN | SIP Digest (username/password on both sides) | Voicebot places outbound calls with your Exotel DID as CLI |
| **Integration 2 — Inbound** | PSTN → Exotel DID → ElevenLabs | FQDN (no registration); ACL on ElevenLabs | Callers reach your ElevenLabs agent via your Exotel number |

## Alpha and transport

- **Exotel vSIP is Alpha** — not production-grade SLAs; confirm with Exotel before relying on it in production.
- **UDP is not supported** for this integration path — use **TCP or TLS** only.

## Publishing these docs

These files are the **source of truth** in this repo. To publish:

1. Copy or sync `elevenlabs/integrations/exotel-vsip/` to your internal wiki, docs site, or support portal.
2. Keep **placeholders** in public copies; never paste live API keys or SIP passwords into published HTML/PDF.
3. Update **Last updated** and **Revision history** in the connector reference when you change procedures.

## References (external)

- [Exotel dynamic SIP trunking overview](https://docs.exotel.com/dynamic-sip-trunking/overview)
- [ElevenLabs SIP trunking](https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking)
- [Exotel + ElevenLabs integration guide](https://docs.exotel.com/dynamic-sip-trunking/elevenlabs-and-exotel-sip-trunking-integration-guide-for-voice-ai)

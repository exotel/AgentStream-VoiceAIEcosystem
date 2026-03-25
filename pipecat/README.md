# Voice AI Ecosystem: Pipecat

**[Pipecat](https://pipecat.ai/)** is a voice / multimodal agent framework. **Telephony in Pipecat is not a standalone SIP product** — real-time transport is typically **[Daily](https://www.daily.co/)** (WebRTC) with optional **SIP dial-in / dial-out** on Daily rooms.

| Topic | Doc |
|-------|-----|
| **Exotel vSIP + Pipecat (Daily SIP)** | [`integrations/exotel-vsip/`](./integrations/exotel-vsip/) |
| **Support article (Exotel + Pipecat)** | [`docs/support/exotel-pipecat-sip-trunk.md`](../docs/support/exotel-pipecat-sip-trunk.md) |

## Official Pipecat telephony guides

- [Pipecat telephony — PSTN + Daily SIP](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip) — **PSTN → webhook → Daily room with SIP → bridge to Daily `sip_uri`**
- [Daily PSTN](https://docs.pipecat.ai/guides/telephony/daily-pstn) — Daily-provisioned numbers and webhooks
- [Daily WebRTC dial-in](https://docs.pipecat.ai/guides/telephony/daily-webrtc)

## Publishing

Do not commit live API keys or SIP passwords.

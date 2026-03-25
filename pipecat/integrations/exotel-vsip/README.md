# Voice AI Ecosystem: Pipecat + Exotel vSIP

Connect **[Exotel](https://exotel.com/)** to **[Pipecat](https://pipecat.ai/)** by treating **Exotel** as the **PSTN / SIP carrier** in front of **[Daily](https://www.daily.co/)**, which Pipecat uses for **WebRTC + SIP** transport.

**Pipecat does not expose a “Pipecat SIP trunk” API.** Integration follows the same **orchestration pattern** as [Pipecat’s PSTN + Daily SIP guide](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip): inbound call → your server creates a **Daily room with SIP** → **`on_dialin_ready`** (or equivalent) → **bridge** the carrier leg to Daily’s **`sip_uri`**. For Exotel, use **Exotel’s** documented call-control (Voice APIs / applets / SIP) to connect an active session to that **external SIP URI** (confirm the exact flow with [Exotel](https://docs.exotel.com/) / support).

| Doc | Use when |
|-----|----------|
| [**QUICKSTART.md**](./QUICKSTART.md) | Short checklist: Daily SIP + Exotel trunk steps. |
| [**pipecat-exotel-voice-ai-connector.md**](./pipecat-exotel-voice-ai-connector.md) | Full reference: architecture, inbound vs outbound, codecs, limitations. |

## When you do not need Exotel vSIP

If you use **[Daily PSTN](https://docs.pipecat.ai/guides/telephony/daily-pstn)** (numbers purchased from Daily), PSTN is already terminated by Daily — **no Exotel trunk** is required for that path.

## Exotel alignment (when SIP hits Exotel)

Same rules as other Voice AI packs in this repo: **outbound Exotel** = create trunk → map DID → credentials; **optional** `whitelisted-ips` only for **static** IPs (`mask: 32`); **inbound** uses **destination URI** on the trunk when routing PSTN toward a **fixed** SIP partner; **Flow → Connect** = **`sip:<trunk_sid>`** where applicable.

**Important:** Daily exposes a **per-room** `sip_uri` for SIP dial-in. Static **destination-uris-only** trunk routing (as used for some Voice AI platforms with fixed SIP ingress) **does not replace** the **webhook + bridge** flow from Pipecat’s PSTN guide — unless you add your own **SBC / routing** layer.

## Publishing

Do not commit live API keys or SIP passwords.

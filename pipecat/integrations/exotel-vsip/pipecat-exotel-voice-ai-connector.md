# Voice AI Ecosystem: Pipecat + Exotel vSIP Connector

**Exotel Virtual SIP Trunking ↔ Pipecat (Daily transport)**

| Field | Details |
|-------|---------|
| Document ID | VAIEC-EXO-PC-01 |
| Scope | Pipecat telephony via **Daily SIP** + **Exotel vSIP** where Exotel is the carrier |

---

## What Pipecat is (for telephony)

| Topic | Detail |
|--------|--------|
| Framework | [Pipecat](https://pipecat.ai/) — pipelines, transports, agents |
| Media / SIP | Typically **[Daily](https://www.daily.co/)** — WebRTC + [SIP dial-in / dial-out](https://docs.daily.co/guides/products/dial-in-dial-out/sip) |
| Official SIP + PSTN example | [Pipecat PSTN + Daily SIP guide](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip) — use **Exotel** as the PSTN carrier in the same **orchestration** role when you use Exotel numbers / vSIP |

---

## Two integration paths

### A — Daily PSTN (no Exotel vSIP)

[Pipecat — Daily PSTN](https://docs.pipecat.ai/guides/telephony/daily-pstn): numbers from Daily, webhooks, **`DailyDialinSettings`**. **Exotel** is not in the media path.

### B — Exotel as PSTN / SIP carrier + Daily SIP (Pipecat)

1. **Architecture** matches [Pipecat’s PSTN + Daily SIP guide](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip): inbound PSTN → **your server** creates a Daily room with **`sip`** config → bot joins → **`on_dialin_ready`** → **bridge** the telco leg to Daily’s **`sip_uri`**.  
2. **Sample carrier code** in that upstream guide maps to **Exotel’s** product for **connecting an active call to a SIP URI** — use **Exotel documentation** or support for the exact control plane (Voice APIs, applets, or SIP).  
3. **Exotel vSIP** trunk APIs (**create trunk → map DID → credentials**) apply to the **SIP legs** that **Exotel** terminates with digest auth and edge **`IP:port`** ([Exotel network](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)).

---

## Inbound (conceptual)

| Step | Owner | Notes |
|------|--------|--------|
| PSTN → Exotel | Exotel | Exophone / Flow |
| **HTTP / webhook** to your app | **You** | Same role as the webhook in Pipecat’s PSTN guide |
| Create Daily room + SIP | **You / Daily API** | `sip_uri` appears on room ([Daily SIP Dial-in](https://docs.daily.co/guides/products/dial-in-dial-out/sip)) |
| Bridge carrier call → Daily `sip_uri` | **You** via **Exotel** | Same intent as redirecting the answered PSTN leg to a **SIP URI** in Pipecat’s sample (implement with Exotel Voice APIs / applets) |

**Static destination URI** on an Exotel trunk (toward a **fixed** partner SIP host) is used for platforms with **one** SIP ingress. **Daily** normally uses a **per-room** `sip_uri`, so the **dynamic bridge** from Pipecat’s PSTN flow is the usual pattern.

**Flow → Connect:** when Exotel docs prescribe **`sip:<trunk_sid>`** in **Dial whom** for routing to a trunk, use the **`trunk_sid`** from **create trunk** (not a full URI).

---

## Outbound (conceptual)

| Step | Owner | Notes |
|------|--------|--------|
| Bot / room initiates dial-out | **Daily** | `start_dialout` / SIP dial-out ([Daily REST](https://docs.daily.co/reference/rest-api/rooms/dialout/start)) |
| SIP to Exotel edge | **Daily → Exotel** | Trunk must allow **digest** matching **`POST .../credentials`** |
| Exotel → PSTN | Exotel | **Outbound** trunk setup: **create trunk → map DID → credentials** |

**Optional:** `POST .../whitelisted-ips` **only** if the **remote peer** (e.g. Daily’s SIP egress) uses a **published static IP** — **`mask: 32`**.

---

## Codecs and media

Daily documents **PCMU, PCMA, G722, Opus** for SIP ([Daily SIP](https://docs.daily.co/guides/products/dial-in-dial-out/sip)). Exotel PSTN interop is typically **G.711**-friendly — validate **SDP** on a test call.

---

## Exotel API reference (same as other Voice AI packs)

| Outbound SIP | Create trunk → map DID → credentials |
| Optional ACL | `whitelisted-ips` only for **static** IPs, `mask: 32` |
| Inbound SIP (fixed partner) | `destination-uris` on trunk; **Connect** **`sip:<trunk_sid>`** where applicable |

Shared curls: [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

---

## References

| Resource | URL |
|----------|-----|
| Pipecat — PSTN + Daily SIP | https://docs.pipecat.ai/guides/telephony/twilio-daily-sip |
| Pipecat — Daily PSTN | https://docs.pipecat.ai/guides/telephony/daily-pstn |
| Daily — SIP dial-in / dial-out | https://docs.daily.co/guides/products/dial-in-dial-out/sip |
| Pipecat examples (phone) | https://github.com/pipecat-ai/pipecat-examples/tree/main/phone-chatbot |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |

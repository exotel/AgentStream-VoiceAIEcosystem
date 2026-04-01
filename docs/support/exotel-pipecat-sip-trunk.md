# Connect Exotel SIP trunking to Pipecat (via Daily)

This guide aligns **Exotel SIP trunking** with **[Pipecat](https://pipecat.ai/)** using the same **Exotel** patterns as the other Voice AI integrations in this repository: **outbound** = create trunk → map DID → credentials; **optional ACL** = static IPs only (`mask: 32`), no CIDR ranges on the trunk; **inbound** = destination URI on the trunk when routing toward a **fixed** SIP partner; **Connect** = **`sip:<trunk_sid>`** where Exotel’s product uses that form.

> **Applicability:** **API/engineering-driven** (Pipecat orchestration + Daily rooms/SIP). Inbound is typically a **dynamic** Daily `sip_uri` bridge, not a single static destination URI.

**Pipecat is not a SIP trunk provider.** Pipecat agents typically use **[Daily](https://www.daily.co/)** for **WebRTC** and **[SIP dial-in / dial-out](https://docs.daily.co/guides/products/dial-in-dial-out/sip)**. Pipecat publishes a **[PSTN + Daily SIP walkthrough](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip)** (upstream doc path). Treat **Exotel** as the **PSTN carrier**: your **webhook server** still creates a **Daily room with SIP** and bridges the live call to Daily’s **`sip_uri`** after **`on_dialin_ready`**.

**Engineering detail:** [`pipecat/integrations/exotel-vsip/pipecat-exotel-voice-ai-connector.md`](../../pipecat/integrations/exotel-vsip/pipecat-exotel-voice-ai-connector.md)
**Quickstart:** [`pipecat/integrations/exotel-vsip/QUICKSTART.md`](../../pipecat/integrations/exotel-vsip/QUICKSTART.md)

---

## What Pipecat + Daily expect

| Topic | Detail |
|--------|--------|
| SIP on rooms | [Daily SIP](https://docs.daily.co/guides/products/dial-in-dial-out/sip) — `sip_uri` on the room, `dialin-ready` / Pipecat **`on_dialin_ready`** |
| PSTN example | [Pipecat PSTN + Daily SIP guide](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip) — webhook → Daily room → forward to **`sip_endpoint`** |
| PSTN without Exotel | [Daily PSTN](https://docs.pipecat.ai/guides/telephony/daily-pstn) — Daily-provisioned numbers |

---

## What you will set up

| Direction | Summary |
|-----------|---------|
| **Inbound (typical)** | PSTN → Exotel → **your webhook** → Daily room + SIP → **bridge** to Daily **`sip_uri`** (same **shape** as Pipecat’s PSTN guide; use **Exotel** call-control APIs to attach the live leg to **`sip_uri`**) |
| **Outbound** | Daily **SIP dial-out** / `start_dialout` → **Exotel edge `IP:port`** (digest) → PSTN — **Exotel** trunk + DID + **`POST .../credentials`** |

---

## Part A — Pipecat + Daily

1. Follow **[Pipecat’s PSTN + Daily SIP guide](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip)** to implement **`DailyTransport`**, **`on_dialin_ready`**, and bridging to **`sip_endpoint`**.  
2. Replace the **sample carrier** control APIs from that guide with **Exotel’s** documented way to **connect the active carrier leg** to an **external SIP URI** (your Daily `sip_uri` for that session). Confirm details with [Exotel](https://docs.exotel.com/) if needed.  
3. For **outbound**, use Daily’s **dial-out** / **SIP dial-out** toward **Exotel** as the next SIP hop, then complete **Part B**.

**Note:** Daily exposes a **per-room** `sip_uri`. The **static trunk destination** pattern (single SIP host for all calls) matches some Voice AI platforms but **differs** from typical **Daily** room SIP — prefer the **dynamic bridge** unless you operate an **SBC** or fixed ingress.

---

## Part B — Exotel (outbound SIP toward PSTN)

When **Daily** (or your SIP client) sends media to **Exotel** to reach PSTN:

1. **Create trunk**  
2. **Map DID** — `POST .../trunks/{TRUNK_SID}/phone-numbers`  
3. **`POST .../credentials`** — `user_name`, `password` (digest aligned with the SIP client leg)

**Optional:** `POST .../whitelisted-ips` **only** if Daily (or your egress) publishes a **single static IP** you must allow. Use **`mask: 32`**.

---

## Part C — Exotel (inbound PSTN toward a fixed SIP host)

Use **only** when your **partner SIP** destination is **fixed** (not the usual **per-room Daily `sip_uri`** case):

1. **`POST .../destination-uris`** on the trunk toward that host/port/transport.  
2. **Flow → Connect** applet: **Dial whom** = **`sip:<trunk_sid>`** (the **`trunk_sid`** from Exotel **create trunk** — not a full SIP URI).  
3. Map the Exophone to the Flow.

---

## Exotel API snippets

**Authentication:** `https://API_KEY:API_TOKEN@api.in.exotel.com/...`  
**Rate limit:** **200 requests/minute** on trunk configuration APIs.

Full reference: [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md)

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| Call never reaches Daily | Exotel **bridge** to the **current** `sip_uri`; room **SIP** enabled; **`dialin-ready`** / `on_dialin_ready` |
| One-way audio / codec mismatch | **SDP** codecs — Daily **PCMU/PCMA** vs Exotel PSTN leg |
| Outbound fails | Trunk **credentials**; **Exotel edge `IP:port`** and transport; DID on trunk |
| Connect misrouted | **`sip:<trunk_sid>`** only in **Dial whom** (when using that applet pattern) |

---

## Official references

| Resource | URL |
|----------|-----|
| Daily dashboard | https://dashboard.daily.co/ |
| Pipecat — PSTN + Daily SIP | https://docs.pipecat.ai/guides/telephony/twilio-daily-sip |
| Pipecat — Daily PSTN | https://docs.pipecat.ai/guides/telephony/daily-pstn |
| Daily — SIP | https://docs.daily.co/guides/products/dial-in-dial-out/sip |
| Pipecat phone example | https://github.com/pipecat-ai/pipecat-examples/tree/main/phone-chatbot |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |

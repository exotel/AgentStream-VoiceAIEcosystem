# Connect Exotel SIP trunking to Bolna Voice AI

This guide aligns **Exotel SIP trunking** with **[Bolna AI](https://www.bolna.ai/)** using the same patterns as the other Voice AI integrations in this repository: **outbound Exotel** = create trunk → map DID → credentials; **inbound** = destination URI on the trunk; **Connect** = **`sip:<trunk_sid>`**; **ACL** = static IPs only (`mask: 32`), no CIDR ranges on the trunk.

**GitHub repo (reference):** https://github.com/exotel/AgentStream-VoiceAIEcosystem

> **Applicability:** **Hybrid** — BYOT is **API/config-driven** (SIP trunk objects) and may also have portal steps depending on account access (SIP is Beta).

**Outbound SIP is supported.** With BYOT, Bolna **places outbound PSTN calls over SIP** through your trunk: it resolves `from_number` to your trunk, then signals to your **gateway** (Exotel **edge IP:port**) using **userpass** (or **ip-based**) auth. That is the flow described in [Make Outbound Calls via Your SIP Trunk](https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls). **Part B** below is exactly what Exotel needs on the **carrier** side for that outbound SIP leg.

Bolna also offers a **dashboard connector** for Exotel (REST API link) — see [Connect Your Exotel Account to Bolna](https://www.bolna.ai/docs/exotel-connect-provider). This article focuses on **SIP BYOT** where you configure **Exotel SIP trunking** and a **Bolna SIP trunk** together.

> **Bolna:** SIP trunking is **Beta**; **SRTP is not supported** (plain RTP). See [Bring Your Own SIP Trunk](https://www.bolna.ai/docs/sip-trunking/introduction).  
> **Engineering detail:** [`bolna/integrations/exotel-vsip/bolna-exotel-voice-ai-connector.md`](../../bolna/integrations/exotel-vsip/bolna-exotel-voice-ai-connector.md)
> **Quickstart:** [`bolna/integrations/exotel-vsip/QUICKSTART.md`](../../bolna/integrations/exotel-vsip/QUICKSTART.md)

---

## What Bolna expects (BYOT)


| Topic               | Detail                                                                                                                                                                                         |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create trunk        | [Create SIP Trunk API](https://www.bolna.ai/docs/api-reference/sip-trunks/create) — `POST https://api.bolna.ai/sip-trunks/trunks` with Bearer token                                            |
| Auth                | `userpass` (username/password) or `ip-based` with IP identifiers on Bolna                                                                                                                      |
| Gateway             | Points to your carrier — for Exotel, use **Exotel edge `IP:port`** from [Exotel network doc](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)                  |
| Inbound origination | Carrier sends traffic to **`sip:13.200.45.61:5060`** per [Receive Inbound Calls via Your SIP Trunk](https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls) — confirm in current Bolna docs |
| Outbound calls      | [Make Outbound Calls via Your SIP Trunk](https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls) — agent `telephony_provider`: `sip-trunk`, `from_number` on trunk                         |


---

## What you will set up


| Direction    | Summary                                                                                                  |
| ------------ | -------------------------------------------------------------------------------------------------------- |
| **Outbound** | Bolna → SIP digest → Exotel edge → PSTN                                                                  |
| **Inbound**  | PSTN → Exotel DID → trunk **destination URI** toward Bolna (`13.200.45.61:5060` per Bolna) → Bolna agent |


---

## Part A — Bolna

1. Obtain **SIP trunk / BYOT** access ([enterprise@bolna.ai](mailto:enterprise@bolna.ai) if required).
2. **Create SIP trunk** with gateway = **Exotel edge IP:port** and `userpass` matching Exotel `POST .../credentials` — this is what enables **outbound SIP** from Bolna → Exotel → PSTN.
3. **Add phone numbers** to the Bolna trunk (required for `from_number` on outbound calls).
4. Set agent `telephony_provider` to `sip-trunk`, then place outbound calls with the [call API](https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls) (`from_number` must be a DID on the trunk).
5. For **inbound** only: map numbers to agents per [inbound BYOT](https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls) and ensure Exotel routes to **`sip:13.200.45.61:5060`** per Bolna (Part C).

**Alternative:** Use [Exotel provider connection](https://www.bolna.ai/docs/exotel-connect-provider) in Bolna **Providers** instead of manual SIP BYOT when that product path fits.

---

## Part B — Exotel (outbound SIP)

1. **Create trunk**
2. **Map DID** — `POST .../trunks/{TRUNK_SID}/phone-numbers`
3. `POST .../credentials` — `user_name`, `password` (same as Bolna `auth_username` / `auth_password` for `userpass`)

**Optional:** `POST .../whitelisted-ips` **only** if Bolna publishes a **single static IP** you must allow on Exotel (Bolna docs reference **13.200.45.61** in troubleshooting — **always confirm** with current Bolna documentation). Use **`mask: 32`**.

---

## Part C — Exotel (inbound SIP)

1. `POST .../destination-uris` on the trunk so **inbound** PSTN is routed toward Bolna’s SIP entry (host/port per Bolna — typically aligned with **`13.200.45.61:5060`**; format per Exotel API).
2. **Flow → Connect** applet: **Dial whom** = **`sip:<trunk_sid>`** (the `trunk_sid` from Exotel **create trunk** — not a full SIP URI).
3. Map the Exophone to the Flow.

---

## Exotel API snippets

**Authentication:** `https://API_KEY:API_TOKEN@api.in.exotel.com/...`  
**Rate limit:** **200 requests/minute** on trunk configuration APIs.

Full reference: [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md)

---

## Troubleshooting


| Symptom                  | What to check                                                       |
| ------------------------ | ------------------------------------------------------------------- |
| No media / failed SDP    | **SRTP** — Bolna does not support SRTP; use plain RTP               |
| Outbound fails           | Trunk `is_active` on Bolna; gateway IP:port; digest match           |
| Inbound never hits Bolna | Exotel **destination URI**; Bolna `inbound_enabled`; number mapping |
| Connect misrouted        | **`sip:<trunk_sid>`** only in Dial whom                             |


---

## Official references


| Resource                      | URL                                                                                                                                                                  |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bolna BYOT setup (start here) | [https://www.bolna.ai/byot-setup](https://www.bolna.ai/byot-setup)                                                                                                   |
| Bolna SIP introduction        | [https://www.bolna.ai/docs/sip-trunking/introduction](https://www.bolna.ai/docs/sip-trunking/introduction)                                                           |
| Bolna + Exotel (dashboard)    | [https://www.bolna.ai/docs/exotel-connect-provider](https://www.bolna.ai/docs/exotel-connect-provider)                                                               |
| Bolna Create SIP Trunk        | [https://www.bolna.ai/docs/api-reference/sip-trunks/create](https://www.bolna.ai/docs/api-reference/sip-trunks/create)                                               |
| Bolna BYOT outbound           | [https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls](https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls)                                             |
| Bolna BYOT inbound            | [https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls](https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls)                                               |
| Exotel SIP API                | [https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference](https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference) |



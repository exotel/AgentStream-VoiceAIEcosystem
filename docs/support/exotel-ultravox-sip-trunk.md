# Connect Exotel SIP trunking to Ultravox

This guide aligns **Exotel SIP trunking** with **[Ultravox](https://www.ultravox.ai/)** using the same patterns as the other Voice AI integrations in this repository: **outbound** = create trunk → map DID → credentials; **optional ACL** = static IPs only (`mask: 32`), no CIDR ranges on the Exotel trunk; **inbound** = destination URI on the trunk; **Connect** = **`sip:<trunk_sid>`** where Exotel’s product uses that form.

> **Applicability:** **Hybrid** — Ultravox supports SIP (allowlist/registration) and also a native **Exotel streaming** medium; choose one path.

Ultravox documents **two** relevant approaches: a **native `exotel` call medium** (Voice Streaming — see [Telephony platforms](https://docs.ultravox.ai/telephony/telephony-platforms) and Exotel Voice Streaming docs), and **generic SIP** ([SIP guide](https://docs.ultravox.ai/telephony/sip)). **This article focuses on SIP + Exotel SIP trunking.** For the native medium, use Ultravox + Exotel streaming docs directly.

**Engineering detail:** [`ultravox/integrations/exotel-vsip/ultravox-exotel-voice-ai-connector.md`](../../ultravox/integrations/exotel-vsip/ultravox-exotel-voice-ai-connector.md)
**Quickstart:** [`ultravox/integrations/exotel-vsip/QUICKSTART.md`](../../ultravox/integrations/exotel-vsip/QUICKSTART.md)

---

## What Ultravox expects (SIP)

| Topic | Detail |
|--------|--------|
| Account SIP | [GET `/api/sip`](https://docs.ultravox.ai/api-reference/sip/sip-get) — account SIP **`domain`**, **`allowedCidrRanges`**, agent patterns |
| Incoming | **IP allowlisting** ([`allowedCidrRanges`](https://docs.ultravox.ai/telephony/sip#ip-allowlisting)) — CIDR entries include **`/32`** for one IPv4 — or **SIP registration** ([SIP guide](https://docs.ultravox.ai/telephony/sip)) |
| INVITE pattern | Default `agent_{agent_id}@{domain}`; override with regex per agent ([incoming](https://docs.ultravox.ai/telephony/sip#incoming-sip-calls)) |
| Outgoing | Create call with **`medium.sip.outgoing`** — `to`, `from`, optional `username` / `password` ([outgoing SIP](https://docs.ultravox.ai/telephony/sip#outgoing-sip-calls)) |
| Codecs / transport | [Supported codecs](https://docs.ultravox.ai/telephony/sip#supported-codecs). **UDP** default; **TCP/TLS** via `;transport=` in SIP URI ([transport](https://docs.ultravox.ai/telephony/sip#supported-transport-protocols)) |
| Billing | SIP minutes billed separately from agent minutes — [SIP billing](https://docs.ultravox.ai/telephony/sip#sip-billing) |

---

## What you will set up (SIP + Exotel SIP trunking)

| Direction | Summary |
|-----------|---------|
| **Outbound** | Ultravox → SIP → Exotel edge (digest) → PSTN |
| **Inbound** | PSTN → Exotel DID → trunk **destination URI** toward Ultravox (`domain` from GET `/api/sip`) → agent |

---

## Part A — Ultravox

1. Create an **agent** (required before SIP ingress — [SIP guide](https://docs.ultravox.ai/telephony/sip)).  
2. Call [GET `/api/sip`](https://docs.ultravox.ai/api-reference/sip/sip-get) and record **`domain`**.  
3. **Inbound:** Update [SIP configuration](https://docs.ultravox.ai/api-reference/sip/sip-partial-update) with **`allowedCidrRanges`** including Exotel signalling IPs (from [Exotel network](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)), using **`/32`** per host. **Or** configure **SIP registration** if that matches your deployment ([registration](https://docs.ultravox.ai/telephony/sip#sip-registration)).  
4. **Outbound:** Place calls using **`medium.sip.outgoing`** toward your Exotel SIP endpoint (`to` / auth per [outgoing SIP](https://docs.ultravox.ai/telephony/sip#outgoing-sip-calls)).

---

## Part B — Exotel (outbound SIP)

1. **Create trunk**  
2. **Map DID** — `POST .../trunks/{TRUNK_SID}/phone-numbers`  
3. **`POST .../credentials`** — `user_name`, `password` (same as Ultravox `username` / `password` when using digest auth)

**Optional:** `POST .../whitelisted-ips` **only** if Ultravox publishes a **fixed static egress IP** to allow — **`mask: 32`**, one POST per IP.

---

## Part C — Exotel (inbound SIP)

1. **`POST .../destination-uris`** on the trunk toward Ultravox’s SIP endpoint (host/port/transport from Ultravox + testing).  
2. **Flow → Connect** applet: **Dial whom** = **`sip:<trunk_sid>`** (the **`trunk_sid`** from Exotel **create trunk** — not a full SIP URI).  
3. Map the Exophone to the Flow.

---

## Native Exotel medium (not SIP trunking)

If you use the **`exotel`** call medium (`"exotel": {}`) plus Voice Streaming instead of BYOT SIP, see [Telephony platforms — Exotel](https://docs.ultravox.ai/telephony/telephony-platforms) and Exotel’s Voice Streaming API documentation — no SIP trunk steps required for that path.

---

## Exotel API snippets

**Authentication:** `https://API_KEY:API_TOKEN@api.in.exotel.com/...`  
**Rate limit:** **200 requests/minute** on trunk configuration APIs.

Full reference: [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md)

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| INVITE rejected at Ultravox | **`allowedCidrRanges`** includes Exotel signalling **/32**; agent pattern matches `To` URI |
| Codec failure | Codec list in [SIP guide](https://docs.ultravox.ai/telephony/sip#supported-codecs) — only listed codecs work |
| Outbound auth failure | Trunk credentials; Exotel edge **IP:port**; `from` allowed on trunk |
| Connect misrouted | **`sip:<trunk_sid>`** only in Dial whom |

---

## Official references

| Resource | URL |
|----------|-----|
| Ultravox console | https://app.ultravox.ai/ |
| Ultravox SIP guide | https://docs.ultravox.ai/telephony/sip |
| Ultravox telephony platforms | https://docs.ultravox.ai/telephony/telephony-platforms |
| Ultravox GET SIP config | https://docs.ultravox.ai/api-reference/sip/sip-get |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |

# Voice AI Ecosystem: Ultravox + Exotel vSIP Connector

**Exotel Virtual SIP Trunking ↔ Ultravox Realtime**

| Field | Details |
|-------|---------|
| Document ID | VAIEC-EXO-UV-01 |
| Scope | SIP BYOT + optional native Exotel medium |

---

## Two integration paths

### A — Native Exotel call medium (Voice Streaming)

Ultravox supports a dedicated call medium **`"exotel": {}`** with streaming via Exotel’s **Voice Streaming** product ([Telephony platforms](https://docs.ultravox.ai/telephony/telephony-platforms)). Credential **import** is **not** listed for Exotel in that table — integration is **manual** relative to the fully guided native flows for some other providers. Follow Ultravox **and** Exotel Voice Streaming documentation together.

### B — SIP BYOT (Exotel vSIP + Ultravox SIP)

Use when you want **standard SIP** between **Exotel** (PSTN) and **Ultravox** ([SIP guide](https://docs.ultravox.ai/telephony/sip)).

| Direction | Ultravox | Exotel |
|-----------|----------|--------|
| **Inbound** (carrier → Ultravox) | Allowlist Exotel signalling sources in **`allowedCidrRanges`**, or use **SIP registration** | Trunk **`destination-uris`** toward Ultravox; **Connect** **`sip:<trunk_sid>`** |
| **Outbound** (Ultravox → carrier → PSTN) | **`medium.sip.outgoing`** with `to`, `from`, optional `username` / `password` | **Create trunk → map DID → credentials** matching digest |

SIP infrastructure for Ultravox is described in-product as backed by their SIP partner; SIP calls incur **additional SIP minute** charges — [SIP guide — billing](https://docs.ultravox.ai/telephony/sip#sip-billing).

---

## Ultravox SIP (official behaviour)

### Account domain

[GET `/api/sip`](https://docs.ultravox.ai/api-reference/sip/sip-get) returns **`domain`** and allowlist settings. Default routing uses `agent_{agent_id}@{domain}` for INVITEs; **regex** overrides per agent are supported ([incoming SIP](https://docs.ultravox.ai/telephony/sip#incoming-sip-calls)).

### IP allowlisting (incoming)

Use [SIP partial update](https://docs.ultravox.ai/api-reference/sip/sip-partial-update) to set **`allowedCidrRanges`** (IPv4 CIDR strings). A **single IP** is **`x.x.x.x/32`** ([SIP guide](https://docs.ultravox.ai/telephony/sip#ip-allowlisting)).

### SIP registration (incoming)

[Create registration](https://docs.ultravox.ai/api-reference/sip/sip-registrations-create) with `username`, `password`, `proxy` — Ultravox registers as a client to **your** SIP server (use when your PBX / carrier expects registration).

### Outgoing SIP

Create calls with **`medium.sip.outgoing`** — `to`, `from`, optional `username` / `password` ([outgoing SIP](https://docs.ultravox.ai/telephony/sip#outgoing-sip-calls)).

### Codecs and transport

Supported codecs and **UDP / TCP / TLS** in SIP URI are listed under [Supported Transport Protocols](https://docs.ultravox.ai/telephony/sip#supported-transport-protocols) and [Supported Codecs](https://docs.ultravox.ai/telephony/sip#supported-codecs). Using an unsupported codec **fails** the call.

---

## Exotel API reference (same as other Voice AI packs)

| Outbound SIP | Create trunk → map DID → credentials |
| Optional ACL | `whitelisted-ips` only for **static** IPs, `mask: 32` |
| Inbound SIP | `destination-uris` on trunk toward Ultravox host |

Shared curls: [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

---

## References

| Resource | URL |
|----------|-----|
| Ultravox SIP guide | https://docs.ultravox.ai/telephony/sip |
| Telephony platforms (incl. `exotel` medium) | https://docs.ultravox.ai/telephony/telephony-platforms |
| Telephony overview | https://docs.ultravox.ai/telephony/overview |
| GET SIP config | https://docs.ultravox.ai/api-reference/sip/sip-get |
| SIP partial update | https://docs.ultravox.ai/api-reference/sip/sip-partial-update |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |
| Exotel network / firewall | https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration |

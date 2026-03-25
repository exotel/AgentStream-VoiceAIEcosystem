# Quickstart: Exotel vSIP + Ultravox (SIP)

**Prerequisites:** Ultravox account, Exotel vSIP + API credentials, agent created in Ultravox.

**Ultravox SIP:** [SIP guide](https://docs.ultravox.ai/telephony/sip) — incoming via **IP allowlist** ([`allowedCidrRanges`](https://docs.ultravox.ai/api-reference/sip/sip-partial-update)) or **SIP registration**; outgoing via `medium.sip.outgoing` ([Create call](https://docs.ultravox.ai/api-reference/calls/calls-post)). Fetch your account SIP **`domain`** with [GET `/api/sip`](https://docs.ultravox.ai/api-reference/sip/sip-get).

**Exotel:** **Outbound** = create trunk → map DID → `POST .../credentials`. **Inbound** = `POST .../destination-uris` toward Ultravox; **Flow → Connect** → **`sip:<trunk_sid>`**.

---

## 1 — Ultravox: read SIP domain

```http
GET https://api.ultravox.ai/api/sip
X-API-Key: <YOUR_KEY>
```

Note **`domain`** — default INVITE target pattern is `agent_{agent_id}@{domain}` ([SIP guide](https://docs.ultravox.ai/telephony/sip)).

---

## 2 — Ultravox: allowlist Exotel signaling (inbound SIP)

Add Exotel’s **SIP signalling IP:port** / ranges from [Exotel network](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration) to Ultravox **`allowedCidrRanges`** using [SIP partial update](https://docs.ultravox.ai/api-reference/sip/sip-partial-update). Use **`x.x.x.x/32`** for a single IPv4 address (Ultravox documents this pattern in the [SIP guide](https://docs.ultravox.ai/telephony/sip)).

---

## 3 — Exotel: trunk + credentials (outbound / termination)

```bash
# Create trunk → map DID → POST .../credentials
# See shared snippets
```

Digest must match what you pass in Ultravox **`medium.sip.outgoing`** (`username` / `password`) when Exotel is the next hop.

---

## 4 — Exotel: inbound (PSTN → Ultravox)

`POST .../destination-uris` on the trunk toward Ultravox’s SIP host (host/port/transport from Ultravox + your testing). **Connect** applet: **`sip:<trunk_sid>`** in **Dial whom**.

---

## 5 — Alternative: SIP registration

If you use **SIP registration** (Ultravox registers to your PBX), configure the **Exotel-side user** and map per [SIP guide — registration](https://docs.ultravox.ai/telephony/sip#sip-registration) and [create registration API](https://docs.ultravox.ai/api-reference/sip/sip-registrations-create).

---

## Native Exotel medium (non–SIP-trunk)

For **`"exotel": {}`** + Voice Streaming (no vSIP BYOT), see [Telephony platforms — Exotel](https://docs.ultravox.ai/telephony/telephony-platforms) and Exotel Voice Streaming docs.

---

## Shared curls

[`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

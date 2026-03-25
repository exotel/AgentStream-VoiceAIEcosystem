# Voice AI Ecosystem: Bolna AI + Exotel vSIP Connector

**Exotel Virtual SIP Trunking ↔ Bolna Voice AI**

| Field | Details |
|-------|---------|
| Document ID | VAIEC-EXO-BL-01 |
| Scope | SIP BYOT + optional Exotel native provider link |

---

## Two integration paths

### A — Exotel provider in Bolna (dashboard)

Bolna can link **Exotel REST API** credentials so agents use your Exotel numbers and billing. See [Connect Your Exotel Account to Bolna](https://www.bolna.ai/docs/exotel-connect-provider) — fields: `API_KEY`, `API_TOKEN`, `ACCOUNT_SID`, `DOMAIN`, `PHONE_NUMBER`.

This path does **not** replace vSIP trunk APIs when you need raw SIP control; use it when Bolna’s productized connector fits.

### B — SIP BYOT (Exotel vSIP + Bolna SIP trunk API)

1. **Exotel:** `POST` create trunk → map DID → `POST .../credentials` (same digest on both sides for `userpass`).  
2. **Bolna:** `POST https://api.bolna.ai/sip-trunks/trunks` with `gateways[]` pointing to **Exotel edge `IP:port`**, `auth_type: userpass`, `auth_username` / `auth_password` matching Exotel.  
3. **Bolna:** Add DIDs to the trunk; set agent `telephony_provider` to `sip-trunk`; place calls via [call API](https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls).

**Bolna limitations (from docs):** SIP trunking **Beta**; **no SRTP** — plain RTP only; contact [enterprise@bolna.ai](mailto:enterprise@bolna.ai) for access.

---

## Inbound PSTN → Bolna (BYOT)

Per [Receive Inbound Calls via Your SIP Trunk](https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls):

1. Provider routes DIDs to **`sip:13.200.45.61:5060`** (Bolna SIP server).  
2. On **Exotel**, set **destination URI** on the trunk toward that target (host/port/transport per Exotel API and Bolna).  
3. **Exotel Flow → Connect:** **`sip:<trunk_sid>`** in **Dial whom** (`trunk_sid` from Exotel create-trunk response).  
4. On **Bolna:** `inbound_enabled: true`, numbers on trunk, [map number to agent](https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls).

**IP allowlisting:** Bolna troubleshooting references **13.200.45.61** for reachability to provider RTP; for **Exotel** `whitelisted-ips`, use **static** entries with **`mask: 32`** only (no CIDR range on trunk).

---

## Outbound (Bolna → Exotel → PSTN)

**Outbound SIP is the standard BYOT path:** Bolna’s stack sends the call to your configured **gateway** (Exotel edge) over SIP using the trunk auth — not “HTTP-only” telephony.

Per [Make Outbound Calls via Your SIP Trunk](https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls):

- Patch agent: `"telephony_provider": "sip-trunk"`.  
- `POST https://api.bolna.ai/call` with `from_number` = DID on trunk.  
- If calls fail, verify trunk `is_active`, gateway/credentials, and **disable SRTP** on the Exotel side if forced.

---

## Exotel API reference (same as other Voice AI packs)

| Outbound SIP | Create trunk → map DID → credentials |
| Optional ACL | `whitelisted-ips` only for **static** IPs, `mask: 32` |
| Inbound SIP | `destination-uris` on trunk toward Bolna |

Shared curls: [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

---

## References

| Resource | URL |
|----------|-----|
| Bolna SIP introduction | https://www.bolna.ai/docs/sip-trunking/introduction |
| Bolna Exotel provider | https://www.bolna.ai/docs/exotel-connect-provider |
| Create SIP trunk API | https://www.bolna.ai/docs/api-reference/sip-trunks/create |
| BYOT outbound | https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls |
| BYOT inbound | https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |

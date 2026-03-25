# Quickstart: Exotel vSIP + Vapi (BYO SIP trunk)

**Prerequisites:** Exotel vSIP, KYC, Exophone (E.164), [Vapi](https://dashboard.vapi.ai/) account with **private API key**.

**Vapi SIP:** [SIP trunking](https://docs.vapi.ai/advanced/sip/sip-trunk) — `byo-sip-trunk` credential + `byo-phone-number`. **Allowlist** Vapi’s two SBC IPs on Exotel ([networking](https://docs.vapi.ai/advanced/sip/sip-networking)).

**Exotel:** **Outbound** = create trunk → map DID → `POST .../credentials` → **`whitelisted-ips`** for **both** Vapi IPs (`mask: 32`). **Inbound** = `POST .../destination-uris` toward **`sip.vapi.ai`** (port/transport per Vapi) → **Connect** → **`sip:<trunk_sid>`**.

---

## 1 — Exotel: trunk + DID + digest

Use shared snippets: [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

Note **`user_name` / `password`** — reuse in Vapi **`outboundAuthenticationPlan`**.

---

## 2 — Exotel: whitelist Vapi SBC (both IPs)

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "44.229.228.186", "mask": 32}'

curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "44.238.177.138", "mask": 32}'
```

---

## 3 — Vapi: resolve Exotel edge to IPv4

Vapi **`gateways[].ip`** must be **IPv4** ([troubleshoot](https://docs.vapi.ai/advanced/sip/troubleshoot-sip-trunk-credential-errors)). Resolve Exotel’s edge host to an address, then use **`IP:port`** and **`outboundProtocol`** per Exotel.

---

## 4 — Vapi: credential + phone number

`POST https://api.vapi.ai/credential` (`byo-sip-trunk`) and `POST https://api.vapi.ai/phone-number` (`byo-phone-number`) — see [`vapi-exotel-voice-ai-connector.md`](./vapi-exotel-voice-ai-connector.md).

---

## 5 — Inbound (optional)

`POST .../destination-uris` toward Vapi (example shape in [`exotel-vapi-sip-trunk.md`](../../../docs/support/exotel-vapi-sip-trunk.md)); Flow **Connect** **`sip:<trunk_sid>`**.

---

## Shared curls

[`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

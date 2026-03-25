# Voice AI Ecosystem: Retell AI + Exotel vSIP Connector

**Exotel Virtual SIP Trunking ↔ Retell AI ([Custom telephony](https://docs.retellai.com/deploy/custom-telephony))**

| Field | Details |
|-------|---------|
| Document ID | VAIEC-EXO-RT-01 |
| Scope | Elastic SIP with Exotel (India PSTN) |

> **Exotel trunk ACL:** **`whitelisted-ips`** accepts **single static IPs** (`mask: 32`). **CIDR ranges are not supported** on the trunk — add **one POST per static IP** if your provider gives multiple fixed addresses, or use **digest** and confirm with Exotel.

---

## Retell (official)

- **SIP server:** `sip:sip.retellai.com` + `;transport=tcp` / `tls` / `udp` — [Custom telephony](https://docs.retellai.com/deploy/custom-telephony)
- Retell publishes **IP ranges** for carriers; mapping those to Exotel ACL may require **per-IP** entries or coordination with Exotel — not automatic CIDR on trunk.

---

## Outbound vs inbound (Exotel)

| Flow | APIs |
|------|------|
| **Outbound SIP** | 1. Create trunk 2. Map DID 3. `POST .../credentials`. Optional: `whitelisted-ips` **only** for **static** provider egress IP(s), `mask: 32`. |
| **Inbound SIP** | `POST .../destination-uris` on trunk toward Retell. **Flow → Connect:** **`sip:<trunk_sid>`** in Dial whom (`trunk_sid` from create trunk). |

---

## Exotel API order

1. Create trunk  
2. Map DID  
3. Credentials (digest)  
4. *(Optional)* Whitelisted IPs — static IP only, `mask: 32`  
5. *(Inbound)* Destination URIs toward `sip.retellai.com:…;transport=…`  

**No `trunk_external_alias` in this connector** — removed from recommended path.

---

## Credentials

```bash
curl -s -X POST \
  "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "<SIP_USER>",
    "password": "<SIP_PASS>",
    "friendly_name": "retell"
  }'
```

---

## Destination URI (inbound)

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "sip.retellai.com:5060;transport=tcp" }
    ]
  }'
```

---

## Allowlisting

| Direction | Notes |
|-----------|--------|
| Exotel ← Retell | Optional **static** Retell egress IPs on trunk (`mask: 32` each). Retell doc ranges are not a direct CIDR map on Exotel trunk. |
| Retell ← Exotel | Allow **Exotel signaling IPs** on Retell side if required — [Exotel network](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration) |

---

## Dial to SIP URI (Method 2)

[Register Phone Call](https://docs.retellai.com/api-references/register-phone-call) → `sip:{call_id}@sip.retellai.com` within 5 minutes — [Custom telephony](https://docs.retellai.com/deploy/custom-telephony).

---

## References

| Resource | URL |
|----------|-----|
| Retell custom telephony | https://docs.retellai.com/deploy/custom-telephony |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |
| Shared curls | [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md) |

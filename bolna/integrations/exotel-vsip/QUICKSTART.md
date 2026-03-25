# Quickstart: Exotel vSIP + Bolna AI (BYOT SIP)

**Outbound Exotel (minimal):** create trunk → map DID → `POST .../credentials`.  
**Bolna:** create SIP trunk with **gateway** = Exotel **edge `IP:port`**, **`auth_type`: `userpass`**, credentials **matching** Exotel.

**Prerequisites:** Exotel vSIP, KYC, Exophone (E.164), Bolna account with **SIP trunking (Beta)** — [enterprise@bolna.ai](mailto:enterprise@bolna.ai).

---

## 1 — Exotel: trunk + DID + digest

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "Bolna_Out_Trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "'"${ACCOUNT_SID}"'.pstn.exotel.com"
  }'
```

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/phone-numbers" \
  -H "Content-Type: application/json" \
  -d "{\"phone_number\": \"${EXOPHONE}\"}"
```

```bash
curl -s -X POST \
  "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "'"${SIP_USER}"'",
    "password": "'"${SIP_PASS}"'",
    "friendly_name": "bolna"
  }'
```

---

## 2 — Bolna: create SIP trunk (Bearer token)

```bash
curl -s -X POST "https://api.bolna.ai/sip-trunks/trunks" \
  -H "Authorization: Bearer ${BOLNA_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Exotel India",
    "provider": "custom",
    "auth_type": "userpass",
    "auth_username": "'"${SIP_USER}"'",
    "auth_password": "'"${SIP_PASS}"'",
    "gateways": [
      {
        "gateway_address": "<EXOTEL_EDGE_IP>",
        "port": 443,
        "priority": 1
      }
    ],
    "allow": "ulaw,alaw",
    "inbound_enabled": true,
    "outbound_leading_plus_enabled": true
  }'
```

Replace `gateway_address` / `port` with **Exotel edge IP and port** from Exotel ([network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)). Field names and defaults follow [Create SIP Trunk](https://www.bolna.ai/docs/api-reference/sip-trunks/create).

Add **phone numbers** to the Bolna trunk per Bolna [BYOT setup](https://www.bolna.ai/docs/sip-trunking/byot-setup) / `POST` add number APIs.

Set agent **`telephony_provider`** to **`sip-trunk`** and place calls per [Make Outbound Calls via Your SIP Trunk](https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls).

---

## 3 — Optional: Exotel ACL (static IP)

If Bolna’s egress is a **single static IP** (Bolna docs reference **13.200.45.61** for provider allowlisting in some flows):

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "13.200.45.61", "mask": 32}'
```

Confirm current IPs in **Bolna** and **Exotel** documentation. Exotel trunk **does not support CIDR range** ACL — use **`mask: 32`** per IP.

---

## 4 — Inbound: destination URI on Exotel trunk

Bolna expects your carrier to send INVITEs toward **`sip:13.200.45.61:5060`** ([inbound BYOT](https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls)). Map Exotel **destination URI** accordingly (format per Exotel API).

**Flow → Connect:** **`sip:<trunk_sid>`** in Dial whom.

---

## Shared Exotel curls

[`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

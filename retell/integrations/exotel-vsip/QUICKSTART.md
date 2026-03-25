# Quickstart: Exotel vSIP + Retell AI (elastic SIP, outbound digest)

**Outbound Exotel steps:** create trunk → map DID → credentials. **Optional ACL:** only if Retell gives a **static egress IP** (`mask: 32`); **no CIDR range** on trunk. **Inbound:** destination URI on trunk; **Connect** → **`sip:<trunk_sid>`**.

**Prerequisites:** Exotel vSIP, KYC, Exophone (E.164), Retell [custom telephony](https://docs.retellai.com/deploy/custom-telephony).

---

## 1 — Exotel: create trunk and map DID

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "Retell_Out_Trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "'"${ACCOUNT_SID}"'.pstn.exotel.com"
  }'
```

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/phone-numbers" \
  -H "Content-Type: application/json" \
  -d "{\"phone_number\": \"${EXOPHONE}\"}"
```

---

## 2 — Exotel: SIP digest

```bash
curl -s -X POST \
  "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "'"${SIP_USER}"'",
    "password": "'"${SIP_PASS}"'",
    "friendly_name": "retell"
  }'
```

---

## 3 — Retell: import number

Per [Custom telephony](https://docs.retellai.com/deploy/custom-telephony): import the Exotel DID; digest must match step 2. Termination toward Exotel uses **Exotel edge `IP:port`**.

---

## 4 — Optional: static IP ACL

Only if Retell provides a **single static IP**:

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "<STATIC_IP>", "mask": 32}'
```

---

## 5 — Inbound: destination URI (on trunk)

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{"destinations": [{"destination": "sip.retellai.com:5060;transport=tcp"}]}'
```

**Connect applet:** **`sip:<trunk_sid>`** in Dial whom.

---

## Shared curls

[`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

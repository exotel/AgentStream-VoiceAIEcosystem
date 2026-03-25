# Quickstart: Exotel vSIP + Smallest AI (Atoms)

**Prerequisites:** Exotel vSIP, KYC, Exophone (E.164), [Smallest AI](https://app.smallest.ai/) account.

**Atoms:** [Phone Numbers → Import SIP](https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md) — **SIP Termination URL** = Exotel edge **IP:port**; optional digest = Exotel **`/credentials`**; copy **SIP Origination URL** for Exotel inbound.

**Exotel:** create trunk → map DID → **`/credentials`** → **`/destination-uris`** (origination URI from Atoms) → Flow **Connect** **`sip:<trunk_sid>`**.

---

## 1 — Exotel: trunk + DID + digest

[`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

---

## 2 — Atoms: Import SIP

1. **Add Number** → **Import SIP**  
2. **Phone Number:** your Exotel DID (E.164)  
3. **SIP Termination URL:** Exotel edge from [network doc](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)  
4. **Username** / **Password:** match step 1 digest (if used)  
5. Copy **SIP Origination URL**

---

## 3 — Exotel: destination-uris (inbound)

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{"destinations": [{"destination": "<SIP_ORIGINATION_FROM_ATOMS>"}]}'
```

**Connect:** **`sip:<trunk_sid>`**

---

## 4 — Assign agent + test

Assign the number to your agent; test outbound with [Start an outbound call](https://atoms-docs.smallest.ai/api-reference/calls/start-an-outbound-call.md).

---

## Shared curls

[`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

# Quickstart: Exotel vSIP + ElevenLabs (outbound digest)

**Voice AI Ecosystem: ElevenLabs Voice AI Connector** — shortest path to an **outbound** test call through Exotel using **SIP digest** on both Exotel and ElevenLabs.

> **Outbound SIP (Exotel) is only:** create trunk → map DID → `POST .../credentials`. **Optional:** `whitelisted-ips` **only** if ElevenLabs gives you a **static egress IP** — Exotel trunk **does not support CIDR range** ACL; use **`mask: 32`** per IP. **Destination URI** and **Connect** apply to **inbound SIP**, not this minimal outbound path.

**Full detail:** [elevenlabs-voice-ai-connector.md](./elevenlabs-voice-ai-connector.md)

---

## What you’ll build

```text
ElevenLabs Agent → SIP (digest) → Exotel vSIP → PSTN → Customer
```

---

## Prerequisites

- [ ] Exotel **vSIP** enabled; **KYC**; **Exophone** (E.164)  
- [ ] Exotel **API Key**, **API Token**, **Account SID**, **SUBDOMAIN** (`api.in.exotel.com` for India)  
- [ ] **ElevenLabs** Conversational AI + SIP; **API key**  
- [ ] **Exotel edge `IP:port`** for ElevenLabs “outbound address” (from Exotel — not a generic hostname)

---

## Variables

| Placeholder | Meaning |
|-------------|---------|
| `TRUNK_SID` | From create-trunk response |
| `SIP_USER`, `SIP_PASS` | Same on Exotel `/credentials` and ElevenLabs import |

---

## 1 — Exotel: create trunk

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "ElevenLabs_Outbound_Trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "'"${ACCOUNT_SID}"'.pstn.exotel.com"
  }'
```

Save **`trunk_sid`** as `TRUNK_SID`.

---

## 2 — Exotel: map DID

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/phone-numbers" \
  -H "Content-Type: application/json" \
  -d "{\"phone_number\": \"${EXOPHONE}\"}"
```

---

## 3 — Exotel: SIP digest (must match ElevenLabs)

```bash
curl -s -X POST \
  "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "'"${SIP_USER}"'",
    "password": "'"${SIP_PASS}"'",
    "friendly_name": "eleven_labs"
  }'
```

---

## 4 — ElevenLabs: agent + import Exophone

1. **Conversational AI** → **Agents** — publish agent.  
2. **Phone Numbers** → **Import from SIP trunk**  
3. **E.164** Exophone; **Digest** = `SIP_USER` / `SIP_PASS`  
4. **Outbound address** = **Exotel edge `IP:port`** (from Exotel documentation/support).  
5. Assign number to agent; note **`agent_phone_number_id`**.

---

## 5 — Optional: Exotel ACL (static IP only)

If ElevenLabs provides a **single static egress IP** for SIP toward Exotel:

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "<STATIC_EGRESS_IP>", "mask": 32}'
```

Repeat only for **additional distinct static IPs** if both sides agree. **Do not** use CIDR range on trunk.

---

## 6 — Inbound add-on (separate): destination URI + Flow

For **PSTN → ElevenLabs**, map **destination URI** on the **same** trunk and use **Connect** with **`sip:<trunk_sid>`** in **Dial whom** (the `trunk_sid` string from step 1 — **not** a full SIP URI). See [elevenlabs-voice-ai-connector.md](./elevenlabs-voice-ai-connector.md) Integration 2.

---

## 7 — Test outbound (ElevenLabs API)

Confirm the current outbound endpoint in [ElevenLabs API docs](https://elevenlabs.io/docs).

```bash
curl -s -X POST "https://api.elevenlabs.io/v1/convai/<outbound-endpoint-per-docs>" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "'"${AGENT_ID}"'",
    "agent_phone_number_id": "'"${PHONE_NUMBER_ID}"'",
    "to_number": "+91XXXXXXXXXX"
  }'
```

---

## Common failures

| Symptom | What to check |
|---------|----------------|
| **401** | Digest mismatch |
| **403** inbound | ElevenLabs ACL vs Exotel signaling IPs |

---

## Next steps

- **Integration 2 (inbound):** [elevenlabs-voice-ai-connector.md](./elevenlabs-voice-ai-connector.md)  
- **Support article:** [`docs/support/exotel-elevenlabs-sip-trunk.md`](../../../docs/support/exotel-elevenlabs-sip-trunk.md)

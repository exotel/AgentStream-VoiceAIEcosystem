# Quickstart — ElevenLabs + Exotel SIP trunking

Goal: first successful **outbound** and (optionally) **inbound** call using **Exotel as the India PSTN carrier** and **ElevenLabs Conversational AI** as the Voice AI platform.

Shared Exotel API snippets:

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md) (Trunk APIs: **200 requests/minute**; outbound call initiation default: **200 calls/minute**, contact CSM for higher)

Full support article:

- [`docs/support/exotel-elevenlabs-sip-trunk.md`](../../../docs/support/exotel-elevenlabs-sip-trunk.md)

---

## Prereqs

- [ ] Exotel **SIP trunking** enabled; **KYC**; **Exophone** (E.164)  
- [ ] Exotel **API Key**, **API Token**, **Account SID**, **SUBDOMAIN** (`api.in.exotel.com` for India)  
- [ ] **ElevenLabs** Conversational AI + SIP; **API key**  
- [ ] **Exotel edge `IP:port`** for ElevenLabs “outbound address” (from Exotel — not a generic hostname)

---

## Outbound (ElevenLabs → Exotel → PSTN)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - Create digest credentials on the trunk (`POST .../credentials`)
2. **ElevenLabs**
   - Create/publish agent
   - Phone Numbers → Import from SIP trunk
   - Set digest auth to match Exotel trunk credentials
   - Set outbound address = Exotel edge `IP:port`
3. Place an outbound test call via ElevenLabs.

Optional:

- Exotel trunk `whitelisted-ips` only if ElevenLabs provides **static `/32`** SIP egress IPs (one IP per POST, `mask: 32`; do not attempt CIDR ranges).

---

## Inbound (PSTN → Exotel → ElevenLabs) (optional)

1. **Exotel**
   - Set trunk `destination-uris` toward ElevenLabs SIP ingress (per support article)
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`
2. Call the DID and confirm ElevenLabs answers.

---

## If calls fail

- **401/403**: digest mismatch between Exotel `/credentials` and ElevenLabs import.
- **Inbound not reaching ElevenLabs**: wrong `destination-uris` target, or Flow Connect not set to `sip:<trunk_sid>`.
- Use the full guide: [`docs/support/exotel-elevenlabs-sip-trunk.md`](../../../docs/support/exotel-elevenlabs-sip-trunk.md)

## Links

- ElevenLabs SIP trunking: https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking
- Repo support article: [`docs/support/exotel-elevenlabs-sip-trunk.md`](../../../docs/support/exotel-elevenlabs-sip-trunk.md)

---

## Appendix: raw Exotel curls (optional)

If you want copy/paste curls instead of the shared snippets, the original examples are kept below.

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

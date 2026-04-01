# Connect Exotel Virtual SIP Trunk to ElevenLabs Conversational AI

This guide explains how to connect **Exotel SIP trunking** to **ElevenLabs Conversational AI** so you can place and receive PSTN calls in India through Exotel while your agent runs on ElevenLabs.

> **Applicability:** **UI-driven** (ElevenLabs console for agents + phone numbers) with optional **API-driven** outbound triggering.

> **Exotel edge:** Exotel provides **SIP edge IP address(es) and port(s)** for signaling (for example **TLS `443`** or **TCP `5070`** per [Exotel network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)). Configure **`<EXOTEL_EDGE_IP>:<PORT>`** in ElevenLabs — use the values Exotel assigns for your account.

> **Edge hostnames you may see (India):** `in.voip.exotel.com:5070` (TCP) and `in.voip.exotel.com:443` (TLS). Use the exact host/IP + port + transport Exotel assigns. See [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md) for details.

> **ACL vs digest (important):** Avoid trying to whitelist **CIDR ranges**. Exotel trunk ACL is intended for **static `/32` IPs** only (`mask: 32`). If a provider publishes only **CIDR** / shared egress ranges, prefer **digest** and coordinate with Exotel/provider support—mixing allowlists and digest can cause auth/routing issues in multi-tenant egress setups.

> **Product status:** Exotel SIP trunking may be labeled Alpha or require enablement. **UDP transport is not supported** for the flows below — use **TCP** or **TLS** only. Confirm details with Exotel.

> **Deeper reference:** [`elevenlabs/integrations/exotel-vsip/elevenlabs-voice-ai-connector.md`](../../elevenlabs/integrations/exotel-vsip/elevenlabs-voice-ai-connector.md)

> **Quickstart:** [`elevenlabs/integrations/exotel-vsip/QUICKSTART.md`](../../elevenlabs/integrations/exotel-vsip/QUICKSTART.md)

---

## What you will set up

| Integration | Direction | When to use |
|-------------|-----------|-------------|
| **Outbound SIP (digest)** | ElevenLabs → Exotel → PSTN | Agent **places outbound** calls via your Exotel DID |
| **Inbound SIP** | PSTN → Exotel DID → ElevenLabs | Callers **dial** your Exotel number and reach the agent |

**Separate the API work:** **Outbound SIP** uses only **create trunk → map DID → credentials**. **Inbound SIP** adds **destination URI** on the trunk (and Flow). **Trunk ACL** (`whitelisted-ips`) applies **only** when your Voice AI provider gives you a **static egress IP** — Exotel trunk **does not support CIDR range** allowlisting; use **one static IP per API call** (`mask: 32`) if needed.

---

## Architecture

### Outbound SIP (digest)

```text
ElevenLabs → SIP digest → Exotel edge IP:port → Indian PSTN → Customer
```

### Inbound SIP

```text
Customer → PSTN → Exotel DID → Flow (Connect) → sip:<trunk_sid> → … → sip.rtc.elevenlabs.io → ElevenLabs Agent
```

**Destination URI** on the trunk defines where Exotel sends **inbound** SIP toward ElevenLabs. In the **Connect** applet **Dial whom**, use **`sip:<trunk_sid>`** only — the **`trunk_sid`** string returned from **Create trunk** (not a full `sip:user@host` URI).

For FQDN-only inbound (no digest on trunk), **do not** add `POST .../credentials` unless Exotel requires it for your design.

---

## Prerequisites

### Exotel

- [my.in.exotel.com](https://my.in.exotel.com) with **SIP trunking** enabled.
- **KYC**; Exophone (DID) in **E.164** (`+91…`).
- **API Key**, **API Token**, **Account SID** from [API credentials](https://my.in.exotel.com/apisettings/site#api-credentials).
- APIs: **`https://api.in.exotel.com`** (India).

### ElevenLabs

- [Agents / Conversational AI](https://elevenlabs.io/app/agents) and **SIP** phone import.
- **Published agent**; **API key** if testing outbound via HTTP API.

### Network

- SIP: **TCP** or **TLS**; RTP: **UDP** per [Exotel network doc](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration).

---

## Part A — ElevenLabs (dashboard)

### Outbound SIP (digest)

1. **Agents** → create/publish agent.
2. **Phone Numbers** → **Import a phone number from SIP trunk**.
3. **E.164** Exotel DID; **Transport** TCP/TLS per Exotel; **SIP digest** = same values you will set in Exotel `POST .../credentials`.
4. **Outbound address** = **Exotel edge `IP:port`** from Exotel.
5. Import → **assign** number to agent. Note **`agent_phone_number_id`** for API tests.

### Inbound SIP (ACL path)

1. Import number; leave digest **empty** if using ACL on ElevenLabs.
2. Allowlist **Exotel signaling IPs** on ElevenLabs if required ([Exotel network doc](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)).

---

## Part B — Exotel console

- [Numbers](https://my.in.exotel.com/numbers), KYC, [App Bazaar / Flows](https://my.in.exotel.com/apps#installed-apps) for **Connect** when using inbound.

---

## Part C — Exotel APIs

**Auth:** `https://API_KEY:API_TOKEN@api.in.exotel.com/...`  
**Rate limit:** **200 requests/minute**.  
Templates: [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md).

### Outbound SIP — required steps only

1. **Create trunk**
2. **Map DID** to trunk
3. **`POST .../credentials`** — digest; must match ElevenLabs import

**Optional (only if ElevenLabs gives a static egress IP):** `POST .../whitelisted-ips` with that **single IP**, `mask: 32`. Repeat per static IP if Exotel and your provider agree. **Do not** assume CIDR range whitelist on trunk.

**Do not** add **destination URI** for the minimal outbound-only path unless Exotel documents it for your account.

```bash
curl -s -X POST \
  "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "SIP_USER",
    "password": "SIP_PASS",
    "friendly_name": "eleven_labs"
  }'
```

### Inbound SIP — destination URI on trunk

Map **inbound** SIP toward ElevenLabs (host/port/transport per ElevenLabs):

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "sip.rtc.elevenlabs.io:5060;transport=tcp" }
    ]
  }'
```

### Connect applet (inbound)

1. [App Bazaar](https://my.in.exotel.com/apps#installed-apps) → Flow → **Connect** applet.
2. **Dial whom:** **`sip:<trunk_sid>`** — paste the **`trunk_sid`** from the create-trunk API response (prefix `sip:` only; **not** a full SIP URI).
3. Map the Exophone to this Flow.

Overview: [Exotel Voice AI / SIP trunking](https://support.exotel.com/support/solutions/articles/3000133452-flow-and-api-configuration-guide-for-voice-ai-contact-centre-platforms-via-exotel-virtual-sip-trunk).

---

## Test calls

### Lab validation (outbound)

Outbound SIP has been **tested** end-to-end when trunk + DID + digest + (optional) static-IP ACL align. A **connected call** does not guarantee the **agent speaks** — see below.

### Outbound API

Use ElevenLabs **Conversational AI outbound call** API — confirm the current URL in [ElevenLabs API docs](https://elevenlabs.io/docs) (paths change over time).

```bash
curl -s -X POST "https://api.elevenlabs.io/v1/convai/<outbound-call-endpoint-per-current-docs>" \
  -H "xi-api-key: ${ELEVENLABS_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "YOUR_AGENT_ID",
    "agent_phone_number_id": "YOUR_PHONE_NUMBER_ID",
    "to_number": "+91XXXXXXXXXX"
  }'
```

### Inbound

Dial your Exotel DID; agent should answer via ElevenLabs.

---

### Call connects but agent does not speak (no bot audio)

This section applies when the **call is triggered** but the **agent does not play** audio.

| Check | Action |
|--------|--------|
| Assignment | Imported DID **assigned** to the agent used in the API |
| IDs | `agent_phone_number_id` matches the imported SIP number |
| Agent | Published; first message / voice configured |
| Logs | ElevenLabs ConvAI traces for session errors |
| RTP | If total silence, check UDP/RTP per [Exotel network doc](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration) |

---

## Troubleshooting

| Symptom | Likely cause |
|---------|----------------|
| SIP **401** | Digest mismatch (Exotel `/credentials` vs ElevenLabs) |
| SIP **403** inbound | ElevenLabs ACL vs Exotel source IPs |
| **408** / timeout | DNS/firewall to ElevenLabs FQDN |
| Connect does nothing | **Dial whom** must be **`sip:<trunk_sid>`**, not a full URI |
| **Call triggers, no speech** | See [Call connects but agent does not speak (no bot audio)](#call-connects-but-agent-does-not-speak-no-bot-audio) |

---

## Official references

| Resource | URL |
|----------|-----|
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |
| Exotel + ElevenLabs | https://docs.exotel.com/dynamic-sip-trunking/elevenlabs-and-exotel-sip-trunking-integration-guide-for-voice-ai |
| Exotel network | https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration |
| ElevenLabs SIP | https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking |

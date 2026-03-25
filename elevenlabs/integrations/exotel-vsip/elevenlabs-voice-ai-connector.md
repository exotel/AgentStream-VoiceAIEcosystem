# Voice AI Ecosystem: ElevenLabs Voice AI Connector

**Exotel vSIP (Alpha) ↔ ElevenLabs Conversational AI**

| Field | Details |
|-------|---------|
| Document ID | VAIEC-EXO-EL-01 |
| Version | 1.0 |
| Last Updated | March 2026 |
| Scope | Exotel vSIP (Alpha) ↔ ElevenLabs Conversational AI |
| Classification | Internal Use Only |

> **Alpha notice:** Exotel vSIP is in Alpha. Not covered by production-grade SLAs. **UDP transport is not supported.** Use **TCP** or **TLS** only.

---

## Platform SIP trunking — two integration patterns

| Integration | Direction | Auth method | Use case |
|-------------|-----------|-------------|----------|
| **Integration 1** | Exotel → ElevenLabs (outbound) | SIP Digest (username/password) | ElevenLabs voicebot places PSTN calls via Exotel DID using credential-based auth |
| **Integration 2** | PSTN → Exotel DID → ElevenLabs (inbound) | FQDN-based (no registration) | Inbound caller reaches an ElevenLabs AI agent via Exotel DID using ElevenLabs FQDN on the trunk |

**Fast path:** [QUICKSTART.md](./QUICKSTART.md) (outbound digest only).

**Other approach:** If you use Exotel **Voicebot** **`wss://`** streaming (same idea as [exotel/Agent-Stream](https://github.com/exotel/Agent-Stream)) instead of SIP trunks, see [WebSocket + bridge → ElevenLabs ConvAI](../exotel-wss/README.md).

---

## Architecture

```text
INTEGRATION 1 — Outbound (SIP Auth / Digest)
─────────────────────────────────────────────
ElevenLabs Agent (initiates outbound)
    │  SIP INVITE → sip.rtc.elevenlabs.io
    │  Digest Auth (username + password)
    ▼
Exotel vSIP Gateway (pstn.in2.exotel.com:5070)
    │
    ▼
Indian PSTN → Customer Phone


INTEGRATION 2 — Inbound (FQDN-based)
──────────────────────────────────────
Customer dials Exotel DID (Exophone)
    │
    ▼
Exotel vSIP Trunk
    │  DNS resolves ElevenLabs FQDN
    │  SIP INVITE → sip.rtc.elevenlabs.io
    ▼
ElevenLabs AI Agent handles call
```

---

## Prerequisites

### Exotel

- Active Exotel account with **vSIP (Alpha)** enabled — contact your Exotel Account Manager or `hello@exotel.com`
- KYC completed: [KYC verification](https://docs.exotel.com/business-phone-system/kyc-verification)
- API credentials: [API credentials](https://my.in.exotel.com/apisettings/site#api-credentials)
- At least one SIP-capable **Exophone (DID)** for the region (MUM example: `pstn.in2.exotel.com`)
- If using ACL: **static egress IP** from ElevenLabs for `whitelisted-ips` (single IP, `mask: 32` only)

### ElevenLabs

- Active ElevenLabs account with **Conversational AI** and **SIP trunking** access
- A configured and published **AI Agent**
- **Integration 1:** SIP digest — credentials must **match** between Exotel `POST .../credentials` and ElevenLabs phone import
- **Integration 2:** ElevenLabs SIP FQDN — `sip.rtc.elevenlabs.io` (or India residency host if required)

### Network / firewall

- SIP signalling: **TCP 5060** (or **5061** TLS) to/from Exotel PoP
- RTP media: **UDP 10000–60000** to/from Exotel media IPs (confirm current IPs in [Exotel network docs](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration))
- **Integration 2:** Exotel must resolve and reach `sip.rtc.elevenlabs.io`
- Disable **SIP ALG** on intermediate NAT devices where possible

---

## Common variables

Use placeholders in all commands; do not commit real secrets.

| Variable | Description |
|----------|-------------|
| `ACCOUNT_SID` | Exotel Account SID |
| `API_KEY` | Exotel API Key |
| `API_TOKEN` | Exotel API Token |
| `SUBDOMAIN` | `api.in.exotel.com` (MUM) or `api.exotel.com` (SGP) |
| `EXOPHONE` | Exotel DID in E.164, e.g. `+918069XXXXXX` |
| `TRUNK_SID` | Trunk SID from create-trunk response |
| `SIP_USER` / `SIP_PASS` | Same values on Exotel credentials API and ElevenLabs SIP digest (Integration 1) |

---

# Integration 1 — Outbound voicebot via Exotel DID (SIP digest)

## What this does

```text
ElevenLabs Agent → Exotel vSIP Trunk (Digest Auth) → PSTN → Customer
```

ElevenLabs authenticates to Exotel using SIP digest. **Exotel digest must be created via API** and must **match** ElevenLabs import settings.

## Recommended order (outbound SIP)

1. **Exotel API:** Create trunk → map DID → **`POST .../credentials`** (digest)  
2. **ElevenLabs UI:** Import the same E.164 number with the **same** username/password  
3. **Optional:** `POST .../whitelisted-ips` **only** if ElevenLabs provides a **single static egress IP** — use `mask: 32`. Exotel trunk **does not support CIDR range** ACL.  
4. **ElevenLabs API:** Place test outbound call  

**Inbound SIP** (separate): map **destination URI** on the trunk toward ElevenLabs; **Flow → Connect** with **`sip:<trunk_sid>`** in Dial whom (see Integration 2). Do **not** add destination URI to the minimal outbound-only path unless Exotel requires it.

---

## Step 1.1 — Create Exotel vSIP trunk (API)

```bash
curl -X POST "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "ElevenLabs_Outbound_Trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "<ACCOUNT_SID>.pstn.exotel.com"
  }'
```

Save **`trunk_sid`** as `TRUNK_SID`.

---

## Step 1.2 — Map Exophone to trunk

```bash
curl -X POST "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "<EXOPHONE>"
  }'
```

Default mode is **`pstn`**. Save the returned **`id`** if you need mode updates later.

---

## Step 1.3 — Create SIP digest on Exotel trunk (API)

**Critical:** `user_name` and `password` here must match **exactly** what you enter in ElevenLabs under **SIP Digest** when importing the number (Step 1.4).

```bash
curl -s -X POST \
  "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "<SIP_USER>",
    "password": "<SIP_PASS>",
    "friendly_name": "eleven_labs"
  }'
```

---

## Step 1.4 — Configure ElevenLabs agent and import number (dashboard)

1. **elevenlabs.io** → **Conversational AI** → **Agents** — create or open an agent  
2. Configure agent (system prompt, first message, LLM, interruption handling as needed)  
3. **Phone Numbers** → **Import a phone number from SIP trunk**  
4. **Label:** e.g. `Exotel-India-Outbound`  
5. **Phone number:** `<EXOPHONE>` (E.164)  
6. **Transport:** `TCP` (or `TLS` if Exotel supports it end-to-end)  
7. **Media encryption:** `Allowed` (use `Required` only if TLS is confirmed everywhere)  
8. **Outbound address:** **Exotel edge `IP:port`** (from Exotel — see [network doc](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration))  
9. **SIP Digest:** **same** `<SIP_USER>` / `<SIP_PASS>` as Step 1.3  
10. **Import**, then **assign** the number to the agent  

> **SIP URI note:** ElevenLabs uses identifiers like  
> `sip:<EXOPHONE>@sip.rtc.elevenlabs.io:5060;transport=tcp`  
> The user part must match the imported number.

---

## Step 1.5 — Optional: whitelist static egress IP (ACL)

Use **only** when ElevenLabs gives you a **fixed static IP** for SIP toward Exotel. Exotel trunk ACL is **per single IP** (`mask: 32`); **CIDR ranges are not supported** on the trunk.

```bash
curl -X POST "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{
    "ip": "<STATIC_EGRESS_IP>",
    "mask": 32
  }'
```

---

## Step 1.6 — Trigger outbound call (ElevenLabs API)

```bash
curl -X POST "https://api.elevenlabs.io/v1/convai/<outbound-call-endpoint-per-current-docs>" \
  -H "xi-api-key: <ELEVENLABS_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "<AGENT_ID>",
    "agent_phone_number_id": "<PHONE_NUMBER_ID>",
    "to_number": "<CUSTOMER_E164_NUMBER>"
  }'
```

`agent_phone_number_id` is the imported Exophone’s ID in ElevenLabs. Confirm the exact URL in the [ElevenLabs API reference](https://elevenlabs.io/docs).

---

## Integration 1 — Verification checklist

| Check | How | Pass |
|-------|-----|------|
| Trunk created | `GET /trunks/<TRUNK_SID>` | Trunk details returned |
| Exophone mapped | `GET /trunks/<TRUNK_SID>/phone-numbers` | Exophone listed, mode `pstn` |
| Digest on Exotel | Trunk credentials configured | Same user/pass as ElevenLabs |
| Static IPs (if used) | `GET .../whitelisted-ips` | One entry per static IP (`mask: 32`) |
| Outbound call | ElevenLabs API | Customer answers; AI speaks |
| Caller ID | Callee handset | Shows Exophone |
| SIP digest | Logs / traces | No **401/403** on INVITE |

---

# Integration 2 — Inbound calls to ElevenLabs via Exotel DID (FQDN-based)

## What this does

```text
Customer → Exotel DID → DNS → sip.rtc.elevenlabs.io → ElevenLabs Agent
```

No SIP registration; **no** username/password on the Exotel trunk for this pattern. **Do not** create SIP credentials on the Exotel trunk for FQDN-only inbound.

---

## Step 2.1 — Configure ElevenLabs (dashboard)

1. **Agents** — create/select agent  
2. **Phone Numbers** → **Import from SIP trunk**  
3. **Label**, **E.164 Exophone**, **TCP**, **Media encryption: Allowed**  
4. **Outbound address:** optional — **Exotel edge `IP:port`** if needed for transfer legs  
5. **Authentication:** leave username/password **empty** (ACL path)  
6. **Import** — note **SIP ID** in ElevenLabs if you need it for troubleshooting  
7. **Assign** number to agent  

**Endpoints:**

- `sip.rtc.elevenlabs.io:5060;transport=tcp`  
- India residency (if required): `sip-static.rtc.in.residency.elevenlabs.io`  

---

## Step 2.2 — Exotel trunk + FQDN destination (API)

### Create trunk

```bash
curl -X POST "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "ElevenLabs_Inbound_FQDN_Trunk",
    "nso_code": "ANY-ANY",
    "domain_name": "<ACCOUNT_SID>.pstn.exotel.com"
  }'
```

### Map Exophone

```bash
curl -X POST "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/phone-numbers" \
  -H "Content-Type: application/json" \
  -d '{
    "phone_number": "<EXOPHONE>"
  }'
```

### Destination URI to ElevenLabs

FQDN mode: **ACL on Exotel side not required** for resolving ElevenLabs (Exotel resolves DNS per call).

```bash
curl -X POST "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      {
        "destination": "sip.rtc.elevenlabs.io:5060;transport=tcp"
      }
    ]
  }'
```

India residency example:

```json
{ "destination": "sip-static.rtc.in.residency.elevenlabs.io:5060;transport=tcp" }
```

---

## Step 2.3 — Exotel flow (Connect applet)

1. **App Bazaar:** [my.in.exotel.com/apps](https://my.in.exotel.com/apps)  
2. New flow → **Connect** applet  
3. **Dial whom:** **`sip:<trunk_sid>`** — use the **`trunk_sid`** string returned by **Create trunk** (prefix `sip:` only; **not** a full SIP URI).  
4. Save flow  
5. Map **Exophone** to this flow in number settings  

---

## Step 2.5 — ElevenLabs ACL for Exotel IPs

Integration 2 uses ACL on the ElevenLabs side. Exotel Mumbai PoP IPs (verify current list in Exotel docs):

- `182.76.143.61`  
- `122.15.8.184`  

If calls get **403**, ask ElevenLabs support to allowlist Exotel source IPs for your account.

---

## Integration 2 — Verification checklist

| Check | How | Pass |
|-------|-----|------|
| Trunk + DID | `GET` APIs | Exophone mapped |
| FQDN destination | `GET .../destination-uris` | ElevenLabs host listed |
| Connect applet | App Bazaar | **`sip:<trunk_sid>`** in Dial whom |
| Exophone → flow | Number settings | Flow assigned |
| Inbound test | Dial DID | Agent answers |
| DNS | `dig` / resolver | FQDN resolves |

> **Internal ops only:** If your org uses Homer or similar SIP capture tools for traces, use your **internal** URLs and credentials — do not embed live operator endpoints in customer-facing copies of this doc.

---

## SIP header reference

**Exotel (read-only on inbound legs):**

| Header | Use |
|--------|-----|
| `X-Exotel-CallSid` | Call correlation / CDR |
| `X-Exotel-LegSid` | Leg ID |
| `X-Exotel-TrunkSid` | Trunk |
| `X-Exotel-AccountSid` | Account |

**ElevenLabs mapping (when forwarded):**

| Header | System variable |
|--------|-----------------|
| `X-CALL-ID` | `call_id` |
| `X-CALLER-ID` | `caller_id` |

---

## Codec reference

| Layer | Codecs |
|-------|--------|
| Exotel vSIP (preferred) | PCMA (G.711 A-law) |
| Exotel vSIP (supported) | PCMU (G.711 μ-law) |
| ElevenLabs SIP | G.711 8 kHz or G.722 16 kHz |
| Transport | TCP or TLS (no UDP for this guide) |

Prefer **PCMA** for India PSTN where applicable.

---

## Troubleshooting

| Symptom | Likely cause | Resolution |
|---------|----------------|------------|
| SIP **401** outbound | Digest mismatch | Align Exotel `credentials` and ElevenLabs digest |
| SIP **403** inbound | ACL | ElevenLabs allowlist for Exotel IPs |
| **408** / no response | DNS / firewall / port | Check FQDN resolution; TCP **5060** |
| **488** Not acceptable | Codec / SDP | PCMA in SDP; check media encryption settings |
| Drop ~30s | RTP blocked | Open UDP media range to Exotel IPs |
| One-way audio | NAT / ALG | Disable SIP ALG; RTP pinholes |
| **481** on BYE | BYE to wrong target | BYE to **Contact** from **200 OK** |
| Connect applet silent | Wrong Dial whom | Use **`sip:<trunk_sid>`** (API `trunk_sid` value), not a full URI |

---

## Useful API queries (Exotel)

```bash
curl -X GET "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>"

curl -X GET "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/phone-numbers"

curl -X GET "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/whitelisted-ips"

curl -X GET "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/destination-uris"

curl -X PUT "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/phone-numbers/<PHONE_NUMBER_ID>" \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "<EXOPHONE>", "mode": "pstn"}'
```

---

## References

| Resource | URL |
|----------|-----|
| Exotel vSIP overview | https://docs.exotel.com/dynamic-sip-trunking/overview |
| Exotel Trunk Configuration APIs (GitHub) | https://github.com/exotel/exotel-vsip-trunk-Configuration-API |
| Exotel FQDN vSIP | https://docs.exotel.com/dynamic-sip-trunking/exotel-virtual-sip-trunking-fqdn-based |
| Exotel + ElevenLabs guide | https://docs.exotel.com/dynamic-sip-trunking/elevenlabs-and-exotel-sip-trunking-integration-guide-for-voice-ai |
| ElevenLabs SIP trunking | https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking |
| Exotel network / firewall | https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration |
| Exotel SIP error codes | https://docs.exotel.com/dynamic-sip-trunking/sip-error-codes-and-troubleshooting-guide |

---

## Revision history

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | March 2026 | Outbound = trunk + DID + credentials only; ACL static IP only (no CIDR on trunk); removed trunk alias; Connect = `sip:<trunk_sid>`; no third-party product names |
| 1.0 | March 2026 | Initial — Integration 1 & 2; Exotel `POST .../credentials` step for digest alignment |

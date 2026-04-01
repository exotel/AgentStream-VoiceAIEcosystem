# Exotel SIP trunk API — shared reference

Use these snippets from the support articles for **ElevenLabs**, **LiveKit**, **Retell**, **Bolna**, **Pipecat (via Daily SIP)**, **Ultravox**, **Vapi**, **Smallest AI (Atoms)**, **Vocallabs**, **Rapida AI**, and **NLPearl.AI** integrations. Replace placeholders; do not commit real secrets.

**GitHub repo (reference):** https://github.com/exotel/AgentStream-VoiceAIEcosystem

| Placeholder | Description |
|-------------|-------------|
| `API_KEY` | Exotel API Key ([API Settings](https://my.in.exotel.com/apisettings/site#api-credentials)) |
| `API_TOKEN` | Exotel API Token |
| `ACCOUNT_SID` | Exotel Account SID |
| `SUBDOMAIN` | `api.in.exotel.com` (India) or `api.exotel.com` (Singapore) |
| `TRUNK_SID` | Returned when you create a trunk (`trunk_sid` in response) |

**Authentication:** HTTP Basic — `https://API_KEY:API_TOKEN@SUBDOMAIN/...`

**Trunk API rate limit:** 200 requests per minute on these trunk configuration APIs ([Exotel SIP API reference](https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference)).

**Outbound call rate (default):** Exotel typically allows **200 outbound call attempts per minute** by default (account-level). If you need a higher outbound initiation limit, contact your **CSM**.

**Where to get API credentials:** [API Settings (India)](https://my.in.exotel.com/apisettings/site#api-credentials) (or your cluster dashboard).

**Headers:** `Content-Type: application/json` on POST/PUT.

### Exotel edge: IP and port

Exotel documents **SIP signaling toward their gateway** using **edge IP addresses and ports** — for example **TLS on port 443** or **TCP on port 5070** — per [Exotel network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration). Use the **IP:port** (and transport) Exotel gives you in onboarding or support.

Exotel may also share **edge hostnames** (instead of raw IPs). Common India examples you may see are:

- **TCP:** `in.voip.exotel.com:5070`
- **TLS:** `in.voip.exotel.com:443`

Use the exact **host/IP + port + transport** Exotel assigns to your account/cluster. If a provider UI requires an **IPv4 literal** (no hostname), resolve the hostname to the IPv4 Exotel intends you to use (or request the explicit edge IPs from Exotel support).

The **`domain_name`** field in **Create trunk** is Exotel’s **account SIP domain** for the trunk record (`{ACCOUNT_SID}.pstn.exotel.com`). That is separate from the **edge IP:port** your Voice AI platform uses to send SIP to Exotel.

### Outbound trunk vs inbound SIP trunk

| Flow | Exotel API steps |
|------|-------------------|
| **Outbound SIP** (Voice AI → Exotel → PSTN) | **1.** Create trunk → **2.** Map DID → **3.** `POST .../credentials` (digest). **Optional:** `POST .../whitelisted-ips` **only** if the Voice AI provider gives you a **fixed static egress IP** to allow — see below. **Do not** use destination URI for this path unless Exotel instructs you otherwise. |
| **Inbound SIP** (PSTN → Exotel → Voice AI) | After trunk + DID, **map destination URI** on the trunk to the partner’s SIP host/port/transport. Use **Flow → Connect** with **`sip:<trunk_sid>`** in **Dial whom** (see support articles). |

### Trunk ACL (`whitelisted-ips`)

Exotel trunk ACL is for **static IP allowlisting** from your Voice AI provider when they give you a **single fixed egress IP**. **Exotel does not support CIDR range whitelist on the trunk** — use **one IP per `POST`** with `mask: 32`. If the provider only offers non-static or range-based egress, use **digest credentials** and coordinate with Exotel on what is supported.

**Important (auth precedence):** Avoid mixing **IP allowlisting** and **digest auth** unless Exotel support has confirmed the expected behavior for your account. In some SIP deployments, once an **IP allowlist** is enabled, the platform may treat **source-IP** as the primary trust signal, and digest behavior can become confusing (especially if a provider publishes **shared / multi-tenant** egress ranges). If your provider only publishes **CIDR ranges** (no dedicated static `/32` IPs), do **not** attempt to “whitelist the range” on Exotel — rely on **digest** and work with Exotel/provider support for the correct model.

---

## Create trunk

`POST /v2/accounts/{ACCOUNT_SID}/trunks`

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks" \
  -H "Content-Type: application/json" \
  -d '{
    "trunk_name": "my_trunk_name",
    "nso_code": "ANY-ANY",
    "domain_name": "'"${ACCOUNT_SID}"'.pstn.exotel.com"
  }'
```

`trunk_name`: alphanumeric + underscores, max 16 characters.

---

## Map phone number (DID) to trunk

`POST /v2/accounts/{ACCOUNT_SID}/trunks/{TRUNK_SID}/phone-numbers`

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/phone-numbers" \
  -H "Content-Type: application/json" \
  -d "{\"phone_number\": \"+9198XXXXXXXX\"}"
```

Optional: `"mode": "flow"` for StreamKit/Voice AI routing. Save returned `id` for updates.

---

## Create SIP digest credentials (outbound auth)

`POST /v2/accounts/{ACCOUNT_SID}/trunks/{TRUNK_SID}/credentials`

Use the **same** `user_name` and `password` on the Voice AI platform (ElevenLabs SIP digest, LiveKit `authUsername` / `authPassword`, Retell termination, etc.).

```bash
curl -s -X POST \
  "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "SIP_USER",
    "password": "SIP_PASS",
    "friendly_name": "voice_ai_platform"
  }'
```

---

## Whitelist IP (ACL) — static provider IP only

`POST /v2/accounts/{ACCOUNT_SID}/trunks/{TRUNK_SID}/whitelisted-ips`

Use **only** when your Voice AI provider gives a **single static egress IP** you must allow. **Repeat the call for each distinct static IP** (no CIDR ranges on trunk).

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "203.0.113.50", "mask": 32}'
```

---

## Set destination URI (inbound SIP — PSTN toward Voice AI partner)

`POST /v2/accounts/{ACCOUNT_SID}/trunks/{TRUNK_SID}/destination-uris`

Used for **inbound** routing: PSTN → Exotel → your SIP partner (FQDN or host/port/transport per partner docs). **Not** part of the minimal **outbound** SIP setup.

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "partner.example.com:5061;transport=tls" }
    ]
  }'
```

---

## Verify (GET)

```bash
curl -s "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}"
curl -s "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/phone-numbers"
curl -s "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips"
curl -s "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris"
```

---

## Related docs

- [Support hub — provider URLs, consoles, quick checklists](./README.md)
- [WebRTC application setup (Exotel + Voice AI)](../integrations/webrtc-application-setup.md)
- [Exotel + ElevenLabs support article](./exotel-elevenlabs-sip-trunk.md)
- [Exotel + LiveKit support article](./exotel-livekit-sip-trunk.md)
- [Exotel + Retell AI support article](./exotel-retell-sip-trunk.md)
- [Exotel + Bolna AI support article](./exotel-bolna-sip-trunk.md)
- [Exotel + Pipecat support article](./exotel-pipecat-sip-trunk.md)
- [Exotel + Ultravox support article](./exotel-ultravox-sip-trunk.md)
- [Exotel + Vapi support article](./exotel-vapi-sip-trunk.md)
- [Exotel + Smallest AI support article](./exotel-smallest-ai-sip-trunk.md)
- [Exotel + Vocallabs support article](./exotel-vocallabs-sip-trunk.md)
- [Exotel + Rapida AI support article](./exotel-rapida-ai-sip-trunk.md)
- [Exotel + NLPearl.AI support article](./exotel-nlpearl-sip-trunk.md)
- [Exotel network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)

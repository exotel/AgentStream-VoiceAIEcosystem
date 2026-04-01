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

Additional References:
## When to use Credentials vs ACL (Whitelisted IPs)

Use these guidelines to decide whether you should configure **credentials**, **ACL (whitelisted IPs)**, or **both** on a trunk.

### Credentials (SIP Digest) — recommended for Voice AI direct trunking

Use **credentials** when your SIP endpoint is a **cloud Voice AI platform** (or any environment where source IPs are dynamic/unknown), and you want to **avoid managing IP allowlists**.

- **Best for**: Voice AI direct trunking, dynamic SBCs, multi-tenant provider networks.
- **Typical choice**: **Credentials-only** (skip ACL whitelisting) when IPs are not stable.

### ACL (Whitelisted IPs) — recommended for static enterprise PBX/SBC

Use **ACL-only** when your trunk connects to a customer-controlled PBX/SBC with **stable, known egress IPs**.

- **Best for**: On‑prem SBCs, fixed datacenter IPs, tightly controlled networks.
- **Typical choice**: **ACL-only** if credentials are not required and IPs are stable.

### Combination (ACL + Credentials) — highest security when IPs are stable

Use **both** when you have credentials *and* stable IPs and want a stricter security posture.

- **Best for**: Production trunks with fixed IP ranges and stricter access controls.
- **Why**: Reduces blast radius—credentials alone aren’t sufficient without also matching the allowlist (and vice‑versa).

---

### 1. Create credentials (SIP digest)

Creates a **username/password** pair for **SIP Digest authentication** on the trunk. Configure the same values on your Voice AI platform’s SIP trunk settings.

#### HTTP Request

POST `https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials`

#### Request Headers

| Header | Value |
| --- | --- |
| Content-Type | application/json |

#### Request Parameters

The following parameters are sent as JSON in the body of the request:

| Parameter Name | Mandatory/Optional | Value |
| --- | --- | --- |
| user_name | Mandatory | String; SIP digest username. Example: `voice_ai_user` |
| password | Mandatory | String; SIP digest password. Use a strong secret. |
| friendly_name | Optional | String; Label to identify where the creds are used (max 32 chars). Example: `elevenlabs-prod`, `livekit-staging` |

#### Example Request

```bash
curl -s -X POST "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "voice_ai_user",
    "password": "REPLACE_WITH_STRONG_PASSWORD",
    "friendly_name": "voice_ai_platform"
  }'
```

#### HTTP Response

On success, the HTTP response status code will be **200 OK**.

#### Example Response

```json
{
  "request_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "method": "POST",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "id": "1234",
      "trunk_sid": "trmum17d8e9a37a3732ecbf91a3u",
      "user_name": "voice_ai_user",
      "friendly_name": "voice_ai_platform",
      "date_created": "2026-01-23T11:37:36Z",
      "date_updated": "2026-01-23T11:37:36Z"
    }
  }
}
```

#### Response Parameters

| Parameter Name | Type & Value |
| --- | --- |
| request_id | String; Unique identifier for this API request |
| method | String; HTTP method used (POST) |
| http_code | Integer; HTTP status code (200 for success) |
| id | String; Unique identifier for this credential entry. Example: `1234` |
| trunk_sid | String; The trunk these credentials are associated with |
| user_name | String; The SIP digest username you set |
| friendly_name | String or null; Optional label |
| date_created | String; ISO 8601 timestamp when credentials were created |
| date_updated | String; ISO 8601 timestamp when credentials were last updated |

---

### 2. List credentials (verify)

Lists credentials configured for the trunk.

#### HTTP Request

GET `https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials`

#### Example Request

```bash
curl -s "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials"
```

#### HTTP Response

On success, the HTTP response status code will be **200 OK**.

#### Example Response

```json
{
  "request_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "method": "GET",
  "http_code": 200,
  "metadata": {
    "total": 1,
    "page_size": 50,
    "page": 1,
    "first_page_uri": "/v2/accounts/exotelveenotesting1m/trunks/trmum17d8e9a37a3732ecbf91a3u/credentials?page_size=50&offset=0",
    "prev_page_uri": null,
    "next_page_uri": null
  },
  "response": [
    {
      "code": 200,
      "error_data": null,
      "status": "success",
      "data": {
        "id": "1234",
        "trunk_sid": "trmum17d8e9a37a3732ecbf91a3u",
        "user_name": "voice_ai_user",
        "friendly_name": "voice_ai_platform",
        "date_created": "2026-01-23T11:37:36Z",
        "date_updated": "2026-01-23T11:37:36Z"
      }
    }
  ]
}
```

#### Response Parameters

| Parameter Name | Type & Value |
| --- | --- |
| request_id | String; Unique identifier for this API request |
| method | String; HTTP method used (GET) |
| http_code | Integer; HTTP status code (200 for success) |
| metadata.total | Integer; Total credential records available |
| metadata.page_size | Integer; Page size applied |
| metadata.page | Integer; Page number (if present) |
| metadata.first_page_uri | String; URI for first page |
| metadata.prev_page_uri | String or null; URI for previous page |
| metadata.next_page_uri | String or null; URI for next page |
| response | Array; List of credential objects |
| response[].data.id | String; Unique identifier for the credential entry |
| response[].data.trunk_sid | String; The trunk these credentials are associated with |
| response[].data.user_name | String; SIP digest username |
| response[].data.friendly_name | String or null; Optional label |
| response[].data.date_created | String; ISO 8601 timestamp when created |
| response[].data.date_updated | String; ISO 8601 timestamp when updated |

---

### 3. Delete credentials (rotate / revoke)

Deletes a credential entry when rotating credentials or removing access for a provider environment.

#### HTTP Request

DELETE `https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials?id=<CREDENTIAL_ID>`

**Important:** credential id is passed as **query param** `id` (not `/credentials/<CREDENTIAL_ID>`).

#### Example Request

```bash
curl -s -X DELETE "https://<API_KEY>:<API_TOKEN>@<SUBDOMAIN>/v2/accounts/<ACCOUNT_SID>/trunks/<TRUNK_SID>/credentials?id=<CREDENTIAL_ID>"
```

#### HTTP Response

On success, the HTTP response status code will be **200 OK**.

#### Example Response

```json
{
  "request_id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "method": "DELETE",
  "http_code": 200,
  "response": {
    "code": 200,
    "error_data": null,
    "status": "success",
    "data": {
      "id": "1234",
      "trunk_sid": "trmum17d8e9a37a3732ecbf91a3u",
      "user_name": "voice_ai_user",
      "friendly_name": "voice_ai_platform",
      "date_created": "2026-01-23T11:37:36Z",
      "date_updated": "2026-01-23T11:37:36Z"
    }
  }
}
```

#### Response Parameters

| Parameter Name | Type & Value |
| --- | --- |
| request_id | String; Unique identifier for this API request |
| method | String; HTTP method used (DELETE) |
| http_code | Integer; HTTP status code (200 for success) |
| id | String; Deleted credential identifier |
| trunk_sid | String; Trunk SID this credential belonged to |
| user_name | String; SIP digest username that was deleted |
| friendly_name | String or null; Optional label |
| date_created | String; ISO 8601 timestamp when credential was originally created |
| date_updated | String; ISO 8601 timestamp when credential was last updated |


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

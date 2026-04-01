# Connect Exotel SIP trunking to NLPearl.AI (Custom VoIP — Option B)

This guide connects **Exotel SIP trunking** to **[NLPearl.AI](https://platform.nlpearl.ai/)** using NLPearl’s **Custom VoIP** feature, where **Exotel is the SIP carrier** behind NLPearl (NLPearl’s portal drives the AI agent; Exotel provides the PSTN DID and SIP trunk).

**GitHub repo (reference):** https://github.com/exotel/AgentStream-VoiceAIEcosystem

> **Applicability:** **UI-driven + API-driven** (Custom VoIP configuration in NLPearl portal; optional outbound via API).

> **Exotel edge:** Use **IP:port** (and transport) from Exotel for SIP toward their gateway ([network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)). Don’t guess these values.

> **Edge hostnames you may see (India):** `in.voip.exotel.com:5070` (TCP) and `in.voip.exotel.com:443` (TLS). Use the exact host/IP + port + transport Exotel assigns. See [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md).

> **ACL vs digest (important):** Exotel trunk ACL (`whitelisted-ips`) is intended for **static `/32` IPs** only (`mask: 32`). Do **not** attempt to whitelist **CIDR ranges** on the Exotel trunk. If your platform/provider doesn’t give static `/32` egress, prefer **digest** and coordinate with Exotel support.

> **Option B definition (what we’re doing):** **NLPearl** is your Voice AI platform, and **Exotel SIP trunking** is the SIP provider behind NLPearl’s **Custom VoIP** (NLPearl controls the call; SIP signaling goes between NLPearl ↔ Exotel).

> **Engineering detail:** [`nlpearl/integrations/exotel-vsip/nlpearl-exotel-voice-ai-connector.md`](../../nlpearl/integrations/exotel-vsip/nlpearl-exotel-voice-ai-connector.md)

> **Quickstart:** [`nlpearl/integrations/exotel-vsip/QUICKSTART.md`](../../nlpearl/integrations/exotel-vsip/QUICKSTART.md)

---

## NLPearl (from official docs)

| Topic | Detail |
|--------|--------|
| Custom VoIP | [Custom VoIP integration](https://developers.nlpearl.ai/pages/custom_voip) — inbound SIP Domain shown after save; outbound requires SIP Trunk URL + User Part + optional auth |
| Getting started | [Getting started](https://developers.nlpearl.ai/pages/getting_started) |
| Outbound API | [Outbound/API](https://developers.nlpearl.ai/pages/outbound_api) and [Make Call API request](https://developers.nlpearl.ai/api-reference/v1/outbound/make-call) |
| Variables / callData | [Variables](https://developers.nlpearl.ai/pages/variables) — `callData` used in Make Call / Lead APIs |

---

## Flows (what you configure)

| Direction | What to configure |
|-----------|-------------------|
| **Outbound** (NLPearl → Exotel → PSTN) | **Exotel:** trunk + DID + **digest credentials**. **NLPearl:** Custom VoIP **Outbound** with **SIP Trunk URL** (Exotel trunk domain) + **User Part** + optional **credentials auth**. |
| **Inbound** (PSTN → Exotel → NLPearl) | **NLPearl:** Custom VoIP **Inbound** (choose IP auth or credentials) → save to get a **SIP Domain**. **Exotel:** set trunk **`destination-uris`** to that NLPearl SIP Domain (plus transport/port). **Exotel Flow:** Connect using **`sip:<trunk_sid>`**. |

Important: **Outbound** does **not** need `destination-uris`. **Inbound** does.

---

## Part A — NLPearl portal (Custom VoIP)

### A1. Prepare the AI agent

1. Create and **publish** your agent (Pearl) in [platform.nlpearl.ai](https://platform.nlpearl.ai/).
2. Ensure the agent supports your required language/flow and is ready for inbound/outbound usage.

### A2. Add Custom VoIP phone number

1. Open **Settings** → **Phone Numbers**.
2. Click **Custom VoIP**.
3. Enter your **Exotel DID** in E.164 (display/reference).
4. Choose **Call direction**: inbound, outbound, or both.

### A3. Configure Outbound (Exotel as SIP trunk)

In the **Outbound configuration** section ([Custom VoIP docs](https://developers.nlpearl.ai/pages/custom_voip)):

- **TLS (SRTP) Encryption**: enable only if you will use **SIP TLS** to Exotel and Exotel confirms TLS/SRTP requirements for your account.
- **SIP Trunk URL**: set to Exotel trunk SIP domain:  
  - `sip:${ACCOUNT_SID}.pstn.exotel.com` (recommended form), or  
  - `${ACCOUNT_SID}.pstn.exotel.com` if NLPearl UI expects host-only.
- **User Part**: use one of:
  - your Exotel trunk **digest username**, or
  - your DID in E.164 (if you want the SIP From-user to mirror the DID).
- **Authentication methods (Credentials Authentication)**: if enabled, set the **same** username/password as Exotel **`POST .../credentials`**.
- **Data center**: pick the closest region to Exotel’s SIP edge for latency.
- **Transfer Call using SIP REFER**: keep **off** initially. Turn it on only after you confirm Exotel supports/accepts REFER behavior for your trunk.

### A4. Configure Inbound (NLPearl receives from Exotel)

In the **Inbound configuration** section ([Custom VoIP docs](https://developers.nlpearl.ai/pages/custom_voip)):

- **TLS (SRTP) Encryption**: enable only if you will use TLS/SRTP and Exotel confirms.
- **Authentication**:
  - **Credentials Authentication**: recommended when you don’t have stable IPs and want strict auth.
  - **IP Address Authentication**: only if Exotel provides the fixed IPs NLPearl should accept traffic from.

After saving inbound settings, NLPearl shows a **SIP Domain to connect**. You will copy that domain into Exotel **`destination-uris`** (Part B).

---

## Part B — Exotel APIs

**Auth:** `API_KEY:API_TOKEN@api.in.exotel.com` · **200 requests/minute (SIP trunk APIs)** · [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md)

### B1. Create trunk + map DID + set digest credentials (outbound prerequisite)

Use the shared snippets:

- Create trunk
- Map phone number (DID)
- `POST .../credentials`

For NLPearl **Outbound**, these digest credentials should match what you configure in NLPearl’s **Outbound** auth section.

### B2. Inbound routing: set destination URI toward NLPearl SIP Domain

Once NLPearl gives you a **SIP Domain**, set it as the trunk destination URI:

```bash
curl -s -X PUT "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "YOUR_NLPEARL_SIP_DOMAIN:5061;transport=tls" }
    ]
  }'
```

Notes:
- Use **the exact domain** NLPearl shows after saving inbound config.
- Align **port + transport** with how you configured NLPearl (TLS vs TCP). If you’re unsure, start with what Exotel supports for your SIP trunking and what NLPearl’s Custom VoIP expects.

### B3. Exotel Flow: Connect applet

In your Exotel flow, use:

- **Applet**: Connect
- **Dial whom**: `sip:<trunk_sid>`

(`trunk_sid` is the value returned by create trunk; it is not a SIP URI.)

---

## Tests (quick)

### Outbound (NLPearl → PSTN)

1. In NLPearl, create/assign an outbound activity using the Custom VoIP number.
2. Trigger a test call from the UI and confirm Exotel sees SIP invites on the trunk.
3. If using API-driven outbound, use the Make Call endpoint per docs: [Make Call API request](https://developers.nlpearl.ai/api-reference/v1/outbound/make-call).

### Inbound (PSTN → NLPearl)

1. Call the Exotel DID from a mobile phone.
2. Verify Exotel routes to trunk (Flow Connect `sip:<trunk_sid>`) and then to the trunk `destination-uris` (NLPearl SIP Domain).
3. Confirm NLPearl receives the call and the assigned agent answers.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|--------|--------------|-----|
| `401/403` on outbound SIP | Digest mismatch | Ensure NLPearl outbound credentials match Exotel `POST .../credentials` exactly |
| Inbound reaches Exotel but not NLPearl | Missing/wrong `destination-uris` | Paste NLPearl SIP Domain exactly; confirm port/transport; re-GET destination URIs |
| TLS failures | TLS/SRTP toggles mismatched | Keep TLS/SRTP off on both sides for first smoke test unless Exotel confirms required TLS/SRTP; then enable consistently |
| Confusing auth failures after enabling allowlist | ACL + digest interaction | Remove `whitelisted-ips` unless you have dedicated `/32` static IP requirements; rely on digest and coordinate with Exotel |


# Connect Exotel SIP trunking to Smallest AI (Atoms)

This guide connects **Exotel SIP trunking** to **[Smallest AI](https://smallest.ai/)** **Atoms** using **Import SIP** (bring your own number over SIP). Smallest documents this in the platform **Phone Numbers** flow — you provide a **SIP Termination URL** (where Atoms sends **outbound** SIP toward your carrier) and copy the **SIP Origination URL** that Atoms gives you into your carrier for **inbound** routing.

> **Applicability:** **UI-driven** (Atoms “Import SIP” screen) with optional **API-driven** outbound call triggering.

> **Exotel edge:** Use **IP:port** (and transport) from Exotel for SIP toward their gateway ([network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)). Enter the value Smallest expects as the **termination** target (often `host:port` or `sip:host:port` — follow the **Import SIP** form and [phone numbers](https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md) doc).

> **Edge hostnames you may see (India):** `in.voip.exotel.com:5070` (TCP) and `in.voip.exotel.com:443` (TLS). Use the exact host/IP + port + transport Exotel assigns. See [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md).

> **ACL vs digest (important):** Exotel trunk ACL (`whitelisted-ips`) is intended for **static `/32` IPs** only (`mask: 32`). If a provider publishes only **CIDR/shared egress**, do **not** attempt to whitelist ranges—prefer **digest** and coordinate with Exotel/provider support if calls fail.

> **Origination URL is tenant-specific:** After you add a custom SIP number, Atoms shows a **SIP Origination URL** — **copy it exactly** into Exotel **`destination-uris`** for PSTN → Exotel → Smallest. Do **not** reuse example hostnames from third-party summaries.

> **Engineering detail:** [`smallest/integrations/exotel-vsip/smallest-exotel-voice-ai-connector.md`](../../smallest/integrations/exotel-vsip/smallest-exotel-voice-ai-connector.md)

> **Quickstart:** [`smallest/integrations/exotel-vsip/QUICKSTART.md`](../../smallest/integrations/exotel-vsip/QUICKSTART.md)

---

## Smallest AI (from official docs)

| Topic | Detail |
|--------|--------|
| Import SIP | [Phone Numbers — Import SIP](https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md): **Phone Number** (E.164), **SIP Termination URL**, optional **Username** / **Password**, **SIP Origination URL** (provided by Atoms → paste into provider) |
| Telephony overview | [Phone Numbers capability](https://atoms-docs.smallest.ai/intro/capabilities/telephony.md) — inbound, outbound, **SIP** to existing infrastructure |
| Outbound API | [Start an outbound call](https://atoms-docs.smallest.ai/api-reference/calls/start-an-outbound-call.md) — requires agent + linked phone number |
| Console | [app.smallest.ai](https://app.smallest.ai/) |

**Codec / security:** Smallest’s public docs describe SIP integration in product terms; confirm **codec** (e.g. G.711 / Opus) and **SRTP** requirements with [Smallest support](https://atoms-docs.smallest.ai/platform/troubleshooting/getting-help.md) if calls fail at SDP negotiation.

---

## Flows

| Direction | What to configure |
|-----------|-------------------|
| **Outbound SIP** (Atoms → Exotel → PSTN) | **Exotel:** create trunk → map DID → **`POST .../credentials`** (digest). **Smallest:** **Import SIP** — **SIP Termination URL** = Exotel **edge `IP:port`** (format per UI); **Username** / **Password** = same as Exotel credentials if you use digest auth. |
| **Inbound SIP** (PSTN → Exotel → Atoms) | **Smallest:** copy **SIP Origination URL** from the imported number. **Exotel:** **`POST .../destination-uris`** on the trunk with that URI (host, port, `;transport=` per Atoms). **Flow → Connect:** **`sip:<trunk_sid>`** in **Dial whom**. |

**Exotel trunk ACL (`whitelisted-ips`):** use **only** if Smallest publishes **fixed static SIP egress IPs** you must allow — **one IP per POST**, **`mask: 32`**. Exotel trunk **does not** support arbitrary CIDR range ACL entries. If Smallest does not publish static egress IPs, rely on **digest** and Smallest’s documented networking.

---

## Part A — Smallest AI (Atoms)

1. Sign in at [app.smallest.ai](https://app.smallest.ai/).  
2. **Phone Numbers** → **Add Number** → **Import SIP** ([guide](https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md)).  
3. Enter your Exotel DID in **E.164**.  
4. **SIP Termination URL:** Exotel **edge** host/IP and port from [Exotel network doc](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration) (align **transport** with Exotel and the Import SIP field).  
5. If using SIP digest with Exotel, set **Username** / **Password** to match **`POST .../credentials`** on the Exotel trunk.  
6. Save and copy **SIP Origination URL** for Exotel **inbound** routing.  
7. Assign the number to your agent (**Agent Settings → Phone Number** per [docs](https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md)).

---

## Part B — Exotel APIs

**Auth:** `API_KEY:API_TOKEN@api.in.exotel.com` · **200 requests/minute (SIP trunk APIs)** · [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md)

### Outbound SIP (minimal)

1. Create trunk  
2. Map DID  
3. `POST .../credentials` — must match Smallest **Username** / **Password** when used  

**Optional:** `POST .../whitelisted-ips` only for each **static** Smallest egress IP Smallest documents (`mask: 32`).

### Inbound SIP — destination URI on trunk

Use the **SIP Origination URL** from Atoms (example shape only — **replace with your copied value**):

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "<PASTE_SIP_ORIGINATION_URI_FROM_ATOMS>" }
    ]
  }'
```

### Connect applet (inbound)

**Dial whom:** **`sip:<trunk_sid>`** — [Voice AI / SIP trunking](https://support.exotel.com/support/solutions/articles/3000133452-flow-and-api-configuration-guide-for-voice-ai-contact-centre-platforms-via-exotel-virtual-sip-trunk).

---

## Testing

- **Outbound:** [Start an outbound call](https://atoms-docs.smallest.ai/api-reference/calls/start-an-outbound-call.md) with `agentId` and the imported **phone number**.  
- **Inbound:** PSTN dial your Exotel DID; call should reach the agent assigned in Atoms.

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| **401** on SIP | Digest mismatch (Exotel `/credentials` vs Smallest Import SIP) |
| **408** / timeout | **Termination URL** wrong **IP:port** or transport blocked |
| Inbound never reaches Atoms | **destination-uris** must match **SIP Origination URL** exactly; **Connect** uses **`sip:<trunk_sid>`** |
| Media / codec issues | Confirm codecs and SRTP with Smallest docs or support |

---

## References

| Resource | URL |
|----------|-----|
| Smallest — app | https://app.smallest.ai/ |
| Atoms — Phone Numbers (Import SIP) | https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md |
| Atoms — Telephony capability | https://atoms-docs.smallest.ai/intro/capabilities/telephony.md |
| Atoms — Start outbound call API | https://atoms-docs.smallest.ai/api-reference/calls/start-an-outbound-call.md |
| Atoms — Get acquired phone numbers | https://atoms-docs.smallest.ai/api-reference/phone-numbers/get-acquired-phone-numbers.md |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |

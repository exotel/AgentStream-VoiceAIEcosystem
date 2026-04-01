# Connect Exotel to Rapida AI

This guide aligns **Exotel** with **[Rapida AI](https://www.rapida.ai/)** for voice assistants. Rapida documents **two** relevant patterns:

> **Applicability:** **Hybrid** — **UI-driven** native Exotel integration (webhook/streaming) OR **SIP-driven** vSIP trunk path.

1. **Native Exotel integration** — Exotel **app / Flow** calls Rapida’s **webhook + bidirectional media stream** (no Exotel vSIP trunk API required for this path).  
2. **SIP trunk** — Exotel as **SIP carrier** (vSIP) ↔ Rapida’s **SIP server** at **`sip-01.in.rapida.ai:5060`** — same **trunk / credentials / destination-uris** patterns as other articles in this repo.

> **Primary Rapida reference:** [Exotel integration](https://doc.rapida.ai/integrations/telephony/exotel) · [SIP trunk integration](https://doc.rapida.ai/integrations/telephony/sip) · [Phone deployment](https://doc.rapida.ai/voice-deployment-options/phone)

> **Engineering detail:** [`rapida/integrations/exotel-vsip/rapida-exotel-voice-ai-connector.md`](../../rapida/integrations/exotel-vsip/rapida-exotel-voice-ai-connector.md)

> **Quickstart:** [`rapida/integrations/exotel-vsip/QUICKSTART.md`](../../rapida/integrations/exotel-vsip/QUICKSTART.md)

---

## Choose a path

| Path | Best when | Exotel work | Rapida work |
|------|-----------|-------------|-------------|
| **A — Native Exotel** | You want Rapida’s documented **streaming** integration | Configure **App / Flow** webhook to Rapida; assign DID | **Integration → Tools** → Exotel credentials; **Phone** deployment with **App ID** + number |
| **B — SIP trunk (vSIP)** | You need **SIP** toward Rapida from Exotel (or digest toward Exotel for outbound) | **Create trunk → map DID → credentials**; **`destination-uris`** toward Rapida SIP host; **Connect** **`sip:<trunk_sid>`** | **SIP Trunk** credential + **Phone** deployment with **SIP** as provider |

If you use **Path A**, you may not need **`POST …/trunks`** at all — follow Rapida’s Exotel guide first.

---

## Path A — Native Exotel (webhook + media stream)

From [Rapida — Exotel](https://doc.rapida.ai/integrations/telephony/exotel):

### Rapida — credentials

1. **Integration → Tools** → **Exotel** → **Setup Credential**.  
2. Fields (per Rapida): **Account SID**, **Client ID**, **Client Secret** — sourced from the Exotel dashboard (API / app settings).  
   - Exotel India often labels credentials **API Key** and **API Token**; map them to whatever Rapida’s form expects ([Exotel API credentials](https://my.in.exotel.com/apisettings/site#api-credentials) for India).

### Rapida — phone deployment

1. Assistant → **Deploy** → **Phone**.  
2. **Telephony:** provider **Exotel**, select credential, **Phone number** (Exotel virtual number), **App ID** (Exotel applet / flow id that will hit Rapida).

### Exotel — applet / Flow

Set the inbound URL Rapida documents (replace placeholders):

```text
https://websocket-01.in.rapida.ai/v1/talk/exotel/call/{your-assistant-id}?x-api-key={your-api-key}
```

Assign your Exotel number to this app. **Confirm the exact hostname and path** in [Rapida’s Exotel guide](https://doc.rapida.ai/integrations/telephony/exotel) if it changes.

### Outbound

Use Rapida **SDK** or **REST** (`POST https://api.rapida.ai/v1/talk/call`) — examples in [Rapida — Exotel](https://doc.rapida.ai/integrations/telephony/exotel).

---

## Path B — Exotel vSIP + Rapida SIP trunk

From [Rapida — SIP trunk](https://doc.rapida.ai/integrations/telephony/sip):

### Rapida SIP endpoint (for routing **to** Rapida)

```text
sip:sip-01.in.rapida.ai:5060
```

Transport **UDP** or **TCP**; codecs **G.711 PCMU** (preferred) / **PCMA**. Allow **RTP** per Rapida + your firewall docs.

### Exotel — inbound PSTN → Rapida

1. **Create trunk** → **map DID** → (optional) **`POST …/credentials`** if your design requires digest on the Exotel side.  
2. **`POST …/destination-uris`** toward Rapida, e.g.:

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "sip-01.in.rapida.ai:5060;transport=udp" }
    ]
  }'
```

3. **Flow → Connect:** **Dial whom** = **`sip:<trunk_sid>`** ([Voice AI / vSIP](https://support.exotel.com/support/solutions/articles/3000133452-flow-and-api-configuration-guide-for-voice-ai-contact-centre-platforms-via-exotel-virtual-sip-trunk)).

### Rapida — SIP trunk credential

**Integration → Tools** → **SIP Trunk**: set **SIP URI** to your **Exotel edge `IP:port`** (and digest if used) for **outbound** from Rapida toward Exotel — mirror **ElevenLabs-style** termination. Use [Exotel network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration) for edge values.

**Optional Exotel ACL:** `POST …/whitelisted-ips` **only** if Rapida publishes **fixed static SIP egress IPs** to allow — **one IP per POST**, **`mask: 32`** (Exotel trunk does not support arbitrary CIDR ranges).

### Shared Exotel curls

[`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md)

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| Inbound never hits Rapida (Path A) | Webhook URL, **assistant id**, **x-api-key**, number linked to correct app |
| SIP failures (Path B) | **sip-01.in.rapida.ai** reachability, **UDP/TCP**, **codec**; **destination-uris** format |
| Outbound fails | Rapida credential + deployment; **from** number is your Exotel DID |
| **Connect** misrouted | **`sip:<trunk_sid>`** only in Dial whom (Path B) |

---

## References

| Resource | URL |
|----------|-----|
| Rapida — Exotel | https://doc.rapida.ai/integrations/telephony/exotel |
| Rapida — SIP trunk | https://doc.rapida.ai/integrations/telephony/sip |
| Rapida — Phone deployment | https://doc.rapida.ai/voice-deployment-options/phone |
| Rapida — Credentials | https://doc.rapida.ai/credential/rapida-credentials |
| Rapida — Overview | https://doc.rapida.ai/introduction/overview |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |

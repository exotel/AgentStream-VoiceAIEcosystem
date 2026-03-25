# Connect Exotel with Vocallabs (Superflow B2B API)

This guide links **Exotel Virtual SIP Trunking (vSIP)** and your **Exotel DID** to **[Vocallabs](https://docs.vocallabs.ai/vocallabs)**. Vocallabs publishes a **B2B REST API** on **`https://api.superflow.run/b2b/`** — including **`createSIPCall`** with `did`, `phone_number`, `websocket_url`, and `webhook_url` — not the same **dashboard BYO SIP trunk** pattern as Vapi or ElevenLabs. Use this article for **API + telephony alignment**; confirm **inbound SIP URIs** and **static egress IPs** with Vocallabs if you need classic trunk **`destination-uris`** / **`whitelisted-ips`**.

> **Docs:** [Vocallabs API documentation](https://docs.vocallabs.ai/vocallabs) (hosted API reference and samples).

> **Engineering detail:** [`vocallabs/integrations/exotel-vsip/vocallabs-exotel-voice-ai-connector.md`](../../vocallabs/integrations/exotel-vsip/vocallabs-exotel-voice-ai-connector.md)

---

## Vocallabs API (from official docs)

| Topic | Detail |
|--------|--------|
| Base | `https://api.superflow.run/b2b/` |
| Auth | `POST …/createAuthToken/` — JSON `clientId`, `clientSecret` → **Bearer** token for subsequent calls ([docs](https://docs.vocallabs.ai/vocallabs)) |
| SIP call | `POST …/vocallabs/createSIPCall` — `phone_number`, `did`, `websocket_url`, `webhook_url`, `sample_rate` |
| Outbound-style calls | `POST …/vocallabs/initiateVocallabsCall` — `agentId`, `prospect_id` |
| Webhook dial | `POST …/vocallabs/initiateCallWebhook` — `from` (DID), `number` (destination) |
| Websocket URL | `GET …/vocallabs/getWebsocketUrl` — query `agent_id`, `prospect_id` |

**Wallet / usage:** `GET …/getGreenBalance`, transaction history — see Vocallabs docs for billing context.

---

## How this maps to Exotel

| Concept | Exotel side | Vocallabs side |
|--------|-------------|----------------|
| **DID** | Exophone on vSIP trunk ([snippets](./_exotel-trunk-api-snippets.md)) | Use the same E.164 as **`did`** (or `from` in webhook flows) where the API expects your caller / rented number |
| **PSTN termination** | Exotel edge **IP:port** + digest (`POST …/credentials`) | **Not** fully specified in the public reference as a single “SIP gateway hostname” like other providers — **coordinate with Vocallabs** for SIP leg details if `createSIPCall` is meant to drive traffic to Exotel |
| **Inbound PSTN → AI** | Trunk **`destination-uris`** + Flow **Connect** **`sip:<trunk_sid>`** | Requires a **SIP origination target** from Vocallabs. If their team only documents **REST + websocket**, implement that path first; add **destination-uris** when they provide a stable SIP URI |

---

## Part A — Vocallabs (auth + SIP call)

### 1. Create token

```bash
curl -s -X POST 'https://api.superflow.run/b2b/createAuthToken/' \
  -H 'Content-Type: application/json' \
  -d '{"clientId":"CLIENT_ID","clientSecret":"CLIENT_SECRET"}'
```

Use the returned token as **`Authorization: Bearer <token>`**.

### 2. Create SIP call (example shape)

Per [Vocallabs API docs](https://docs.vocallabs.ai/vocallabs):

```bash
curl -s -X POST 'https://api.superflow.run/b2b/vocallabs/createSIPCall' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer AUTH_TOKEN' \
  -d '{
    "phone_number": "+91XXXXXXXXXX",
    "did": "+91YYYYYYYYYY",
    "websocket_url": "wss://your-bridge.example.com/media",
    "webhook_url": "https://your-app.example.com/vocallabs/webhook",
    "sample_rate": "16000"
  }'
```

Replace **`did`** with your **Exotel number** in E.164 when that number is the identity Vocallabs should use for the session. **`websocket_url`** / **`webhook_url`** must be **your** endpoints as required by Vocallabs — see their latest field definitions.

### 3. Other flows

- **`initiateVocallabsCall`** — agent + prospect ([docs](https://docs.vocallabs.ai/vocallabs)).  
- **`initiateCallWebhook`** — `from` / `number` for click-to-call style flows.  
- **`getWebsocketUrl`** — retrieve media URL for `agent_id` + `prospect_id`.

---

## Part B — Exotel (vSIP + DID)

When you use Exotel as the **Indian PSTN carrier** for the same DID you pass to Vocallabs:

1. **Create trunk** → **map DID** → **`POST …/credentials`** (if your design uses SIP digest toward Exotel).  
2. Templates: [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md).  
3. **Optional:** `POST …/whitelisted-ips` **only** if Vocallabs publishes **fixed static egress IPs** (`mask: 32` per IP).  
4. **Inbound** (only if Vocallabs gives you a **SIP URI** to send calls to):  
   `POST …/destination-uris` toward that URI → **Flow → Connect** → **`sip:<trunk_sid>`** ([Voice AI / vSIP](https://support.exotel.com/support/solutions/articles/3000133452-flow-and-api-configuration-guide-for-voice-ai-contact-centre-platforms-via-exotel-virtual-sip-trunk)).

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| **401** on Superflow | Valid **`createAuthToken`** + **Bearer** header |
| Call fails / wrong CLI | **`did`** / **`from`** match **E.164** Exotel number you own |
| No media | **`websocket_url`**, **`getWebsocketUrl`**, firewall to Vocallabs / your bridge |
| SIP vs API mismatch | Vocallabs may be **API-first** — confirm with their team before assuming full vSIP parity |

---

## References

| Resource | URL |
|----------|-----|
| Vocallabs API docs | https://docs.vocallabs.ai/vocallabs |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |
| Exotel network / firewall | https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration |

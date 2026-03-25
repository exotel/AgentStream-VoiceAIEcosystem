# Vocallabs + Exotel — connector reference

Companion to [`docs/support/exotel-vocallabs-sip-trunk.md`](../../../docs/support/exotel-vocallabs-sip-trunk.md).

---

## API host

| Environment | Base URL |
|-------------|----------|
| Production (per [docs](https://docs.vocallabs.ai/vocallabs)) | `https://api.superflow.run/b2b/` |

---

## Authentication

```http
POST /createAuthToken/
Content-Type: application/json

{"clientId":"...","clientSecret":"..."}
```

Use **`Authorization: Bearer <token>`** on subsequent requests.

---

## SIP-related endpoints (Vocallabs namespace)

| Method | Path | Notes |
|--------|------|--------|
| POST | `/vocallabs/createSIPCall` | `phone_number`, `did`, `websocket_url`, `webhook_url`, `sample_rate` |
| POST | `/vocallabs/initiateVocallabsCall` | `agentId`, `prospect_id` |
| POST | `/vocallabs/initiateCallWebhook` | `from`, `number` |
| GET | `/vocallabs/getWebsocketUrl` | `agent_id`, `prospect_id` |

Full list: [Vocallabs API documentation](https://docs.vocallabs.ai/vocallabs).

---

## Exotel alignment

- **DID:** Use your Exotel **E.164** Exophone where the API expects **`did`** or **`from`**.  
- **Trunk:** Standard vSIP steps — [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md).  
- **Inbound SIP URI:** Obtain from Vocallabs if they support carrier **`destination-uris`**; not enumerated in the public REST reference alone.

---

## References

- [Vocallabs API docs](https://docs.vocallabs.ai/vocallabs)  
- [Exotel SIP API](https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference)

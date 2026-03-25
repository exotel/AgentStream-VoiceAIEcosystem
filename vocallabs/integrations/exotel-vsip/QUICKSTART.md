# Quickstart: Exotel DID + Vocallabs (Superflow B2B)

**Prerequisites:** [Vocallabs API credentials](https://docs.vocallabs.ai/vocallabs) (`clientId` / `clientSecret`); Exotel vSIP + **E.164** DID if Exotel is your carrier.

**API base:** `https://api.superflow.run/b2b/`

---

## 1 — Auth token

```bash
curl -s -X POST 'https://api.superflow.run/b2b/createAuthToken/' \
  -H 'Content-Type: application/json' \
  -d '{"clientId":"'"$CLIENT_ID"'","clientSecret":"'"$CLIENT_SECRET"'"}'
```

Export **`AUTH_TOKEN`** from the response (field name per Vocallabs response).

---

## 2 — Create SIP call (example)

```bash
curl -s -X POST 'https://api.superflow.run/b2b/vocallabs/createSIPCall' \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $AUTH_TOKEN" \
  -d '{
    "phone_number": "+91XXXXXXXXXX",
    "did": "+91YYYYYYYYYY",
    "websocket_url": "wss://your-bridge.example.com/media",
    "webhook_url": "https://your-app.example.com/webhook",
    "sample_rate": "16000"
  }'
```

Set **`did`** to your **Exotel DID** when that is the caller identity for the session.

---

## 3 — Exotel trunk (if using vSIP)

[`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

---

## Full reference

- [Vocallabs API docs](https://docs.vocallabs.ai/vocallabs)  
- [`exotel-vocallabs-sip-trunk.md`](../../../docs/support/exotel-vocallabs-sip-trunk.md)

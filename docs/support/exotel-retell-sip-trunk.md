# Connect Exotel Virtual SIP Trunk to Retell AI

This guide connects **Exotel vSIP** to **Retell AI** using elastic SIP per [Retell custom telephony](https://docs.retellai.com/deploy/custom-telephony), with Exotel as the Indian PSTN provider.

> **Exotel edge:** Use **IP:port** from Exotel for SIP toward their gateway ([network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)).

> **Full reference:** [`retell/integrations/exotel-vsip/retell-exotel-voice-ai-connector.md`](../../retell/integrations/exotel-vsip/retell-exotel-voice-ai-connector.md)

---

## Retell (from official docs)

- **SIP server:** `sip:sip.retellai.com` with `;transport=tcp` (or `tls` / `udp`) — [Custom telephony](https://docs.retellai.com/deploy/custom-telephony).
- Retell publishes **IP ranges** for carriers to allowlist **toward Retell**; on **Exotel trunk ACL**, you can only add **static single IPs** (`mask: 32`) per Exotel — **not** full CIDR ranges on the trunk. If Retell gives ranges, coordinate with Exotel or use **digest** auth.

---

## Flows

| Direction | What to configure |
|-----------|-------------------|
| **Outbound SIP** | Exotel: **create trunk → map DID → credentials**. Optional **`whitelisted-ips`** only if Retell provides a **fixed static egress IP** (one IP per POST, `mask: 32`). |
| **Inbound SIP** | Exotel: **destination URI** on trunk toward Retell (`sip.retellai.com` host/port/transport per Retell). **Connect** applet: **`sip:<trunk_sid>`** in **Dial whom** (value = API `trunk_sid`, not a full URI). |

---

## Part A — Retell

1. Configure agent; **import** Exotel DID after Exotel trunk exists ([Custom telephony](https://docs.retellai.com/deploy/custom-telephony)).
2. Match **digest** to Exotel `POST .../credentials` for outbound termination.

---

## Part B — Exotel APIs

**Auth:** `API_KEY:API_TOKEN@api.in.exotel.com` · **200 CPM** · [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md)

### Outbound SIP

1. Create trunk  
2. Map DID  
3. `POST .../credentials`  
4. *(Optional)* `whitelisted-ips` — **only** for a **static IP** from Retell, `mask: 32`

### Inbound SIP

`POST .../destination-uris` — example shape (confirm port/transport with Retell):

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "sip.retellai.com:5060;transport=tcp" }
    ]
  }'
```

**Connect:** **`sip:<trunk_sid>`** in Dial whom.

---

## Dial to SIP URI (alternative)

[Register Phone Call](https://docs.retellai.com/api-references/register-phone-call) → dial `sip:{call_id}@sip.retellai.com` within **5 minutes** — [Method 2](https://docs.retellai.com/deploy/custom-telephony).

---

## References

| Resource | URL |
|----------|-----|
| Retell dashboard | https://dashboard.retellai.com/ |
| Retell — custom telephony | https://docs.retellai.com/deploy/custom-telephony |
| Retell — quick start | https://docs.retellai.com/get-started/quick-start |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |

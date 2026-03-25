# Smallest AI (Atoms) + Exotel vSIP — connector reference

Companion to [`docs/support/exotel-smallest-ai-sip-trunk.md`](../../../docs/support/exotel-smallest-ai-sip-trunk.md).

---

## Terminology mapping (Atoms ↔ Exotel)

| Atoms (Import SIP) | Typical Exotel side |
|--------------------|---------------------|
| **SIP Termination URL** | Where Atoms sends SIP for **outbound** PSTN calls → set to Exotel **edge `IP:port`** ([Exotel network](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)) |
| **Username** / **Password** | Same values as Exotel **`POST .../trunks/{id}/credentials`** (`user_name`, `password`) when using digest |
| **SIP Origination URL** | Value Atoms **displays after** import → put into Exotel **`POST .../destination-uris`** for **inbound** PSTN → Smallest |

---

## Exotel checklist

1. `POST .../trunks`  
2. `POST .../trunks/{TRUNK_SID}/phone-numbers` — E.164 DID  
3. `POST .../trunks/{TRUNK_SID}/credentials` — align with Atoms Import SIP  
4. *(Optional)* `POST .../whitelisted-ips` — only if Smallest gives **static** egress IPs, **`mask: 32`** each  
5. `POST .../trunks/{TRUNK_SID}/destination-uris` — **SIP Origination URL** from Atoms  
6. Exotel Flow **Connect** — **Dial whom:** **`sip:<trunk_sid>`**

Shared curls: [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md).

---

## Smallest checklist

1. [app.smallest.ai](https://app.smallest.ai/) → **Phone Numbers** → **Import SIP**  
2. Fill **SIP Termination URL** + optional digest fields  
3. Copy **SIP Origination URL** → Exotel step 5  
4. Assign number to agent  
5. Test outbound via API ([start an outbound call](https://atoms-docs.smallest.ai/api-reference/calls/start-an-outbound-call.md))

---

## References

- [Atoms — Phone Numbers](https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md)  
- [Exotel SIP API](https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference)

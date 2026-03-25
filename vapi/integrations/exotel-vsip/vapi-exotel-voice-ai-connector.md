# Vapi + Exotel vSIP — connector reference

This document complements [`docs/support/exotel-vapi-sip-trunk.md`](../../../docs/support/exotel-vapi-sip-trunk.md) with **API-oriented** detail for **BYO SIP trunk** + **BYO phone number**.

---

## Roles

| System | Role |
|--------|------|
| **Exotel vSIP** | PSTN carrier in India; trunk, DID, digest, optional **destination URI** for inbound toward Vapi |
| **Vapi** | Voice AI; **`byo-sip-trunk`** credential points **outbound** SIP at Exotel **edge IPv4:port** |

---

## Vapi: create BYO SIP trunk credential

Use **`POST https://api.vapi.ai/credential`** with **`Authorization: Bearer <VAPI_PRIVATE_KEY>`**.

**Important:** `gateways[].ip` must be a **numeric IPv4** (not a hostname). Resolve Exotel’s edge hostname to IPv4 if needed ([Vapi troubleshooting](https://docs.vapi.ai/advanced/sip/troubleshoot-sip-trunk-credential-errors)).

Example shape (adjust `port` and `outboundProtocol` to match Exotel vSIP — often **TCP** or **TLS** on the port Exotel assigns):

```json
{
  "provider": "byo-sip-trunk",
  "name": "Exotel India",
  "gateways": [
    {
      "ip": "198.51.100.10",
      "port": 5070,
      "outboundEnabled": true,
      "inboundEnabled": false,
      "outboundProtocol": "tcp"
    }
  ],
  "outboundLeadingPlusEnabled": true,
  "outboundAuthenticationPlan": {
    "authUsername": "SIP_USER_FROM_EXOTEL_CREDENTIALS",
    "authPassword": "SIP_PASS_FROM_EXOTEL_CREDENTIALS"
  }
}
```

- Replace **`ip` / `port` / `outboundProtocol`** with values that match **Exotel’s** edge for your account ([Exotel network](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)).
- Set **`inboundEnabled": true`** when you configure **inbound** PSTN via Exotel toward Vapi (and follow Vapi’s inbound notes).

---

## Vapi: associate phone number

`POST https://api.vapi.ai/phone-number`:

```json
{
  "provider": "byo-phone-number",
  "name": "Exotel DID",
  "number": "+9198XXXXXXXX",
  "numberE164CheckEnabled": true,
  "credentialId": "<CREDENTIAL_ID_FROM_PREVIOUS_STEP>"
}
```

Attach the number to an assistant in the [dashboard](https://dashboard.vapi.ai/) or via API.

---

## Exotel: allowlist Vapi SBC IPs

Vapi uses **two** signalling IPs ([docs](https://docs.vapi.ai/advanced/sip/sip-networking)):

- `44.229.228.186/32`
- `44.238.177.138/32`

On Exotel, add **each** via **`POST .../whitelisted-ips`** with **`mask: 32`** (two API calls). Exotel does **not** support a single CIDR range entry for arbitrary subnets on the trunk ACL.

---

## Exotel: trunk steps (summary)

1. `POST .../trunks` — create trunk  
2. `POST .../trunks/{TRUNK_SID}/phone-numbers` — map E.164 DID  
3. `POST .../trunks/{TRUNK_SID}/credentials` — **same** digest as Vapi `outboundAuthenticationPlan`  
4. `POST .../trunks/{TRUNK_SID}/whitelisted-ips` — both Vapi IPs  
5. **Inbound only:** `POST .../trunks/{TRUNK_SID}/destination-uris` toward **`sip.vapi.ai`** (port/transport per Vapi + Exotel)  
6. **Flow → Connect:** **`sip:<trunk_sid>`** in **Dial whom**

Shared curls: [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md).

---

## Test call (Vapi)

`POST https://api.vapi.ai/call/phone` — see [SIP trunking](https://docs.vapi.ai/advanced/sip/sip-trunk) for the latest JSON shape (`assistantId`, `phoneNumberId`, `customer.number`).

---

## References

- [Vapi SIP trunking](https://docs.vapi.ai/advanced/sip/sip-trunk)  
- [Vapi SIP networking](https://docs.vapi.ai/advanced/sip/sip-networking)  
- [Exotel SIP API](https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference)

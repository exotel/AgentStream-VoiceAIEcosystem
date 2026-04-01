# Quickstart — Retell AI + Exotel vSIP

Goal: first successful **outbound** and **inbound** call using **Exotel as the India PSTN carrier** and **Retell** as the Voice AI platform (elastic SIP / custom telephony).

## Prereqs

- Exotel: vSIP enabled, DID active (E.164), Exotel edge **IP:port** known
- Retell: Custom telephony enabled ([docs](https://docs.retellai.com/deploy/custom-telephony))

Shared Exotel API snippets:

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

## Outbound (Retell → Exotel → PSTN)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - Create digest credentials on the trunk (`POST .../credentials`)
2. **Retell**
   - Import the Exotel DID using Retell custom telephony
   - Set SIP auth to the same digest credentials as Exotel
   - Set Retell termination toward Exotel using the Exotel **edge `IP:port`**

Optional:

- Exotel trunk `whitelisted-ips` only if Retell provides **static `/32`** egress IPs (one IP per POST, `mask: 32`). Do **not** attempt CIDR ranges on Exotel trunk.

## Inbound (PSTN → Exotel → Retell)

1. **Retell**
   - Confirm the inbound SIP destination details in Retell docs for your configuration
2. **Exotel**
   - Set trunk `destination-uris` toward Retell SIP ingress (example is in the support article)
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`
3. Call the Exotel DID and confirm Retell answers.

## If calls fail

- **401/403**: digest mismatch between Exotel `/credentials` and Retell custom telephony configuration.
- **Inbound not reaching Retell**: wrong `destination-uris` host/transport, or Flow Connect is not `sip:<trunk_sid>`.
- Use the full troubleshooting guide: [`docs/support/exotel-retell-sip-trunk.md`](../../../docs/support/exotel-retell-sip-trunk.md)

## Links

- Retell custom telephony: https://docs.retellai.com/deploy/custom-telephony
- Repo support article: [`docs/support/exotel-retell-sip-trunk.md`](../../../docs/support/exotel-retell-sip-trunk.md)

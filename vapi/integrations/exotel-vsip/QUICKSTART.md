# Quickstart — Vapi (BYO SIP trunk) + Exotel SIP trunking

Goal: first successful **outbound** and **inbound** call using **Exotel as the India PSTN carrier** and **Vapi** as the Voice AI platform via **BYO SIP trunk**.

## Prereqs

- Exotel: SIP trunking enabled, DID active (E.164), Exotel edge **IPv4** `IP:port` known
- Vapi: dashboard access + private API key

Shared Exotel API snippets:

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

## Outbound (Vapi → Exotel → PSTN)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - Create digest credentials on the trunk (`POST .../credentials`)
   - Whitelist both Vapi SBC IPs (`mask: 32` each): `44.229.228.186`, `44.238.177.138`
2. **Vapi**
   - Create `byo-sip-trunk` credential with gateway = Exotel **edge IPv4** and matching transport/port
   - Set `outboundAuthenticationPlan` to the same digest as Exotel trunk credentials
   - Create `byo-phone-number` linked to the credential
3. Place a test call (Vapi `POST /call/phone`).

## Inbound (PSTN → Exotel → Vapi)

1. **Vapi**
   - Ensure inbound is enabled for the trunk/gateway if you want PSTN inbound
2. **Exotel**
   - Set trunk `destination-uris` toward `sip.vapi.ai` (port/transport per Vapi networking docs)
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`
3. Call the Exotel DID and confirm Vapi answers.

## If calls fail

- **Vapi gateway rejects hostname**: Vapi requires IPv4 in `gateways[].ip`. Use Exotel-provided IPv4 (do not guess).
- **401/403**: digest mismatch, or missing one of the two Vapi SBC allowlist entries.
- Use the full guide: [`docs/support/exotel-vapi-sip-trunk.md`](../../../docs/support/exotel-vapi-sip-trunk.md)

## Links

- Vapi SIP trunking: https://docs.vapi.ai/advanced/sip/sip-trunk
- Vapi networking: https://docs.vapi.ai/advanced/sip/sip-networking
- Repo support article: [`docs/support/exotel-vapi-sip-trunk.md`](../../../docs/support/exotel-vapi-sip-trunk.md)

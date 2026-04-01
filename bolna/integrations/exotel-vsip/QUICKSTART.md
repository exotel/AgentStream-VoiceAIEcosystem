# Quickstart — Bolna (BYOT SIP) + Exotel SIP trunking

Goal: first successful **outbound** and **inbound** call using **Exotel as the India PSTN carrier** and **Bolna BYOT SIP** for the Voice AI leg.

## Prereqs

- Exotel: SIP trunking enabled, DID active (E.164), Exotel edge **IP:port** known
- Bolna: SIP trunking enabled (BYOT is Beta per Bolna docs)

Shared Exotel API snippets:

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

## Outbound (Bolna → Exotel → PSTN)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - Create digest credentials on the trunk (`POST .../credentials`)
2. **Bolna**
   - Create a SIP trunk with **gateway** = Exotel **edge `IP:port`**
   - Use `userpass` auth and set username/password to match Exotel digest
   - Assign the DID/phone number to your Bolna agent and place an outbound call

Optional:

- Exotel trunk `whitelisted-ips` only if Bolna provides a **static `/32`** egress IP. (Use one IP per POST, `mask: 32`; do not attempt CIDR ranges on Exotel trunk.)

## Inbound (PSTN → Exotel → Bolna)

1. **Bolna**
   - Confirm inbound BYOT SIP ingress details in Bolna docs (may be IP-based)
2. **Exotel**
   - Set trunk `destination-uris` toward Bolna inbound SIP host
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`
3. Call the DID and confirm Bolna answers.

## If calls fail

- **401/403**: digest mismatch between Exotel `/credentials` and Bolna `userpass`.
- **Inbound not reaching Bolna**: wrong `destination-uris` target, or Connect not set to `sip:<trunk_sid>`.
- Use the full guide: [`docs/support/exotel-bolna-sip-trunk.md`](../../../docs/support/exotel-bolna-sip-trunk.md)

## Links

- Bolna BYOT setup: https://www.bolna.ai/docs/sip-trunking/byot-setup
- Repo support article: [`docs/support/exotel-bolna-sip-trunk.md`](../../../docs/support/exotel-bolna-sip-trunk.md)

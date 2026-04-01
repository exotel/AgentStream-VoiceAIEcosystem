# Quickstart — Ultravox (SIP) + Exotel SIP trunking

Goal: first successful **outbound** and **inbound** call using **Exotel as the India PSTN carrier** and **Ultravox SIP** for the Voice AI leg.

## Prereqs

- Exotel: SIP trunking enabled, DID active (E.164), Exotel edge **IP:port** known
- Ultravox: account + agent created; SIP enabled

Shared Exotel API snippets:

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

## Outbound (Ultravox → Exotel → PSTN)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - Create digest credentials on the trunk (`POST .../credentials`)
2. **Ultravox**
   - Place an outgoing SIP call using `medium.sip.outgoing` toward Exotel edge `IP:port`
   - Provide `username/password` matching Exotel trunk credentials

## Inbound (PSTN → Exotel → Ultravox)

1. **Ultravox**
   - Determine your SIP `domain` (GET `/api/sip`) and the expected INVITE target pattern
   - Allowlist Exotel signaling on Ultravox (`allowedCidrRanges`) using `/32` where applicable (Ultravox-side CIDR)
2. **Exotel**
   - Set trunk `destination-uris` toward Ultravox SIP host/URI (per Ultravox docs)
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`
3. Call the Exotel DID and confirm Ultravox answers.

## If calls fail

- Ultravox inbound allowlisting uses CIDR on **Ultravox side**; Exotel trunk ACL is `/32` per-IP only and should not be used for CIDR ranges.
- Use the full guide: [`docs/support/exotel-ultravox-sip-trunk.md`](../../../docs/support/exotel-ultravox-sip-trunk.md)

## Links

- Ultravox SIP guide: https://docs.ultravox.ai/telephony/sip
- Repo support article: [`docs/support/exotel-ultravox-sip-trunk.md`](../../../docs/support/exotel-ultravox-sip-trunk.md)

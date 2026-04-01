# Quickstart — Pipecat (via Daily SIP) + Exotel SIP trunking

Goal: first successful **PSTN↔agent** call where **Exotel is the India PSTN carrier** and **Pipecat** bridges into **Daily SIP / rooms**.

## Prereqs

- Exotel: SIP trunking enabled, DID active (E.164), Exotel edge **IP:port** known
- Daily: paid account with SIP enabled ([Daily SIP](https://docs.daily.co/guides/products/dial-in-dial-out/sip))
- Pipecat: follow Pipecat telephony guide using Daily SIP ([Pipecat PSTN + Daily SIP](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip))

Shared Exotel API snippets:

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

## Outbound (Daily SIP dial-out → Exotel → PSTN)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - Create digest credentials on the trunk (`POST .../credentials`)
2. **Daily / your Pipecat dial-out logic**
   - SIP dial-out toward Exotel using the Exotel edge `IP:port`
   - Use digest auth aligned to Exotel trunk credentials

Optional:

- Exotel trunk `whitelisted-ips` only if your Daily/SIP egress is **static `/32`** (one IP per POST, `mask: 32`). Do **not** attempt CIDR ranges on Exotel trunk.

## Inbound (PSTN → Exotel → Daily SIP / Pipecat)

Preferred (typical for Pipecat):

1. Use Pipecat’s **webhook + `sip_uri` bridge** model (dynamic Daily `sip_uri` per call) instead of a single static destination URI.

Static inbound SIP (only if you have a fixed SIP ingress target):

1. **Exotel**
   - Set trunk `destination-uris` toward your fixed SIP ingress target
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`

## If calls fail

- **Not “5 minutes”**: Pipecat + Daily is intentionally more engineering-heavy than the “single static SIP host” providers.
- Use the full guide: [`docs/support/exotel-pipecat-sip-trunk.md`](../../../docs/support/exotel-pipecat-sip-trunk.md)

## Links

- Pipecat telephony guide: https://docs.pipecat.ai/guides/telephony/twilio-daily-sip
- Daily SIP: https://docs.daily.co/guides/products/dial-in-dial-out/sip
- Repo support article: [`docs/support/exotel-pipecat-sip-trunk.md`](../../../docs/support/exotel-pipecat-sip-trunk.md)

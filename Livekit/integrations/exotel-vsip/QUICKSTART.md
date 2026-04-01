# Quickstart — LiveKit Cloud Telephony + Exotel SIP trunking

Goal: first successful **outbound** and **inbound** call using **Exotel as the India PSTN carrier** and **LiveKit rooms** as the SIP destination for agents.

## Prereqs

- Exotel: SIP trunking enabled, DID active (E.164), Exotel edge **IP:port** known
- LiveKit: Cloud project with **Telephony** enabled; you can access **SIP URI** and create SIP trunks + dispatch rules

Shared Exotel API snippets live in:

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

Full detail (recommended to keep open while following this):

- [`docs/support/exotel-livekit-sip-trunk.md`](../../../docs/support/exotel-livekit-sip-trunk.md)

## Outbound (LiveKit → Exotel → PSTN)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - Create digest credentials on the trunk (`POST .../credentials`)
2. **LiveKit Cloud**
   - Telephony → SIP trunks → **Outbound**
   - Set **address** = Exotel **edge `IP:port`** (from Exotel)
   - Set **numbers** = your Exotel DID in **E.164**
   - Set **authUsername/authPassword** = the same digest as Exotel trunk credentials
3. Place an outbound call using your LiveKit app/agent.

If you’re using the repo sample, follow:

- `Livekit/livekit-outbound-caller-agent/README.md`
- Exotel-specific notes: `Livekit/livekit-outbound-caller-agent/OUTBOUND-EXOTEL-NOTES.md`

## Inbound (PSTN → Exotel → LiveKit)

1. **LiveKit Cloud**
   - Create an **Inbound** SIP trunk with your Exotel DID (E.164)
   - Create at least one **Dispatch rule** so calls land in a room
   - Note your project SIP URI / region host (e.g. `YOUR_SUBDOMAIN.india.sip.livekit.cloud`)
2. **Exotel**
   - Set trunk `destination-uris` to LiveKit SIP host (port/transport per LiveKit docs)
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`
3. Call the Exotel DID from a phone and confirm the call is dispatched into the room and handled by your agent.

## If calls fail

- **403 from Exotel (`X-Exotel-ErrorCode: 4001`)**: digest mismatch, wrong Exotel edge `IP:port`, or an IP allowlist expectation on your trunk. See `Livekit/livekit-outbound-caller-agent/OUTBOUND-EXOTEL-NOTES.md` and the support article.
- **Rings but no bot audio**: the SIP participant is in a room, but **no agent is publishing audio in the same room**. See `OUTBOUND-EXOTEL-NOTES.md` (“no audio” section).
- **Inbound doesn’t reach LiveKit**: verify Exotel `destination-uris` points to the correct LiveKit SIP host and the Flow Connect dial string is exactly `sip:<trunk_sid>`.

## Links

- LiveKit SIP trunk setup: https://docs.livekit.io/telephony/start/sip-trunk-setup/
- Repo support article: [`docs/support/exotel-livekit-sip-trunk.md`](../../../docs/support/exotel-livekit-sip-trunk.md)


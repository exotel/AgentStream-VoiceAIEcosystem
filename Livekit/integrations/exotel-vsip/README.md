# LiveKit Cloud + Exotel vSIP

This integration connects **LiveKit Cloud Telephony** (SIP trunks + dispatch to rooms) with **Exotel Virtual SIP Trunking (vSIP)** (Indian PSTN DID + SIP trunk APIs).

## What this enables

- **Inbound PSTN → LiveKit**: PSTN → Exotel DID → Exotel trunk `destination-uris` → LiveKit inbound SIP → dispatch rule → room
- **Outbound PSTN from LiveKit**: LiveKit outbound trunk → SIP digest → Exotel edge `IP:port` → PSTN

## Start here

- Quickstart: [`Livekit/integrations/exotel-vsip/QUICKSTART.md`](./QUICKSTART.md)
- Full support article: [`docs/support/exotel-livekit-sip-trunk.md`](../../../docs/support/exotel-livekit-sip-trunk.md)

## References

- LiveKit SIP trunk setup: [SIP trunk setup](https://docs.livekit.io/telephony/start/sip-trunk-setup/)
- LiveKit inbound trunk: [Inbound trunk](https://docs.livekit.io/telephony/accepting-calls/inbound-trunk/)
- LiveKit dispatch rules: [Dispatch rule](https://docs.livekit.io/telephony/accepting-calls/dispatch-rule/)
- Exotel vSIP API: [Detailed SIP trunking API reference](https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference)


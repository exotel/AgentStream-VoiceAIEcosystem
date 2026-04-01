# NLPearl.AI + Exotel vSIP

This integration connects **NLPearl.AI** (voice agent + campaigns) with **Exotel Virtual SIP Trunking (vSIP)** (Indian PSTN DID + SIP trunk).

## Supported integration shape (Option B)

NLPearl’s **Custom VoIP** uses Exotel as the SIP trunk provider:

- **Outbound:** NLPearl → SIP to Exotel trunk → PSTN
- **Inbound:** PSTN → Exotel DID → SIP to NLPearl (via trunk destination URI)

For the full “do this in portals + API curls” guide, use:

- [`docs/support/exotel-nlpearl-sip-trunk.md`](../../../docs/support/exotel-nlpearl-sip-trunk.md)

## References

- NLPearl Custom VoIP: [Custom VoIP integration](https://developers.nlpearl.ai/pages/custom_voip)
- NLPearl Outbound API overview: [Outbound/API](https://developers.nlpearl.ai/pages/outbound_api)
- Exotel trunk APIs: [Detailed SIP trunking API reference](https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference)


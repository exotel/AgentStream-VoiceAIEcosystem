# Voice AI Ecosystem: Retell AI + Exotel vSIP

Connect **[Exotel](https://exotel.com/) Virtual SIP Trunking (vSIP)** to **[Retell AI](https://www.retellai.com/)** using **elastic SIP trunking** per [Retell custom telephony](https://docs.retellai.com/deploy/custom-telephony). This mirrors the structure of the [ElevenLabs Exotel pack](../../../elevenlabs/integrations/exotel-vsip/README.md).

| Doc | Use when |
|-----|----------|
| [**QUICKSTART.md**](./QUICKSTART.md) | Short path: Exotel trunk + digest + Retell import (outbound-focused). |
| [**retell-exotel-voice-ai-connector.md**](./retell-exotel-voice-ai-connector.md) | Full reference: Retell SIP URIs, IP allowlists, Exotel APIs, inbound/outbound patterns. |

## Retell methods (from official docs)

1. **Elastic SIP trunking (recommended)** — Configure SIP trunk at Exotel, point origination/termination appropriately, **import the number** into Retell. Same feature set as Retell-managed numbers when your provider supports it.
2. **Dial to SIP URI** — Your system dials `sip:{call_id}@sip.retellai.com` after [Register Phone Call](https://docs.retellai.com/api-references/register-phone-call); no transfer feature from Retell’s side. Use when elastic SIP is not possible.

This repo focuses on **Method 1** with Exotel.

## Alpha / transport

- Confirm **Exotel vSIP** availability and **UDP** policy with Exotel; align **TCP/TLS** with Retell ([supported transports](https://docs.retellai.com/deploy/custom-telephony)).
- **Exotel edge** is typically **`IP:port`** (e.g. TLS `443`, TCP `5070`) — see [Exotel network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration).

## Publishing

Keep placeholders in exported copies; rotate any exposed SIP passwords.

## References

- [Retell — Custom telephony](https://docs.retellai.com/deploy/custom-telephony)
- [Exotel — SIP trunking API](https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference)

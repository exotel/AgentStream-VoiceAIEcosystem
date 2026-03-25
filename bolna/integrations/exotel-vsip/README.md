# Voice AI Ecosystem: Bolna AI + Exotel vSIP

Connect **[Exotel](https://exotel.com/)** to **[Bolna Voice AI](https://www.bolna.ai/)** using either:

1. **Bolna dashboard — Exotel provider** — Link Exotel REST credentials in Bolna (`Providers` → Exotel). See [Connect Your Exotel Account to Bolna](https://www.bolna.ai/docs/exotel-connect-provider).
2. **SIP BYOT (Bring Your Own Trunk)** — Configure **Exotel vSIP** (trunk + DID + credentials), then create a **Bolna SIP trunk** whose **gateway** is Exotel’s **edge IP:port** with matching digest. Bolna uses this for **outbound SIP** to Exotel ([outbound BYOT](https://www.bolna.ai/docs/sip-trunking/byot-outbound-calls)) and for **inbound** after you route Exotel toward Bolna’s SIP entry. See [SIP trunking introduction](https://www.bolna.ai/docs/sip-trunking/introduction).

| Doc | Use when |
|-----|----------|
| [**QUICKSTART.md**](./QUICKSTART.md) | Short path: Exotel trunk + credentials + Bolna trunk API (outbound-focused). |
| [**bolna-exotel-voice-ai-connector.md**](./bolna-exotel-voice-ai-connector.md) | Full reference: Bolna gateways, inbound `13.200.45.61:5060`, codecs, limitations. |

## Notes from Bolna (verify in current docs)

- SIP trunking is **Beta** — contact [enterprise@bolna.ai](mailto:enterprise@bolna.ai) for access.
- **SRTP is not supported** — plain RTP only; disable mandatory SRTP on the carrier side.
- Inbound origination target published in Bolna docs: **`sip:13.200.45.61:5060`** — confirm in [Receive Inbound Calls via Your SIP Trunk](https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls).

## Exotel alignment

Same rules as other Voice AI packs in this repo: **outbound Exotel** = create trunk → map DID → credentials; **optional** `whitelisted-ips` only for **static** IPs (`mask: 32`); **destination URI** for **inbound** toward Bolna; **Connect** = **`sip:<trunk_sid>`**.

## Publishing

Do not commit live API keys or SIP passwords.

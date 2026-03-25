# Voice AI Ecosystem: Ultravox + Exotel

Connect **[Exotel](https://exotel.com/)** to **[Ultravox](https://www.ultravox.ai/)** in either of these ways:

1. **Native Exotel medium** — Ultravox call medium `"exotel": {}` with Exotel **[Voice Streaming](https://developer.exotel.com/api/product-voice-version-3)**. Ultravox does **not** offer “import Exotel credentials” in-console the way some other native integrations do; you wire streaming per Ultravox + Exotel docs. See [Telephony platforms](https://docs.ultravox.ai/telephony/telephony-platforms).

2. **SIP BYOT (this pack)** — Treat **Exotel vSIP** as the PSTN carrier and use Ultravox **[SIP guide](https://docs.ultravox.ai/telephony/sip)**: **IP allowlisting** (`allowedCidrRanges`) or **SIP registration**, plus **outgoing** `medium.sip.outgoing` toward Exotel’s gateway with digest. Same Exotel trunk patterns as the rest of this repo: **create trunk → map DID → credentials**; optional **`whitelisted-ips`** only for **static** IPs (`mask: 32`); **inbound** **`destination-uris`**; **Connect** **`sip:<trunk_sid>`** where applicable.

| Doc | Use when |
|-----|----------|
| [**QUICKSTART.md**](./QUICKSTART.md) | Short checklist: Ultravox SIP + Exotel trunk. |
| [**ultravox-exotel-voice-ai-connector.md**](./ultravox-exotel-voice-ai-connector.md) | Full reference: allowlist, domain, registration, codecs, native `exotel` pointer. |

## Exotel alignment

Same rules as other Voice AI packs: **outbound Exotel** = create trunk → map DID → credentials; **optional** `whitelisted-ips` only for **static** IPs (`mask: 32`); **destination URI** for **inbound** toward Ultravox; **Connect** = **`sip:<trunk_sid>`** (API `trunk_sid`).

**Ultravox note:** On **Ultravox**, SIP ingress allowlisting uses **IPv4 CIDR** (`allowedCidrRanges`), including **`/32`** for a single host — [SIP guide](https://docs.ultravox.ai/telephony/sip). Exotel trunk ACL remains **per static IP** (`mask: 32`) per Exotel’s API.

## Publishing

Do not commit live API keys or SIP passwords.

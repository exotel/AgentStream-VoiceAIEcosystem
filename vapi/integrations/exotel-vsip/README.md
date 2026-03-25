# Voice AI Ecosystem: Vapi + Exotel vSIP

Connect **[Exotel](https://exotel.com/)** Virtual SIP Trunking to **[Vapi](https://vapi.ai/)** using Vapi’s **BYO SIP trunk** (`byo-sip-trunk`) and **BYO phone number** (`byo-phone-number`). Vapi’s SBC uses **two fixed signalling IPs** — add **both** to Exotel **`whitelisted-ips`** (`mask: 32` each) when Vapi places SIP toward Exotel.

| Doc | Use when |
|-----|----------|
| [**QUICKSTART.md**](./QUICKSTART.md) | Short checklist: Exotel trunk + Vapi credential + whitelist. |
| [**vapi-exotel-voice-ai-connector.md**](./vapi-exotel-voice-ai-connector.md) | API JSON, IPv4 gateway rule, Exotel alignment. |
| [**exotel-vapi-sip-trunk.md**](../../../docs/support/exotel-vapi-sip-trunk.md) | End-to-end support article: flows, inbound destination URI, troubleshooting. |

## Vapi specifics

- **Gateway `ip`:** must be **IPv4**, not hostname ([troubleshoot](https://docs.vapi.ai/advanced/sip/troubleshoot-sip-trunk-credential-errors)).
- **Allowlist:** `44.229.228.186/32` and `44.238.177.138/32` on Exotel ([SIP networking](https://docs.vapi.ai/advanced/sip/sip-networking)).

## Publishing

Do not commit live API keys or SIP passwords.

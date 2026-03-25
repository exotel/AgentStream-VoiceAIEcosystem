# Voice AI Ecosystem: Smallest AI (Atoms) + Exotel vSIP

Connect **[Exotel](https://exotel.com/)** to **[Smallest AI](https://smallest.ai/)** **Atoms** using **Import SIP** on [Phone Numbers](https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md): **SIP Termination URL** points at Exotel’s **edge IP:port**; **SIP Origination URL** (from Atoms) goes into Exotel **destination-uris** for inbound PSTN.

| Doc | Use when |
|-----|----------|
| [**QUICKSTART.md**](./QUICKSTART.md) | Short ordered checklist. |
| [**smallest-exotel-voice-ai-connector.md**](./smallest-exotel-voice-ai-connector.md) | Field mapping Atoms ↔ Exotel. |
| [**exotel-smallest-ai-sip-trunk.md**](../../../docs/support/exotel-smallest-ai-sip-trunk.md) | Full support article + troubleshooting. |

## Notes

- **SIP Origination URL** is **account/import specific** — always copy from the Atoms UI after creating the custom number.  
- Confirm **transport** and **codec** expectations with Smallest if SIP negotiates but media fails.

## Publishing

Do not commit live API keys or SIP passwords.

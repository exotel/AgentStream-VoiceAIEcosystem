# Voice AI Ecosystem: Vocallabs + Exotel

**Vocallabs** documents a **Superflow B2B API** (`api.superflow.run`) with **`createSIPCall`**, **`initiateVocallabsCall`**, and related endpoints — see [Vocallabs API docs](https://docs.vocallabs.ai/vocallabs). Pair your **Exotel vSIP DID** with the **`did`** / **`from`** fields where applicable; use **Exotel trunk APIs** for the PSTN leg per [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md).

| Doc | Use when |
|-----|----------|
| [**QUICKSTART.md**](./QUICKSTART.md) | Auth + `createSIPCall` + Exotel DID reminder. |
| [**vocallabs-exotel-voice-ai-connector.md**](./vocallabs-exotel-voice-ai-connector.md) | Endpoint table + Exotel mapping. |
| [**exotel-vocallabs-sip-trunk.md**](../../../docs/support/exotel-vocallabs-sip-trunk.md) | Full support article + troubleshooting. |

## Publishing

Do not commit `clientId`, `clientSecret`, or bearer tokens.

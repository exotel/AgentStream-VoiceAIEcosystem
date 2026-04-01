# NLPearl Custom VoIP ↔ Exotel vSIP — connector notes

This document is an engineering-focused companion to the support article:

- [`docs/support/exotel-nlpearl-sip-trunk.md`](../../../docs/support/exotel-nlpearl-sip-trunk.md)

## Field mapping (NLPearl → Exotel)

### Outbound

NLPearl Custom VoIP outbound fields map to Exotel as follows:

- **SIP Trunk URL**
  - Use Exotel trunk SIP domain: `sip:${ACCOUNT_SID}.pstn.exotel.com`
  - This is separate from Exotel **edge IP:port** values (those are gateway termination points used by some providers; Exotel’s trunk API uses the SIP domain for trunk identity).
- **User Part**
  - Appears in the SIP “From” user identity NLPearl uses.
  - Prefer the **Exotel trunk username** (digest) for simplest alignment, unless Exotel requires DID-as-user for a specific account setup.
- **Credentials Authentication**
  - Must match Exotel trunk credentials created via `POST /trunks/{TRUNK_SID}/credentials`.

### Inbound

After saving NLPearl inbound config, you get a **SIP Domain** (tenant-specific).

On Exotel, set:

- `PUT /trunks/{TRUNK_SID}/destination-uris` with `destination = "<NLPEARL_SIP_DOMAIN>:<port>;transport=<tls|tcp>"`

## Security notes

- Prefer **digest auth** over ACL unless you have a dedicated static `/32` egress IP model.
- If enabling **TLS/SRTP** in NLPearl, enable it only after confirming Exotel’s supported transport and media requirements for your vSIP deployment.

## API-driven outbound (NLPearl)

NLPearl supports API-triggered calls for outbound activities:

- Overview: [Outbound/API](https://developers.nlpearl.ai/pages/outbound_api)
- Make Call: [Make Call API request](https://developers.nlpearl.ai/api-reference/v1/outbound/make-call)
- Variables: [Variables](https://developers.nlpearl.ai/pages/variables) — `callData` payload for personalization


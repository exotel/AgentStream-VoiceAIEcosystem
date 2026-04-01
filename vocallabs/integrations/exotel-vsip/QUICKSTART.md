# Quickstart — Vocallabs (Superflow B2B) + Exotel

Goal: first successful call using **Vocallabs API-first flow** aligned with an **Exotel DID** (and Exotel SIP trunking only if your design uses a classic SIP trunk leg).

## Prereqs

- Vocallabs: API credentials (`clientId` / `clientSecret`) from https://docs.vocallabs.ai/vocallabs
- Exotel: DID available (E.164). If you are using SIP trunking, enable SIP trunking and generate API credentials.

Shared Exotel SIP trunk API snippets (only if you need a SIP trunk leg):

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

## Outbound

API-first (typical):

1. Get a Vocallabs auth token.
2. Use `createSIPCall` / other Vocallabs endpoints with:
   - `phone_number` = destination (E.164)
   - `did` = your Exotel DID (E.164) when Vocallabs expects caller identity

If your design includes SIP trunking through Exotel:

1. Exotel trunk + DID + digest (`POST .../credentials`) must be aligned to whatever SIP leg Vocallabs expects (confirm with Vocallabs).

## Inbound

Inbound PSTN → AI through Exotel requires a stable SIP origination target from Vocallabs (confirm with their team). If you have that:

1. Exotel trunk `destination-uris` → Vocallabs SIP target
2. Exotel Flow Connect `sip:<trunk_sid>`

## If calls fail

- Treat Vocallabs as **API-first** unless they explicitly provide a stable SIP target for classic trunk routing.
- Use the full guide: [`docs/support/exotel-vocallabs-sip-trunk.md`](../../../docs/support/exotel-vocallabs-sip-trunk.md)

## Links

- Vocallabs docs: https://docs.vocallabs.ai/vocallabs
- Repo support article: [`docs/support/exotel-vocallabs-sip-trunk.md`](../../../docs/support/exotel-vocallabs-sip-trunk.md)

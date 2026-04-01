# Quickstart — Smallest AI (Atoms Import SIP) + Exotel vSIP

Goal: first successful **outbound** and **inbound** call using **Exotel as the India PSTN carrier** and **Atoms Import SIP** for the Voice AI leg.

## Prereqs

- Exotel: vSIP enabled, DID active (E.164), Exotel edge **IP:port** known
- Smallest (Atoms): account access; Phone Numbers → Import SIP available

Shared Exotel API snippets:

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

## Outbound (Atoms → Exotel → PSTN)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - Create digest credentials on the trunk (`POST .../credentials`) (if you will use SIP auth)
2. **Atoms**
   - Phone Numbers → Add Number → **Import SIP**
   - Set **SIP Termination URL** = Exotel edge **IP:port** (format per Atoms UI)
   - If using digest, set Username/Password to match Exotel trunk credentials
3. Trigger an outbound call via Atoms and confirm it terminates through Exotel.

## Inbound (PSTN → Exotel → Atoms)

1. **Atoms**
   - Copy the **SIP Origination URL** shown after Import SIP
2. **Exotel**
   - Set trunk `destination-uris` to the Atoms SIP Origination URL
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`
3. Call the Exotel DID and confirm Atoms answers.

## If calls fail

- **Inbound not reaching Atoms**: wrong Origination URL copied into Exotel `destination-uris`.
- **401/403**: digest mismatch (if enabled) between Exotel and Atoms.
- Use the full guide: [`docs/support/exotel-smallest-ai-sip-trunk.md`](../../../docs/support/exotel-smallest-ai-sip-trunk.md)

## Links

- Atoms Import SIP: https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md
- Repo support article: [`docs/support/exotel-smallest-ai-sip-trunk.md`](../../../docs/support/exotel-smallest-ai-sip-trunk.md)

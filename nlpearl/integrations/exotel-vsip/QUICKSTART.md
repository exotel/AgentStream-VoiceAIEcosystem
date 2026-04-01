# Quickstart — NLPearl Custom VoIP + Exotel vSIP (Option B)

Goal: first successful **inbound** and **outbound** call with **Exotel as PSTN carrier** and **NLPearl as Voice AI platform**.

## Prereqs

- Exotel: vSIP enabled, DID active (E.164), Exotel edge **IP:port** known
- NLPearl: agent created + published, account ready for inbound/outbound activities

Shared Exotel API snippets:

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

## Outbound (NLPearl → Exotel → PSTN)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - Create digest credentials on the trunk (`POST .../credentials`)
2. **NLPearl**
   - Settings → Phone Numbers → Custom VoIP → select your number → **Outbound**
   - Set **SIP Trunk URL** = `sip:${ACCOUNT_SID}.pstn.exotel.com`
   - Set **User Part** = your Exotel SIP username (or your DID)
   - Enable **Credentials Authentication** and set the same username/password as Exotel trunk credentials
3. Place a test outbound call from NLPearl (UI or API Make Call).

## Inbound (PSTN → Exotel → NLPearl)

1. **NLPearl**
   - Settings → Phone Numbers → Custom VoIP → **Inbound**
   - Choose auth (IP auth only if Exotel gives stable IPs; else credentials)
   - Save and copy the **SIP Domain** that NLPearl shows
2. **Exotel**
   - Set trunk `destination-uris` to NLPearl SIP Domain (port/transport matching TLS vs TCP)
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`
3. Call the DID from a phone and confirm NLPearl answers.

## If calls fail

Use the troubleshooting section in:

- [`docs/support/exotel-nlpearl-sip-trunk.md`](../../../docs/support/exotel-nlpearl-sip-trunk.md)

## Links

- NLPearl Custom VoIP: https://developers.nlpearl.ai/pages/custom_voip
- Repo support article: [`docs/support/exotel-nlpearl-sip-trunk.md`](../../../docs/support/exotel-nlpearl-sip-trunk.md)


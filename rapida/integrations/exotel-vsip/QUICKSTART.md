# Quickstart — Rapida AI + Exotel

Goal: first successful call using **Rapida** with Exotel, choosing either **native Exotel integration** (recommended) or **vSIP SIP trunk**.

## Prereqs

- Exotel: DID active (E.164)
- Rapida: account + assistant ready

Shared Exotel vSIP API snippets (only for the SIP trunk path):

- [`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

## Outbound

### Option A (recommended): Native Exotel (no vSIP trunk)

1. **Rapida**: Integration → Tools → **Exotel** credential.
2. **Rapida**: Deploy → Phone → **Exotel** with **App ID** + Exotel **DID**.
3. **Exotel**: configure Flow/webhook per Rapida’s Exotel guide.

### Option B: vSIP + Rapida SIP trunk (SIP path)

1. **Exotel**
   - Create trunk
   - Map DID to trunk
   - (If required) create digest credentials on the trunk (`POST .../credentials`)
2. **Exotel inbound**
   - Set trunk `destination-uris` toward `sip-01.in.rapida.ai:5060` (transport per testing)
   - In Exotel Flow, use **Connect** with `sip:<trunk_sid>`
3. **Rapida**
   - Configure Rapida SIP trunk credential pointing to Exotel **edge `IP:port`** if Rapida is expected to originate SIP calls toward Exotel for PSTN termination

## Inbound

- **Native Exotel (Option A)**: inbound is handled via Exotel Flow/webhook per Rapida docs.
- **SIP trunk (Option B)**: inbound is Exotel DID → Flow Connect `sip:<trunk_sid>` → trunk `destination-uris` → Rapida SIP host.

## If calls fail

- Choose one path first (native vs SIP) and validate it end-to-end before mixing.
- Use the full guide: [`docs/support/exotel-rapida-ai-sip-trunk.md`](../../../docs/support/exotel-rapida-ai-sip-trunk.md)

## Links

- Rapida Exotel integration: https://doc.rapida.ai/integrations/telephony/exotel
- Rapida SIP trunk: https://doc.rapida.ai/integrations/telephony/sip
- Repo support article: [`docs/support/exotel-rapida-ai-sip-trunk.md`](../../../docs/support/exotel-rapida-ai-sip-trunk.md)

# Exotel SIP Trunking + Voice AI — support hub

Use this page to jump to **official provider docs**, **consoles**, and the **per-vendor support articles** in this repo. Shared Exotel trunk curls live in [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md).

**GitHub repo (reference):** https://github.com/exotel/AgentStream-VoiceAIEcosystem

---

## Honest “5 minutes”

A **first successful PSTN ↔ SIP test** is often **5–15 minutes only after**:

| Prerequisite | Why it is not instant |
|--------------|------------------------|
| Exotel **KYC**, **DID** in **E.164**, **SIP trunking enabled** | Account and product gates |
| **Edge IP:port** from Exotel (not guessed) | Firewall and SIP termination |
| Voice AI **agent published** + **SIP / telephony** configured on the provider | Product-specific |
| **Digest / ACL** values **identical** on Exotel and the provider | One typo = 401/403 |

Treat the steps below as **minimum click/API paths** once those are true.

---

## Provider quick matrix

| Voice AI | Console / dashboard | Primary telephony / SIP docs | Support article (this repo) |
|----------|---------------------|------------------------------|----------------------------|
| **ElevenLabs** | [Agents / app](https://elevenlabs.io/app/agents) · [Phone numbers / SIP](https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking) | [SIP trunking](https://elevenlabs.io/docs/agents-platform/phone-numbers/sip-trunking) · [API hub](https://elevenlabs.io/docs) | [`exotel-elevenlabs-sip-trunk.md`](./exotel-elevenlabs-sip-trunk.md) |
| **LiveKit** | [LiveKit Cloud](https://cloud.livekit.io/) | [SIP trunk setup](https://docs.livekit.io/telephony/start/sip-trunk-setup/) · [Inbound trunk](https://docs.livekit.io/telephony/accepting-calls/inbound-trunk/) · [Dispatch rule](https://docs.livekit.io/telephony/accepting-calls/dispatch-rule/) | [`exotel-livekit-sip-trunk.md`](./exotel-livekit-sip-trunk.md) |
| **Retell AI** | [Dashboard](https://dashboard.retellai.com/) | [Custom telephony](https://docs.retellai.com/deploy/custom-telephony) · [Quick start](https://docs.retellai.com/get-started/quick-start) | [`exotel-retell-sip-trunk.md`](./exotel-retell-sip-trunk.md) |
| **Bolna** | [Bolna docs / BYOT](https://www.bolna.ai/byot-setup) (SIP **Beta** — access may require **enterprise@bolna.ai**) | [SIP introduction](https://www.bolna.ai/docs/sip-trunking/introduction) · [Exotel connector](https://www.bolna.ai/docs/exotel-connect-provider) | [`exotel-bolna-sip-trunk.md`](./exotel-bolna-sip-trunk.md) |
| **Pipecat** (orchestration) + **Daily** (WebRTC/SIP) | [Daily dashboard](https://dashboard.daily.co/) | [Pipecat — PSTN + Daily SIP](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip) · [Daily — SIP](https://docs.daily.co/guides/products/dial-in-dial-out/sip) | [`exotel-pipecat-sip-trunk.md`](./exotel-pipecat-sip-trunk.md) |
| **Ultravox** | [App / console](https://app.ultravox.ai/) | [SIP guide](https://docs.ultravox.ai/telephony/sip) · [Telephony platforms](https://docs.ultravox.ai/telephony/telephony-platforms) (native Exotel streaming = alternate path) | [`exotel-ultravox-sip-trunk.md`](./exotel-ultravox-sip-trunk.md) |
| **Vapi** | [Dashboard](https://dashboard.vapi.ai/) | [SIP trunking](https://docs.vapi.ai/advanced/sip/sip-trunk) · [SIP networking](https://docs.vapi.ai/advanced/sip/sip-networking) | [`exotel-vapi-sip-trunk.md`](./exotel-vapi-sip-trunk.md) |
| **Smallest AI (Atoms)** | [app.smallest.ai](https://app.smallest.ai/) | [Phone Numbers — Import SIP](https://atoms-docs.smallest.ai/platform/deployment/phone-numbers.md) · [Telephony](https://atoms-docs.smallest.ai/intro/capabilities/telephony.md) | [`exotel-smallest-ai-sip-trunk.md`](./exotel-smallest-ai-sip-trunk.md) |
| **Vocallabs** | [API docs](https://docs.vocallabs.ai/vocallabs) | [Superflow B2B](https://api.superflow.run/b2b/) — `createSIPCall`, `initiateVocallabsCall` ([reference](https://docs.vocallabs.ai/vocallabs)) | [`exotel-vocallabs-sip-trunk.md`](./exotel-vocallabs-sip-trunk.md) |
| **Rapida AI** | [rapida.ai](https://www.rapida.ai/) | [Exotel integration](https://doc.rapida.ai/integrations/telephony/exotel) · [SIP trunk](https://doc.rapida.ai/integrations/telephony/sip) · [Phone deployment](https://doc.rapida.ai/voice-deployment-options/phone) | [`exotel-rapida-ai-sip-trunk.md`](./exotel-rapida-ai-sip-trunk.md) |
| **NLPearl.AI** | [platform.nlpearl.ai](https://platform.nlpearl.ai/) | [Custom VoIP](https://developers.nlpearl.ai/pages/custom_voip) · [Outbound/API](https://developers.nlpearl.ai/pages/outbound_api) · [Make Call API](https://developers.nlpearl.ai/api-reference/v1/outbound/make-call) | [`exotel-nlpearl-sip-trunk.md`](./exotel-nlpearl-sip-trunk.md) |

**Exotel (all paths):** [API credentials (India)](https://my.in.exotel.com/apisettings/site#api-credentials) · [SIP API reference](https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference) · [Network / firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration) · [Voice AI Flow / Connect](https://support.exotel.com/support/solutions/articles/3000133452-flow-and-api-configuration-guide-for-voice-ai-contact-centre-platforms-via-exotel-virtual-sip-trunk)

**Exotel edge hostname examples (India):** `in.voip.exotel.com:5070` (TCP) · `in.voip.exotel.com:443` (TLS). Always use the exact host/IP + port + transport Exotel assigns (see [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md)).  
**ACL note:** only use `whitelisted-ips` for **static `/32`** IPs (`mask: 32`)—do **not** attempt CIDR ranges; if a provider publishes only CIDR/shared egress, prefer **digest** and coordinate with Exotel support.

---

## Per-provider: minimum steps (after prerequisites)

### ElevenLabs

1. **Exotel:** create trunk → map DID → `POST .../credentials` (match digest everywhere).  
2. **ElevenLabs:** **Phone numbers** → import from SIP trunk → **outbound address** = Exotel **edge IP:port**; same digest as Exotel.  
3. **Inbound:** `POST .../destination-uris` toward ElevenLabs host (see article) → Flow **Connect** → **`sip:<trunk_sid>`**.  
4. Test outbound via [ConvAI API](https://elevenlabs.io/docs) (confirm current path in docs).

### LiveKit Cloud

1. **LiveKit:** Telephony on → copy **SIP URI** / region; create **inbound** trunk (DID) + **dispatch**; **outbound** trunk → Exotel edge **IP:port** + digest matching Exotel credentials.  
2. **Exotel:** same trunk/DID/credentials pattern; **destination-uris** toward LiveKit SIP host for inbound PSTN.  
3. Ensure an **agent joins the same room** as the SIP participant (see repo `OUTBOUND-EXOTEL-NOTES.md`).

### Retell AI

1. **Exotel:** trunk + DID + credentials (+ optional static-IP ACL per Exotel rules).  
2. **Retell:** import number / elastic SIP per [custom telephony](https://docs.retellai.com/deploy/custom-telephony); align digest.  
3. **Inbound:** destination URI toward `sip.retellai.com` (port/transport per Retell) → Connect **`sip:<trunk_sid>`**.

### Bolna (BYOT SIP)

1. **Bolna:** SIP trunk → gateway = Exotel **edge IP:port**; `userpass` = Exotel credentials; agent `telephony_provider` = `sip-trunk` for outbound.  
2. **Exotel:** standard trunk/DID/credentials; destination URI toward Bolna ingress for inbound (host/port per [current Bolna docs](https://www.bolna.ai/docs/sip-trunking/byot-inbound-calls)).  
3. **Alternative:** [Exotel dashboard connector](https://www.bolna.ai/docs/exotel-connect-provider) if you are not doing raw BYOT.

### Pipecat + Daily

1. Implement **webhook → Daily room + SIP** per [Pipecat PSTN guide](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip); bridge carrier leg to room **`sip_uri`** (not the static “single SIP host” pattern unless you designed for it).  
2. **Exotel:** trunk credentials for SIP toward PSTN; use Exotel **Voice APIs / Flow** to attach the live call to your **`sip_uri`**.  
3. This path is **engineering-heavy** vs fixed-destination Voice AI platforms — budget more than 5 minutes unless you already have the Pipecat sample running.

### Ultravox (SIP)

1. **Ultravox:** agent exists → `GET /api/sip` for **domain** → allowlist Exotel signalling IPs (`/32`) or use **SIP registration** per docs.  
2. **Exotel:** trunk + DID + credentials; outbound via **`medium.sip.outgoing`** toward Exotel.  
3. **Inbound:** destination URI toward Ultravox SIP endpoint → Connect **`sip:<trunk_sid>`**.  
4. **Alternate:** native **`exotel`** medium + streaming — no SIP trunk; use [telephony platforms](https://docs.ultravox.ai/telephony/telephony-platforms) + Exotel Voice Streaming docs.

### Vapi (BYO SIP trunk)

1. **Exotel:** trunk + DID + digest; **`whitelisted-ips`** for **both** Vapi SBC IPs (`44.229.228.186`, `44.238.177.138`), **`mask: 32`** each.  
2. **Vapi:** `byo-sip-trunk` credential — gateway **`ip`** = **Exotel edge IPv4** (not hostname); **`outboundAuthenticationPlan`** = Exotel digest; **`outboundProtocol`** / port match Exotel.  
3. **Vapi:** `byo-phone-number` linked to credential; test with **`POST /call/phone`**.  
4. **Inbound:** `destination-uris` toward **`sip.vapi.ai`** (port/transport per [Vapi networking](https://docs.vapi.ai/advanced/sip/sip-networking)) → Connect **`sip:<trunk_sid>`**.

### Smallest AI (Atoms — Import SIP)

1. **Exotel:** trunk + DID + digest (`/credentials`).  
2. **Atoms:** **Import SIP** — **SIP Termination URL** = Exotel **edge IP:port**; **Username** / **Password** match Exotel digest when used.  
3. **Atoms:** copy **SIP Origination URL** → **Exotel** `destination-uris` → Flow **Connect** **`sip:<trunk_sid>`**.  
4. Assign the imported number to your agent; test outbound via [Start an outbound call](https://atoms-docs.smallest.ai/api-reference/calls/start-an-outbound-call.md).

### Vocallabs (Superflow B2B — API-first)

1. **Vocallabs:** `POST …/createAuthToken/` → **Bearer** token; use **`createSIPCall`** with `did` = Exotel **E.164** where applicable; wire **`websocket_url`** / **`webhook_url`** per [docs](https://docs.vocallabs.ai/vocallabs).  
2. **Exotel:** trunk + DID + **`/credentials`** when your design uses SIP digest toward Exotel; optional **`whitelisted-ips`** only if Vocallabs publishes **static** egress IPs.  
3. **Inbound:** add **`destination-uris`** + Flow **Connect** **`sip:<trunk_sid>`** only if Vocallabs provides a **SIP origination URI** — confirm with their team; public reference is **REST-heavy**, not full BYO dashboard SIP like Vapi.

### Rapida AI (native Exotel vs SIP trunk)

1. **Path A (native):** Rapida **Integration → Tools** → **Exotel** credentials; **Phone** deployment with **App ID** + DID; Exotel Flow → **`https://websocket-01.in.rapida.ai/v1/talk/exotel/call/...`** ([guide](https://doc.rapida.ai/integrations/telephony/exotel)).  
2. **Path B (SIP):** Exotel SIP trunking **`destination-uris`** toward **`sip-01.in.rapida.ai:5060`**; **Connect** **`sip:<trunk_sid>`**; Rapida **SIP Trunk** credential toward Exotel **edge** for PSTN outbound if needed ([SIP guide](https://doc.rapida.ai/integrations/telephony/sip)).

### NLPearl.AI (Custom VoIP — Option B)

1. **Exotel:** trunk + DID + digest (`POST .../credentials`).  
2. **NLPearl:** Settings → Phone Numbers → **Custom VoIP** → configure **Outbound** (SIP Trunk URL = `sip:<ACCOUNT_SID>.pstn.exotel.com`, credentials) and **Inbound** (save to get the NLPearl **SIP Domain**).  
3. **Exotel inbound:** set trunk `destination-uris` to NLPearl SIP Domain + Exotel Flow Connect **`sip:<trunk_sid>`**.  
4. Test outbound (UI/API) and inbound (call the DID).

---

## What was easy to miss (gaps we closed in docs)

| Topic | Where it lives |
|-------|----------------|
| Single **entry** for URLs + consoles | This **`README.md`** |
| **Pipecat** is not a trunk — **Daily** supplies SIP/WebRTC | [`exotel-pipecat-sip-trunk.md`](./exotel-pipecat-sip-trunk.md) |
| **Ultravox** has **two** paths (SIP vs native Exotel streaming) | [`exotel-ultravox-sip-trunk.md`](./exotel-ultravox-sip-trunk.md) |
| Exotel **Connect** dial string is **`sip:<trunk_sid>`** only | Each support article + snippets |
| **Scripts** for ElevenLabs + Exotel API | [`scripts/exotel-elevenlabs/README.md`](../../scripts/exotel-elevenlabs/README.md) |
| **Vapi** needs **two** Exotel ACL lines for its SBC IPs | [`exotel-vapi-sip-trunk.md`](./exotel-vapi-sip-trunk.md) |
| **Vocallabs** is **API-first** (`createSIPCall`, websockets) — not the same as BYO SIP trunk UI | [`exotel-vocallabs-sip-trunk.md`](./exotel-vocallabs-sip-trunk.md) |
| **Rapida** has **native Exotel** (webhook/stream) **and** optional **SIP trunk** | [`exotel-rapida-ai-sip-trunk.md`](./exotel-rapida-ai-sip-trunk.md) |
| **NLPearl** uses **Custom VoIP** (SIP Domain inbound + SIP Trunk URL outbound) | [`exotel-nlpearl-sip-trunk.md`](./exotel-nlpearl-sip-trunk.md) |

---

## Related

- [WebRTC / Exotel app flows (browser SDK, not SIP trunking)](../integrations/webrtc-application-setup.md)
- [Integrations index](../integrations/README.md)

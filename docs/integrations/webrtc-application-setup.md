# WebRTC application setup (Voice AI Ecosystem)

This guide walks **application → number → endpoint → client**: the **authoritative** telephony steps are **[Exotel](https://docs.exotel.com/)** — Voice APIs, **Web Client SDK**, Flows, and (optionally) **Agent-Stream** / Voice AI bridges documented in this repo.

**Goal:** Use **Exotel** for PSTN and signalling, then attach **WebRTC in the browser** (official SDK) or **Voicebot / SIP / WSS** paths to your Voice AI stack.

| | |
|--|--|
| **Time** | ~20–60 minutes (first time), depending on SDK vs bridge vs SIP |
| **Difficulty** | Intermediate — public **HTTPS/WSS** for streaming bridges; **SIP** paths need trunk setup |
| **Sources** | [docs.exotel.com](https://docs.exotel.com/) · [developer.exotel.com](https://developer.exotel.com/) |

---

## How WebRTC is available (what you write vs what ships)

**You do not write a WebRTC or SIP stack from scratch for Exotel’s browser product.** Exotel publishes a **JavaScript/npm SDK** that already embeds the **WebRTC + SIP-over-WSS** behaviour described in [Voice APIs — Introduction](https://docs.exotel.com/voice-apis/introduction).

| If the integrator wants… | Is browser WebRTC required? | What they use | What they typically code |
|---------------------------|-----------------------------|---------------|---------------------------|
| **Softphone in the browser** (agent dialer / web phone) | **Yes** | **`@exotel-npm-dev/webrtc-client-sdk`** (+ core SDK) per [workflow doc](https://docs.exotel.com/voice-apis/web-client-sdk-apis-and-integration-workflow) | App integration: `initWebrtc`, `DoRegister`, callbacks, UI — **not** low-level RTP/SIP |
| **PSTN ↔ your server audio** (Voicebot / streaming) | **No** for the PSTN leg; media hits **your** `wss://` bridge | [Agent-Stream](https://github.com/exotel/Agent-Stream) pattern, Voicebot applet docs | **Bridge** service (audio in/out + your AI) — see [`elevenlabs/integrations/exotel-wss/README.md`](../../elevenlabs/integrations/exotel-wss/README.md) |
| **PSTN ↔ Voice AI over SIP** | **Usually no** browser WebRTC | Exotel **vSIP** + partner SIP | Trunk + Flow per [`docs/support/`](../support/) — **SIP**, not the Web SDK |
| **Pipecat / Daily agent** | WebRTC **inside Daily** (not Exotel’s Web SDK) | Daily + Pipecat | Per [Pipecat](https://docs.pipecat.ai/) / [`exotel-pipecat-sip-trunk.md`](../support/exotel-pipecat-sip-trunk.md) |

**Server-only voice control** (no browser): use **REST Voice APIs** (e.g. outbound connect, **Leg Actions**) from your backend — **HTTP + EXOML**, not npm WebRTC.

**Getting the SDK:** packages are under the **`@exotel-npm-dev`** org on npm; access/publishing may need Exotel account setup (see [Introduction](https://docs.exotel.com/voice-apis/introduction)). [GitHub sample](https://github.com/exotel/webrtc-client-sdk).

---

## 1 — Exotel building blocks (official)

Use these as the **source of truth** for names, endpoints, and payloads.

| Building block | What it is | Doc |
|----------------|------------|-----|
| **WebRTC Web Client SDK** | Browser VoIP: SIP over **WSS**, register, dial, mute/hold — built on **web-client-sdk** + **webrtc-core-sdk** | [Voice APIs — Introduction](https://docs.exotel.com/voice-apis/introduction) |
| **Web Client SDK — workflow** | `initWebrtc` → `DoRegister` / `UnRegister`, callbacks | [Web Client SDK APIs and integration workflow](https://docs.exotel.com/voice-apis/web-client-sdk-apis-and-integration-workflow) |
| **Voice APIs (programmatic voice)** | Outbound calls, connect customer to a **Flow/app**, **Leg Actions** with **EXOML** | [Voice APIs](https://docs.exotel.com/voice-apis) |
| **Leg Actions** | After a leg exists: play, record, gather DTMF, **stream audio**, bridge — **`exoml`** XML in JSON | [Leg Actions](https://docs.exotel.com/voice-apis/leg-actions) |
| **Outbound: call customer → connect to app** | `POST` …`/Calls/connect` — rings **From**, then connects to your **app/flow** via **`Url`** | [Outbound call to connect a customer to an app](https://docs.exotel.com/voice-apis/outbound-call-to-connect-a-customer-to-an-app) |
| **Voicebot / Agent-Stream** | GenAI Voicebot product; **Agent-Stream** streaming sample | [Developer portal — VoiceBot / AgentStream](https://developer.exotel.com/) · [Agent-Stream (GitHub)](https://github.com/exotel/Agent-Stream) |
| **SIP trunking (vSIP)** | Trunks, DIDs, credentials — PSTN ↔ SIP | [Dynamic SIP trunking](https://docs.exotel.com/dynamic-sip-trunking/overview) · [shared curls](../support/_exotel-trunk-api-snippets.md) |

**API hosts (from Exotel docs):**

| Cluster | Base host (typical) |
|---------|---------------------|
| **India (Mumbai)** | `https://api.in.exotel.com` — use for `v1` Voice/EXOML style APIs where documented |
| **Singapore** | `https://api.exotel.com` |
| **Leg Actions (example in docs)** | `https://cpaas-api.in.exotel.com/v2/accounts/{account_sid}/...` |

**Authentication:** HTTP **Basic** — **API Key** as username, **API Token** as password — from [API settings](https://my.in.exotel.com/apisettings/site#api-credentials) (India) / your cluster’s dashboard.

---

## 2 — Official browser WebRTC SDK (Exotel)

Exotel ships a **layered** npm stack: **web-client-sdk** (high level) + **webrtc-core-sdk** (SIP stack). See [Introduction](https://docs.exotel.com/voice-apis/introduction).

### Packages and repo

| Artifact | Notes |
|----------|--------|
| **npm org** | `@exotel-npm-dev` (organizational publishing — contact Exotel if you need access) |
| **Packages** | `@exotel-npm-dev/webrtc-client-sdk`, `@exotel-npm-dev/webrtc-core-sdk` |
| **GitHub** | [github.com/exotel/webrtc-client-sdk](https://github.com/exotel/webrtc-client-sdk) |
| **Account** | You need an **Exotel account** for VoIP; contact Exotel support for demo/licensing per [Introduction](https://docs.exotel.com/voice-apis/introduction) |

### Initialize and register (from Exotel docs)

1. Build **`sipAccountInfo`**: `userName`, `authUser`, `secret`, `sipdomain`, `domain` (host + port), `port` (e.g. **443** for WebSockets), **`security`: `wss`** (typical).
2. Call **`initWebrtc(sipAccountInfo, RegisterEventCallBack, CallListenerCallback, SessionCallback)`**.
3. Call **`DoRegister()`** before placing or receiving calls; handle **`registered` / `terminated` / …** in `RegisterEventCallBack`.
4. Optional: **`setPreferredCodec("opus")`** if Opus is enabled on your VoIP domain (request via Exotel per docs).
5. Optional: **`downloadLogs()`** for a support bundle.

Full callback tables and edge cases: [Web Client SDK APIs and integration workflow](https://docs.exotel.com/voice-apis/web-client-sdk-apis-and-integration-workflow).

**Success criteria:** Registration state **`registered`**, then test inbound/outbound per your Exotel app / number configuration.

---

## 3 — REST Voice API patterns (server-side)

Use these when a **backend** places calls or controls legs (not only the browser SDK).

### Outbound: customer answers, then connect to your Flow/app

- **Endpoint pattern:** `POST` `https://API_KEY:API_TOKEN@<cluster>/v1/Accounts/<AccountSid>/Calls/connect`
- **Key params:** `From`, `CallerId` (your Exotel number), `CallType` (`trans`), **`Url`** = your **app/flow** entry (Exotel documents the `…/exoml/start/~appid~` style — see [Outbound call to connect a customer to an app](https://docs.exotel.com/voice-apis/outbound-call-to-connect-a-customer-to-an-app)).
- **Optional:** `StatusCallback`, `TimeLimit`, `TimeOut`; **rate limit** stated in doc (e.g. **200 calls/minute** — confirm current limit in Exotel docs).
- **Samples:** Exotel references **cURL, Node, PHP, Ruby** via [developer portal](https://developer.exotel.com/) and samples such as [ExotelAPI (GitHub)](https://github.com/exotel/ExotelAPI).

### Leg Actions (control an existing call)

- **POST** `…/v2/accounts/{account_sid}/legs/{leg_sid}/actions` with JSON body containing **`exoml`** (XML string).
- **Base URL (from Leg Actions doc):** `https://cpaas-api.in.exotel.com/v2/accounts/{account_sid}` (India example — follow current Exotel doc for your account).
- See [Leg Actions](https://docs.exotel.com/voice-apis/leg-actions) for **EXOML** actions (play, bridge, stream, etc.).

---

## 4 — Typical WebRTC voice app pattern → Exotel

| Typical step | Exotel equivalent |
|--------------|-------------------|
| **Voice application** + **answer / webhook URL** | **Flow / App** in Exotel; **Passthru** or applet **URL**; or **Voicebot** / **Agent-Stream** `wss://` to your server |
| **Status / event callback URL** | **`StatusCallback`** on outbound APIs; applet-specific status webhooks per product docs |
| **Phone number** | **Exophone** / Company Numbers; vSIP: map DID to trunk per [snippets](../support/_exotel-trunk-api-snippets.md) |
| **Endpoint** (browser SIP user / password) | **SIP** credentials for **Web Client SDK** (`sipAccountInfo`) from Exotel VoIP / CCM setup — not interchangeable with Daily/LiveKit tokens |
| **Run the client** | Browser app using **SDK** above, or **Agent-Stream** bridge to your AI |

---

## 5 — Choose a Voice AI path (this repo)

| Path | When | Doc |
|------|------|-----|
| **A — Voicebot / Agent-Stream (`wss`)** | Exotel streams audio to **your** server; you bridge to your **AI / LLM** stack (see linked repo docs). | [`elevenlabs/integrations/exotel-wss/README.md`](../../elevenlabs/integrations/exotel-wss/README.md) · [Agent-Stream](https://github.com/exotel/Agent-Stream) |
| **B — SIP trunk (vSIP)** | PSTN ↔ SIP to the Voice AI integrations under [`docs/support/`](../support/) | [`docs/support/`](../support/) — `exotel-*-sip-trunk.md` |
| **C — Pipecat + Daily** | WebRTC agent + PSTN via Daily SIP / orchestration | [`exotel-pipecat-sip-trunk.md`](../support/exotel-pipecat-sip-trunk.md) |

**Rule of thumb:** **Voicebot / Agent-Stream** = **A**. **Carrier SIP + digest** = **B**. **Pipecat’s Daily transport** = **C**.

---

## 6 — End-to-end checklist

1. **Exotel account** and **API Key + Token** ([API settings](https://my.in.exotel.com/apisettings/site#api-credentials)).
2. **Flow or Voice app** (or Voicebot) attached to an **Exotel number** — verify inbound hits your URL or streaming endpoint.
3. **Browser path:** integrate **Web Client SDK** per §2; **server path:** use **Voice APIs** per §3 where appropriate.
4. **AI path:** add **A**, **B**, or **C** from §5 (bridge, SIP, or Pipecat).
5. **Production:** **`wss://`**, secrets only on server for third-party AI keys; observe **rate limits** on Voice APIs.

---

## Key concepts

### EXOML / Voice XML

Leg Actions and many flows use **EXOML** XML in **`exoml`** fields. Always match the **current** Exotel Voice / Legs documentation — do not assume XML from another vendor’s call-control format.

### Caller ID

`CallerId` / CLI must be an **Exotel number you own** (see [outbound connect doc](https://docs.exotel.com/voice-apis/outbound-call-to-connect-a-customer-to-an-app)).

### Security

- Prefer **`wss://`** for browser SIP and for Voicebot bridges.
- Keep **third-party AI / media provider** API keys on the **server**; use **short-lived tokens** to clients per that provider’s docs.

---

## Official references

| Topic | URL |
|-------|-----|
| Exotel Voice APIs hub | [docs.exotel.com/voice-apis](https://docs.exotel.com/voice-apis) |
| WebRTC SDK intro | [voice-apis/introduction](https://docs.exotel.com/voice-apis/introduction) |
| Web Client SDK workflow | [web-client-sdk-apis-and-integration-workflow](https://docs.exotel.com/voice-apis/web-client-sdk-apis-and-integration-workflow) |
| Leg Actions | [voice-apis/leg-actions](https://docs.exotel.com/voice-apis/leg-actions) |
| Outbound → app | [outbound-call-to-connect-a-customer-to-an-app](https://docs.exotel.com/voice-apis/outbound-call-to-connect-a-customer-to-an-app) |
| Developer portal | [developer.exotel.com](https://developer.exotel.com/) |
| Agent-Stream (sample) | [github.com/exotel/Agent-Stream](https://github.com/exotel/Agent-Stream) |
| WebRTC client SDK repo | [github.com/exotel/webrtc-client-sdk](https://github.com/exotel/webrtc-client-sdk) |
| SIP trunking overview | [dynamic-sip-trunking/overview](https://docs.exotel.com/dynamic-sip-trunking/overview) |

# LiveKit ↔ Exotel outbound — what we fixed, and “no audio”

This note records the changes and checks that got **outbound PSTN** working from this repo, and explains why you might still see **no audio** (usually not a dispatch-rule issue).

---

## What was wrong before (and what fixed it)

### 1. Wrong dialed number (E.164)

- **`+7411179773`** is not valid India E.164: it uses country code **`7`** with national **`411179773`**, instead of **`+91`** + **`7411179773`** → **`+917411179773`**.
- **`07411179773`** was previously normalized to **`+7411179773`** (bad). The script now treats common Indian inputs as **`+91`** + 10 digits.

**In code:** `call_phone.py` → `normalize_phone_e164()` plus a typo rule: **`+7` + 9 digits** → **`+917` + those 9 digits** (dropped `9` from `+91`).

### 2. Wrong or stale LiveKit outbound trunk ID

- **`ST_LXS6G49ZL88Y`** returned **`not_found`** for the project (deleted or different Cloud project).
- Use a trunk that exists in **the same** LiveKit project as `LIVEKIT_URL` / API keys (`lk sip outbound list` or Cloud → SIP).

### 3. Two trunks, different CLI formatting

Observability (`--observe`) showed:

| Trunk | `sip.trunkPhoneNumber` (example) |
|--------|-----------------------------------|
| `ST_Bkv2NA6XzogA` | `+918047490924` (E.164) |
| `ST_xCcRCS2Xesvt` | `08047490924` (national — risky) |

**Fix:** In LiveKit **outbound trunk** JSON, set **`numbers`** to **E.164** (e.g. **`+918047490924`**) so Exotel accepts CLI consistently.

### 4. Exotel **`403 Forbidden`** (`X-Exotel-ErrorCode: 4001`)

- **403** is returned by **Exotel’s SIP proxy (Kamailio)** — the INVITE reached them; they **refused** it.
- Typical causes: **digest** mismatch vs LiveKit trunk auth, **IP allowlist** (LiveKit SIP egress, e.g. `92.4.67.147` / ranges Exotel expects), wrong **termination host/port**, or trunk/DID not allowed for that call type.
- **Not** “LiveKit didn’t send SIP” — LiveKit sent INVITE; Exotel rejected.

### 5. Observability in-repo

- **`call_phone.py --no-wait --observe`** polls the room and prints **`sip.callStatus`**, **`sip.trunkPhoneNumber`**, **`sip.hostname`**, participant **state** / **disconnect_reason**.
- **`CreateSIPParticipant` returning OK** only means LiveKit accepted the job; PSTN ring/answer is proven in **Exotel logs** + participant attributes.

### 6. LiveKit project consistency

- SIP traces may show **`From`** / domain for one project (e.g. `…63t2s9xbxnt.sip.livekit.cloud`) while `.env` uses another (`exotel-test-kz66hgr8`). **Trunks and API keys must match the same Cloud project.**

---

## Commands that worked (reference)

```bash
cd livekit-outbound-caller-agent
source venv/bin/activate   # or ./venv/bin/python3

# Outbound call (uses .env / .env.local for LIVEKIT_* and SIP_OUTBOUND_TRUNK_ID)
python3 call_phone.py +917411179773 --no-wait

# Debug: watch SIP attrs in the terminal
python3 call_phone.py +917411179773 --no-wait --observe --observe-seconds 90
```

Env vars: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, `SIP_OUTBOUND_TRUNK_ID`. Optional: `LIVEKIT_PHONE_DEFAULT_CC=91`, `LIVEKIT_OBSERVE_SECONDS`.

---

## “It worked” but **no audio** — what’s missing?

### Not the dispatch rule (for this path)

- **Dispatch rules** map **inbound** SIP (or other triggers) → room / agent name. They are **not** what creates the outbound PSTN leg.
- **Outbound** leg is created by **`CreateSIPParticipant`** + **outbound trunk**. Missing audio is **not** “forgot to add dispatch rule” for that outbound dial.

### Often: **no bot / no second publisher** in the room

- **`call_phone.py`** only creates a **SIP participant** (`phone_user`) in the room. There is **no voice agent** unless you also:
  - run **`agent.py`** (or a Cloud agent) **and** **dispatch** it to the **same room**, or
  - join another client/SDK that **publishes** audio and **subscribes** to the callee.

So: **ring + answer** can work, but you hear **silence** if nothing in the room **plays audio toward** the phone participant (and nothing **subscribes** correctly the other way).

**Fix:** Use the full **outbound caller agent** flow (`agent.py` + `dispatch_call.py` / `lk dispatch create`) so the **agent joins the same room** and runs **STT/LLM/TTS** toward `phone_user`. See [LiveKit outbound calls + agent](https://docs.livekit.io/telephony/making-calls/outbound-calls/).

### Codec / media (Exotel + SIP)

- Exotel often documents **G.711 (A-law/μ-law)** for SIP trunking. If codec negotiation fails or RTP is one-way, you get **no audio** or **one-way audio**.
- Check LiveKit telephony docs for **codec support** and Exotel’s **SIP error / troubleshooting** guides.

### RTP / firewall (one-way or no audio)

- SIP can be **200 OK** while **RTP** is blocked or NAT-asymmetric. Ensure firewall rules for **RTP** between **Exotel media IPs** and LiveKit / your network as per Exotel’s doc.

### Krisp / processing

- `call_phone.py` sets **`krisp_enabled=True`**. If you suspect processing issues, test with **`krisp_enabled=False`** in a forked request (same LiveKit API field) and compare.

### Wrong room / wrong participant identity

- Audio only flows between participants **in the same room** with correct **subscribe** behavior. If the bot joins **another room** or wrong **identity** in `RoomOptions`, you still get “connected but silent.”

---

## Quick checklist for audio

| Check | Question |
|--------|----------|
| Same room? | Bot/agent and `phone_user` in **one** `room_name` |
| Agent running? | Worker up; dispatch **agent name** matches |
| Publish/subscribe? | Agent session targets **`phone_user`** (see `room_io.RoomOptions(participant_identity=...)`) |
| Codecs | G.711 etc. per Exotel + LiveKit |
| RTP | Firewalls / NAT; Exotel media allowlisting |
| Dispatch rule | **Inbound** routing — not required for **outbound-only** `call_phone.py` test |

---

## Files touched in this workspace (summary)

- `call_phone.py` — E.164 normalization, `--observe`, clearer errors.
- `dispatch_call.py` / `agent.py` — optional `LIVEKIT_AGENT_NAME`.
- `.env` — `SIP_OUTBOUND_TRUNK_ID` and comments comparing trunks; keep **API keys and URL** on the **same** LiveKit project as the trunk.

For product reference: [Make outbound calls (LiveKit)](https://docs.livekit.io/telephony/making-calls/outbound-calls/).

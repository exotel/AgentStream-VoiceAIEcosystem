# Exotel vSIP + ElevenLabs — API scripts (SIP)

Run from the **repo root** after copying `.env.example` → `.env` and filling values.

**Requires:** `bash`, `curl`, `jq` (`brew install jq` on macOS).

## Environment (`.env`)

| Variable | Required for | Notes |
|----------|----------------|-------|
| `EXOTEL_API_KEY`, `EXOTEL_API_TOKEN`, `EXOTEL_ACCOUNT_SID` | All | From [API credentials](https://my.in.exotel.com/apisettings/site#api-credentials) |
| `EXOTEL_SUBDOMAIN` | All | e.g. `api.in.exotel.com` (India) |
| `EXOTEL_TRUNK_NAME` | Optional | Default `ElevenLabs_Trunk` |
| `EXOTEL_TRUNK_SID` | Steps 2+ | From `01-create-trunk.sh` output |
| `EXOTEL_PHONE_NUMBER` | 2 | E.164, e.g. `+918069412345` |
| `EXOTEL_SIP_USERNAME`, `EXOTEL_SIP_PASSWORD` | 3 | **Same** values as ElevenLabs → Phone number → SIP Digest |
| `EXOTEL_SIP_FRIENDLY_NAME` | Optional | Default `eleven_labs` |
| `ELEVENLABS_SIP_DESTINATION` | 4 (inbound) | Default `sip.rtc.elevenlabs.io:5060;transport=tcp` |

## Order of operations

### A — Outbound SIP (digest)

1. **`01-create-trunk.sh`** — creates trunk; set `EXOTEL_TRUNK_SID` in `.env`.
2. **`02-map-did.sh`** — attaches Exophone to trunk.
3. **`03-credentials.sh`** — SIP digest on Exotel (**must match** ElevenLabs import).
4. **ElevenLabs (dashboard):** import SIP number; digest match; **outbound address** = **Exotel edge `IP:port`** from Exotel.
5. **Optional:** If ElevenLabs provides a **single static egress IP**, add it via Exotel `whitelisted-ips` with **`mask: 32`** (Exotel trunk does **not** support CIDR range ACL).
6. Test outbound via ElevenLabs API ([current endpoint in ElevenLabs docs](https://elevenlabs.io/docs)).

### B — Inbound SIP (destination on trunk)

When **PSTN → Exotel → ElevenLabs** is required, add **destination URI** on the same trunk:

```bash
./scripts/exotel-elevenlabs/04-destination-uri-elevenlabs.sh
```

**Flow → Connect:** **Dial whom** = **`sip:<trunk_sid>`** (value from step 1 — not a full SIP URI). See [elevenlabs-voice-ai-connector.md](../../elevenlabs/integrations/exotel-vsip/elevenlabs-voice-ai-connector.md) Integration 2.

The script `05-trunk-alias.sh` is **not** part of the recommended integration path (caller ID alias removed from docs).

## Run examples

```bash
chmod +x scripts/exotel-elevenlabs/*.sh
./scripts/exotel-elevenlabs/01-create-trunk.sh
# edit .env → EXOTEL_TRUNK_SID=...

./scripts/exotel-elevenlabs/02-map-did.sh
./scripts/exotel-elevenlabs/03-credentials.sh

# When ready for inbound routing to ElevenLabs:
./scripts/exotel-elevenlabs/04-destination-uri-elevenlabs.sh
```

## References

- [Exotel vSIP Trunk Configuration API (GitHub)](https://github.com/exotel/exotel-vsip-trunk-Configuration-API)
- [Voice AI Connector](../../elevenlabs/integrations/exotel-vsip/elevenlabs-voice-ai-connector.md)

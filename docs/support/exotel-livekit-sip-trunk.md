# Connect Exotel Virtual SIP Trunk to LiveKit Telephony

This guide connects **Exotel SIP trunking** to **LiveKit Cloud** telephony so PSTN calls can reach **LiveKit rooms** and outbound calls can use Exotel as the Indian PSTN leg.

> **Applicability:** **UI-driven + developer-driven** (LiveKit Cloud console for trunks/dispatch; your app/agent joins rooms). Not a single “import trunk” wizard like some providers.

> **Exotel edge:** Signaling toward Exotel uses **edge IP:port** from Exotel ([network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)). Configure **`IP:port`** as Exotel assigns — not an assumed carrier hostname.

> **Edge hostnames you may see (India):** `in.voip.exotel.com:5070` (TCP) and `in.voip.exotel.com:443` (TLS). Use the exact host/IP + port + transport Exotel assigns. See [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md).

> **ACL vs digest (important):** Exotel trunk ACL (`whitelisted-ips`) is intended for **static `/32` IPs** only (`mask: 32`), not CIDR ranges. If the provider/network only has **CIDR/shared egress**, prefer **digest** and coordinate with Exotel support—IP allowlisting can become the primary trust signal and cause intermittent auth/routing issues in shared egress setups.

> **Scope:** LiveKit **Cloud** with **Telephony** enabled. See [`OUTBOUND-EXOTEL-NOTES.md`](../../Livekit/livekit-outbound-caller-agent/OUTBOUND-EXOTEL-NOTES.md) for 403, E.164, and “no audio” patterns.

> **Quickstart:** [`Livekit/integrations/exotel-vsip/QUICKSTART.md`](../../Livekit/integrations/exotel-vsip/QUICKSTART.md)

---

## What you will set up

| Direction | Path |
|-----------|------|
| **Inbound PSTN → LiveKit** | PSTN → Exotel DID → trunk **destination URI** → LiveKit SIP endpoint → dispatch → room |
| **Outbound PSTN ← LiveKit** | LiveKit outbound trunk → digest → Exotel edge **IP:port** → PSTN |

**Exotel trunk ACL:** use **`whitelisted-ips`** **only** when LiveKit (or your network) provides a **fixed static egress IP** to allow. Exotel trunk **does not support CIDR range** allowlisting — use **`mask: 32`** and **one POST per static IP**. Otherwise rely on **digest** (`POST .../credentials`).

---

## Architecture

```text
Inbound:  PSTN → Exotel DID → destination URI on trunk → LiveKit SIP host → room → agent
Outbound: LiveKit → Exotel edge IP:port (digest) → PSTN
```

---

## Prerequisites

- Exotel: KYC, DID **E.164**, [API credentials](https://my.in.exotel.com/apisettings/site#api-credentials), `https://api.in.exotel.com`.
- LiveKit: [Cloud](https://cloud.livekit.io/) project, Telephony, SIP URI from **Project settings** ([SIP trunk setup](https://docs.livekit.io/telephony/start/sip-trunk-setup/)).

---

## Part A — LiveKit Cloud

### SIP endpoint and region (inbound)

Copy **SIP URI** from project settings. For India pinning: `{subdomain}.india.sip.livekit.cloud` ([region pinning](https://docs.livekit.io/telephony/features/region-pinning/)).

### Inbound trunk

**Telephony** → **SIP trunks** → **Inbound** — include your Exotel DID in E.164 ([Inbound trunk](https://docs.livekit.io/telephony/accepting-calls/inbound-trunk/)).

### Dispatch rule

At least one rule so calls land in a room ([Dispatch rule](https://docs.livekit.io/telephony/accepting-calls/dispatch-rule/)).

### Outbound trunk

- **`address`** — Exotel **edge `IP:port`** from Exotel.
- **`numbers`** — Exotel DID **E.164**.
- **`authUsername` / `authPassword`** — same as Exotel **`POST .../credentials`**.

```json
{
  "name": "Exotel outbound",
  "address": "YOUR_EXOTEL_EDGE_IP:443",
  "numbers": ["+9198XXXXXXXX"],
  "authUsername": "SIP_USER",
  "authPassword": "SIP_PASS"
}
```

### Agent in same room

[`OUTBOUND-EXOTEL-NOTES.md`](../../Livekit/livekit-outbound-caller-agent/OUTBOUND-EXOTEL-NOTES.md) — ring without bot audio usually means no publisher in the room.

---

## Part B — Exotel APIs

**Rate limit:** 200/minute. Snippets: [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md).

### Outbound SIP — three steps

1. **Create trunk**
2. **Map DID** to trunk
3. **`POST .../credentials`** (`user_name`, `password`) — must match LiveKit outbound trunk auth

**Optional:** `POST .../whitelisted-ips` **only if** LiveKit gives you a **static SIP egress IP** to allow — **single IP**, `mask: 32` per entry. No CIDR range on trunk.

**Inbound only:** `POST .../destination-uris` toward your LiveKit SIP host (not required for minimal outbound-only testing).

```bash
curl -s -X POST \
  "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/credentials" \
  -H "Content-Type: application/json" \
  -d '{
    "user_name": "SIP_USER",
    "password": "SIP_PASS",
    "friendly_name": "livekit"
  }'
```

### Inbound SIP — destination URI on trunk

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "YOUR_SUBDOMAIN.india.sip.livekit.cloud:5061;transport=tls" }
    ]
  }'
```

### Connect applet (inbound)

**Dial whom:** **`sip:<trunk_sid>`** — use the **`trunk_sid`** from create trunk (**not** a full SIP URI). Map DID to Flow. [Voice AI / SIP trunk guide](https://support.exotel.com/support/solutions/articles/3000133452-flow-and-api-configuration-guide-for-voice-ai-contact-centre-platforms-via-exotel-virtual-sip-trunk).

---

## Testing

**Outbound SIP** was validated with correct **edge IP:port**, **digest**, and **E.164**; optional static-IP ACL when applicable. Audio still requires an **agent** in the **same** room as the SIP participant.

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| **403** / `4001` | Digest; optional static-IP ACL; correct **edge IP:port** |
| Wrong format | **E.164** for India |
| Ring, no bot | Agent + room ([OUTBOUND-EXOTEL-NOTES.md](../../Livekit/livekit-outbound-caller-agent/OUTBOUND-EXOTEL-NOTES.md)) |
| Connect broken | **`sip:<trunk_sid>`** only in Dial whom |

---

## References

| Resource | URL |
|----------|-----|
| LiveKit Cloud | https://cloud.livekit.io/ |
| LiveKit SIP trunk setup | https://docs.livekit.io/telephony/start/sip-trunk-setup/ |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |

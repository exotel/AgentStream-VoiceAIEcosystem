# Connect Exotel SIP trunking to Vapi

This guide connects **Exotel SIP trunking** to **[Vapi](https://vapi.ai/)** using Vapi’s **Bring Your Own (BYO) SIP trunk** credential (`byo-sip-trunk`) and **BYO phone number** (`byo-phone-number`), with Exotel as the Indian PSTN carrier.

**GitHub repo (reference):** https://github.com/exotel/AgentStream-VoiceAIEcosystem

> **Applicability:** **UI-driven + API-driven** (Vapi dashboard objects, also creatable via API).

> **Exotel edge:** Use **IPv4 `IP:port`** from Exotel for SIP toward their gateway ([network and firewall](https://docs.exotel.com/dynamic-sip-trunking/network-and-firewall-configuration)). **Vapi’s SBC expects a numeric IPv4 in the gateway field** — resolve any hostname to IPv4 before saving the credential ([hostname vs IP](https://docs.vapi.ai/advanced/sip/troubleshoot-sip-trunk-credential-errors)).

> **Edge hostnames you may see (India):** `in.voip.exotel.com:5070` (TCP) and `in.voip.exotel.com:443` (TLS). If you see hostnames but need IPv4, resolve to IPv4 only if Exotel confirms that mapping. See [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md).

> **ACL vs digest (important):** Only use Exotel `whitelisted-ips` for **static `/32` IPs** (`mask: 32`). Do **not** attempt to whitelist **CIDR ranges**; if your egress is shared/range-based, prefer **digest** and coordinate with Exotel support—allowlists can become the primary trust signal and cause auth/routing issues in multi-tenant egress setups.

> **Vapi → Exotel allowlist:** Vapi signals from **two static SBC IPs**. Add **both** to Exotel **`whitelisted-ips`** with **`mask: 32`** (one POST per IP) so Vapi can reach your trunk ([Vapi SIP trunking](https://docs.vapi.ai/advanced/sip/sip-trunk), [networking](https://docs.vapi.ai/advanced/sip/sip-networking)).

> **Engineering detail:** [`vapi/integrations/exotel-vsip/vapi-exotel-voice-ai-connector.md`](../../vapi/integrations/exotel-vsip/vapi-exotel-voice-ai-connector.md)

> **Quickstart:** [`vapi/integrations/exotel-vsip/QUICKSTART.md`](../../vapi/integrations/exotel-vsip/QUICKSTART.md)

---

## Vapi (from official docs)

| Topic | Detail |
|--------|--------|
| BYO SIP trunk | [SIP trunking](https://docs.vapi.ai/advanced/sip/sip-trunk) — `POST /credential` with `provider: "byo-sip-trunk"`, `gateways[]`, `outboundAuthenticationPlan` |
| Phone number | `POST /phone-number` with `provider: "byo-phone-number"`, `credentialId`, E.164 `number` |
| Vapi SBC IPs (allow on **Exotel**) | `44.229.228.186/32`, `44.238.177.138/32` ([networking](https://docs.vapi.ai/advanced/sip/sip-networking)) |
| Signalling host | **`sip.vapi.ai`** (DNS for SBC); ports **5060** (UDP) / **5061** (TLS) per Vapi |
| RTP | UDP **40000–60000**; media IPs are **dynamic** on Vapi side ([networking](https://docs.vapi.ai/advanced/sip/sip-networking)) |
| Troubleshooting | [SIP trunk credential errors](https://docs.vapi.ai/advanced/sip/troubleshoot-sip-trunk-credential-errors) — IPv4 only, `inboundEnabled` for outbound-only trunks, allowlist |

---

## Flows

| Direction | What to configure |
|-----------|-------------------|
| **Outbound SIP** | **Exotel:** create trunk → map DID → `POST .../credentials`. **`POST .../whitelisted-ips`** for **both** Vapi SBC IPs (`mask: 32` each). **Vapi:** BYO credential → gateway **`ip`** = **Exotel edge IPv4**, **`port`** / **`outboundProtocol`** aligned with Exotel (often **TCP** or **TLS** — confirm with Exotel for SIP trunking). **Digest** must match Exotel credentials. |
| **Inbound SIP** | **Exotel:** **`POST .../destination-uris`** on the trunk toward Vapi’s SIP entry (typically **`sip.vapi.ai`** with port/transport per [Vapi networking](https://docs.vapi.ai/advanced/sip/sip-networking)). **Flow → Connect:** **`sip:<trunk_sid>`** in **Dial whom** (`trunk_sid` from create trunk, not a full URI). **Vapi:** enable **inbound** on the gateway if you receive PSTN-in via Exotel; follow Vapi’s inbound testing notes in [SIP trunking](https://docs.vapi.ai/advanced/sip/sip-trunk). |

**Exotel trunk ACL:** no **CIDR ranges** — only **one static IP per `whitelisted-ips` call** (`mask: 32`). Vapi publishes **two** fixed signalling IPs; add **both**.

---

## Part A — Vapi (API / dashboard)

1. Create an **assistant** in [Dashboard](https://dashboard.vapi.ai/) or via API ([quickstart](https://docs.vapi.ai/quickstart/dashboard)).
2. **Outbound:** Create a **BYO SIP trunk** credential — gateway points to **Exotel edge IPv4:port**, **`outboundAuthenticationPlan`** matches Exotel **`user_name` / `password`**. Set **`outboundProtocol`** to match Exotel (e.g. `tcp` or `tls`; align port). Use **`inboundEnabled: false`** if the trunk is outbound-only ([troubleshooting](https://docs.vapi.ai/advanced/sip/troubleshoot-sip-trunk-credential-errors)).
3. Create a **BYO phone number** linked to that **`credentialId`** ([SIP trunking](https://docs.vapi.ai/advanced/sip/sip-trunk)).
4. Test outbound with **`POST /call/phone`** using `phoneNumberId` and `assistantId` per docs.
5. **Inbound:** After Exotel routes to Vapi, place a test PSTN call to your DID; confirm **`destination-uris`** and Vapi inbound gateway settings match current Vapi documentation.

---

## Part B — Exotel APIs

**Auth:** `API_KEY:API_TOKEN@api.in.exotel.com` · **200 requests/minute (SIP trunk APIs)** · [`_exotel-trunk-api-snippets.md`](./_exotel-trunk-api-snippets.md)

### Whitelist Vapi SBC (recommended for Vapi → Exotel)

Repeat once per IP (`mask: 32`):

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "44.229.228.186", "mask": 32}'
```

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/whitelisted-ips" \
  -H "Content-Type: application/json" \
  -d '{"ip": "44.238.177.138", "mask": 32}'
```

### Outbound SIP (minimal)

1. Create trunk  
2. Map DID  
3. `POST .../credentials` — same username/password as Vapi `outboundAuthenticationPlan`  
4. `whitelisted-ips` for both Vapi IPs above (unless Exotel support documents a different allowlist model for your account)

### Inbound SIP — destination URI on trunk

Point Exotel **inbound** SIP toward Vapi’s signalling endpoint. **Confirm port and transport** with [Vapi networking](https://docs.vapi.ai/advanced/sip/sip-networking) and Exotel compatibility (UDP vs TLS):

```bash
curl -s -X POST "https://${API_KEY}:${API_TOKEN}@${SUBDOMAIN}/v2/accounts/${ACCOUNT_SID}/trunks/${TRUNK_SID}/destination-uris" \
  -H "Content-Type: application/json" \
  -d '{
    "destinations": [
      { "destination": "sip.vapi.ai:5060;transport=udp" }
    ]
  }'
```

If your account requires **TLS** signalling toward Vapi, use **`5061`** and **`transport=tls`** instead — align with Vapi and Exotel.

### Connect applet (inbound)

**Dial whom:** **`sip:<trunk_sid>`** — [Voice AI / SIP trunking](https://support.exotel.com/support/solutions/articles/3000133452-flow-and-api-configuration-guide-for-voice-ai-contact-centre-platforms-via-exotel-virtual-sip-trunk).

---

## Troubleshooting

| Symptom | What to check |
|---------|----------------|
| Vapi **gateway creation failed** | Hostname in `gateways[].ip` — use **IPv4 only** ([troubleshoot](https://docs.vapi.ai/advanced/sip/troubleshoot-sip-trunk-credential-errors)) |
| **401 / intermittent failures** | **Both** Vapi IPs on Exotel **`whitelisted-ips`**; digest match on trunk |
| Outbound-only trunk errors | Set **`inboundEnabled: false`** on Vapi gateway ([troubleshoot](https://docs.vapi.ai/advanced/sip/troubleshoot-sip-trunk-credential-errors)) |
| One-way audio / no RTP | Firewall: allow **UDP 40000–60000** bidirectional per [Vapi networking](https://docs.vapi.ai/advanced/sip/sip-networking) |
| Connect misrouted | **`sip:<trunk_sid>`** only in Dial whom |

---

## References

| Resource | URL |
|----------|-----|
| Vapi dashboard | https://dashboard.vapi.ai/ |
| Vapi — SIP trunking | https://docs.vapi.ai/advanced/sip/sip-trunk |
| Vapi — SIP networking | https://docs.vapi.ai/advanced/sip/sip-networking |
| Vapi — troubleshoot SIP trunk | https://docs.vapi.ai/advanced/sip/troubleshoot-sip-trunk-credential-errors |
| Vapi — SIP overview | https://docs.vapi.ai/advanced/sip |
| Exotel SIP API | https://docs.exotel.com/dynamic-sip-trunking/detailed-sip-trunking-api-reference |

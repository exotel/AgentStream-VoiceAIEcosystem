# Quickstart: Exotel vSIP + Pipecat (via Daily SIP)

**Pipecat** uses **Daily** for media. **SIP** is enabled on **Daily rooms** ([Daily SIP](https://docs.daily.co/guides/products/dial-in-dial-out/sip)). **Exotel vSIP** applies when **Exotel** is your **PSTN carrier** or **SIP peer** to Daily.

**Inbound (typical):** Follow [Pipecat’s PSTN + Daily SIP guide](https://docs.pipecat.ai/guides/telephony/twilio-daily-sip) — use **Exotel’s** call-control to attach the live call to Daily’s **`sip_uri`** after the room is ready (`on_dialin_ready`).

**Outbound (SIP):** Daily can **SIP dial-out** to a `sip:` URI ([Daily SIP dial-out](https://docs.daily.co/guides/products/dial-in-dial-out/sip)). Point that leg at **Exotel’s edge `IP:port`** with digest auth aligned to Exotel **`POST .../credentials`**.

---

## 1 — Daily (Pipecat)

1. Paid Daily account with **SIP** enabled ([Daily SIP prerequisites](https://docs.daily.co/guides/products/dial-in-dial-out/sip)).  
2. Implement the **PSTN + SIP** pattern from Pipecat’s guide — **DailyTransport**, **`on_dialin_ready`**, bridge to **`sip_endpoint`**.  
3. Confirm codecs: Daily supports **PCMU/PCMA** (common with PSTN); align with Exotel / your region.

---

## 2 — Exotel: outbound SIP (carrier toward PSTN)

When **Daily** (or your dial-out logic) sends SIP to **Exotel** to reach PSTN:

```bash
# Create trunk → map DID → POST .../credentials
# See shared snippets for full curls
```

**Order:** create trunk → map DID → **`POST .../credentials`** (`user_name`, `password`).

**Optional ACL:** `POST .../whitelisted-ips` **only** if Daily (or your egress) publishes a **single static IP** — **`mask: 32`**, no CIDR range on the trunk.

---

## 3 — Exotel: inbound PSTN (when using static SIP partner)

If a **fixed** SIP ingress is used (less common for Pipecat + dynamic Daily rooms), set **`destination-uris`** on the trunk toward that host and use **Flow → Connect** with **`sip:<trunk_sid>`** per Exotel docs.

For **dynamic Daily `sip_uri` per call**, prefer the **webhook + bridge** model from Pipecat’s PSTN guide rather than a single static destination.

---

## Shared curls

[`docs/support/_exotel-trunk-api-snippets.md`](../../../docs/support/_exotel-trunk-api-snippets.md)

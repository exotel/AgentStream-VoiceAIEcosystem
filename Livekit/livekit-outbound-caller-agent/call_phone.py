#!/usr/bin/env python3
"""Place an outbound call using your existing SIP trunk (no agent required).

Uses CreateSIPParticipantRequest: creates a room, then a SIP participant that
dials the given number. The callee is connected to the room when they answer.

Requires in .env.local:
  LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, SIP_OUTBOUND_TRUNK_ID

Usage:
  python3 call_phone.py <phone_number>
  python3 call_phone.py +1234567890
  python3 call_phone.py +1234567890 --no-wait  # return immediately without waiting for answer (default: wait)
  python3 call_phone.py +1234567890 --no-wait --observe  # poll room: SIP status, state, disconnect_reason
  LIVEKIT_OBSERVE_SECONDS=120 python3 call_phone.py +1234567890 --no-wait --observe

Phone number: prefer full E.164 (+919876543210). Without +, Indian numbers are normalized:
  9876543210 / 09876543210 → +919876543210. Other regions: include + and country code.

Env: LIVEKIT_PHONE_DEFAULT_CC (default 91). Trunk must have at least one number (caller ID) in LiveKit.
"""
import argparse
import asyncio
import os
import re
import sys
import time
from datetime import datetime, timezone
from uuid import uuid4

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
load_dotenv(dotenv_path=".env.local")

if os.getenv("LIVEKIT_INSECURE_SSL") == "1":
    import aiohttp
    _orig = aiohttp.TCPConnector.__init__
    aiohttp.TCPConnector.__init__ = lambda self, *a, ssl=True, **k: _orig(self, *a, ssl=False, **k)

from livekit import api
from livekit.protocol.models import DisconnectReason, ParticipantInfo


def normalize_phone_e164(raw: str, default_cc: str) -> str:
    """Best-effort E.164; India (cc=91) fixes 0-prefixed / 10-digit mobile input."""
    s = raw.strip().replace(" ", "").replace("-", "")
    if not s:
        return s
    cc = (default_cc or "91").lstrip("+")
    if s.startswith("+"):
        # Common typo: +7411… instead of +917411… (dropped "9" from +91)
        if cc == "91":
            m = re.fullmatch(r"\+7(\d{9})", s)
            if m:
                return "+917" + m.group(1)
        return s
    digits = "".join(c for c in s if c.isdigit())
    if not digits:
        return "+" + s

    if cc == "91":
        if len(digits) == 12 and digits.startswith("91"):
            return "+" + digits
        if len(digits) == 11 and digits.startswith("0"):
            national = digits[1:]
            if len(national) == 10:
                return "+91" + national
        if len(digits) == 10:
            return "+91" + digits

    return "+" + digits.lstrip("0") if digits.lstrip("0") else "+" + digits


def _enum_name(enum_wrapper, value: int) -> str:
    try:
        return enum_wrapper.Name(value)
    except ValueError:
        return f"UNKNOWN({value})"


def _format_participant(p) -> str:
    lines = [
        f"  identity={p.identity!r} name={p.name!r} sid={p.sid}",
        f"  state={_enum_name(ParticipantInfo.State, p.state)} ({p.state})",
        f"  disconnect_reason={_enum_name(DisconnectReason, p.disconnect_reason)} ({p.disconnect_reason})",
    ]
    attrs = dict(p.attributes)
    if attrs:
        lines.append("  attributes:")
        for k in sorted(attrs):
            lines.append(f"    {k}={attrs[k]!r}")
    else:
        lines.append("  attributes: (none)")
    return "\n".join(lines)


async def observe_room(
    lkapi: api.LiveKitAPI,
    room_name: str,
    watch_identity: str,
    total_seconds: float,
    interval: float = 2.0,
) -> None:
    """Poll ListParticipants to show SIP leg progress (local observability)."""
    deadline = time.monotonic() + total_seconds
    print()
    print("--- observe: polling room (local only; use Cloud dashboard for full traces) ---")
    print(f"room={room_name!r}  watch_identity={watch_identity!r}  ~{total_seconds:.0f}s every {interval}s")
    print(f"search this room name in LiveKit Cloud → Telephony / Rooms if needed")
    print("---")

    last_snapshot = ""
    zero_streak = 0
    warned_empty = False
    while time.monotonic() < deadline:
        try:
            res = await lkapi.room.list_participants(
                api.ListParticipantsRequest(room=room_name)
            )
        except api.TwirpError as e:
            print(f"observe: list_participants failed: {e.code} {e.message}", file=sys.stderr)
            return
        now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        block_lines = [f"[{now}] participants={len(res.participants)}"]
        target = None
        for p in res.participants:
            block_lines.append(_format_participant(p))
            if p.identity == watch_identity:
                target = p
        block = "\n".join(block_lines)
        if block != last_snapshot:
            print(block)
            print("---")
            last_snapshot = block

        if len(res.participants) == 0:
            zero_streak += 1
            if zero_streak >= 3 and not warned_empty:
                warned_empty = True
                print(
                    "observe: still 0 participants — SIP leg may be failing before join "
                    "(Exotel ACL, trunk address/auth, caller ID on trunk). "
                    "Check Exotel call logs and LiveKit outbound trunk JSON.",
                    file=sys.stderr,
                )
        else:
            zero_streak = 0

        if target is not None and target.state == ParticipantInfo.State.DISCONNECTED:
            print("observe: target participant disconnected; stopping poll.")
            return
        if target is not None:
            st = target.attributes.get("sip.callStatus", "")
            if st == "active":
                print("observe: sip.callStatus is active; stopping poll.")
                return

        await asyncio.sleep(interval)

    print("observe: time limit reached; stopping poll.")


async def main():
    parser = argparse.ArgumentParser(description="Outbound SIP call via LiveKit CreateSIPParticipant")
    parser.add_argument("phone_number", help="E.164 number, e.g. +919876543210")
    parser.add_argument("--no-wait", action="store_true", help="Do not block until callee answers")
    parser.add_argument(
        "--observe",
        action="store_true",
        help="After placing call, poll room and print participant state and sip.* attributes",
    )
    parser.add_argument(
        "--observe-seconds",
        type=float,
        default=None,
        help="How long to poll (default: LIVEKIT_OBSERVE_SECONDS or 90)",
    )
    args = parser.parse_args()

    phone_number = args.phone_number.strip()
    wait_until_answered = not args.no_wait
    observe_seconds = (
        args.observe_seconds
        if args.observe_seconds is not None
        else float(os.getenv("LIVEKIT_OBSERVE_SECONDS", "90"))
    )
    sip_identity = "phone_user"

    if args.observe and wait_until_answered:
        print(
            "Tip: use --no-wait with --observe to watch ringing / sip.callStatus before answer.",
            file=sys.stderr,
        )

    cc_default = os.getenv("LIVEKIT_PHONE_DEFAULT_CC", "91")
    raw_input = phone_number
    phone_number = normalize_phone_e164(phone_number, cc_default)
    if raw_input != phone_number:
        print(f"Normalized {raw_input!r} → {phone_number!r} (default CC {cc_default!r})")

    url = os.getenv("LIVEKIT_URL")
    key = os.getenv("LIVEKIT_API_KEY")
    secret = os.getenv("LIVEKIT_API_SECRET")
    trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")

    if not all((url, key, secret, trunk_id)):
        print("Error: Set LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, SIP_OUTBOUND_TRUNK_ID in .env.local", file=sys.stderr)
        sys.exit(1)

    if not trunk_id.startswith("ST_"):
        print("Error: SIP_OUTBOUND_TRUNK_ID should look like ST_... (outbound trunk ID)", file=sys.stderr)
        sys.exit(1)

    room_name = f"call-{uuid4().hex[:12]}"

    print("Trunk:", trunk_id)
    print("Dialing:", phone_number)
    print("Room:", room_name)
    print("Waiting for answer:", wait_until_answered)
    print("Placing call...")

    request = api.CreateSIPParticipantRequest(
        sip_trunk_id=trunk_id,
        sip_call_to=phone_number,
        room_name=room_name,
        participant_identity=sip_identity,
        participant_name="Caller",
        krisp_enabled=True,
        wait_until_answered=wait_until_answered,
        play_dialtone=True,
    )

    async with api.LiveKitAPI() as lkapi:
        await lkapi.room.create_room(api.CreateRoomRequest(name=room_name))
        try:
            participant = await lkapi.sip.create_sip_participant(request)
            print("Participant created:", participant.participant_identity, "in room", participant.room_name)
            if participant.sip_call_id:
                print("sip_call_id:", participant.sip_call_id)
            if participant.participant_id:
                print("participant_id:", participant.participant_id)
            if wait_until_answered:
                print("Call answered; callee is in room:", room_name)
            else:
                print("Call placed; room:", room_name)
            if args.observe:
                await observe_room(
                    lkapi, room_name, sip_identity, observe_seconds, interval=2.0
                )
        except api.TwirpError as e:
            print("SIP/API error:", e.message, file=sys.stderr)
            print("Code:", e.code, file=sys.stderr)
            if e.metadata:
                for k, v in e.metadata.items():
                    print(f"  {k}: {v}", file=sys.stderr)
                sip_code = e.metadata.get("sip_status_code")
                sip_msg = e.metadata.get("sip_status")
                if sip_code or sip_msg:
                    print("SIP status code:", sip_code, file=sys.stderr)
                    print("SIP status:", sip_msg, file=sys.stderr)
            print("\nCheck: trunk address/auth, trunk 'numbers' (caller ID), and E.164 number (+countrycode...).", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print("Error creating SIP participant:", e, file=sys.stderr)
            if hasattr(e, "metadata") and getattr(e, "metadata", None):
                m = e.metadata
                if isinstance(m, dict):
                    for k, v in m.items():
                        print(f"  {k}: {v}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

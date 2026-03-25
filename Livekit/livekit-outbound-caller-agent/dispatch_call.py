#!/usr/bin/env python3
"""Dispatch the outbound-caller agent to place a call (no LiveKit CLI required).

Uses LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET from .env.local.

Usage:
  python3 dispatch_call.py +917696016726
  ./venv/bin/python3 dispatch_call.py +1234567890
"""
import asyncio
import os
import sys
from uuid import uuid4

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
load_dotenv(dotenv_path=".env.local")

# Skip SSL verification for API calls if requested (e.g. macOS cert store issues).
# Keep wss:// so LiveKit Cloud API works.
if os.getenv("LIVEKIT_INSECURE_SSL") == "1":
    import aiohttp
    _orig = aiohttp.TCPConnector.__init__
    aiohttp.TCPConnector.__init__ = lambda self, *a, ssl=True, **k: _orig(self, *a, ssl=False, **k)

from livekit import api


async def main():
    if len(sys.argv) < 2:
        print("Usage: python3 dispatch_call.py <phone_number>", file=sys.stderr)
        print("Example: python3 dispatch_call.py +917696016726", file=sys.stderr)
        sys.exit(1)

    phone_number = sys.argv[1].strip()
    if not phone_number:
        print("Error: phone number is required", file=sys.stderr)
        sys.exit(1)

    url = os.getenv("LIVEKIT_URL")
    key = os.getenv("LIVEKIT_API_KEY")
    secret = os.getenv("LIVEKIT_API_SECRET")
    if not url or not key or not secret:
        print("Error: Set LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET in .env.local", file=sys.stderr)
        sys.exit(1)

    agent_name = (os.getenv("LIVEKIT_AGENT_NAME") or "outbound-caller").strip()
    if not agent_name:
        print("Error: LIVEKIT_AGENT_NAME is empty", file=sys.stderr)
        sys.exit(1)

    room_name = f"outbound-{uuid4().hex[:12]}"
    print(f"Dispatching agent {agent_name!r} to room {room_name} for {phone_number!r}")
    async with api.LiveKitAPI() as lkapi:
        await lkapi.room.create_room(api.CreateRoomRequest(name=room_name))
        await lkapi.agent_dispatch.create_dispatch(
            api.CreateAgentDispatchRequest(
                agent_name=agent_name,
                room=room_name,
                metadata=phone_number,
            )
        )
        print(f"Dialing {phone_number}... (waiting for call to connect)")
        for _ in range(90):
            await asyncio.sleep(2)
            r = await lkapi.room.list_participants(
                api.ListParticipantsRequest(room=room_name)
            )
            for p in r.participants:
                if p.identity == "phone_user":
                    status = p.attributes.get("sip.callStatus", "")
                    if status == "active":
                        print("Call connected.")
                        return
                    if p.state == 3:  # DISCONNECTED
                        print("Call ended before answer.")
                        return
            print(".", end="", flush=True)
        print("\nTimeout waiting for call.")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""Update an existing SIP outbound trunk via LiveKit API.

Uses SIPOutboundTrunkInfo, SIPTransport, and update_sip_outbound_trunk only.
Requires an existing trunk ID (SIP_OUTBOUND_TRUNK_ID in .env.local or first argument).
Config from outbound-trunk.json or outbound-trunk-example.json.

Run:
  python3 create_outbound_trunk.py
  python3 create_outbound_trunk.py <trunk_id>
"""
import asyncio
import json
import os
import sys

from dotenv import load_dotenv
load_dotenv(".env")
load_dotenv(".env.local")

if os.getenv("LIVEKIT_INSECURE_SSL") == "1":
    import aiohttp
    _o = aiohttp.TCPConnector.__init__
    aiohttp.TCPConnector.__init__ = lambda self, *a, ssl=True, **k: _o(self, *a, ssl=False, **k)

from livekit import api
from livekit.protocol.sip import SIPOutboundTrunkInfo, SIPTransport


async def main():
    trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID") or (sys.argv[1].strip() if len(sys.argv) > 1 else None)
    if not trunk_id:
        print("Error: Set SIP_OUTBOUND_TRUNK_ID in .env.local or pass trunk ID as first argument", file=sys.stderr)
        sys.exit(1)

    path = "outbound-trunk.json"
    if not os.path.isfile(path):
        path = "outbound-trunk-example.json"
    with open(path) as f:
        data = json.load(f)
    t = data.get("trunk", data)

    trunk = SIPOutboundTrunkInfo(
        address=t["address"],
        numbers=t.get("numbers", ["*"]),
        name=t["name"],
        transport=SIPTransport.SIP_TRANSPORT_AUTO,
        auth_username=t["auth_username"],
        auth_password=t["auth_password"],
    )

    async with api.LiveKitAPI() as lkapi:
        trunk = await lkapi.sip.update_sip_outbound_trunk(trunk_id, trunk)

    print("Trunk updated. ID:", trunk.sip_trunk_id)


if __name__ == "__main__":
    asyncio.run(main())

# Use certifi for SSL on macOS
import os
try:
    c = __import__("certifi").where()
    if c:
        os.environ.setdefault("SSL_CERT_FILE", c)
        os.environ.setdefault("REQUESTS_CA_BUNDLE", c)
except Exception:
    pass

import asyncio
import logging

from dotenv import load_dotenv
load_dotenv(".env")
load_dotenv(".env.local")

if os.getenv("LIVEKIT_INSECURE_SSL") == "1":
    _u = os.getenv("LIVEKIT_URL", "")
    if _u.startswith("wss://"):
        os.environ["LIVEKIT_URL"] = "ws://" + _u[6:]
    import aiohttp
    _o = aiohttp.ClientSession.ws_connect
    async def _p(self, url, *a, **k):
        if "livekit" in url:
            k.setdefault("ssl", False)
        return await _o(self, url, *a, **k)
    aiohttp.ClientSession.ws_connect = _p

from livekit import rtc, api
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents.voice import AgentSession, Agent, room_io

from livekit.plugins import openai, deepgram

logger = logging.getLogger("outbound-caller")
logger.setLevel(logging.INFO)

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
SIP_OUTBOUND_TRUNK_ID = os.getenv("SIP_OUTBOUND_TRUNK_ID")
# Must match LIVEKIT_AGENT_NAME used by dispatch_call.py / lk dispatch create
AGENT_NAME = (os.getenv("LIVEKIT_AGENT_NAME") or "outbound-caller").strip()

# Optional: OPENAI_API_KEY, DEEPGRAM_API_KEY for voice bot (defaults from env)
VOICE_BOT_INSTRUCTIONS = (
    "You are a friendly phone assistant. Keep responses short and clear for a phone call. "
    "Greet the caller and help with their questions."
)


async def entrypoint(ctx: JobContext):
    if not SIP_OUTBOUND_TRUNK_ID or not SIP_OUTBOUND_TRUNK_ID.startswith("ST_"):
        raise ValueError("SIP_OUTBOUND_TRUNK_ID not set in .env.local")
    logger.info("connecting to room %s", ctx.room.name)
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    phone = ctx.job.metadata or ""
    user_id = "phone_user"
    logger.info("dialing %s", phone)

    await ctx.api.sip.create_sip_participant(
        api.CreateSIPParticipantRequest(
            room_name=ctx.room.name,
            sip_trunk_id=SIP_OUTBOUND_TRUNK_ID,
            sip_call_to=phone,
            participant_identity=user_id,
        )
    )
    participant = await ctx.wait_for_participant(identity=user_id)

    # Wait for call to be active so the user hears the bot
    for _ in range(75):
        status = participant.attributes.get("sip.callStatus")
        if status == "active":
            break
        if participant.disconnect_reason in (
            rtc.DisconnectReason.USER_REJECTED,
            rtc.DisconnectReason.USER_UNAVAILABLE,
        ):
            logger.info("call ended before answer: %s", participant.disconnect_reason)
            return
        await asyncio.sleep(0.5)
    else:
        logger.warning("call did not become active in time, starting bot anyway")

    # Voice bot: STT (Deepgram) -> LLM (OpenAI) -> TTS (OpenAI); talks to phone_user
    stt = deepgram.STT()
    llm = openai.LLM(model="gpt-4o-mini")
    tts = openai.TTS(voice="alloy")

    agent = Agent(
        instructions=VOICE_BOT_INSTRUCTIONS,
        stt=stt,
        llm=llm,
        tts=tts,
    )

    session = AgentSession(
        stt=stt,
        llm=llm,
        tts=tts,
    )

    close_fut: asyncio.Future[None] = asyncio.Future()

    def on_close(_):
        if not close_fut.done():
            close_fut.set_result(None)

    session.on("close", on_close)

    await session.start(
        agent,
        room=ctx.room,
        room_options=room_io.RoomOptions(participant_identity=user_id),
    )

    # Greet the caller
    session.say("Hello! Thanks for calling. How can I help you today?")

    # Run until the caller hangs up (session closes)
    try:
        await asyncio.wait_for(close_fut, timeout=600.0)
    except asyncio.TimeoutError:
        logger.info("call timeout")
    finally:
        session.shutdown(drain=False)
        try:
            await asyncio.wait_for(session.aclose(), timeout=5.0)
        except Exception:
            pass
    ctx.shutdown()


if __name__ == "__main__":
    if not LIVEKIT_URL or not LIVEKIT_API_KEY or not LIVEKIT_API_SECRET:
        logger.error("Set LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET in .env.local")
        raise SystemExit(1)
    if "demo.livekit.io" in (LIVEKIT_URL or ""):
        logger.error("Use your real LiveKit URL in .env.local (e.g. wss://your-project.livekit.cloud)")
        raise SystemExit(1)
    if LIVEKIT_URL and LIVEKIT_URL.startswith("https://") and "livekit.cloud" in LIVEKIT_URL:
        os.environ["LIVEKIT_URL"] = "wss://" + LIVEKIT_URL[8:]

    cli.run_app(
        WorkerOptions(entrypoint_fnc=entrypoint, agent_name=AGENT_NAME)
    )

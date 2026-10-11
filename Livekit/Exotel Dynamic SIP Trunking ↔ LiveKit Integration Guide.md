# Exotel Dynamic SIP Trunking ↔ LiveKit Integration Guide

Connect Exotel's Dynamic SIP Trunk to LiveKit Agents to power outbound AI voice calls over PSTN and mobile networks.

---

## Table of Contents

1. [Overview](#overview)  
2. [Architecture](#architecture)  
3. [Prerequisites](#prerequisites)  
4. [Step 1 — Install LiveKit CLI](#step-1--install-livekit-cli)  
5. [Step 2 — Authenticate LiveKit CLI](#step-2--authenticate-livekit-cli)  
6. [Step 3 — Set Environment Variables](#step-3--set-environment-variables)  
7. [Step 4 — Verify SIP Trunk](#step-4--verify-sip-trunk)  
8. [Step 5 — Verify Agent and Dispatch Name](#step-5--verify-agent-and-dispatch-name)  
9. [Step 6 — Dispatch Agent to Room](#step-6--dispatch-agent-to-room)  
10. [Step 7 — Verify Room Creation](#step-7--verify-room-creation)  
11. [Step 8 — Prepare Outbound Call Payload](#step-8--prepare-outbound-call-payload)  
12. [Step 9 — Initiate Outbound Call](#step-9--initiate-outbound-call)  
13. [Step 10 — Verify End-to-End Connection](#step-10--verify-end-to-end-connection)  
14. [Configuration Checklists](#configuration-checklists)  
15. [Troubleshooting](#troubleshooting)  
16. [Quick Reference — CLI Commands](#quick-reference--cli-commands)

---

## Overview

This guide walks through integrating **Exotel Dynamic SIP Trunking** with **LiveKit Agents** to make outbound AI-powered voice calls to PSTN and mobile numbers.

In this setup, a LiveKit Agent (your AI bot) joins a LiveKit Room, a SIP participant bridges that room to the Exotel SIP Trunk, and Exotel places the actual call to the end user's phone number.

### Call Flow

```
LiveKit Agent (AI Bot / LLM)
        │
        ▼
   LiveKit Room
        │
        ▼
LiveKit SIP Participant
        │
        ▼
  Exotel SIP Trunk
        │
        ▼
  PSTN / Mobile User
```

---

## Architecture

```
┌─────────────────────────┐
│    LiveKit Agent        │
│  (AI Bot / LLM)         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│      LiveKit Room       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  LiveKit SIP Participant│
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   Exotel SIP Trunk      │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│   PSTN / Mobile User    │
└─────────────────────────┘
```

**Component Responsibilities:**

| Component | Role |
| :---- | :---- |
| LiveKit Agent | Hosts your AI model (LLM \+ STT \+ TTS) and handles conversation logic |
| LiveKit Room | A virtual audio/video room where the agent and SIP participant meet |
| LiveKit SIP Participant | Bridges LiveKit Room audio to and from the SIP trunk |
| Exotel SIP Trunk | Terminates the SIP call to the PSTN network and dials the end user |
| PSTN / Mobile User | The real person receiving the AI call |

---

## Prerequisites

### Exotel Side

Ensure the following are configured in your Exotel account before proceeding:

| Requirement | Details |
| :---- | :---- |
| Dynamic SIP Trunk | Enabled on your Exotel account |
| SIP Username | Provided by Exotel |
| SIP Password | Provided by Exotel |
| SIP Edge Hostname | e.g., `in.voip.exotel.com:5070` |
| DID / Outbound Number | e.g., `+91XXXXXXXXXX` |
| Outbound Calling | Enabled on the SIP trunk |
| Auth Type | Digest Authentication |
| Transport | TCP (recommended) |
| Public Internet Access | LiveKit must be able to reach Exotel SIP edge over the internet |
| TCP Connectivity | SIP port must be open (default: 5070\) |

📖 **Reference:** [Exotel Dynamic SIP Trunking Docs](https://docs.exotel.com/dynamic-sip-trunking/connect-exotel-sip-trunk-to-livekit)

### LiveKit Side

Ensure the following are ready before proceeding:

| Requirement | Details |
| :---- | :---- |
| LiveKit Cloud Account | Active account at [livekit.io](https://livekit.io) |
| LiveKit API Key | Available in your LiveKit project settings |
| LiveKit API Secret | Available in your LiveKit project settings |
| SIP Feature Enabled | Must be enabled for your LiveKit project |
| LiveKit Agent | Deployed and running |
| LiveKit CLI | Installed locally (see Step 1\) |

---

## Step 1 — Install LiveKit CLI

The LiveKit CLI (`lk`) is used to manage rooms, agents, dispatches, and SIP participants.

### macOS

```shell
brew install livekit-cli
```

### Verify Installation

```shell
lk --version
```

You should see a version string like `lk version 2.x.x`.

💡 For Linux or Windows installation, refer to the [LiveKit CLI GitHub repository](https://github.com/livekit/livekit-cli).

---

## Step 2 — Authenticate LiveKit CLI

Log in to your LiveKit Cloud account via the CLI:

```shell
lk cloud auth
```

This opens a browser window for authentication. After completing it, verify your project is accessible:

```shell
lk project list
```

You should see your LiveKit project(s) listed.

---

## Step 3 — Set Environment Variables

Export your LiveKit credentials so the CLI and any scripts can authenticate automatically:

```shell
export LIVEKIT_URL="wss://<your-project>.livekit.cloud"
export LIVEKIT_API_KEY="<your-api-key>"
export LIVEKIT_API_SECRET="<your-api-secret>"
```

Replace the placeholders with your actual values from the LiveKit dashboard.

**Verify the variables are set:**

```shell
echo $LIVEKIT_URL
echo $LIVEKIT_API_KEY
```

⚠️ **Security Note:** Do not commit these values to version control. Use a `.env` file (with `.gitignore`) or a secrets manager in production.

---

## Step 4 — Verify SIP Trunk

Confirm that your Exotel SIP trunk has been registered with LiveKit:

```shell
lk sip outbound list
```

**Expected output:**

```
ST_xxxxxxxxxxxxxxxxxxxx
```

This is your **SIP Trunk ID**. You will use it when initiating calls. Note it down.

If no trunk appears, you need to create an outbound SIP trunk in LiveKit pointing to your Exotel SIP edge. Refer to [LiveKit SIP documentation](https://docs.livekit.io/sip/) for trunk creation steps. For Indian calls, set `destination_country` to `in` on the trunk so calls originate from LiveKit's India region ([region pinning](https://docs.livekit.io/telephony/features/region-pinning/)), and list your Exotel number in E.164 (`+91...`).

---

## Step 5 — Verify Agent and Dispatch Name

List your deployed agents to retrieve the correct **Dispatch Name**:

```shell
lk agent list
```

**Example output:**

```
Dispatch Name = <your-agent-dispatch-name>
Agent ID      = CA_xxxxxxxxxxxxxxxxxxxx
```

⚠️ **Important:** Always use the **Dispatch Name** (e.g., `<your-agent-dispatch-name>`) when dispatching agents — NOT the Agent ID (e.g., `CA_xxxxxxxxxxxxxxxxxxxx`). Using the Agent ID will result in the bot failing to join the room.

---

## Step 6 — Dispatch Agent to Room

Create a dispatch to assign the AI agent to a specific LiveKit Room. The room will be created automatically if it does not exist.

```shell
lk dispatch create \
  --room "my-room" \
  --agent-name <your-agent-dispatch-name> \
  --metadata '{"phone_number":"+91XXXXXXXXXX"}'
```

**Parameters:**

| Parameter | Description |
| :---- | :---- |
| `--room` | The name of the LiveKit Room. Must match exactly across all steps. |
| `--agent-name` | The Dispatch Name from Step 5 (NOT the Agent ID). |
| `--metadata` | Optional JSON metadata passed to the agent (e.g., phone number for call context). |

**Verify the dispatch was created:**

````shell
lk dispatch list "my-room"
``` — Verify Room Creation

Confirm the room exists and the agent has joined:

```bash
lk room list
````

**Expected output:**

```
my-room | Participants = 1
```

At this point, 1 participant (the AI agent) has joined the room. The phone participant will join after the SIP call is initiated in the next steps.

---

## Step 8 — Prepare Outbound Call Payload

Create a JSON file that defines the outbound SIP call parameters:

```shell
cat > sip-call.json << 'EOF'
{
  "sip_trunk_id": "ST_xxxxxxxxxxxxxxxxxxxx",
  "sip_call_to": "+91XXXXXXXXXX",
  "room_name": "my-room",
  "participant_identity": "sip-participant-001",
  "participant_name": "Test Call",
  "wait_until_answered": true
}
EOF
```

**Field Reference:**

| Field | Required | Description |
| :---- | :---- | :---- |
| `sip_trunk_id` | Yes | The SIP Trunk ID from Step 4 |
| `sip_call_to` | Yes | The phone number to dial (E.164 format, e.g., `+91XXXXXXXXXX`) |
| `room_name` | Yes | Must exactly match the room name used in Step 6 |
| `participant_identity` | Yes | A unique identifier for this SIP participant in the room |
| `participant_name` | No | A human-readable display name for the participant |
| `wait_until_answered` | No | If `true`, the CLI waits for the call to be answered before returning |

**Verify the file:**

```shell
cat sip-call.json
```

---

## Step 9 — Initiate Outbound Call

Place the outbound call using the LiveKit SIP participant API:

```shell
lk sip participant create sip-call.json
```

**Expected output:**

```
SIPCallID:     SC_xxxxxxxxxxxxxxx
ParticipantID: PA_xxxxxxxxxxxxxxx
RoomName:      my-room
```

The target phone number should now ring. When the user answers, they will be connected to the AI agent in the LiveKit Room.

---

## Step 10 — Verify End-to-End Connection

Open a second terminal and check the room status after the call is answered:

```shell
lk room list
```

**Expected output when call is active:**

```
my-room | Participants = 2 | Publishers = 2
```

**Participants breakdown:**

| Participant | Type | Description |
| :---- | :---- | :---- |
| Participant 1 | LiveKit Agent | The AI bot running your LLM/TTS/STT pipeline |
| Participant 2 | SIP / Phone | The phone user bridged in via Exotel SIP Trunk |

Both participants publishing audio (`Publishers = 2`) confirms the two-way voice connection is live.

---

## Configuration Checklists

### Exotel Configuration Checklist

| Item | Required | Notes |
| :---- | :---- | :---- |
| SIP Username | ✅ Yes | Provided by Exotel |
| SIP Password | ✅ Yes | Provided by Exotel |
| SIP Edge Host | ✅ Yes | e.g., `in.voip.exotel.com` |
| SIP Port | ✅ Yes | Default: `5070` |
| Transport TCP | ✅ Recommended | UDP may work but TCP is more reliable |
| Outbound Calling Enabled | ✅ Yes | Must be enabled on the trunk |
| DID Attached | ✅ Yes | Caller ID for outbound calls |
| Digest Auth Enabled | ✅ Yes | Required for SIP registration |

### LiveKit Configuration Checklist

| Item | Required | Notes |
| :---- | :---- | :---- |
| SIP Feature Enabled | ✅ Yes | Enable in LiveKit project settings |
| Agent Running | ✅ Yes | Verify with `lk agent list` |
| Outbound SIP Trunk Created | ✅ Yes | Pointing to Exotel SIP edge |
| Trunk `destination_country` = `in` | ✅ Yes | Originates calls from LiveKit's India region ([region pinning](https://docs.livekit.io/telephony/features/region-pinning/)) |
| Numbers in E.164 | ✅ Yes | e.g. `+912247790801`, not `02247790801` |
| Dispatch Name Known | ✅ Yes | Use Dispatch Name, NOT Agent ID |
| Dispatch Created Before SIP Call | ✅ Yes | Agent must join room first |
| Same Room Name Used Everywhere | ✅ Yes | Dispatch, SIP call JSON must match exactly |

---

## Troubleshooting

### SIP 400 Bad Request

**Symptoms:** The outbound call fails immediately with a `400 Bad Request` SIP error.

**Causes:**

- Incorrect SIP Trunk ID  
- Invalid or unregistered Caller ID / DID  
- Wrong SIP authentication credentials  
- Exotel account does not have outbound calling enabled

**Fix:**

1. Verify the trunk ID with `lk sip outbound list`  
2. Confirm the DID is active on your Exotel account  
3. Double-check SIP username and password in your LiveKit SIP trunk configuration  
4. Ensure outbound calling is enabled in Exotel dashboard

---

### Bot Not Joining the Room

**Symptoms:** Room shows `Participants = 0` or `Participants = 1` (only phone, no agent) after dispatch.

**Cause:** The Agent ID was used instead of the Dispatch Name.

| ❌ Wrong (Agent ID) | ✅ Correct (Dispatch Name) |
| :---- | :---- |
| `CA_xxxxxxxxxxxxxxxxxxxx` | `<your-agent-dispatch-name>` |

**Fix:** Run `lk agent list` and use the value shown under `Dispatch Name`.

---

### Room Shows Only 1 Participant

**Symptoms:** After both dispatch and SIP call, the room only shows 1 participant.

**Possible Causes:**

- Room name mismatch between dispatch command and `sip-call.json`  
- Agent dispatch was never created before the SIP call  
- SIP call failed silently (check SIP error codes)

**Fix:**

1. Ensure `--room` in `lk dispatch create` exactly matches `room_name` in `sip-call.json`  
2. Confirm dispatch exists: `lk dispatch list "my-room"`  
3. Check for SIP errors in LiveKit logs

---

### Agent Running But Silent (No Audio)

**Symptoms:** Both participants are in the room but no conversation happens.

**Possible Causes:**

- TTS (Text-to-Speech) service not responding  
- STT (Speech-to-Text) service not configured or failing  
- LLM API key missing or quota exceeded  
- Agent business logic error preventing conversation start

**Fix:**

Check agent logs:

```shell
lk agent logs --id <agent-id>
```

Stop log streaming:

```shell
CTRL + C
```

Look for errors related to your TTS/STT/LLM provider and fix accordingly.

---

### Dispatch Created But Agent Not Joining

**Symptoms:** Dispatch is listed but agent never appears in the room.

**Fix:**

Check the agent's runtime status:

```shell
lk agent status --id <agent-id>
```

**Expected:**

```
Status = Running
```

If the status is not `Running`, restart the agent and re-create the dispatch.

---

### Call Rings But Immediately Disconnects

**Symptoms:** The phone rings once but the call drops before the user can speak.

**Possible Causes:**

- `wait_until_answered: true` timeout exceeded  
- Agent crashed after joining the room  
- SIP re-INVITE negotiation failed

**Fix:**

1. Check agent logs for crash errors  
2. Verify your SIP trunk supports audio codec negotiation (G.711 recommended)  
3. Try setting `wait_until_answered: false` to confirm if the issue is timing-related

---

## Quick Reference — CLI Commands

### Room Management

```shell
# List all active rooms
lk room list

# Delete a room
lk room delete "my-room"
```

### Agent Management

```shell
# List agents and their Dispatch Names
lk agent list

# Check agent status
lk agent status --id <agent-id>

# View agent logs
lk agent logs --id <agent-id>
```

### SIP Trunk Management

```shell
# List all outbound SIP trunks
lk sip outbound list

# Initiate an outbound SIP call
lk sip participant create sip-call.json
```

### Dispatch Management

```shell
# Create a dispatch (assign agent to room)
lk dispatch create \
  --room "my-room" \
  --agent-name <your-agent-dispatch-name> \
  --metadata '{"phone_number":"+91XXXXXXXXXX"}'

# List dispatches in a room
lk dispatch list "my-room"

# Delete a specific dispatch
lk dispatch delete <dispatch-id>
```

---

## End-to-End Flow Summary

```
1. Dispatch Agent to Room
         │
         ▼
2. Agent Joins LiveKit Room
         │
         ▼
3. Create SIP Participant (sip-call.json)
         │
         ▼
4. Exotel Places PSTN Call to Phone Number
         │
         ▼
5. User Answers → Phone Joins Same Room
         │
         ▼
6. Agent + Phone Connected → AI Conversation Begins
```

---

## Related Resources

- [Exotel Dynamic SIP Trunking Documentation](https://docs.exotel.com/dynamic-sip-trunking/connect-exotel-sip-trunk-to-livekit)  
- [LiveKit Agents Documentation](https://docs.livekit.io/agents/)  
- [LiveKit SIP Documentation](https://docs.livekit.io/sip/)  
- [LiveKit CLI Reference](https://github.com/livekit/livekit-cli)  
- [LiveKit Cloud Dashboard](https://cloud.livekit.io)

---

*Last updated: May 2026*  

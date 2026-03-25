# LiveKit Outbound Caller Voice Agent

A basic example of a voice agent using LiveKit and Python. Has a few extras to get started:

**Exotel outbound + “no audio” troubleshooting:** see [`OUTBOUND-EXOTEL-NOTES.md`](./OUTBOUND-EXOTEL-NOTES.md).

## Dev Setup

Run the following commands to:
- clone the repository
- change directory to `livekit-outbound-caller-agent`
- create a virtual environment and activate it
- install dependencies
- download files

**Requirements:** Python 3.10 or newer (3.11+ recommended). The LiveKit agents stack uses features that require Python 3.10+.

### Linux/macOS
```console
git clone https://github.com/kylecampbell/livekit-outbound-caller-agent.git
cd livekit-outbound-caller-agent
# Use Python 3.10+ if available (e.g. python3.11 -m venv venv)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 agent.py download-files
```

Alternatively, use the run script (creates venv and installs deps if needed):
```console
./run.sh
```

<details>
  <summary>Windows instructions (click to expand)</summary>
  
```cmd
:: Windows (CMD/PowerShell)
cd livekit-outbound-caller-agent
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
</details>


Set up the environment by copying `.env.example` to `.env.local` and filling in the required values:

- `LIVEKIT_URL` — Your project's **WebSocket URL** (e.g. `wss://your-project.livekit.cloud`). Get it from [LiveKit Cloud](https://cloud.livekit.io) → your project → Settings. Do **not** use `demo.livekit.io`; it is not a valid server.
- `LIVEKIT_API_KEY` and `LIVEKIT_API_SECRET` — From the same project Settings.
- `OPENAI_API_KEY` — From OpenAI.
- `DEEPGRAM_API_KEY` — From Deepgram.
- `SIP_OUTBOUND_TRUNK_ID` — Obtained from directions below.

You can also do this automatically using the LiveKit CLI:

```console
lk app env
```

Run the agent:

```console
python3 agent.py dev
```

Now, your worker is running, and waiting for dispatches in order to make outbound calls.

## Create Twilio SIP Outbound Trunk
1. Create a Twilio account
2. Get a Twilio phone number
3. Create a SIP trunk
- In Twilio console go to Explore products > Elastic SIP Trunking > SIP Trunks > Get started > Create a SIP Trunk, name it, then Save.
4. Configure SIP Termination
- Go to Termination, enter a Termination SIP URI, select the plus icon for Credentials Lists, enter a friendly name, username, and password.

## Create LiveKit SIP Outbound Trunk
1. Using the outbound-trunk-example.json file, copy and rename to outbound-trunk.json and update it with your SIP provider's credentials. Do not push this file to a public repo.
- `name`: Can be anything
- `address`: Your SIP provider's outbound trunk address you created in previous step `Termination SIP URI`
- `numbers`: Your Twilio phone number you want to call from
- `auth_username`: Your username created in previous step in Twilio console.
- `auth_password`: Your password created in previous step in Twilio console.
2. Run LiveKit CLI command to create the trunk:
```console
lk sip outbound create outbound-trunk.json
```
3. Copy the `SIPTrunkID` returned in the response and add it to the `.env.local` file as `SIP_OUTBOUND_TRUNK_ID`.

You should now be able to make a call by dispatching an agent...

## Making a call

With your agent running in one terminal, trigger an outbound call in another.

### Option A: Python script (no CLI install)

```console
python3 dispatch_call.py +917696016726
# or
./venv/bin/python3 dispatch_call.py +1234567890
```

Uses the same `.env.local` as the agent (LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET).

### Option B: LiveKit CLI (`lk`)

1. **Install the CLI**
   - **macOS:** `brew install livekit-cli`
   - **Linux:** `curl -sSL https://get.livekit.io/cli | bash`
   - **Windows:** `winget install LiveKit.LiveKitCLI`

2. **Link a project** (the CLI does not read `.env.local`; it needs a linked project):
   - **LiveKit Cloud:** run `lk cloud auth` and complete the browser login.
   - **Or use the same credentials as in `.env.local`:**
     ```console
     lk project add my-project \
       --url "wss://your-project.livekit.cloud" \
       --api-key "your_api_key" \
       --api-secret "your_api_secret"
     lk project set-default my-project
     ```
     Use the same `LIVEKIT_URL`, `LIVEKIT_API_KEY`, and `LIVEKIT_API_SECRET` values from your `.env.local`.

3. **Dispatch** (replace with the number you want to call):

```console
lk dispatch create \
  --new-room \
  --agent-name outbound-caller \
  --metadata '+917696016726'
```

### Helpful commands (with LiveKit CLI)

```console
lk project list
lk sip outbound list
lk sip dispatch list
```


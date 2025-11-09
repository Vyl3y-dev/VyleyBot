# eventsub.py
import os
import json
import asyncio
import requests
import websockets
from dotenv import dotenv_values
import sys, io

sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)

# --- Load broadcaster/bot env ---
env = dotenv_values(".env.broadcaster")
broadcaster_id = env.get("BROADCASTER_USER_ID")
bot_id = dotenv_values(".env").get("BOT_USER_ID")

# ---- load bot token)
with open("auth/token_bot.json") as f:
    token_data = json.load(f)

CLIENT_ID = os.getenv("CLIENT_ID") or dotenv_values(".env").get("CLIENT_ID")

# Load broadcaster token too
with open("auth/token_broadcaster.json") as f:
    broadcaster_token_data = json.load(f)
BROADCASTER_ACCESS_TOKEN = broadcaster_token_data["access_token"]


# --- Twitch API endpoints ---
EVENTSUB_URL = "https://api.twitch.tv/helix/eventsub/subscriptions"
EVENTSUB_WS = "wss://eventsub.wss.twitch.tv/ws"

# --- Headers for Twitch API calls ---
HEADERS = {
    "Authorization": f"Bearer {BROADCASTER_ACCESS_TOKEN}",
    "Client-Id": CLIENT_ID,
    "Content-Type": "application/json"
}

# ======================================================
# Send chat messages through the bot account
# ======================================================
def send_chat_message(message: str):
    """Send a chat message using the bot token."""
    try:
        with open("auth/token_bot.json") as f:
            bot_token = json.load(f)["access_token"]
    except FileNotFoundError:
        print("⚠️ token_bot.json missing — cannot send message.")
        return

    headers = {
        "Authorization": f"Bearer {bot_token}",
        "Client-Id": CLIENT_ID,
        "Content-Type": "application/json",
    }

    payload = {
        "broadcaster_id": broadcaster_id,
        "sender_id": bot_id,
        "message": message
    }

    r = requests.post("https://api.twitch.tv/helix/chat/messages",
                      headers=headers, json=payload)
    if r.status_code != 200:
        print(f"⚠️ Failed to send chat message: {r.text}")


async def subscribe_to_events(session_id: str):
    """Registers EventSub subscriptions for follows and subs."""
    events = [
        {"type": "channel.follow", "version": "2"},
        {"type": "channel.subscribe", "version": "1"},
    ]

    for event in events:
        # Pick the right condition first
        if event["type"] == "channel.follow":
            condition = {
                "broadcaster_user_id": broadcaster_id,
                "moderator_user_id": broadcaster_id  # broadcaster moderating self
            }
        else:
            condition = {"broadcaster_user_id": broadcaster_id}

        # Then build the payload
        payload = {
            "type": event["type"],
            "version": event["version"],
            "condition": condition,
            "transport": {"method": "websocket", "session_id": session_id},
        }

        print(f"[EventSub] → Subscribing to {event['type']} ...")
        resp = requests.post(EVENTSUB_URL, headers=HEADERS, json=payload)
        print(f"[EventSub] ← {resp.status_code} {resp.text}")

        if resp.status_code == 202:
            print(f"✅ Subscribed to {event['type']}")
        else:
            print(f"❌ Failed to subscribe {event['type']}")


async def listen_eventsub():
    """Main WebSocket listener for Twitch EventSub."""
    print("[EventSub] Attempting to connect to Twitch EventSub WebSocket...")
    try:
        async with websockets.connect(EVENTSUB_WS) as ws:
            print("[EventSub] 🟢 Connected to EventSub WebSocket")

            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                metadata = data.get("metadata", {})
                payload = data.get("payload", {})
                msg_type = metadata.get("message_type")

                # --- Log all messages we receive ---
                print(f"[EventSub] Message type: {msg_type}")

                # --- When Twitch first welcomes us, register our subscriptions ---
                if msg_type == "session_welcome":
                    session_id = payload["session"]["id"]
                    print(f"✅ Session started: {session_id}")
                    await subscribe_to_events(session_id)
                    print("[EventSub] 📡 Subscriptions sent — waiting for notifications...")

                # --- Handle follow / sub notifications ---
                elif msg_type == "notification":
                    sub_type = payload["subscription"]["type"]
                    event = payload["event"]

                    if sub_type == "channel.follow":
                        user = event['user_name']
                        msg = f"Welcome to the channel, @{user}! Thanks for the follow 💖"
                        print(f"🎉 {msg}")
                        send_chat_message(msg)

                    elif sub_type == "channel.subscribe":
                        user = event['user_name']
                        msg = f"💎 Huge thanks to @{user} for subscribing! You’re amazing 💕"
                        print(f"💎 {msg}")
                        send_chat_message(msg)

                    else:
                        print(f"📨 {sub_type}: {event}")

                # --- Twitch might ask you to reconnect mid-session ---
                elif msg_type == "session_reconnect":
                    new_url = payload["session"]["reconnect_url"]
                    print(f"🔁 Twitch requested reconnect to: {new_url}")
                    return await listen_eventsub()

                # --- Revocation notice if authorization is revoked ---
                elif msg_type == "revocation":
                    print("⚠️ Subscription revoked, you’ll need to reauthorize.")

    except websockets.ConnectionClosedError as e:
        print(f"[EventSub] ⚠️ Connection closed: {e}. Reconnecting in 10 s...")
        await asyncio.sleep(10)
        await listen_eventsub()

    except Exception as e:
        print(f"[EventSub] ❌ Error: {e}")
        await asyncio.sleep(10)
        await listen_eventsub()

async def main():
    await listen_eventsub()

if __name__ == "__main__":
    asyncio.run(main())

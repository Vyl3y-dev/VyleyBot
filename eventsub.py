# eventsub.py
import os
import json
import asyncio
import requests
import websockets
from dotenv import dotenv_values
import sys, io

# --- Force UTF-8 safe output ---
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding="utf-8", errors="replace")

# --- Load broadcaster/bot env ---
env = dotenv_values(".env.broadcaster")
broadcaster_id = env.get("BROADCASTER_USER_ID")
bot_id = dotenv_values(".env").get("BOT_USER_ID")

# ---- load broadcaster token (only) 🟢 now used for everything
with open("auth/token_broadcaster.json") as f:
    token_data = json.load(f)
ACCESS_TOKEN = token_data["access_token"]

CLIENT_ID = os.getenv("CLIENT_ID") or dotenv_values(".env").get("CLIENT_ID")

# --- Twitch API endpoints ---
EVENTSUB_URL = "https://api.twitch.tv/helix/eventsub/subscriptions"
EVENTSUB_WS = "wss://eventsub.wss.twitch.tv/ws"

# --- Headers for all EventSub calls 🟢 use broadcaster only ---
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Client-Id": CLIENT_ID,
    "Content-Type": "application/json",
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

# ======================================================
# Subscribe to Twitch EventSub events
# ======================================================
async def subscribe_to_events(session_id: str):
    """Registers EventSub subscriptions for follows and subs."""
    events = [
        {"type": "channel.follow", "version": "2"},
        {"type": "channel.subscribe", "version": "1"},
    ]

    for event in events:
        if event["type"] == "channel.follow":
            condition = {
                "broadcaster_user_id": broadcaster_id,
                "moderator_user_id": broadcaster_id,  # required for follow v2
            }
        else:
            condition = {"broadcaster_user_id": broadcaster_id}

        payload = {
            "type": event["type"],
            "version": event["version"],
            "condition": condition,
            "transport": {"method": "websocket", "session_id": session_id},
        }

        print(f"[EventSub] → Subscribing to {event['type']} ...")
        # 🟢 Always use broadcaster headers here now:
        resp = requests.post(EVENTSUB_URL, headers=HEADERS, json=payload)
        print(f"[EventSub] ← {resp.status_code} {resp.text}")

        if resp.status_code == 202:
            print(f"✅ Subscribed to {event['type']}")
        else:
            print(f"❌ Failed to subscribe {event['type']}")

# ======================================================
# Main WebSocket listener
# ======================================================
async def listen_eventsub():
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

                print(f"[EventSub] Message type: {msg_type}")

                if msg_type == "session_welcome":
                    session_id = payload["session"]["id"]
                    print(f"✅ Session started: {session_id}")
                    await subscribe_to_events(session_id)
                    print("[EventSub] 📡 Subscriptions sent — waiting for notifications...")

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

                elif msg_type == "session_reconnect":
                    new_url = payload["session"]["reconnect_url"]
                    print(f"🔁 Twitch requested reconnect to: {new_url}")
                    return await listen_eventsub()

                elif msg_type == "revocation":
                    print("⚠️ Subscription revoked, you’ll need to reauthorize.")

    except websockets.ConnectionClosedError as e:
        print(f"[EventSub] ⚠️ Connection closed: {e}. Reconnecting in 10s...")
        await asyncio.sleep(10)
        await listen_eventsub()

# ======================================================
# Entry point
# ======================================================
async def main():
    await listen_eventsub()

if __name__ == "__main__":
    asyncio.run(main())

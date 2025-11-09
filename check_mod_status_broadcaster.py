# check_mod_status.py
import os, json, requests
from dotenv import dotenv_values

env = dotenv_values(".env")
broadcaster_id = dotenv_values(".env.broadcaster").get("BROADCASTER_USER_ID")
bot_id = env.get("BOT_USER_ID")

with open("auth/token_broadcaster.json") as f:
    token = json.load(f)["access_token"]

client_id = env.get("CLIENT_ID")

r = requests.get(
    f"https://api.twitch.tv/helix/moderation/moderators?broadcaster_id={broadcaster_id}",
    headers={"Authorization": f"Bearer {token}", "Client-Id": client_id}
)

mods = [m["user_id"] for m in r.json().get("data", [])]
print(f"Broadcaster is mod? {'✅ yes' if broadcaster_id in mods else '❌ no'}")
print(json.dumps(r.json(), indent=2))

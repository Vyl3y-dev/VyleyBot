# check_token_owner.py
import json, requests
with open("auth/token_bot.json") as f:
    token = json.load(f)["access_token"]

client_id = input("Client ID: ").strip()

r = requests.get(
    "https://api.twitch.tv/helix/users",
    headers={"Authorization": f"Bearer {token}", "Client-Id": client_id}
)
print(r.json())

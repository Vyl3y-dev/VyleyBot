# get_token.py (dual account version)
import os
import sys
import json
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

TOKEN_URL = "https://id.twitch.tv/oauth2/token"
AUTH_URL = "https://id.twitch.tv/oauth2/authorize"

# ----------------------------
# DEFINE SCOPES FOR EACH ACCOUNT
# ----------------------------
BOT_SCOPES = (
    "chat:read chat:edit "
    "moderator:read:chatters "
    "moderator:read:followers "
    "moderator:manage:banned_users "
    "moderation:read "
    "channel:manage:broadcast "
    "channel:read:redemptions "
    "clips:edit "
    "user:read:follows "
    "channel:read:hype_train "
    "channel:manage:raids "
    "user:bot "
    "user:write:chat"
)

BROADCASTER_SCOPES = (
    "chat:read chat:edit "
    "moderation:read "
    "channel:read:subscriptions "
    "channel:read:goals "
    "channel:read:polls "
    "channel:read:predictions "
    "moderator:read:followers "
    "channel:read:hype_train "
    "channel:manage:raids "
    "channel:read:redemptions "
    "user:read:email "
    "user:write:chat"
)

# ----------------------------
# SELECT ACCOUNT TYPE
# ----------------------------
if len(sys.argv) < 2 or sys.argv[1] not in ["bot", "broadcaster"]:
    print("❌ Usage: python get_token.py [bot|broadcaster]")
    sys.exit(1)

account_type = sys.argv[1]
SCOPES = BOT_SCOPES if account_type == "bot" else BROADCASTER_SCOPES
SAVE_PATH = f"auth/token_{account_type}.json"

# ----------------------------
# HANDLE REDIRECT & TOKEN EXCHANGE
# ----------------------------
class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if "code" in params:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"✅ {account_type.capitalize()} token received. You can close this window.".encode("utf-8"))
            
            code = params["code"][0]
            response = requests.post(TOKEN_URL, data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI,
            })
            token_data = response.json()

            os.makedirs("auth", exist_ok=True)
            with open(SAVE_PATH, "w") as f:
                json.dump(token_data, f, indent=4)
            print(f"✅ Access token saved to {SAVE_PATH}")
        else:
            self.send_error(400, "Missing code")

# ----------------------------
# MAIN FLOW
# ----------------------------
def main():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
    }
    auth_url = f"{AUTH_URL}?{requests.compat.urlencode(params)}"
    print(f"🌐 Opening authorization for {account_type}...")
    webbrowser.open(auth_url)
    print("🔄 Waiting for redirect...")

    server = HTTPServer(("localhost", 3000), AuthHandler)
    server.handle_request()

if __name__ == "__main__":
    main()

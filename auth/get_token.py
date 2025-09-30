# get_token.py for TwitchIO 2.9.1
import os
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
SCOPES = "chat:read chat:edit user:read:follows"

TOKEN_URL = "https://id.twitch.tv/oauth2/token"
AUTH_URL = "https://id.twitch.tv/oauth2/authorize"

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        if "code" in params:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("✅ Token received. You can close this window.".encode("utf-8"))
            code = params["code"][0]
            response = requests.post(TOKEN_URL, data={
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": REDIRECT_URI,
            })
            token_data = response.json()
            with open("auth/token.json", "w") as f:
                import json
                json.dump(token_data, f, indent=4)
            print("✅ Access token saved to auth/token.json")
        else:
            self.send_error(400, "Missing code")

def main():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
    }
    auth_url = f"{AUTH_URL}?{requests.compat.urlencode(params)}"
    print(f"🌐 Opening: {auth_url}")
    webbrowser.open(auth_url)
    print("🔄 Waiting for redirect...")
    server = HTTPServer(("localhost", 3000), AuthHandler)
    server.handle_request()

if __name__ == "__main__":
    main()

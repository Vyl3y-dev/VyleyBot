# auth/get_token.py

import os
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
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "token.json")

AUTH_URL = "https://id.twitch.tv/oauth2/authorize"
TOKEN_URL = "https://id.twitch.tv/oauth2/token"

SCOPES = [
    "chat:read",
    "chat:edit"
]

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        if "code" in query:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<h1>You can close this window now.</h1>")
            code = query["code"][0]
            tokens = exchange_code_for_token(code)
            with open(TOKEN_FILE, "w") as f:
                json.dump(tokens, f, indent=4)
            print("✅ Tokens saved to token.json")
        else:
            self.send_error(400, "Missing code in query")

def exchange_code_for_token(code):
    response = requests.post(TOKEN_URL, data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
    })

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get token: {response.text}")

def main():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
    }
    auth_link = f"{AUTH_URL}?{requests.compat.urlencode(params)}"

    print("🌐 Opening browser for authorization...")
    webbrowser.open(auth_link)

    print(f"🔄 Waiting for Twitch redirect to {REDIRECT_URI}...")
    server = HTTPServer(("localhost", 3000), AuthHandler)
    server.handle_request()

if __name__ == "__main__":
    main()
